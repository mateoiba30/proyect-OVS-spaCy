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
    for token in doc: print(token.text, token.pos_, token.dep_, token.head.text) #para ver más a fondo la descripción de cada token

    matcher = Matcher(nlp.vocab)
    matcher.add("fotPatterns", [
            [{"LOWER": {"IN":["fot", "factor de ocupación del suelo"]}},{"POS": "ADJ", "OP":"?"},{"LIKE_NUM": True}]
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


#    matcher.add("adressPatterns", [
#        [{"POS": {"IN":["PROPN", "NOUN"]}},{"LIKE_NUM": True},{"POS":"ADJ", "OP":"?"},{"POS": {"IN": ["ADP", "PROPN"]}, "OP":"+"},{"LIKE_NUM":True, "OP":"?"}],
#        [{"POS": {"IN":["PROPN", "NOUN"]}},{"LIKE_NUM": True},{"POS":"ADJ", "OP":"?"},{"POS": {"IN": ["ADP", "PROPN"]}, "OP":"*"},{"LIKE_NUM":True, "OP":"?"},{"TEXT":"y"},{"POS": "PROPN", "OP":"?"},{"LIKE_NUM": True, "OP":"+"}],
#        [{"POS": {"IN":["PROPN", "NOUN"]}},{"LIKE_NUM": True},{"POS":"ADJ", "OP":"?"},{"POS": {"IN": ["ADP", "PROPN"]}, "OP":"*"},{"LIKE_NUM":True, "OP":"?"},{"TEXT":"y"},{"POS": "PROPN", "OP":"?"},{"LIKE_NUM": True, "OP":"?"},{"POS": "ADP", "OP": "*"},{"POS": "PROPN", "OP": "+"}],
#
#        #[{"POS": {"IN":["PROPN", "NOUN"]}},{"LIKE_NUM": True},{"POS":"ADJ", "OP":"?"},{"POS": {"IN": ["ADP", "PROPN"]}, "OP":"*"},{"LIKE_NUM":True, "OP":"?"},{"TEXT":"y", "OP":"?"},{"POS": "PROPN", "OP":"?"},{"LIKE_NUM": True, "OP":"?"},{"POS": "ADP", "OP":"?"},{"POS": "PROPN", "OP": "*"}],
#        #[{"POS": {"IN":["PROPN", "NOUN"]}},{"LIKE_NUM": True},{"POS":"ADJ", "OP":"?"},{"POS": "ADP", "OP":"?"},{"POS": "PROPN", "OP": "*"},{"LIKE_NUM":True, "OP":"?"},{"TEXT":"y", "OP":"?"},{"POS": "PROPN", "OP":"?"},{"LIKE_NUM": True, "OP":"?"},{"POS": "ADP", "OP":"?"},{"POS": "PROPN", "OP": "*"}],
#        #[{"TEXT": {"IN":["calle", "avenida", "ruta"]}},{"LIKE_NUM": True},{"POS":"ADJ", "OP":"?"},{"POS": "ADP", "OP":"?"},{"POS": "PROPN", "OP": "*"},{"LIKE_NUM":True, "OP":"?"},{"TEXT":"y", "OP":"?"},{"POS": {"IN":["PROPN", "NOUN"]}, "OP":"?"},{"LIKE_NUM": True, "OP":"?"},{"POS": "ADP", "OP":"?"},{"POS": "PROPN", "OP": "*"}],
#        #[{"POS": {"IN":["PROPN", "NOUN"]}},{"LIKE_NUM": True},{"TEXT":"y", "OP":"?"},{"LIKE_NUM": True, "OP":"?"}]
#
#        ])#defino los patrones para encontrar la direccion