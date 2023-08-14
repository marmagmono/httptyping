import re

import definitiongenerator.fromjson as fj

result1 = re.split("[A-Z]", "ThisIsString")
result2 = re.split("([A-Z])", "thisIsAnotherString")

...