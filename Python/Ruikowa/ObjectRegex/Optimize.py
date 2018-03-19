def analyze(ebnf):
    from .Node import LiteralValueParser
    if len(ebnf) is 1 or not all(ebnf):
        return None

    groups = dict()
    group_order = []

    for case in ebnf:
        head = case[0]
        if isinstance(head, LiteralValueParser):
            group_id = "value:" + head.mode
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


def grammar_remake(groups, groupOrder):
    from .Node import AccompaniedAstParser
    return tuple(
        (
            (groups[groupId][0][0],
             AccompaniedAstParser(*[case[1:] for case in groups[groupId]])
             )
            if len(groups[groupId]) > 1 else groups[groupId][0]
        )
        for groupId in groupOrder)


def optimize(ebnf):
    analyzed = analyze(ebnf)
    if analyzed is None:
        return ebnf
    groups, group_order = analyzed
    return grammar_remake(groups, group_order)
