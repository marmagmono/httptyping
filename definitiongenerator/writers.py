import json
from dataclasses import dataclass, field
from typing import IO, Literal, Tuple
import definitiongenerator.model as m
import dataclasses as dc


@dataclass
class _TypeDescription:
    name: str
    properties: dict[str, "_TypeDescription"] = field(default_factory=dict)
    is_array: bool = field(default=False)
    sample_values: list[str] = field(default_factory=list)


@dataclass
class _MapperState:
    found_types: list[_TypeDescription] = field(default_factory=list)


def convert_to_dict(mapping: m.ModelMapping) -> list[dict]:
    state = _MapperState()
    final_state, model = _new_type_model(mapping, state, [])

    result = [dc.asdict(found_type) for found_type in final_state.found_types]
    return result


DumpFormat = Literal["TypedDict", "Markdown"]


def _dump_typed_dict_model(model_state: _MapperState, output: IO[str]):
    def print_header(output: IO[str]):
        output.write("from typing import TypedDict\n")
        output.write("\n")

    def print_type(type_description: _TypeDescription, output: IO[str]):
        indent = 4 * " "
        output.write("\n")
        output.write(f"class {type_description.name}(TypedDict):\n")
        for property_name, property_type_description, in type_description.properties.items():
            if property_type_description.is_array:
                property_type = f"list[{property_type_description.name}]"
            else:
                property_type = property_type_description.name

            output.write(f"{indent}{property_name}: {property_type}\n")

        output.write("\n")

    print_header(output)

    for found_type in model_state.found_types:
        print_type(found_type, output)


def _dump_markdown(model_state: _MapperState, output: IO[str]):
    def print_type(type_description: _TypeDescription, output: IO[str]):
        output.write(f"# {type_description.name} \n")
        for (
            property_name,
            property_type_description,
        ) in type_description.properties.items():
            if property_type_description.is_array:
                property_type = f"list[{property_type_description.name}]"
            else:
                property_type = property_type_description.name

            output.write(f"- {property_name}: {property_type}\n")
            if len(property_type_description.sample_values) > 0:
                for sv in property_type_description.sample_values:
                    output.write(f"  - {sv}\n")
        output.write("\n")

    for found_type in model_state.found_types:
        print_type(found_type, output)


def dump_model(
    mapping: m.ModelMapping, output: IO[str], *, dump_format: DumpFormat = "TypedDict"
):
    state = _MapperState()
    final_state, model = _new_type_model(mapping, state, [])
    if dump_format == "TypedDict":
        _dump_typed_dict_model(final_state, output)
        return

    elif dump_format == "Markdown":
        _dump_markdown(final_state, output)
        return

    raise ValueError(f"Unexpected dump_format={dump_format}")


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
    # end = len(path)
    # start = end - 1
    # while start >= 0:
    #     name = "".join(path[start:end]) + "Dict"
    #     if not any((s for s in state.found_types if s.name == name)):
    #         return name
    #
    #     start = start - 1

    # return "MainDict"


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
