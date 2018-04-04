import linq

try:
    from cytoolz import curry
except ModuleNotFoundError:
    from toolz import curry


@curry
def function_debugger(tag: str, content: str, dictionary: dict, indent: int, inc_indent: int):
    case_map = {tag: 1,
                content: 2}

    indent = " " * indent
    inc_indent = f"{indent}" + " " * inc_indent;

    groups = linq.Flow(dictionary.items()).Map(lambda a, b: (a, b)).GroupBy(
        lambda a, b: case_map.get(a, 0)).Unboxed()

    others = '\n'.join(map(lambda each: f"{inc_indent}<{each[0]}> {each[1]} </{each[0]}>", groups[0]))

    content = f"<{groups[2][0][1]}>"

    return (f"{indent}<{groups[1][0][1]}>\n"
            f"{others}\n"
            f'{inc_indent}{content}\n'
            f"{indent}</{groups[1][0][1]}>")
