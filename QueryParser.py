from lark import Lark, Transformer


class QueryTransformer(Transformer):
    """
    This class guides the transformations
    of the Lark tree into an AST.
    """

    def or_node(self, vals):
        q1, q2 = vals
        return OrNode(q1, q2)

    def and_node(self, vals):
        q1, q2 = vals
        return AndNode(q1, q2)

    def not_node(self, q):
        (q,) = q
        return NotNode(q)

    def yesno_p(self, vals):
        status, phoneme = vals
        if status == 'present':
            return EqPhoneme('>', 0, phoneme)
        else:
            return EqPhoneme('=', 0, phoneme)

    def yesno_f(self, vals):
        status, features = vals
        if status == 'present':
            return EqFeature('>', 0, features)
        else:
            return EqFeature('=', 0, features)

    def eq_p(self, triple):
        return EqPhoneme(*triple)

    def eq_f(self, triple):
        return EqFeature(*triple)

    def feat_eq(self, triple):
        return EqFeatures(*triple)

    def PHONEME(self, val):
        return val[1:-1]

    def FEATURE(self, val):
        return val[:]

    def NUMBER(self, val):
        return int(val)

    features = set

    def present(self, _):
        return "present"

    def absent(self, _):
        return "absent"

    def ge(self, _):
        return '>='

    def gt(self, _):
        return '>'

    def lt(self, _):
        return '<'

    def le(self, _):
        return '<='

    def exactly(self, _):
        return '='


# Classes for AST nodes
class ASTNode():
    def __init__(self, node_type):
        self.node_type = node_type

    def __str__(self):
        buffer = [self.node_type]
        for k, v in self.__dict__.items():
            if k != 'node_type':
                if issubclass(type(v), ASTNode):
                    buffer.append(f'  {k}: {str_rec(v)}')
                else:
                    buffer.append(f'  {k}: {v}')
        return '\n'.join(buffer)


def str_rec(obj, depth=1):
    buffer = [obj.node_type]
    for k, v in obj.__dict__.items():
        if k != 'node_type':
            if issubclass(type(v), ASTNode):
                buffer.append(f'{"  "*(depth+1)}{k}: {str_rec(v, depth+1)}')
            else:
                buffer.append(f'{"  "*(depth+1)}{k}: {v}')
    return '\n'.join(buffer)


class EqPhoneme(ASTNode):
    def __init__(self, op, number, phoneme):
        super().__init__('EqPhoneme')
        self.phoneme = phoneme
        self.op = op
        self.number = number


class EqFeature(ASTNode):
    def __init__(self, op, number, features):
        super().__init__('EqFeature')
        self.features = set(features)
        self.op = op
        self.number = number


class EqFeatures(ASTNode):
    def __init__(self, op, features_1, features_2):
        super().__init__('EqFeatures')
        self.features_1 = set(features_1)
        self.features_2 = set(features_2)
        self.op = op


class OrNode(ASTNode):
    def __init__(self, q1, q2):
        super().__init__('OrNode')
        self.lhs = q1
        self.rhs = q2


class AndNode(ASTNode):
    def __init__(self, q1, q2):
        super().__init__('AndNode')
        self.lhs = q1
        self.rhs = q2


class NotNode(ASTNode):
    def __init__(self, q):
        super().__init__('NotNode')
        self.query = q


with open(f'search_grammar.lark', 'r', encoding='utf-8') as inp:
    query_parser = Lark(inp.read(), start='query')


if __name__ == "__main__":
    query = '''
    not (
        >= bilabial plosive, labio-dental fricative 
        or 
        <= bilabial plosive, labio-dental fricative
    ) or
    + /p/ and > 4 approximant
'''
    tree = query_parser.parse(query)
    print(f'An example query:\n\n{"*"*55}{query}{"*"*55}\n')
    print('The parse tree:')
    print(QueryTransformer().transform(tree))
