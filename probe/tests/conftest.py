import importlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(autouse=True)
def _isolate_result_archive(tmp_path_factory, monkeypatch, request):
    """Keep the local result archive out of the checkout.

    TaskRunner writes every submitted payload to PROBE_RESULT_DIR (default
    <probe root>/result). Any test that runs a job would otherwise drop real
    JSON into the repo. Point it at a per-test temp dir instead — tests that
    care about archiving set the variable themselves and opt out via
    @pytest.mark.result_archive.
    """
    if request.node.get_closest_marker("result_archive"):
        return
    monkeypatch.setenv(
        "PROBE_RESULT_DIR", str(tmp_path_factory.mktemp("result_archive")))


@pytest.fixture(autouse=True)
def _no_raw_syn_probes(monkeypatch):
    """Never put real SYN probes on the wire from a test.

    SynScanner asks syn_scan_supported() with no arguments, which is True for
    root on Linux. Run as root (a dev container, the agent image), tests that
    drive the engine then send a real paced sweep at their target: 65,535 ports
    to 10.0.0.1, which is minutes per test and somebody's router on a LAN. CI
    runs unprivileged, where the answer is already False. Calls that inject
    platform or socket_factory (the capability tests themselves) are unchanged.
    """
    for name in ("scanner.syn_scanner", "main_scripts.syn_scanner"):
        try:
            module = importlib.import_module(name)
        except ImportError:
            continue   # a tree that cannot be imported cannot send packets either
        real = module.syn_scan_supported

        def no_real_raw_socket(*, platform=None, socket_factory=None, _real=real):
            if platform is None and socket_factory is None:
                return False
            return _real(platform=platform, socket_factory=socket_factory)

        monkeypatch.setattr(module, "syn_scan_supported", no_real_raw_socket)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "result_archive: test manages PROBE_RESULT_DIR itself (see conftest)")
