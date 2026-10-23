import json, sys
from math import gcd
def check(pts, n):
    pts = [tuple(p) for p in pts]; lines = {}
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            a, b = pts[i], pts[j]; d = [b[k]-a[k] for k in range(3)]
            g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = [x//g for x in d]
            if next(x for x in d if x) < 0: d = [-x for x in d]
            c = (a[1]*d[2]-a[2]*d[1], a[2]*d[0]-a[0]*d[2], a[0]*d[1]-a[1]*d[0])   # a x d is constant along a line
            lines.setdefault((tuple(d), c), set()).update([a, b])
    return len(pts), len(set(pts)), all(0 <= c < n for p in pts for c in p), max(len(s) for s in lines.values())
for f in sys.argv[1:]:
    r = json.load(open(f)); print(f, "-> points, distinct, in-grid, max-on-a-line =", check(r['pts'], r['n']))
