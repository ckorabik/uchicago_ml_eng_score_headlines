# uchicago_ml_eng_score_headlines
The "score_headlines.py" file in this repository can be called to score headlines of different news articles as either Optimistic, Neutral, or Pessimistic.
The script takes a txt file name and a news source string as arguments, and it will output scores in separate txt files.
This assumes that the input text file contains one article title per line.

The code can be run like
`python score_headlines.py data/headlines_chicagotribune_2025-07-07.txt chicagotribune`