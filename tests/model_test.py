import unittest
import definitiongenerator.model as fj


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

    def test_simple_object_mapping(self):
        result = fj.new_mapping_model(
            {"propA": "A value", "intProp": 10, "floatProp": 20.0, "boolProp": True}
        )

        self.assertIsInstance(result, fj.ObjectMapping)

        props = result.properties
        self._assert_simple_mapping(props["propA"], str, ["A value"])
        self._assert_simple_mapping(props["intProp"], int)
        self._assert_simple_mapping(props["floatProp"], float)
        self._assert_simple_mapping(props["boolProp"], bool)
        self.assertEqual(4, len(props))

    def test_object_with_none_value_mapping(self):
        result = fj.new_mapping_model(
            {"propA": None, "intProp": 10, "floatProp": 20.0, "boolProp": True}
        )

        self.assertIsInstance(result, fj.ObjectMapping)

        props = result.properties
        self._assert_simple_mapping(props["intProp"], int)
        self._assert_simple_mapping(props["floatProp"], float)
        self._assert_simple_mapping(props["boolProp"], bool)
        self.assertEqual(3, len(props))

    def test_list_of_string_mapping(self):
        result = fj.new_mapping_model(["first", "second", "third"])

        self.assertIsInstance(result, fj.ListMapping)

        element_mapping = result.element_mapping
        self.assertIsInstance(element_mapping, fj.SimpleMapping)
        self.assertEqual(str, element_mapping.value_type)
        self.assertSetEqual(
            set(["first", "second", "third"]), element_mapping.string_value_set
        )

    def test_list_of_objects_mapping(self):
        result = fj.new_mapping_model(
            [
                {"propA": "A value", "intProp": 100},
                {"propA": "B value", "intProp": 200},
                {"intProp": 300},
                {"propA": "C value", "boolProp": True},
            ]
        )

        self.assertIsInstance(result, fj.ListMapping)

        element_mapping: fj.ObjectMapping = result.element_mapping
        self.assertIsInstance(element_mapping, fj.ObjectMapping)

        props = element_mapping.properties
        self._assert_simple_mapping(
            props["propA"], str, ["A value", "B value", "C value"]
        )
        self._assert_simple_mapping(props["intProp"], int)
        self._assert_simple_mapping(props["boolProp"], bool)
        self.assertEqual(3, len(props))

    def test_list_of_objects_with_none_values_mapping(self):
        result = fj.new_mapping_model(
            [
                {"propA": "A value", "intProp": 100},
                {"propA": "B value", "intProp": None},
            ]
        )

        self.assertIsInstance(result, fj.ListMapping)

        element_mapping: fj.ObjectMapping = result.element_mapping
        self.assertIsInstance(element_mapping, fj.ObjectMapping)

        props = element_mapping.properties
        self._assert_simple_mapping(
            props["propA"], str, ["A value", "B value"]
        )
        self._assert_simple_mapping(props["intProp"], int)
        self.assertEqual(2, len(props))

    def test_list_of_objects_with_first_none_values_mapping(self):
        result = fj.new_mapping_model(
            [
                {"propA": "A value", "intProp": None},
                {"propA": "B value", "intProp": 100},
            ]
        )

        self.assertIsInstance(result, fj.ListMapping)

        element_mapping: fj.ObjectMapping = result.element_mapping
        self.assertIsInstance(element_mapping, fj.ObjectMapping)

        props = element_mapping.properties
        self._assert_simple_mapping(
            props["propA"], str, ["A value", "B value"]
        )
        self._assert_simple_mapping(props["intProp"], int)
        self.assertEqual(2, len(props))

    def test_empty_list_in_element_mapping(self):
        result = fj.new_mapping_model(
            [
                {'a': []},
                {'a': [10, 20]}
            ]
        )

        self.assertIsInstance(result, fj.ListMapping)

        em: fj.ObjectMapping = result.element_mapping
        self.assertIsInstance(em, fj.ObjectMapping)

        a_prop: fj.ListMapping = em.properties['a']
        self.assertIsInstance(a_prop, fj.ListMapping)
        self._assert_simple_mapping(a_prop.element_mapping, int)

    def test_empty_list_mapping(self):
        result = fj.new_mapping_model(
            [
                {'a': []},
                {'a': []},
                {'a': []},
            ]
        )

        self.assertIsInstance(result, fj.ListMapping)

        em: fj.ObjectMapping = result.element_mapping
        self.assertIsInstance(em, fj.ObjectMapping)

        a_prop: fj.ListMapping = em.properties['a']
        self.assertIsInstance(a_prop, fj.ListMapping)
        self.assertIsNone(a_prop.element_mapping)

    def test_list_of_complex_types(self):
        input = [
            {
                "propA": {
                    "propB": {"insideB1": "test", "insideB2": "test2"},
                    "listInA": [
                        {"name": "A", "value": 10},
                        {"name": "B", "value": 20},
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
        self.assertIsInstance(result, fj.ListMapping)

        # validate list element
        el: fj.ObjectMapping = result.element_mapping
        self.assertIsInstance(el, fj.ObjectMapping)

        self.assertEqual(1, len(el.properties))

        # validate propA object
        propA: fj.ObjectMapping = el.properties["propA"]
        self.assertIsInstance(propA, fj.ObjectMapping)

        self.assertEqual(2, len(propA.properties))

        # validate propB object
        propB: fj.ObjectMapping = propA.properties["propB"]
        self.assertIsInstance(propB, fj.ObjectMapping)
        self.assertEqual(3, len(propB.properties))

        self._assert_simple_mapping(
            propB.properties["insideB1"], str, ["test", "test2222"]
        )
        self._assert_simple_mapping(
            propB.properties["insideB2"], str, ["test2", "test2ffff"]
        )
        self._assert_simple_mapping(propB.properties["insideB3"], float)

        # validate list in propA
        list_in_A: fj.ListMapping = propA.properties["listInA"]
        self.assertIsInstance(list_in_A, fj.ListMapping)

        list_el: fj.ObjectMapping = list_in_A.element_mapping
        self.assertIsInstance(list_el, fj.ObjectMapping)

        self._assert_simple_mapping(
            list_el.properties["name"], str, ["A", "B", "C"]
        )
        self._assert_simple_mapping(list_el.properties["value"], int)

    def _assert_simple_mapping(
            self,
            mapping: fj.ModelMapping,
            expected_type: type,
            expected_str_values: list[str] | None = None,
    ):
        self.assertIsInstance(mapping, fj.SimpleMapping)
        self.assertEqual(expected_type, mapping.value_type)

        if expected_str_values is not None:
            self.assertSetEqual(set(expected_str_values), mapping.string_value_set)
        else:
            self.assertEqual(0, len(mapping.string_value_set))


if __name__ == "__main__":
    unittest.main()
