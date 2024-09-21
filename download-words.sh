#!/usr/bin/env bash

set -e

mkdir -p words

curl -# https://downloads.cs.stanford.edu/nlp/data/glove.6B.zip -o words/glove.6B.zip

unzip ./words/glove.6B.zip
