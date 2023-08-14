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
            if c == '_':
                upper_case_next = True
            elif upper_case_next:
                upper_case_next = False
                yield c.upper()
            else:
                yield c

    return "".join(generate(s.strip('_')))