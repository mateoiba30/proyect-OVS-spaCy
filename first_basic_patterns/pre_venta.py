#importamos todo
import spacy#para el nlp()
import pandas as pd#para manipular el csv mas facil
from spacy.matcher import Matcher #para hacer los patrones
from spacy.tokens import Doc, Span

nlp = spacy.load("es_core_news_lg")#importamos la info entrenada en español con muchos datos

gt = pd.read_csv("csvFIle.csv")#abrimos el csv -> lo hacemos una DataFrame
gt = gt.fillna("")

rangeRows = gt.iloc[:1]

for index, row in rangeRows.iterrows():#gracias a pandas, recorremos sencillamente el csv

    description = row["DESCRIPCION"]#pedimos una columna especifica segun el nombre de la columna, indicada en la 1er linea del csv
    doc = nlp(description)# el doc tiene cada palabra/token

    print(f"\nDescripcion numero", (index+1))
    print("")
    print(description) #para ver el texto normal, aunque lo podríamos ver en el edit-csv.net
    print("")
    for token in doc: print(token.text, token.pos_, token.dep_, token.head.text) #para ver más a fondo la descripción de cada token

    matcher = Matcher(nlp.vocab)
    matcher.add("preventa", [ 
            #2 medidas:
            [{"LIKE_NUM":True}]

        ])#defino los patrones para encontrar cierto campo

    print("")
    matches = matcher(doc)#mostramos lo que encontramos con el patron
    if len(matches) > 0:
        print("preventa: True")
    else:
        print("preventa: False")

    print("")
    print("------------------------------------------------------------")
    print("")


