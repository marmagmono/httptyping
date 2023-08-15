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
class _SimpleMappingType:
    value_type: type
    string_value_set: set[str] = field(default_factory=set)


@dataclass
class _ListMappingType:
    # None -> if list was always empty
    element_mapping: Optional["_MappingType"]


@dataclass
class _AlternativesMappingType:
    alternatives: list["_MappingType"]


@dataclass
class _ObjectMappingType:
    properties: dict[str, "_MappingType"]


_MappingType = (
    _SimpleMappingType
    | _ListMappingType
    | _ObjectMappingType
    | _AlternativesMappingType
)

# mapping:
# - multiple different types
# - type is list
# - type is object


def _is_simple_type(t: type):
    return (t is bool) or (t is int) or (t is float) or (t is str)


def _new_mapping(v: Any) -> _MappingType:
    v_type = type(v)
    if _is_simple_type(v_type):
        mapping = _SimpleMappingType(value_type=v_type)
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
        return _ListMappingType(element_mapping=None)

    element_mapping = _new_object_mapping(v[0])
    for element in v[1:]:
        _update_mapping(element_mapping, element)

    return _ListMappingType(element_mapping=element_mapping)


def _new_object_mapping(v: dict):
    property_mappings: dict[str, _MappingType] = dict()
    for k, v in v.items():
        property_mappings[k] = _new_mapping(v)

    return _ObjectMappingType(property_mappings)


def _update_mapping(current_mapping: _MappingType, v: Any) -> _MappingType:
    v_type = type(v)
    if isinstance(current_mapping, _SimpleMappingType):
        if current_mapping.value_type == v_type:
            if v_type is str:
                current_mapping.string_value_set.add(v)

            return current_mapping

        new_mapping = _new_mapping(v)
        return _AlternativesMappingType(alternatives=[current_mapping, new_mapping])

    if isinstance(current_mapping, _ListMappingType):
        if isinstance(v, list):
            if len(v) > 0:
                for e in v:
                    current_mapping.element_mapping = _update_mapping(
                        current_mapping.element_mapping, e
                    )
            return current_mapping

        else:
            # v is not a list
            mapping = _new_mapping(v)
            return _AlternativesMappingType(alternatives=[current_mapping, mapping])

    if isinstance(current_mapping, _ObjectMappingType):
        if isinstance(v, dict):
            for property_name, property_value in v.items():
                property_mapping = current_mapping.properties.get(property_name)
                if property_mapping is not None:
                    _update_mapping(property_mapping, property_value)
                else:
                    new_mapping = _new_mapping(property_value)
                    current_mapping.properties[property_name] = new_mapping

            return current_mapping
        else:
            # v is not a dict
            mapping = _new_mapping(v)
            return _AlternativesMappingType(alternatives=[current_mapping, mapping])

    if isinstance(current_mapping, _AlternativesMappingType):
        raise Exception("Updating alternatives mapping is not implemented")

    raise Exception(f"Unexpected mapping type: {type(current_mapping)}")


# def _gather_types(dict_iterable: Iterable[dict]) -> _MappingType:
#     mapping: dict[str, _MappingType] = {}

#     for item in dict_iterable:
#         for k, v in item.items():
#             # determine whether type matches current entry ?
#             if k in mapping:
#                 mapping[k] = _update_mapping(mapping[k], k, v)
#             else:
#                 mapping[k] = _new_mapping(k, v)

#             mapping_item = mapping.setdefault(k, _SimpleMappingType())

#             value_type = type(v)
#             mapping_item.type_set.add(value_type)
#             if isinstance(v, str):
#                 mapping_item.string_value_set.add(v)

#     return mapping
