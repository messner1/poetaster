# Poetaster, a small game demonstration of RAG principles

![Alt text](demo.gif?raw=true "Poetaster demo")

## Motivation
I design and teach [Computational Intelligence for the Humanities](https://cdh.jhu.edu/teaching/4/) an introductory machine learning class for students in disciplines that aren't traditionally computational. I dedicate a segment of the class to student requested ML/LM related topics. Recent iterations have yielded some interest in RAG.

Prompted by this interest, as well as the release of [EmbeddingGemma 300m](https://huggingface.co/google/embeddinggemma-300m), I decided to make an example of a basic RAG workflow... and what better way to do so then in the form of an anachronisitc curses-based console game?

The objective of the game is provide the "judge" with a poem that fits their particular aesthetic desires over three rounds of submission and feedback.

As a pedagogical tool, this is course bare-bones and unoptimized. It is also meant to be an instigator of critical discussion, so any frustrations may be intended.


### Organization

The codebase is designed to be as discrete as possible. The workflow is as follows:

1. (If poetry.json and metrical_embeddings.npy don't already exist) Preprocess and embed poems
2. (Upon starting a new game) Retrieve the 10 poems most similar to the poem in judge_seed.txt, generate a description of this judge's preferences
3. (Upon submitting a poem) Judge poem using judge description


## Installation

Access to Llama 3.18B and EmbeddingGemini through the HuggingFace hub is required. Building the poem database requires the [Metrical Tagging in the Wild](https://github.com/tnhaider/metrical-tagging-in-the-wild) dataset.


Otherwise, simply run:

```
pip install -r requirements.txt
```

## Run
Invoke the curses version with:

```
python poetaster_curses.py
```