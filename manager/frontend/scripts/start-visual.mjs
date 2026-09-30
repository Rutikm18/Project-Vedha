import { cp, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const standalone = join(root, ".next", "standalone");

process.chdir(root);
await mkdir(join(standalone, ".next"), { recursive: true });
await cp(join(root, ".next", "static"), join(standalone, ".next", "static"), {
  recursive: true,
  force: true,
});
await cp(join(root, "public"), join(standalone, "public"), {
  recursive: true,
  force: true,
});

process.env.HOSTNAME = "127.0.0.1";
process.env.PORT = process.env.PORT || "3100";
await import(pathToFileURL(join(standalone, "server.js")).href);
