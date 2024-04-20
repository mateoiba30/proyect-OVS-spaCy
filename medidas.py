#importamos todo
import spacy#para el nlp()
import pandas as pd#para manipular el csv mas facil
from spacy.matcher import Matcher #para hacer los patrones
from spacy.tokens import Doc, Span

nlp = spacy.load("es_core_news_lg")#importamos la info entrenada en español con muchos datos

gt = pd.read_csv("csvFile.csv")#abrimos el csv -> lo hacemos una DataFrame
gt = gt.fillna("")#los datos nulos=incompletos no les asignamos texto

rangeRows = gt.iloc[0:16]# no incluye el numero 5

for index, row in rangeRows.iterrows():#gracias a pandas, recorremos sencillamente el csv

    description = row["DESCRIPCION"]#pedimos una columna especifica segun el nombre de la columna, indicada en la 1er linea del csv
    doc = nlp(description)# el doc tiene cada palabra/token

    print("Descripcion numero ", index+1)
    print("")
    print(description) #para ver el texto normal, aunque lo podríamos ver en el edit-csv.net
    print("")
    #for token in doc: print(token.text, token.pos_, token.dep_, token.head.text) #para ver más a fondo la descripción de cada token

    medidas = ["m2", "metro", "m", "mt", "m^2", "m²", "metros", "mts", "mts2", "ms2", "ms"]
    medidas2D = ["m2", "m^2", "mts2", "ms2", "m²"]
    matcher = Matcher(nlp.vocab)
    matcher.add("measuresPatterns", [
            #pongo un solo LIKE_NUM, porque el m^2 y otros me lo matchea como numero
            [{"LIKE_NUM":True},{"LOWER": {"IN":medidas}}, {"POS":{"IN":["ADP", "ADV", "PROPN", "NOUN"]}, "OP":"*"},{"LOWER":{"IN":["x", "y", "por"]}}, {"LIKE_NUM":True, "OP":"+"}, {"LOWER": {"IN":medidas}, "OP":"?"}],
            [{"LIKE_NUM":True},{"LOWER": {"IN":medidas}, "OP":"?"}, {"POS":{"IN":["ADP", "ADV","PROPN", "NOUN"]}, "OP":"*"},{"LOWER":{"IN":["x", "y", "por"]}}, {"LIKE_NUM":True, "OP":"+"}, {"LOWER": {"IN":medidas}}],
            [{"LIKE_NUM":True}, {"LOWER": {"IN":medidas2D}}] #porque aveces dice "a 1200 metros de tal lugar" y eso lo tengo que esquivar
            #[{"LIKE_NUM":True, "OP":"+"},{"POS": {"IN":["NOUN", "NUM"]}}, {"LOWER":{"IN":["x", "y"]}}, {"LIKE_NUM":True, "OP":"+"}, {"POS": {"IN":["NOUN", "NUM"]}}],
            #[{"LIKE_NUM":True, "OP":"+"}, {"POS": {"IN":["NOUN", "NUM"]}}]
        ])#defino los patrones para encontrar cierto campo

    print("")
    maxSize = 0
    best_span = doc[0:0]
    print("matches:")
    matches = matcher(doc)#mostramos lo que encontramos con el patron
    for match_id, start, end in matches: #para lo que encontramos vamos a mostrar solo eso
        print(doc[start:end].text)
        actSize = end - start
        if (actSize > maxSize):
           maxSize = actSize
           best_span = doc[start:end]

    print("mejor matcheo:")
    print(best_span.text)#mostramos el texto que coincide con el patron

    print("")
    print("------------------------------------------------------------")
    print("")


