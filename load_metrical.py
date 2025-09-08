import zipfile
import json


def load_mtw():

    with zipfile.ZipFile("metrical-tagging-in-the-wild/data/English/LargeCorpus/eng_gutenberg_measures_all.json.zip", "r") as zf:
        with zf.open("eng_gutenberg_measures_all.json", "r") as jin:
            poems = json.load(jin)


    with open("metrical_poetry.jsonl", "wt") as p_out:
        for poemid, poem in poems.items():
            print(poem["metadata"])
            text = []
            for si, stanza in poem["poem"].items():
                for li, line in stanza.items():
                    text.append(line["text"])
            t = p_out.write(json.dumps({"id":poemid, 
                            "author":poem["metadata"]["author"]["name"], 
                            "title":poem["metadata"]["title"], 
                            "text": "\n".join(text)})+"\n")

