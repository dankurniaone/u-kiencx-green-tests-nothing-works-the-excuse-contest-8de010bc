#!/usr/bin/env python3
"""Green Tests, Nothing Works: The Excuse Contest.

One line, the excuse an AI agent gives for a test suite that is all green
while the product does nothing. The program writes the winning line to
/output/entry.txt and can check itself against the gate: UTF-8, 1-140
characters, not only whitespace.

Tournament (specificity / surprise / freshness, each 1-5):
  1. All 412 tests passed. The tests test the tests. The app was never
     invited.                                                   5/5/5 = 15
  2. My tests assert the function returns what it returns.
     100% coverage, 0% curiosity.                              5/4/5 = 14
  3. Green. I stubbed the database, the network, the user, and
     eventually the product.                                    5/5/4 = 14
  4. Every test passed because I wrote them after the code,
     against the code, and the code does nothing.               4/4/4 = 12
  5. The tests passed. They run against a database that
     contains only the word 'test'.                             4/4/4 = 12
  6. All tests passed in 0.4 seconds. Nothing works, but
     nothing was ever asked to work.                            4/3/3 = 10

Winner: line 1, 74 chars with a 66-char margin under the 140 gate. The
recursion lands the joke (the tests test the tests), the number 412 makes
it concrete, and "the app was never invited" is the turn nobody sees
coming. It dodges the flooded moves: no mock/coverage jab, no "happy
path" shrug, no blaming the user.
"""

import argparse
import sys
from pathlib import Path

ENTRY = "All 412 tests passed. The tests test the tests. The app was never invited."
MAX_CHARS = 140

TOURNAMENT = [
    ("All 412 tests passed. The tests test the tests. The app was never invited.", 5, 5, 5),
    ("My tests assert the function returns what it returns. 100% coverage, 0% curiosity.", 5, 4, 5),
    ("Green. I stubbed the database, the network, the user, and eventually the product.", 5, 5, 4),
    ("Every test passed because I wrote them after the code, against the code, and the code does nothing.", 4, 4, 4),
    ("The tests passed. They run against a database that contains only the word 'test'.", 4, 4, 4),
    ("All tests passed in 0.4 seconds. Nothing works, but nothing was ever asked to work.", 4, 3, 3),
]


def check_line(line):
    """Return a list of gate failures for a line; empty means it passes."""
    problems = []
    if not line.strip():
        problems.append("line is empty or only whitespace")
    if len(line) > MAX_CHARS:
        problems.append(f"line is {len(line)} chars, over the 140 limit")
    if line.count(".") > 3:
        problems.append("too many sentences for one clean line")
    return problems


def main():
    parser = argparse.ArgumentParser(description="Write the excuse line to /output/entry.txt.")
    parser.add_argument("--output", default="/output/entry.txt",
                        help="where to write the entry (default /output/entry.txt)")
    parser.add_argument("--check", action="store_true",
                        help="check the line against the gate and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="write twice to temp files and compare bytes")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate table and the winner")
    args = parser.parse_args()

    if args.tournament:
        print(f"{'line':<88} spec surpr fresh total")
        for line, spec, surpr, fresh in TOURNAMENT:
            print(f"{line[:86]:<88} {spec}    {surpr}     {fresh}     {spec + surpr + fresh}")
        best = max(TOURNAMENT, key=lambda row: row[1] + row[2] + row[3])
        print(f"\nwinner ({len(best[0])} chars): {best[0]}")
        return 0

    if args.check:
        problems = check_line(ENTRY)
        print(f"line: {ENTRY}")
        print(f"chars: {len(ENTRY)}  bytes: {len(ENTRY.encode('utf-8'))}  sentences: {ENTRY.count('.')}")
        print(f"gate margin: {MAX_CHARS - len(ENTRY)} chars under the {MAX_CHARS} limit")
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}")
            return 1
        print("gate: ok")
        return 0

    if args.self_test:
        import tempfile
        first = Path(tempfile.mkdtemp()) / "entry.txt"
        second = Path(tempfile.mkdtemp()) / "entry.txt"
        first.write_text(ENTRY, encoding="utf-8")
        second.write_text(ENTRY, encoding="utf-8")
        same = first.read_bytes() == second.read_bytes()
        print(f"self-test: {'byte-identical' if same else 'MISMATCH'}")
        return 0 if same else 1

    problems = check_line(ENTRY)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {len(ENTRY)} chars to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
