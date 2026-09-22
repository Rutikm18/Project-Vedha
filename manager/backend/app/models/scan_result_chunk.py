import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ScanResultChunk(Base, TimestampMixin):
    """One HOST's facts, committed while the job is still RUNNING.

    A job's evidence used to reach the manager exactly once, at the end, so a
    probe that died mid-scan (OOM on a deep sweep, container evicted, host
    rebooted) lost every host it had already finished — and the retry rescanned
    them from zero.

    This is a BUFFER, not a second result path. The job still completes with one
    scan_results row: the final submission, merged with any chunk it does not
    already cover (see result_chunk_service.merge_chunk_facts). Detection,
    coverage and campaign progress therefore see exactly what they saw before.
    What changes is that a job which never reaches its final submission still has
    its finished hosts here — and a retrying probe can ask which hosts to skip.

    One row per (job, host): a later attempt that rescans a host REPLACES its
    evidence rather than appending a second opinion.
    """
    __tablename__ = "scan_result_chunks"
    __table_args__ = (
        UniqueConstraint("job_id", "host", name="uq_result_chunk_job_host"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    # Which attempt produced it. Deliberately NOT unique (unlike
    # scan_results.attempt_id): one attempt commits many hosts.
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="RESTRICT"),
        nullable=True, index=True,
    )
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    scan_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    content_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Did this host finish the job's whole pipeline, or is this mid-scan
    # evidence?
    #
    # committed_hosts() feeds the probe's RESUME list, and that only works
    # because a chunk used to mean "this host is DONE". Once evidence is also
    # committed at stage boundaries — so a probe killed during the port sweep
    # does not lose hours of work — a chunk stops implying completion, and a
    # retry that skipped merely-DISCOVERED hosts would deliver a liveness fact
    # and call them scanned.
    #
    # Defaults TRUE: an older probe omits the field and only ever commits
    # finished hosts, so its behaviour against a newer manager is unchanged.
    complete: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="true", default=True,
    )
    fact_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    facts: Mapped[list] = mapped_column(JSONB, nullable=False)
