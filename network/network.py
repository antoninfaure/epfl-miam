import pandas as pd
import os
import json
import nltk
import re


file_path = os.path.dirname(os.path.abspath(__file__))
menus = pd.read_csv(os.path.join(file_path, '..', 'data', 'menus.csv'), index_col=0)

# Remove \\n characters from the name
menus['name'] = menus['name'].str.replace('\\n', ' ')


def extract_tokens(text):
    if pd.isnull(text):
        return []

    text = text.lower()

    # remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # remove digits
    text = re.sub(r'\d+', '', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    stopwords = [' ', 'de', 'aux', 'au', 'à', 'la', 'le', 'et', 'sur', 'du', 'chef', 'ou', 'notre', 'by', 'en']
    tokens = [token for token in text.split() if token not in stopwords]
    return tokens

tokens = menus['name'].apply(extract_tokens)

def create_vocabulary(tokens):
    vocabulary = {}
    for token_list in tokens:
        for token in token_list:
            if token in vocabulary:
                vocabulary[token] += 1
            else:
                vocabulary[token] = 1
    return vocabulary

vocabulary = create_vocabulary(tokens)


def output_file(data, filename):
    path = os.path.join(file_path)
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path}/{filename}', 'w', encoding='UTF8', newline='') as f:
        writer = json.dump(data, f, ensure_ascii=False)

def create_graph(tokens, vocabulary, min_frequency=100):

    filtered_vocabulary = {k: v for k, v in vocabulary.items() if v >= min_frequency}

    dict_voc_id = dict()
    for i, term in enumerate(filtered_vocabulary):
        dict_voc_id[term] = i

    # List bigrams (edges)
    finder = nltk.BigramCollocationFinder.from_documents(tokens)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bigrams = list(finder.score_ngrams(bigram_measures.raw_freq))
    min_freq = min(list(map(lambda x: x[1], bigrams)))
    bigrams = list(map(lambda x: (x[0], x[1]/min_freq), bigrams))

    # Filter the bigrams with filtered_voc elements and replace by id
    filtered_bigrams = []
    for bigram in bigrams:
        if (bigram[0][0] in filtered_vocabulary.keys() and bigram[0][1] in filtered_vocabulary.keys()):
            new_bigram = bigram[0]
            filtered_bigrams.append((new_bigram, bigram[1]))

    # Format data
    vertices = []
    sizes = list(filtered_vocabulary.values())
    for i, term in enumerate(filtered_vocabulary.keys()):
        vertices.append({
            'id': term,
            'label': term,
            'size': sizes[i]
        })
    
    edges = []
    for i, edge in enumerate(filtered_bigrams):
        (source, target) = edge[0]
        edges.append({
            'id': i,
            'source': source,
            'target': target,
            'size': edge[1]
        })

    
    # Sort bigrams by size
    bigrams_sorted = sorted(filtered_bigrams, key=lambda x: x[1], reverse=True)

    output_file(bigrams_sorted, 'bigrams.json')
    
    # Write JSON files
    output_file(vertices, 'vertices.json')

    output_file(edges, 'edges.json')

create_graph(tokens, vocabulary)