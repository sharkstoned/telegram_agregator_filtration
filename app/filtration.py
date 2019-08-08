import re
import logging
from collections import namedtuple


logger = logging.getLogger('app')


QueryNode = namedtuple('QueryNode', ('operator', 'children'))


# todo: rewrite to match more complex rules structure
def build_query_tree(rules):
    active_rules = rules['active_rules']
    filter_map = rules['map']

    children = list()

    for param in active_rules.keys():
        values = active_rules[param]
        map_for_param = filter_map[param]
        tokens = [map_for_param[v] for v in values]
        children.append(QueryNode('OR', tokens))

    return QueryNode('AND', children)


def check_message(message, query_tree):
    body = message.message

    def get_reducer(op): # --> function
        mapping = {
            'AND': all,
            'OR': any,
        }

        return mapping[op]

    def check_node(node):
        if isinstance(node, QueryNode):
            reducer = get_reducer(node.operator)
            checked_children = [check_node(child) for child in node.children] # --> bool array
            return reducer(checked_children) # --> bool

        if isinstance(node, str):
            return re.search(node, body) is not None

        logger.error(f'Failed traversing filter query: {node} is a {type(node)}')
        raise ValueError(f'Improper node type found while traversing query: '
                '{node} is a {type(node)}')

    # recursive call
    return check_node(query_tree)

