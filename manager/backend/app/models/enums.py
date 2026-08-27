import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    tester = "tester"
    analyst = "analyst"
    auditor = "auditor"
    # Customer-portal login: scoped to exactly one engagement, read-only + may
    # REQUEST (never run) scans. Never granted operator capabilities.
    client = "client"


class EngagementStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    completed = "completed"


class AssetType(str, enum.Enum):
    server = "server"
    workstation = "workstation"
    network = "network"
    cloud = "cloud"
    container = "container"
    iot = "iot"
    printer = "printer"        # from probe device_classifier (device_inventory)
    hypervisor = "hypervisor"  # from probe device_classifier (device_inventory)


class AssetCriticality(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class FindingSeverity(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class FindingStatus(str, enum.Enum):
    open = "open"
    confirmed = "confirmed"
    remediated = "remediated"
    accepted = "accepted"
    fp = "fp"


class DetectionStatus(str, enum.Enum):
    detected = "detected"
    missed = "missed"
    prevented = "prevented"
    unknown = "unknown"


class FindingEventType(str, enum.Enum):
    """A single entry in a finding's lifecycle audit trail. Stored as a plain
    string (not a PG enum) so the log stays append-only and new event kinds never
    need a schema migration. `detected`/`reaffirmed`/`resolved` are also derivable
    from the finding's own timestamp columns (see services.finding_events), so a
    complete timeline exists even for findings created before this log."""

    detected = "detected"                    # genesis — first produced by detection
    reaffirmed = "reaffirmed"                # re-observed in a later coverage-proven run
    confirmed = "confirmed"                  # analyst promoted open -> confirmed
    remediated = "remediated"                # marked fixed (manual)
    resolved = "resolved"                    # auto-closed after coverage-proven clean runs
    accepted = "accepted"                    # risk formally accepted
    false_positive = "false_positive"        # dismissed as not real
    reopened = "reopened"                    # a resolved finding came back / was reversed
    status_changed = "status_changed"        # any other lifecycle transition
    verification_changed = "verification_changed"  # verdict changed (confirmed/inferred/…)
    risk_changed = "risk_changed"            # CVSS / risk score revised
    note = "note"                            # free-text operator annotation


class ScanJobType(str, enum.Enum):
    discovery = "discovery"
    vuln_scan = "vuln_scan"
    exploit = "exploit"
    ad_enum = "ad_enum"
    lateral = "lateral"
    cloud_scan = "cloud_scan"
    detection = "detection"
    ai_report = "ai_report"


class ScanJobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class ReviewStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
