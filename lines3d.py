# Lines with >=3 lattice points in the n x n x n grid {0..n-1}^3
from math import gcd
from itertools import product, combinations

def directions(n):
    m = (n - 1) // 2          # need p, p+d, p+2d inside the grid
    ds = []
    for a, b, c in product(range(-m, m + 1), repeat=3):
        if (a, b, c) == (0, 0, 0): continue
        if gcd(gcd(abs(a), abs(b)), abs(c)) != 1: continue
        first = next(v for v in (a, b, c) if v != 0)
        if first < 0: continue  # canonical sign
        ds.append((a, b, c))
    return ds

def lines(n):
    inside = lambda p: all(0 <= t < n for t in p)
    out = []
    for d in directions(n):
        for p in product(range(n), repeat=3):
            q = (p[0]-d[0], p[1]-d[1], p[2]-d[2])
            if inside(q): continue          # p must be the first point on its line
            pts, cur = [], p
            while inside(cur):
                pts.append(cur); cur = (cur[0]+d[0], cur[1]+d[1], cur[2]+d[2])
            if len(pts) >= 3: out.append(pts)
    return out

def brute_valid(pts):
    """Independent check: no three points collinear (cross product test)."""
    pts = [tuple(p) for p in pts]
    if len(set(pts)) != len(pts): return False, "duplicate"
    for A, B, C in combinations(pts, 3):
        u = (B[0]-A[0], B[1]-A[1], B[2]-A[2]); v = (C[0]-A[0], C[1]-A[1], C[2]-A[2])
        cr = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        if cr == (0, 0, 0): return False, (A, B, C)
    return True, None

if __name__ == "__main__":
    for n in range(3, 11):
        print(n, len(directions(n)), len(lines(n)))
