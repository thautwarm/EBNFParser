def analyze(cases):
    from .Node import LiteralValueParser, LiteralNameValueParser
    if len(cases) is 1 or not all(cases):
        return None

    groups = dict()
    group_order = []

    for case in cases:
        head = case[0]
        if isinstance(head, LiteralValueParser):
            group_id = "value:" + head.mode
        elif isinstance(head, LiteralNameValueParser):
            group_id = f'ref: {head.name} value: {head.mode}'
        else:
            group_id = "ref:" + head.name

        if group_id not in group_order:

            groups[group_id] = [case]
            group_order.append(group_id)
        else:
            groups[group_id].append(case)

    if len(group_order) is 1:
        return None

    return groups, group_order


def grammar_remake(groups, group_order):
    from .Node import AccompaniedAstParser
    return tuple(
        (
            (groups[groupId][0][0],
             AccompaniedAstParser(*[case[1:] for case in groups[groupId]])
             )
            if len(groups[groupId]) > 1 else groups[groupId][0]
        )
        for groupId in group_order)


def optimize(cases):
    analyzed = analyze(cases)
    if analyzed is None:
        return cases
    groups, group_order = analyzed
    return grammar_remake(groups, group_order)
