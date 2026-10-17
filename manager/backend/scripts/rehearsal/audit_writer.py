"""Stand-in for the running application during a migration rehearsal.

Inserts one audit row about every 100 ms and logs how long each insert took, so you can see
what a migration that locks audit_logs does to the writers waiting behind it (the longest
latency is how long the application would have hung).

    python audit_writer.py postgresql://user@host/vedha_rehearsal writer.log old 900

  mode `old`  writes the columns the application writes today (before migration 0067)
  mode `new`  also sets `outcome`, the way the upgraded application does

It INSERTS rows, so it refuses any database whose name does not say it is disposable.
See docs/operations/migrations-0066-0068-rollout.md.
"""
import asyncio
import json
import re
import sys
import time
import uuid

import asyncpg

DSN = sys.argv[1]
OUT = sys.argv[2]
MODE = sys.argv[3] if len(sys.argv) > 3 else "old"
SECONDS = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0


async def main() -> None:
    conn = await asyncpg.connect(DSN, timeout=30)
    name = await conn.fetchval("SELECT current_database()")
    if not re.search(r"rehears|scratch|copy|sandbox", name, re.I):
        raise SystemExit(f"refusing to write to {name}: the database name must contain "
                         "rehearsal, scratch, copy or sandbox")
    await conn.execute("SET statement_timeout = 0")
    end = time.time() + SECONDS
    with open(OUT, "w") as log:
        while time.time() < end:
            started = time.time()
            try:
                if MODE == "old":
                    await conn.execute(
                        "INSERT INTO audit_logs (id, actor_id, action, resource_type, detail, ip_address, \"timestamp\") "
                        "VALUES ($1, 'system', 'rehearsal.write', 'probe', $2::jsonb, '198.51.100.7', now())",
                        uuid.uuid4(), json.dumps({"mode": "old"}))
                else:
                    await conn.execute(
                        "INSERT INTO audit_logs (id, actor_id, action, resource_type, detail, ip_address, \"timestamp\", outcome) "
                        "VALUES ($1, 'system', 'rehearsal.write', 'probe', $2::jsonb, '198.51.100.7', now(), 'success')",
                        uuid.uuid4(), json.dumps({"mode": "new"}))
                ok = 1
            except Exception as exc:  # noqa: BLE001 - a rehearsal records every failure
                ok = 0
                print("insert failed:", type(exc).__name__, str(exc)[:100], file=sys.stderr)
            log.write(f"{started:.3f} {time.time() - started:.3f} {ok}\n")
            log.flush()
            await asyncio.sleep(0.1)
    await conn.close()


asyncio.run(main())
