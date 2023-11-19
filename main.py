import json
from pathlib import Path


import definitiongenerator.model as fj
import definitiongenerator.writers as genjson

test_path = "sample_response.json"
# test_path = "vm_skus.json"


def load_test_file(p: Path | str):
    with open(p, "r", encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    test_data = load_test_file(test_path)
    t = fj.new_mapping_model(test_data)

    with open("outtests/test.py", "w", encoding='utf-8') as f:
        mm = genjson.dump_model(t, f)

    with open("outtests/test.md", "w", encoding='utf-8') as f:
        mm = genjson.dump_model(t, f, dump_format="Markdown")

    with open("outtests/Test.cs", "w", encoding='utf-8') as f:
        csOptions: genjson.CSharpWriterOptions = {
            "Namespace": "Something.TestNamespace",
            "NewStyleNamespace": False
        }

        mm = genjson.dump_model(t, f, dump_format="C#", options=csOptions)
