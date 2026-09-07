from pathlib import Path

from modules.file_reader import _resolve_safe_path, read_local_file


def test_resolve_project_readme():
    path, err = _resolve_safe_path("README.md")
    assert err is None
    assert path is not None
    assert path.name == "README.md"
    assert path.is_file()


def test_resolve_leading_slash_as_project_relative():
    path, err = _resolve_safe_path("/README.md")
    assert err is None
    assert path is not None
    assert path == Path(__file__).resolve().parent.parent / "README.md"


def test_blocks_path_traversal():
    path, err = _resolve_safe_path("../secret.txt")
    assert path is None
    assert err is not None


def test_read_readme():
    content = read_local_file("README.md")
    assert content.startswith("[Dosya: README.md]")
    assert "TalhaGPT" in content
