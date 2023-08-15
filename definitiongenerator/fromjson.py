from dataclasses import field, dataclass
from typing import Any, Iterable, Optional


def to_snake_case(s: str):
    def generate():
        first_char = True
        for c in s:
            if c.isupper():
                if not first_char:
                    yield "_"
                yield c.lower()
            else:
                yield c

            first_char = False

    return "".join(generate())


def to_camel_case(s: str):
    def generate(input_s: str):
        upper_case_next = False
        for c in input_s:
            if c == "_":
                upper_case_next = True
            elif upper_case_next:
                upper_case_next = False
                yield c.upper()
            else:
                yield c

    return "".join(generate(s.strip("_")))


@dataclass
class SimpleMapping:
    value_type: type
    string_value_set: set[str] = field(default_factory=set)


@dataclass
class ListMapping:
    # None -> if list was always empty
    element_mapping: Optional["ModelMapping"]


@dataclass
class AlternativesMapping:
    alternatives: list["ModelMapping"]


@dataclass
class ObjectMapping:
    properties: dict[str, "ModelMapping"]


ModelMapping = (
    SimpleMapping
    | ListMapping
    | ObjectMapping
    | AlternativesMapping
)

# mapping:
# - multiple different types
# - type is list
# - type is object


def _is_simple_type(t: type):
    return (t is bool) or (t is int) or (t is float) or (t is str)


def new_mapping_model(v: Any) -> ModelMapping:
    v_type = type(v)
    if _is_simple_type(v_type):
        mapping = SimpleMapping(value_type=v_type)
        if isinstance(v, str):
            mapping.string_value_set.add(v)

        return mapping

    # object
    if v_type is dict:
        mapping = _new_object_mapping(v)
        return mapping

    if v_type is list:
        mapping = _new_list_mapping(v)
        return mapping

    raise Exception(f"Creation of mapping for type {v_type} is not implemented.")


def _new_list_mapping(v: list):
    if len(v) == 0:
        return ListMapping(element_mapping=None)

    element_mapping = new_mapping_model(v[0])
    for element in v[1:]:
        _update_mapping(element_mapping, element)

    return ListMapping(element_mapping=element_mapping)


def _new_object_mapping(v: dict):
    property_mappings: dict[str, ModelMapping] = dict()
    for k, v in v.items():
        property_mappings[k] = new_mapping_model(v)

    return ObjectMapping(property_mappings)


def _update_mapping(current_mapping: ModelMapping, v: Any) -> ModelMapping:
    v_type = type(v)
    if isinstance(current_mapping, SimpleMapping):
        if current_mapping.value_type == v_type:
            if v_type is str:
                current_mapping.string_value_set.add(v)

            return current_mapping

        new_mapping = new_mapping_model(v)
        return AlternativesMapping(alternatives=[current_mapping, new_mapping])

    if isinstance(current_mapping, ListMapping):
        if isinstance(v, list):
            if len(v) > 0:
                if current_mapping.element_mapping is None:
                    current_mapping.element_mapping = new_mapping_model(v[0])

                for e in v:
                    current_mapping.element_mapping = _update_mapping(
                        current_mapping.element_mapping, e
                    )
            return current_mapping

        else:
            # v is not a list
            mapping = new_mapping_model(v)
            return AlternativesMapping(alternatives=[current_mapping, mapping])

    if isinstance(current_mapping, ObjectMapping):
        if isinstance(v, dict):
            for property_name, property_value in v.items():
                property_mapping = current_mapping.properties.get(property_name)
                if property_mapping is not None:
                    _update_mapping(property_mapping, property_value)
                else:
                    new_mapping = new_mapping_model(property_value)
                    current_mapping.properties[property_name] = new_mapping

            return current_mapping
        else:
            # v is not a dict
            mapping = new_mapping_model(v)
            return AlternativesMapping(alternatives=[current_mapping, mapping])

    if isinstance(current_mapping, AlternativesMapping):
        raise Exception("Updating alternatives mapping is not implemented")

    raise Exception(f"Unexpected mapping type: {type(current_mapping)}")
