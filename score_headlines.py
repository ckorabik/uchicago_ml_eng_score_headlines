"""
Score headlines for Newspaper articles.
Takes a file name and a news source as inputs.
Outputs a new file with headlines scored as Optimistic, Pessimistic, or Neutral.
"""

import sys
from pathlib import Path
from datetime import datetime
import joblib
from sentence_transformers import SentenceTransformer


def score_headlines(path, news_source):
    """Score headlines from a file."""
    now = datetime.now()
    time_suffix = now.strftime("%Y_%m_%d")
    output_name = f"outputs/headline_scores_{news_source}_{time_suffix}.txt"
    clf = joblib.load("models/svm.joblib")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    predictions = []
    with open(path, "r") as fr:
        for line in fr:
            line = line.strip()  # Remove trailing newline characters
            if line:  # Skip empty lines
                encoded = model.encode(line)
                prediction = clf.predict([encoded])[0]
                predictions.append(f"{prediction}, {line}\n")

    with open(output_name, "w") as fw:
        fw.writelines(predictions)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        file_path = Path(file_name)
        assert (
            file_path.suffix == ".txt"
        ), f"First argument must be a .txt file. Got: {file_path}"
    except IndexError as e:
        raise Exception(
            f"Missing filename argument. {sys.argv[0]} requires both "
            "a filename and a source argument to run. \n{e}"
        )
    try:
        source = sys.argv[2]
    except IndexError as e:
        raise Exception(
            f"Missing source argument. {sys.argv[0]} requires both "
            "a filename and a source argument to run. \n{e}"
        )
    score_headlines(file_path, source)
