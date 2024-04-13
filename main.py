import spacy
import pandas as pd
from spacy.matcher import Matcher

nlp = spacy.load("es_core_news_lg")

gt = pd.read_csv("csvFile.csv")
gt = gt.fillna("")

