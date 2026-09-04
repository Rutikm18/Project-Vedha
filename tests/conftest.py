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


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "result_archive: test manages PROBE_RESULT_DIR itself (see conftest)")
