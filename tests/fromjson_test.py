import unittest
import re
import definitiongenerator.fromjson as fj

class Test_Something(unittest.TestCase):
    def test_something(self):
        result = fj.to_snake_case("testSomething")

        self.assertEqual("test_something", result)

    def test_regular_exp(self):
        result1 = re.split("[A-Z]", "ThisIsString")
        result2 = re.split("[A-Z]", "thisIsAnotherString")
        pass

if __name__ == "__main__":
    unittest.main()