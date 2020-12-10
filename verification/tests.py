from enum_source import enum_source

source1 = '''\
limit = 100
assert all(
    sum(n ** 3 for n in range(N)) == (N * (N - 1) // 2) ** 2
    for N in range(1, limit)
)
'''

source2 = '''\
from typing import List

def f(n: int) -> List[int]:
    return [
        square
        for square in (number ** 2 for number in range(n))
        if square % 8
    ]

if __name__ == '__main__':
    from pprint import pprint
    pprint({n: len(squares) for squares in map(f, range(1, 100))})
'''

source3 = '''\
from typing import Dict, Iterator, List, Set

def connected_components(graph: Dict[str, List[str]]) -> Iterator[Set[str]]:
    """
    Generate connected components of an undirected graph
    using adjacency list representation.
    """
    seen = set()
    for start in graph:
        if start in seen:
            continue
        stack, component = [start], set()
        while stack:
            node = stack.pop()
            if node not in component:
                component.add(node)
                stack += [
                    neighbor
                    for neighbor in graph[node]
                    if neighbor not in component
                ]
        yield component
        seen |= component

if __name__ == '__main__':
    vertices = list('ABCDEF')
    edges = ['AC', 'BE', 'ED']
    graph = {vertex: [] for vertex in vertices}
    for A, B in edges:
        graph[A].append(B)
        graph[B].append(A)
    assert sorted(map(sorted, connected_components(graph))) == [
        ['A', 'C'], ['B', 'D', 'E'], ['F']]
'''

source4 = '''\
def S(s
,n=2,v='\\
_' ):
 q,r=divmod(len(s),n)
 return[
s[i*n:(i+1)*n]for i in range(q)]+r*[s[q*n:]+(n-r)*v]
'''

# My most obfuscated code with python3.8... (walrus operator)
source5 = '''\
C,m,T=__import__('functools').lru_cache,map,tuple
def F(d,s):s,f,g=[(P(z),r)for*z,r in s],C(lambda x:{i for i,(c,r)in enumerate(s)if c.d(x)<=r}),lambda r:all(i:=[*m(f,r)])and(1>=r.a()or bool(set.intersection(*i))or all(m(g,r.d())));return g(R((P((0,0)),P((d[0],0)),P(d),P((0,d[1])))))
class P(T):c,d=lambda p,q:P(((p[0]+q[0])/2,(p[1]+q[1])/2)),lambda p,q:((p[0]-q[0])**2+(p[1]-q[1])**2)**.5
class R(T):
 a=lambda s:s[0].d(s[1])*s[0].d(s[3])
 def d(s):a,b,c,d=s;e,f,g,h,i=m(P.c,(a,a,a,b,c),(b,c,d,c,d));return R((a,e,f,g)),R((e,b,h,f)),R((f,h,c,i)),R((g,f,i,d))
'''

TESTS = {
    '1. Expressions': [
        {
            'input': '[n ** 2 for n in range(5)]',
            'answer': {'ListComp': 1},
        },
        {
            'input': 'list(n ** 2 for n in range(5))',
            'answer': {'GeneratorExp': 1},
        },
        {
            'input': 'sum(n ** 2 for n in range(5))',
            'answer': {'GeneratorExp': 1},
        },
        {
            'input': '{n ** 2 for n in range(6)}',
            'answer': {'SetComp': 1},
        },
        {
            'input': 'set(n ** 2 for n in range(6))',
            'answer': {'GeneratorExp': 1},
        },
        {
            'input': '{n: n ** 2 for n in range(7)}',
            'answer': {'DictComp': 1},
        },
        {
            'input': 'dict((n, n ** 2) for n in range(7))',
            'answer': {'GeneratorExp': 1},
        },
        {
            'input': '(n ** 2 for n in range(8))',
            'answer': {'GeneratorExp': 1},
        },
        {
            'input': '[x for x in (n ** 2 for n in range(100)) if x % 8]',
            'answer': {'GeneratorExp': 1, 'ListComp': 1},
        },
    ],
    '2. Modules': [
        {
            'input': 'assert False, "It\'s just false."',
            'answer': {},
        },
        {
            'input': source1,
            'answer': {'GeneratorExp': 2},
        },
        {
            'input': source2,
            'answer': {'DictComp': 1, 'GeneratorExp': 1, 'ListComp': 1},
        },
        {
            'input': source3,
            'answer': {'DictComp': 1, 'ListComp': 1},
        },
        # https://py.checkio.org/mission/three-words/publications/Tubis/python-3/first/share/863c87edf8d31d3286afe2057388508b/#comment-9557
        {
            'input': "checkio=lambda t:'T'*3in''.join(str(w.isalpha())[0]for w in t.split())",
            'answer': {'GeneratorExp': 1},
        },
        {
            'input': source4,
            'answer': {'ListComp': 1},
        },
        {
            'input': source5,
            'answer': {'ListComp': 1, 'SetComp': 1},
        },
    ],
    '3. Real life': [
        {
            'input': enum_source,
            'answer': dict(DictComp=1, SetComp=1, GeneratorExp=3, ListComp=5),
        },
    ],
}


if __name__ == '__main__':
    from typing import Dict

    def count_comprehensions(source: str) -> Dict[str, int]:
        ...

    for tests in TESTS.values():
        for test in tests:
            # if ':=' in test['input']: print('skip walrus operator'); continue
            assert count_comprehensions(test['input']) == test['answer'], test
    print('Well done!')
