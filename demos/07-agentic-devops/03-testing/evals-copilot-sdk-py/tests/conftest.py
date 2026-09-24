from pathlib import Path

import pytest

EVAL_FILE = "test_menu_chat_evals.py"


def pytest_collection_modifyitems(items):
    for item in items:
        if Path(str(item.fspath)).name == EVAL_FILE:
            item.add_marker(pytest.mark.eval)
