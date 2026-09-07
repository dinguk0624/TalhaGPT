from core.agent import Agent, message_likely_needs_tools


def test_parse_arguments_accepts_json_object():
    assert Agent._parse_arguments('{"city": "Ankara"}') == {"city": "Ankara"}


def test_parse_arguments_rejects_invalid_json():
    assert Agent._parse_arguments('{invalid') == {}


def test_limit_tool_output():
    class Registry:
        pass

    agent = Agent("test", Registry(), max_steps=1)
    agent.tool_output_max_chars = 50

    original = "x" * 100
    limited = agent._limit_tool_output(original)

    assert limited.startswith("x" * 50)
    assert limited.endswith("[Tool output truncated.]")
    assert len(limited) < len(original) + 30


def test_fast_path_skips_smalltalk_and_program():
    assert message_likely_needs_tools("sa") is False
    assert message_likely_needs_tools("program nedir") is False
    assert message_likely_needs_tools("karar vermeme yardım et") is False


def test_fast_path_detects_weather_and_launch():
    assert message_likely_needs_tools("yağmur yağacak mı") is True
    assert message_likely_needs_tools("chrome aç") is True
    assert message_likely_needs_tools("not al: yarın toplantı") is True


def test_restricted_tool_denied_without_callback():
    class Registry:
        def has(self, name):
            return True

        def execute(self, name, arguments):
            raise AssertionError("restricted tool must not run")

    agent = Agent(
        "test",
        Registry(),
        max_steps=1,
        require_confirm=True,
        on_confirm=None,
    )
    result = agent._execute_tool("launch_app", {"app_name": "notepad"})
    assert "denied" in result.lower()
    assert "confirmation" in result.lower()
