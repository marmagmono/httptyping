import json
from pathlib import Path
import definitiongenerator.model as fj
import definitiongenerator.json as genjson

# test_path = "prices_eastus.json"
test_path = "vm_skus.json"


def load_test_file(p: Path | str):
    with open(p, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    test_data = load_test_file(test_path)
    t = fj.new_mapping_model(test_data)
    mm = genjson._new_type_model(t, genjson._MapperState())
    ...
