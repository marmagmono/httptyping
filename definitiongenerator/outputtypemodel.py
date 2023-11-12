from dataclasses import dataclass, field
from typing import Tuple
import definitiongenerator.model as m


@dataclass
class _TypeDescription:
    name: str
    properties: dict[str, "_TypeDescription"] = field(default_factory=dict)
    is_array: bool = field(default=False)
    sample_values: list[str] = field(default_factory=list)


@dataclass
class _MapperState:
    found_types: list[_TypeDescription] = field(default_factory=list)


def _simple_mapping_to_type(
    mapping: m.SimpleMapping, state: _MapperState
) -> Tuple[_MapperState, _TypeDescription]:
    return (
        state,
        _TypeDescription(
            name=str(mapping.value_type.__name__),
            sample_values=sorted(mapping.string_value_set),
        ),
    )


def _get_type_name(state: _MapperState, path: list[str]):
    def capitalize(s: str):
        if len(s) == 0:
            return s

        if len(s) == 1:
            return s.upper()

        return s[0].upper() + s[1:]

    if len(path) == 0:
        return "MainDict"

    return "".join((capitalize(p) for p in path)) + "Dict"


def _object_mapping_to_type(
    mapping: m.ObjectMapping, state: _MapperState, path: list[str] | None = None
) -> Tuple[_MapperState, _TypeDescription]:
    # TODO: Uppercase
    if path is None:
        path = []

    type_name = _get_type_name(state, path)
    properties = {}

    new_state = state
    for prop_name, prop_mapping in mapping.properties.items():
        (new_state, mapped_type) = _new_type_model(
            prop_mapping, new_state, [*path, prop_name]
        )

        properties[prop_name] = mapped_type

    t = _TypeDescription(type_name, properties)
    new_state.found_types.append(t)
    return (new_state, t)


def _list_mapping_to_type(
    mapping: m.ListMapping, state: _MapperState, path: list[str] | None = None
) -> Tuple[_MapperState, _TypeDescription]:
    if mapping.element_mapping is None:
        return (state, _TypeDescription("?????", is_array=True))

    (new_state, type_mapping) = _new_type_model(mapping.element_mapping, state, path)
    return (new_state, _TypeDescription(type_mapping.name, is_array=True))


def _new_type_model(
    mapping: m.ModelMapping, state: _MapperState, path: list[str] | None = None
) -> Tuple[_MapperState, _TypeDescription]:
    """Creates type model from model mapping"""

    if isinstance(mapping, m.SimpleMapping):
        return _simple_mapping_to_type(mapping, state)

    if isinstance(mapping, m.ObjectMapping):
        return _object_mapping_to_type(mapping, state, path)

    if isinstance(mapping, m.ListMapping):
        return _list_mapping_to_type(mapping, state, path)

    if isinstance(mapping, m.AlternativesMapping):
        raise NotImplementedError("Not implemented")

    raise TypeError(f"Unsupported mapping type: {type(mapping)}")
