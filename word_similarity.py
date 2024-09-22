import numpy as np
import sqlite3


DATABASE = "./words/itwac128.sqlite"

database_words = []
database_vectors = np.array([])


def is_valid(word):
    return word.isalpha() and word.islower() and len(word) > 2


def cleanup_words():
    global database_words
    global database_vectors

    exclude = [i for i, w in enumerate(database_words) if not is_valid(w)]

    database_words = np.delete(database_words, exclude, axis=0)
    database_vectors = np.delete(database_vectors, exclude, axis=0)


def load_words():
    global database_words
    global database_vectors

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()
    dump = cursor.execute("select * from store where ranking < 100000")

    database_words, database_vectors = zip(*[(l[0], np.array(l[1:-1])) for l in dump])

    database_words = np.array(database_words)
    database_vectors = np.stack(database_vectors)

    cleanup_words()


def get_similar(indices):
    # Get the word which is the closest to the given words indices
    # This could be GREATLY optimized

    # words = [database_words[i] for i in indices]

    word_vectors = database_vectors[indices]
    mean = sum(word_vectors) / len(word_vectors)

    distances = np.linalg.norm(database_vectors - mean, axis=1)
    distances[indices] = np.nan

    closest = np.nanargmin(distances)
    return database_words[closest], database_vectors[closest]


def main():
    load_words()

    for _ in range(10):
        random_indices = np.random.choice(len(database_words), 5)
        random_words = [database_words[i] for i in random_indices]

        closest_word, _ = get_similar(random_indices)
        print("The word closest to", random_words, "is", closest_word)

    words = ["sedia", "cena", "scrivania"]
    indices = np.where(np.isin(database_words, words))

    closest_word, _ = get_similar(indices)
    print("The word closest to", words, "is", closest_word)

if __name__ == "__main__":
    main()
