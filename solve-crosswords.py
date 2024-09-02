import numpy as np
from numpy._typing import NDArray

# 1. Define a crossword structure
# 2. Get a bag of words
# 3. Solve the crossword by filling it with the bag of words

H, V = "→", "↓"
W, B = "_", "█"
GRID = np.array([
    [W, W, W, W, B],
    [W, W, W, B, W],
    [W, W, B, W, W],
    [W, B, W, W, W],
    [B, W, W, W, W],
])

WORDS = [
    [
        "aa", "ab", "ba", "bb"
    ], [
        "aaa", "aab", "aba", "abb", "baa", "bab", "bba", "bbb"
    ], [
        "aaaa", "aaab", "aaba", "aabb", "abaa", "abab", "abba", "abbb",
        "baaa", "baab", "baba", "babb", "bbaa", "bbab", "bbba", "bbbb"
    ]
]

def get_word_candidates(length: int, intersecting = [], similar = []):
    return WORDS[length - 2]

def find_line_hooks(line):
    line = np.insert(line, [0, len(line)], [B, B])
    blacks = np.where(line == B)[0]
    interval_lenths = np.diff(blacks)
    return list(blacks[np.where(interval_lenths > 2)[0]])

def find_hooks(grid):
    horizontal = [find_line_hooks(line) for line in grid]
    vertical = [find_line_hooks(line) for line in grid.T]

    return [(H, i, h) for i, p in enumerate(horizontal) for h in p] + \
        [(V, v, j) for j, p in enumerate(vertical) for v in p]

def solve_crossword(hooks, grid, bow):
    # todo: order hooks by length (longest to shortest)

    if hooks == []:
        return True

    for index, hook in enumerate(hooks):
        # find words of the right length for hook from bow
        # optionally filter for letters in the intersecting words
        words = get_word_candidates(-1)

        for word in words:
            grid_copy = np.copy(grid)
            # insert word in hook a change grid_copy
            remaining_hooks = hooks[index + 1:]
            if solve_crossword(remaining_hooks, grid_copy, bow):
                return True
            # remove word from hook (or simply don't do anything and grid_copy will be destroyed)

    return False


def main():
    hooks = find_hooks(GRID)
    print(hooks)

    for line in GRID:
        print(" ".join(line))

    # solve_crossword(GRID, 0, 0)

if __name__ == "__main__":
    main()
