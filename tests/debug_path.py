import sys
import pytest

def test_sys_path():
    print("\n--- sys.path in pytest ---")
    for p in sys.path:
        print(p)
    print("--------------------------")
    assert True

