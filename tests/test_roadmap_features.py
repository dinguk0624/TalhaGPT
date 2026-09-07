from modules.permissions import PermissionManager
from modules.sessions import SessionStore
from modules.vision import analyze_image


def test_permission_defaults(tmp_path):
    manager = PermissionManager(file_path=str(tmp_path / "missing.json"))
    assert manager.policy_for("get_weather") == "allow"
    assert manager.policy_for("launch_app") == "ask"


def test_permission_persist_and_deny(tmp_path):
    path = tmp_path / "perms.json"
    manager = PermissionManager(file_path=str(path))
    assert "deny" in manager.set_policy("launch_app", "deny")
    again = PermissionManager(file_path=str(path))
    assert again.policy_for("launch_app") == "deny"


def test_agent_honors_deny_policy(tmp_path):
    from core.agent import Agent

    class Registry:
        def has(self, name):
            return True

        def execute(self, name, arguments):
            raise AssertionError("denied tool must not run")

    manager = PermissionManager(file_path=str(tmp_path / "perms.json"))
    manager.set_policy("launch_app", "deny")
    agent = Agent(
        "test",
        Registry(),
        max_steps=1,
        require_confirm=True,
        permissions=manager,
    )
    result = agent._execute_tool("launch_app", {"app_name": "notepad"})
    assert "denied" in result.lower()


def test_sessions_create_and_switch(tmp_path):
    store = SessionStore(sessions_dir=str(tmp_path / "sessions"))
    first = store.current_id()
    second = store.create("work")
    assert second != first
    assert store.current_id() == second
    assert store.switch(first) == first
    assert store.current_id() == first
    ids = {item["id"] for item in store.list_sessions()}
    assert first in ids and second in ids


def test_analyze_image_rejects_text_file():
    result = analyze_image("README.md")
    assert "Görüntü Hatası" in result
