import pickle
import numpy as np

# 1. Keep words which are nouns of at least 2 letters
# 2. Save the results in a slightly more efficient format

INPUT_WORDS_FILE = "./words/glove.6B.50d.txt"

OUTPUT_WORDS_FILE = "./words/words_unicode.pickle"
OUTPUT_VECTORS_FILE = "./words/words_vectors.npy"

def is_valid(word: str):
    return word.isalpha() and len(word) >= 2

def main():
    words, vectors = [], []
    counter = 0

    with open(INPUT_WORDS_FILE, "r") as lines:
        for line in lines:
            word, vector = line.split(" ", 1)
            if is_valid(word):
                words.append(word)
                vectors.append(np.fromstring(vector, dtype=np.float32, sep=" "))
            counter += 1

    pickle.dump(words, open(OUTPUT_WORDS_FILE, "wb"))
    np.save(OUTPUT_VECTORS_FILE, np.array(vectors))

    print("Kept", len(words), "words out of", counter)

if __name__ == "__main__":
    main()
