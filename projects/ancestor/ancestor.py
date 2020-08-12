def earliest_ancestor(ancestors, starting_node, is_child=False):
    for parent, child in ancestors:
        if child == starting_node:
            return earliest_ancestor(ancestors, parent, True)

    if is_child:
        return starting_node
    else:
        return -1

