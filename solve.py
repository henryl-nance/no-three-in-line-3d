import sys, time, json
from ortools.sat.python import cp_model
from lines3d import lines, brute_valid
from itertools import product, permutations

def sym_maps(n, kind):
    r = n - 1
    if kind == "none": return []
    if kind == "inv":  return [lambda p: (r-p[0], r-p[1], r-p[2])]          # point reflection through center
    if kind == "rot3": return [lambda p: (p[1], p[2], p[0])]                 # 3-fold rotation about main diagonal
    if kind == "inv+rot3": return [lambda p: (r-p[0], r-p[1], r-p[2]), lambda p: (p[1], p[2], p[0])]
    if kind == "rot2z": return [lambda p: (r-p[0], r-p[1], p[2])]            # half-turn about z-axis
    if kind == "S3": return [lambda p: (p[1], p[0], p[2]), lambda p: (p[1], p[2], p[0])]
    if kind == "S3+inv": return [lambda p: (p[1], p[0], p[2]), lambda p: (p[1], p[2], p[0]), lambda p: (r-p[0], r-p[1], r-p[2])]
    if kind == "rot4z": return [lambda p: (p[1], r-p[0], p[2])]
    if kind == "rot4z+inv": return [lambda p: (p[1], r-p[0], p[2]), lambda p: (r-p[0], r-p[1], r-p[2])]
    if kind == "rot4z+mz": return [lambda p: (p[1], r-p[0], p[2]), lambda p: (p[0], p[1], r-p[2])]
    raise ValueError(kind)

def orbits(n, maps):
    pts = list(product(range(n), repeat=3)); seen = {}; orbs = []
    for p in pts:
        if p in seen: continue
        orb = {p}; stack = [p]
        while stack:
            q = stack.pop()
            for f in maps:
                s = f(q)
                if s not in orb: orb.add(s); stack.append(s)
        k = len(orbs); orbs.append(sorted(orb))
        for q in orb: seen[q] = k
    return orbs, seen

def solve(n, tlimit=60, kind="none", seed=0, target=None):
    L = lines(n); orbs, idx = orbits(n, sym_maps(n, kind))
    m = cp_model.CpModel(); y = [m.NewBoolVar(f"y{k}") for k in range(len(orbs))]
    seen = set()
    for ln in L:
        cnt = {}
        for p in ln: cnt[idx[p]] = cnt.get(idx[p], 0) + 1
        key = tuple(sorted(cnt.items()))
        if key in seen: continue
        seen.add(key)
        if sum(cnt.values()) <= 2: continue
        m.Add(sum(c * y[k] for k, c in cnt.items()) <= 2)
    total = sum(len(orbs[k]) * y[k] for k in range(len(orbs)))
    if target: m.Add(total >= target)
    m.Maximize(total)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlimit
    s.parameters.num_workers = 1; s.parameters.random_seed = seed
    t = time.time(); st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        pts = [p for k in range(len(orbs)) if s.Value(y[k]) for p in orbs[k]]
        ok, bad = brute_valid(pts)
        return dict(n=n, kind=kind, count=len(pts), status=s.StatusName(st), bound=s.BestObjectiveBound(),
                    secs=round(time.time()-t, 1), valid=ok, pts=sorted(pts))
    return dict(n=n, kind=kind, status=s.StatusName(st), secs=round(time.time()-t, 1))

if __name__ == "__main__":
    n = int(sys.argv[1]); tl = float(sys.argv[2]); kind = sys.argv[3] if len(sys.argv) > 3 else "none"
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    tgt = int(sys.argv[5]) if len(sys.argv) > 5 else None
    r = solve(n, tl, kind, seed, tgt)
    print({k: v for k, v in r.items() if k != "pts"})
    if "pts" in r:
        with open(f"best_n{n}_{kind}_s{seed}_{r['count']}.json", "w") as f: json.dump(r, f)
