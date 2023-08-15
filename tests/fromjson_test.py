import unittest
import re
import definitiongenerator.fromjson as fj


class Test_SnakeCaseAndCamelCaseConversions(unittest.TestCase):
    def test_testSomething_to_snake_case(self):
        result = fj.to_snake_case("testSomething")

        self.assertEqual("test_something", result)

    def test_ComplicatedMultipartStuff_to_snake_case(self):
        result = fj.to_snake_case("ComplicatedMultipartStuff")

        self.assertEqual("complicated_multipart_stuff", result)

    def test_numbers1234_to_snake_case(self):
        result = fj.to_snake_case("numbers1234")

        self.assertEqual("numbers1234", result)

    def test_Numbers1234_to_snake_case(self):
        result = fj.to_snake_case("Numbers1234")

        self.assertEqual("numbers1234", result)

    def test_Numbers1234WithSomething_to_snake_case(self):
        result = fj.to_snake_case("Numbers1234WithSomething")

        self.assertEqual("numbers1234_with_something", result)

    def test_ABC_to_snake_case(self):
        result = fj.to_snake_case("ABC")

        self.assertEqual("a_b_c", result)

    def test_test_something_to_camel_case(self):
        result = fj.to_camel_case("test_something")

        self.assertEqual("testSomething", result)

    def test_test_something1_to_camel_case(self):
        result = fj.to_camel_case("_test_something")

        self.assertEqual("testSomething", result)

    def test_complicated_multipart_string_to_camel_case(self):
        result = fj.to_camel_case("complicated_multipart_string")

        self.assertEqual("complicatedMultipartString", result)

    def test_number1234_multipart_string_to_camel_case(self):
        result = fj.to_camel_case("number1234")

        self.assertEqual("number1234", result)


class GatherMappingTests(unittest.TestCase):
    def test_list_of_complex_types(self):
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


if __name__ == "__main__":
    unittest.main()
