import inspect
from unittest.mock import patch

from modules.app_launcher import launch_app


def test_launch_app_parameter_matches_tool_schema():
    params = inspect.signature(launch_app).parameters
    assert "app_name" in params
    assert "user_input" not in params


def test_launch_app_allowlist_on_windows():
    with (
        patch("modules.app_launcher.platform.system", return_value="Windows"),
        patch("modules.app_launcher.subprocess.Popen") as popen,
    ):
        result = launch_app(app_name="notepad")

    assert "başarıyla" in result.lower()
    popen.assert_called_once()
    assert popen.call_args.args[0] == ["notepad.exe"]


def test_unknown_app_is_rejected():
    with patch("modules.app_launcher.platform.system", return_value="Windows"):
        result = launch_app(app_name="totally-unknown-app")
    assert "izin verilen listede değil" in result
