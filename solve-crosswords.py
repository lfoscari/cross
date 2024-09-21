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


def print_grid(grid):
    for line in grid: print(" ".join(line))


# ---- WORDS ----

WORDS = [
    [
        "aa", "ab", "ba", "bb"
    ], [
        "aab", "aba", "abb", "baa", "bab", "bba", "bbb"
    ], [
        "aaab", "aaba", "aabb", "abaa", "abab", "abba", "abbb",
        "baaa", "baab", "baba", "babb", "bbaa", "bbab", "bbba", "bbbb"
    ]
]


def get_word_candidates(bow, length: int, intersecting = [], similar = []):
    return bow[length - 2]

def exclude_word(bow, word):
    bow[len(word) - 2].remove(word)


# ---- WORD INSERTION AND DELETION ----

def remove_word(grid, insertions):
    for x, y in insertions: grid[x][y] = W


def insert_word(grid, hook, word):
    # Try to insert the word on the grid at the hook, if not possible clean up.
    # Return True if managed to insert the word, signaling where changes were made.
    
    (direction, x, y, length) = hook
    if length != len(word): return False

    insertions = []

    for l in range(length):
        i, j = (x, y + l) if direction == H else (x + l, y)
        
        if grid[i][j] == W:
            grid[i][j] = word[l]
            insertions.append((i, j))

        elif grid[i][j] != word[l]:
            remove_word(grid, insertions)
            return False, []

    return True, insertions


# ---- HOOKS ----

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


# ---- SOLVER ----

def solve_crossword(hooks, grid, bow):
    # todo: order hooks by length (longest to shortest)

    if hooks == []:
        return True

    for index, hook in enumerate(hooks):
        # find words of the right length for hook from bow
        # optionally filter for letters in the intersecting words

        (_, _, _, length) = hook
        words = get_word_candidates(bow, length)

        for word in words:
            fits, insertions = insert_word(grid, hook, word)
            if not fits: continue
            
            exclude_word(bow, word)

            remaining_hooks = hooks[index + 1:]
            if solve_crossword(remaining_hooks, grid, bow):
                return True

            remove_word(grid, insertions)

        return False


def main():
    grid = deepcopy(GRID)
    hooks = find_hooks(grid)

    completed = solve_crossword(hooks, grid, WORDS)
    if not completed:
        print("Could not complete... sorry")
    else:
        print_grid(grid)


if __name__ == "__main__":
    main()
