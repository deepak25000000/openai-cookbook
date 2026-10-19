import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(ROOT_DIR))

from shared.path_utils import validate_example_id, safe_join


def test_validate_example_id_ok():
    validate_example_id("abc-123_0.v1")


@pytest.mark.parametrize("bad", ["..", "../foo", "foo/bar", "/abs", "", "~home", "a b"])
def test_validate_example_id_bad(bad):
    with pytest.raises(ValueError):
        validate_example_id(bad)


def test_safe_join_rejects_parent_escape(tmp_path):
    base = tmp_path / "data"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(base, "../outside.txt")


def test_safe_join_abs_path(tmp_path):
    base = tmp_path / "data"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_join(base, "/etc/passwd")


def test_safe_join_allows_valid(tmp_path):
    base = tmp_path / "data"
    base.mkdir()
    p = safe_join(base, "ok.json")
    assert p.parent == base.resolve()
