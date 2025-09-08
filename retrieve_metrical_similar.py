import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
import json
import csv


def get_judge_context():

    with open("metrical_poetry.jsonl", "rt") as p_in:
        poetry = [json.loads(p) for p in p_in.readlines()]

    with open("judge_seed.txt", "rt") as s_in:
        query = s_in.read()


    poetry_docs = np.load("metrical_embeddings.npy")




    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_id = "google/embeddinggemma-300M"
    model = SentenceTransformer(model_id).to(device=device)

    print(f"Device: {model.device}")

    embedding = model.encode([query], prompt_name="Clustering")
    similarities = 1 - cdist(embedding, poetry_docs)

    descending = np.argsort(similarities)[0][::-1]
    print(descending)
    print(descending.shape)
    with open("context_poems.txt", "wt") as c_out, open("authors.json", "wt") as authors_out:
        authors = []
        for i,match in enumerate(descending[0:10]):
            #print(poetry[match])
            author = poetry[match]["author"].split(",")
            authors.append(author)
            c_out.write(f"{i+1} {author[1]} {author[0]}\n{poetry[match]['text']}\n\n")
        json.dump(authors, authors_out)






