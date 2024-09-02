import numpy as np
from copy import deepcopy

# 1. Define a crossword structure
# 2. Get a bag of words
# 3. Solve the crossword by filling it with the bag of words

H, V = "→", "↓"
W, B = "_", "█"
GRID = np.array([
    [B, W, B, W, B],
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

def print_grid(grid):
    for line in grid: print(" ".join(line))

def insert_word(grid, hook, word):
    (direction, x, y, lenght) = hook

    if lenght != len(word):
        raise ValueError(f"Mismatch between word lenght and slot size: {len(word)} (word) != {lenght} (slot)!")

    if direction == V:
        grid = grid.T
        x, y = y, x

    grid[x][y:y+lenght] = list(word)
    return grid.T if direction == V else grid

def find_line_hooks(line):
    # Insert black square at the beginning and end of the line
    line = np.insert(line, [0, len(line)], [B, B])
    # Isolate black squares
    blacks = np.where(line == B)[0]
    # Consider only the gaps between black square of length at least 2
    interval_lenghts = np.diff(blacks)
    minimum_lenght = np.where(interval_lenghts > 2)
    # Return these gaps and their respective lenghts
    return zip(blacks[minimum_lenght[0]], interval_lenghts[minimum_lenght] - 1)

def find_hooks(grid):
    horizontal = [(row, find_line_hooks(line)) for row, line in enumerate(grid)]
    vertical = [(col, find_line_hooks(line)) for col, line in enumerate(grid.T)]

    return [(H, row, col, len) for row, value in horizontal for (col, len) in value] + \
        [(V, row, col, len) for col, value in vertical for (row, len) in value]

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
            grid_copy = insert_word(grid_copy, hook, word)

            remaining_hooks = hooks[index + 1:]
            if solve_crossword(remaining_hooks, grid_copy, bow):
                return True
            # remove word from hook (or simply don't do anything and grid_copy will be destroyed)

    return False


def main():
    grid = deepcopy(GRID)

    hooks = find_hooks(grid)
    hook = hooks[-1]
    grid = insert_word(grid, hook, "ciao")

    print(hook)
    print_grid(grid)

    # solve_crossword(GRID, 0, 0)

if __name__ == "__main__":
    main()
