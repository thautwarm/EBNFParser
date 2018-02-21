def analyze(ebnf):

    if len(ebnf) is 1 or not all(ebnf): return None

    groups   =  dict()
    groupOrder =  []

    for case in ebnf:
        groupId = case[0].name

        if groupId not in groupOrder:

            groups[groupId] = [case]
            groupOrder.append(groupId)
        else:
            groups[groupId].append(case)

    if len(groupOrder) is 1: return None

    return groups, groupOrder

def grammarRemake(groups, groupOrder):
    from .Node import DependentAstParser
    return [([groups[groupId][0][0], DependentAstParser(
                  *[case[1:] for case in groups[groupId]])]
                if len(groups[groupId])>1 else
              groups[groupId][0])
            for groupId in groupOrder]

def optimize(ebnf):
    analyzed = analyze(ebnf)
    if analyzed is None:
        return ebnf
    groups, groupOrder = analyzed
    return grammarRemake(groups, groupOrder)







