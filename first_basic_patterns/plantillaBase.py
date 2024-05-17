import spacy
import pandas as pd
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

nlp = spacy.load("es_core_news_lg")
gt = pd.read_csv("csvFile.csv")
gt = gt.fillna("")

rangeRows = gt.iloc[0:16]

for index, row in rangeRows.iterrows():
    description = row["DESCRIPCION"]
    doc = nlp(description)

    print("Descripcion numero ", index+1)
    print("")
    print(description)
    print("")
    for token in doc: print(token.text, token.pos_, token.dep_, token.head.text)

    matcher = Matcher(nlp.vocab)
    matcher.add("", [
        []
        ])

    print("")
    print("matches:")

    maxSize = 0
    best_span = doc[0:0]
    matches = matcher(doc)
    for match_id, start, end in matches:
        print(doc[start:end].text)
        actSize = end - start
        if (actSize > maxSize):
           maxSize = actSize
           best_span = doc[start:end]

    print("mejor matcheo:")
    print(best_span.text)

    print("")
    print("------------------------------------------------------------")
    print("")

