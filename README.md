# Poetaster, a small demonstration of RAG principles

![Alt text](demo.gif?raw=true "Poetaster demo")

## Motivation
I design and teach [Computational Intelligence for the Humanities](https://cdh.jhu.edu/teaching/4/) an introductory machine learning class for students in disciplines that aren't traditionally computational. I dedicate a segment of the class to student requested ML and LM related topics.

## Installation

Access to Llama 3.18B and EmbeddingGemini through the HuggingFace hub is required. Building the poem database requires the [Metrical Tagging in the Wild](https://github.com/tnhaider/metrical-tagging-in-the-wild) dataset.


Otherwise, simply run:

'''
pip install -r requirements.txt
'''

## Run
Invoke the curses version with:

'''
python poetaster_curses.py
'''