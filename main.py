import json
from pathlib import Path
from definitiongenerator.fromjson import _gather_types

# test_path = "prices_eastus.json"
test_path = "vm_skus.json"


def load_test_file(p: Path):
    with open(p, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    test_data = load_test_file(test_path)
    t = _gather_types(test_data)
    ...

