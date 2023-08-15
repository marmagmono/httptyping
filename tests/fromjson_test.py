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


class NewMappingModelTests(unittest.TestCase):
    def test_int_mapping(self):
        result = fj.new_mapping_model(10)

        self.assertIsInstance(result, fj.SimpleMapping)
        self.assertEqual(int, result.value_type)
        self.assertEqual(0, len(result.string_value_set))

    def test_str_mapping(self):
        result = fj.new_mapping_model("value")

        self.assertIsInstance(result, fj.SimpleMapping)
        self.assertEqual(str, result.value_type)
        self.assertSetEqual(set(["value"]), result.string_value_set)

    def test_bool_True_mapping(self):
        result = fj.new_mapping_model(True)

        self.assertIsInstance(result, fj.SimpleMapping)
        self.assertEqual(bool, result.value_type)
        self.assertEqual(0, len(result.string_value_set))

    def test_bool_False_mapping(self):
        result = fj.new_mapping_model(False)

        self.assertIsInstance(result, fj.SimpleMapping)
        self.assertEqual(bool, result.value_type)
        self.assertEqual(0, len(result.string_value_set))

    def test_float_mapping(self):
        result = fj.new_mapping_model(10.0)

        self.assertIsInstance(result, fj.SimpleMapping)
        self.assertEqual(float, result.value_type)
        self.assertEqual(0, len(result.string_value_set))

    def test_list_of_string_mapping(self):
        result = fj.new_mapping_model(["first", "second", "third"])

        self.assertIsInstance(result, fj.ListMapping)

        element_mapping = result.element_mapping
        self.assertIsInstance(element_mapping, fj.SimpleMapping)
        self.assertEqual(str, element_mapping.value_type)
        self.assertSetEqual(set(["first", "second", "third"]), result.string_value_set)

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
