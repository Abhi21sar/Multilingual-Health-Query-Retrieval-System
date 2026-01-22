import numpy as np
import pandas as pd
import scipy
from sentence_transformers import SentenceTransformer


def Initiate():

    corpus_embeddings = np.load("corpus_embedding.npy")
    K = 10

    # print(corpus_embeddings.shape)
    # print(K)

    raw_data = pd.read_excel("dataAll.xlsx")
    embedder = SentenceTransformer('Large-Bert')

    # print(raw_data.shape)
    print("Embedder Loaded")

    return corpus_embeddings, K, raw_data, embedder

def getDocs(corpus_embeddings, query_embedding, raw_data, K = 10):

    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    rows = []

    for idx, distance in results[0:K]:
        rows.append(raw_data.iloc[idx,:])

    return rows


