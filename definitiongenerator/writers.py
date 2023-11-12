from typing import IO, Literal, Protocol, TypedDict
import definitiongenerator.model as m

from definitiongenerator.outputtypemodel import (
    _MapperState,
    _TypeDescription,
    _new_type_model,
)


DumpFormat = Literal["TypedDict", "Markdown", "CSharp"]


class _TypeWriterProtocol(Protocol):
    def initialize(self, found_types: list[_TypeDescription], options: dict):
        ...

    def print_type(self, type_description: _TypeDescription, output: IO[str]):
        ...

    def print_header(self, found_types: list[_TypeDescription], output: IO[str]):
        ...


class _PythonTypedDictWriter(_TypeWriterProtocol):
    def initialize(self, options: dict):
        ...

    def print_header(self, found_types: list[_TypeDescription], output: IO[str]):
        output.write("from typing import TypedDict\n")
        output.write("\n")

    def print_type(self, type_description: _TypeDescription, output: IO[str]):
        indent = 4 * " "
        output.write("\n")
        output.write(f"class {type_description.name}(TypedDict):\n")
        for (
            property_name,
            property_type_description,
        ) in type_description.properties.items():
            if property_type_description.is_array:
                property_type = f"list[{property_type_description.name}]"
            else:
                property_type = property_type_description.name

            output.write(f"{indent}{property_name}: {property_type}\n")

        output.write("\n")


class _MarkdownWriter(_TypeWriterProtocol):
    def initialize(self, options: dict):
        ...

    def print_header(self, found_types: list[_TypeDescription], output: IO[str]):
        ...

    def print_type(self, type_description: _TypeDescription, output: IO[str]):
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


class CSharpWriterOptions(TypedDict):
    Namespace: str


class _CSharpWriter(_TypeWriterProtocol):
    options: CSharpWriterOptions | None

    def initialize(self, found_types: list[_TypeDescription], options: dict):
        self.options = options

    def print_header(self, found_types: list[_TypeDescription], output: IO[str]):
        # Using statements

        return super().print_header(found_types, output)


def dump_model(
    mapping: m.ModelMapping,
    output: IO[str],
    *,
    dump_format: DumpFormat = "TypedDict",
    options: dict | None = None,
):
    state = _MapperState()
    type_model, _ = _new_type_model(mapping, state, [])

    writers = {"TypedDict": _PythonTypedDictWriter(), "Markdown": _MarkdownWriter()}

    selected_writer: _TypeWriterProtocol = writers[dump_format]
    if options is not None:
        selected_writer.initialize(options=options)

    selected_writer.print_header(type_model.found_types, output)

    for found_type in type_model.found_types:
        selected_writer.print_type(found_type, output)
