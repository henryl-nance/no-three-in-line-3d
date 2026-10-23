# No-three-in-line in the n×n×n grid — new lower bounds (Oct 22, 2026)

Problem: place as many points as possible in the n×n×n integer grid so that no three lie on any straight line.
Known before this run (SeqFan thread "No three in line, 3D", June 2026): a(1..6) = 1, 8, 16, 28, 40, 64 (n=5, 6 proven by ILP), a(7) ≥ 72, a(8) ≥ 91.

| n | previous public bound | new configuration | how found |
|---|---|---|---|
| 7 | ≥ 72 | **73** | CP-SAT, symmetric under all permutations of (x,y,z); 74 proven impossible within that symmetry class |
| 8 | ≥ 91 | **92** | CP-SAT, symmetric under coordinate permutations + point reflection through the center; optimal within that class |
| 9 | none posted | **116** | same symmetry as n=8; optimal within that class |
| 10 | none posted | **134** | same symmetry; search not finished, likely improvable |

Verification: `python3 verify.py n7_73points.json n8_92points.json n9_116points.json n10_134points.json`
groups every pair of points by the exact line through them and reports the most points on any line (must be 2).
The solver also re-checks every triple with a cross-product test. Code reproduces the known exact values a(3)=16, a(4)=28 and finds 40 and 64 for n=5, 6.

These are lower bounds (existence), not proofs of optimality; a(7) and a(8) remain open.

## n = 7, 73 points
{{0,0,1}, {0,0,4}, {0,1,0}, {0,1,2}, {0,2,1}, {0,2,4}, {0,3,5}, {0,4,0}, {0,4,2}, {0,5,3}, {0,5,5}, {1,0,0}, {1,0,2}, {1,1,5}, {1,1,6}, {1,2,0}, {1,3,5}, {1,3,6}, {1,5,1}, {1,5,3}, {1,6,1}, {1,6,3}, {2,0,1}, {2,0,4}, {2,1,0}, {2,3,6}, {2,4,0}, {2,4,4}, {2,5,5}, {2,5,6}, {2,6,3}, {2,6,5}, {3,0,5}, {3,1,5}, {3,1,6}, {3,2,6}, {3,5,0}, {3,5,1}, {3,6,1}, {3,6,2}, {4,0,0}, {4,0,2}, {4,2,0}, {4,2,4}, {4,4,2}, {4,5,6}, {4,6,5}, {4,6,6}, {5,0,3}, {5,0,5}, {5,1,1}, {5,1,3}, {5,2,5}, {5,2,6}, {5,3,0}, {5,3,1}, {5,4,6}, {5,5,0}, {5,5,2}, {5,6,2}, {5,6,4}, {6,1,1}, {6,1,3}, {6,2,3}, {6,2,5}, {6,3,1}, {6,3,2}, {6,4,5}, {6,4,6}, {6,5,2}, {6,5,4}, {6,6,4}, {6,6,6}}

## n = 8, 92 points
{{0,0,2}, {0,0,5}, {0,1,6}, {0,2,0}, {0,2,4}, {0,3,6}, {0,3,7}, {0,4,2}, {0,4,7}, {0,5,0}, {0,6,1}, {0,6,3}, {0,7,3}, {0,7,4}, {1,0,6}, {1,1,1}, {1,1,3}, {1,2,5}, {1,3,1}, {1,4,5}, {1,4,7}, {1,5,2}, {1,5,4}, {1,6,0}, {1,6,7}, {1,7,4}, {1,7,6}, {2,0,0}, {2,0,4}, {2,1,5}, {2,3,6}, {2,4,0}, {2,5,1}, {2,5,6}, {2,6,3}, {2,6,5}, {2,7,7}, {3,0,6}, {3,0,7}, {3,1,1}, {3,2,6}, {3,5,7}, {3,6,0}, {3,6,2}, {3,7,0}, {3,7,5}, {4,0,2}, {4,0,7}, {4,1,5}, {4,1,7}, {4,2,0}, {4,5,1}, {4,6,6}, {4,7,0}, {4,7,1}, {5,0,0}, {5,1,2}, {5,1,4}, {5,2,1}, {5,2,6}, {5,3,7}, {5,4,1}, {5,6,2}, {5,7,3}, {5,7,7}, {6,0,1}, {6,0,3}, {6,1,0}, {6,1,7}, {6,2,3}, {6,2,5}, {6,3,0}, {6,3,2}, {6,4,6}, {6,5,2}, {6,6,4}, {6,6,6}, {6,7,1}, {7,0,3}, {7,0,4}, {7,1,4}, {7,1,6}, {7,2,7}, {7,3,0}, {7,3,5}, {7,4,0}, {7,4,1}, {7,5,3}, {7,5,7}, {7,6,1}, {7,7,2}, {7,7,5}}
