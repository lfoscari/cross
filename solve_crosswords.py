import numpy as np
import word_similarity

MIN_WORD_LENGTH = 3

# Repeating the topic words improves locality?
TOPIC = ["pet"] * 3

H, V = "→", "↓"
W, B = "_", "█"

GRID = np.array([
    [W, W, W, B, W],
    [B, W, W, W, W],
    [W, W, B, W, W],
    [W, W, W, W, B],
    [W, B, W, W, W],
])


def print_grid(grid):
    for line in grid: print(" ".join(line))


# ---- WORDS ----

word_filter = []

def get_word_candidates(intersecting_points, length):
    intersecting_words = [word for (_, word, _) in intersecting_points]
    similar_words = word_similarity.get_similar(TOPIC + intersecting_words)

    return [word for word in similar_words if is_valid(word, length, intersecting_points)]

def is_valid(word, length, intersecting_points):
    if len(word) != length or word in word_filter: return False

    # Check that the proposed word fits the grid with the intersection points
    for (index, int_word, int_index) in intersecting_points:
        if word[index] != int_word[int_index]: return False

    return True
    

def exclude_word(word):
    global word_filter
    word_filter.append(word)


# ---- WORD INSERTION AND DELETION ----

def remove_word(grid, insertions):
    for x, y in insertions: grid[x][y] = W


def insert_word(grid, hook, word):
    # Try to insert the word on the grid at the hook, if not possible clean up.
    # Return True if managed to insert the word, signaling where changes were made.
    
    (direction, x, y, length) = hook
    insertions = []
    
    if length != len(word): return False, insertions

    for l in range(length):
        i, j = (x, y + l) if direction == H else (x + l, y)
        
        if grid[i][j] == W:
            grid[i][j] = word[l]
            insertions.append((i, j))

        elif grid[i][j] != word[l]:
            remove_word(grid, insertions)
            return False, []

    return True, insertions


def find_intersecting(grid, hook):
    # TODO: rewrite using numpy arrays

    # Find words that intersect the slot denoted by the given hook
    (direction, x, y, length) = hook
    
    # the intersecting word is orthogonal
    int_direction = H if direction == V else V
    int_words = []

    for l in range(length):
        i, j = (x, y + l) if direction == H else (x + l, y)
        if grid[i][j] in [W, B]: break
        
        # Search the intersecting word by backtracking to its start
        int_i, int_j = i, j
        while int_i > 0 and int_j > 0 and grid[int_i][int_j] not in [W, B]:
            int_i, int_j = (int_i, int_j - 1) if int_direction == H else (int_i - 1, int_j)
        
        # Now read the whole word
        int_word = ""
        while int_i < len(GRID) and int_j < len(GRID[0]) and grid[int_i][int_j] not in [W, B]:
            int_word += grid[int_i][int_j]
            int_i, int_j = (int_i, int_j + 1) if int_direction == H else (int_i + 1, int_j)

        # Ensure that the intersecting word is complete by checking that ends with a black square
        if (int_i >= len(GRID) or int_j >= len(GRID[0]) or grid[int_i][int_j] == B) and len(int_word) >= MIN_WORD_LENGTH:
            # Store the index at which the intersecting word intersects 
            int_word_index = j - int_j if int_direction == H else i - int_i
            int_words.append((l, int_word, int_word_index))

    return int_words


# ---- HOOKS ----

def find_line_hooks(line):
    # Insert black square at the beginning and end of the line
    line = np.insert(line, [0, len(line)], [B, B])
    # Isolate black squares
    blacks = np.where(line == B)[0]
    # Consider only the gaps between black square of length at least 2
    interval_lengths = np.diff(blacks)
    minimum_length = np.where(interval_lengths > MIN_WORD_LENGTH)
    # Return these gaps and their respective lengths
    return zip(blacks[minimum_length[0]], interval_lengths[minimum_length] - 1)


def find_hooks(grid):
    horizontal = [(row, find_line_hooks(line)) for row, line in enumerate(grid)]
    vertical = [(col, find_line_hooks(line)) for col, line in enumerate(grid.T)]

    hooks = [(H, row, col, len) for row, value in horizontal for (col, len) in value] + \
        [(V, row, col, len) for col, value in vertical for (row, len) in value]

    # For efficiency reasons, sort them be length
    return sorted(hooks, key=lambda hook: hook[3], reverse=True)


# ---- SOLVER ----

def solve_crossword(hooks, grid):
    if hooks == []:
        return True

    for index, hook in enumerate(hooks):
        (_, _, _, length) = hook

        intersecting_points = find_intersecting(grid, hook)
        words = get_word_candidates(intersecting_points, length)

        for word in words:
            fits, insertions = insert_word(grid, hook, word)
            if not fits: continue
            
            exclude_word(word)

            remaining_hooks = hooks[index + 1:]
            if solve_crossword(remaining_hooks, grid):
                return True

            remove_word(grid, insertions)

        return False


def main():
    hooks = find_hooks(GRID)
    completed = solve_crossword(hooks, GRID)

    if not completed:
        print("Could not complete... sorry")
    else:
        print_grid(GRID)


if __name__ == "__main__":
    main()
