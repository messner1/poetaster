import torch
import numpy as np
from sentence_transformers import SentenceTransformer
import json

def get_embeddings():
    poetry = []
    with open("metrical_poetry.jsonl", "rt") as p_in:
        for p in p_in.readlines():
            pj = json.loads(p)
            poetry.append(pj["text"])



    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_id = "google/embeddinggemma-300M"
    model = SentenceTransformer(model_id).to(device=device)

    print(f"Device: {model.device}")

    embeddings = model.encode(poetry, prompt_name="Clustering")
    np.save("metrical_embeddings.npy", embeddings)



