from modules.api_tools import get_weather
from modules.executor import run_python_code


def test_weather_rejects_empty_city():
    assert "boş" in get_weather("").lower()
    assert "boş" in get_weather("   ").lower()


def test_executor_does_not_run_code():
    result = run_python_code("print(1)")
    assert "Güvenlik" in result
    assert "1" not in result or "devre dışı" in result.lower()
