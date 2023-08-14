import json
from pathlib import Path

test_path = "prices_eastus.json"


def load_test_file(p: Path):
    with open(p, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    test_data = load_test_file(test_path)
