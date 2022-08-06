from pprint import pprint
import re

t = re.compile(r'\w+|[()|]')

def extract_terms(s):
    terms = t.findall(s.lower())
    return terms

def prepare_terms(terms):
    _i = 0
    def _prepare_terms():
        nonlocal _i
        while _i < len(terms):
            if terms[_i] == '(':
                _i += 1
                l = list(_prepare_terms())
                yield l
            elif terms[_i] == ')':
                _i += 1
                break
            else:
                yield terms[_i]
                _i += 1
    return list(_prepare_terms())

def make_ast(terms):
    elements = []
    for term in terms:
        if isinstance(term, list):
            if len(elements) != 0 and elements[-1]['type'] != 'op':
                elements.append({
                    'type': 'op',
                    'op':'and',
                })
            
            elements.append({
                'type': 'combine',
                'values': make_ast(term)
            })
        elif term == '|':
            if len(elements) != 0:
                elements.append({
                    'type': 'op',
                    'op':'or',
                })
        else:
            if len(elements) != 0 and elements[-1]['type'] != 'op':
                elements.append({
                    'type': 'op',
                    'op':'and',
                })

            elements.append({
                'type':'text',
                'value': term
            })
    return elements

if __name__ == '__main__':
    terms = extract_terms("anime (ero | porn) ino kek puk")
    elements = list(prepare_terms(terms))
    print(elements)
    ast = make_ast(elements)
    pprint(ast)