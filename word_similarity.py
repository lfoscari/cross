import numpy as np
import gensim.downloader as api

SIMILAR_WORDS_AMOUNT=1_000

# https://github.com/piskvorky/gensim-data?tab=readme-ov-file#models
# MODEL = api.load("glove-twitter-25")
MODEL = api.load("word2vec-google-news-300")
MODEL.sort_by_descending_frequency()


def get_similar(prompt_words, model = MODEL):
    similar_words = model.most_similar(prompt_words, topn=SIMILAR_WORDS_AMOUNT)
    return [word for (word, _) in similar_words]


if __name__ == "__main__":
    print(get_similar(["animal", "cat", "dog", "bird"]))
