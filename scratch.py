import re

import definitiongenerator.fromjson as fj

input = [
    {
        "propA": {
            "propB": {"insideB1": "test", "insideB2": "test2"},
            "listInA": [
                {"name": "A", "value": 10},
                {"name": "B", "value": "ii"},
            ],
        }
    },
    {
        "propA": {
            "propB": {
                "insideB1": "test2222",
                "insideB2": "test2ffff",
                "insideB3": 9.0,
            },
            "listInA": [
                {"name": "C", "value": 10},
            ],
        }
    },
]

result = fj.new_mapping_model(input)
...