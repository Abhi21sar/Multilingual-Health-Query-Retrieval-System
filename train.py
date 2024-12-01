import pandas as pd
import numpy as np
import torch
import time, sys, os
from translate import Translator
import sklearn.metrics.pairwise
from tqdm import tnrange
from sklearn.metrics import jaccard_score
import scipy
import re
from sentence_transformers import SentenceTransformer

translator=Translator(to_lang='en',from_lang='es')

# Load the dataset

raw_data = pd.read_excel("dataAll.xlsx")

print("Data Loaded with shape : ",raw_data.shape)

# Preprocess the data

new_raw_data = raw_data.drop_duplicates()

print("Data Pre-Processed into shape : ",new_raw_data.shape)

# LARGE BERT
embedder = SentenceTransformer('bert-large-nli-stsb-mean-tokens') 

corpus_embeddings=embedder.encode(new_raw_data['Query'].to_list())

# Saving the Model

embedder.save("Large-Bert")
np.save("corpus_embedding.npy",corpus_embeddings)