def to_snake_case(s: str):
    def generate():
        for c in s:
            if c.isupper():
                yield "_"
                yield s.lower()

    return "".join(generate())
