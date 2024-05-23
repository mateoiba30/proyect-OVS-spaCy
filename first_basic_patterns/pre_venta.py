#importamos todo
import spacy#para el nlp()
import pandas as pd#para manipular el csv mas facil
from spacy.matcher import Matcher #para hacer los patrones
from spacy.tokens import Doc, Span

nlp = spacy.load("es_core_news_lg")#importamos la info entrenada en español con muchos datos

gt = pd.read_csv("DBPreVenta.csv")#abrimos el csv -> lo hacemos una DataFrame
gt = gt.fillna("")

rangeRows = gt.iloc[:27]

for index, row in rangeRows.iterrows():#gracias a pandas, recorremos sencillamente el csv

    description = row["DESCRIPCION"]#pedimos una columna especifica segun el nombre de la columna, indicada en la 1er linea del csv
    resultado = row["PREVENTA"]
    doc = nlp(description)# el doc tiene cada palabra/token

    tiempo = ["año", "años", "mes", "meses"]
    #para usar con LOWER
    palabraPreVenta = ["preventa", "pre-venta"]
    palabrasFuturoExactas = ["concretará", "contará","propuesta", "construcción", "proyecto", "entregará", "entregarán", "entrega", "posesion", "posesión", "obra", "desarrollo"]

    matcher = Matcher(nlp.vocab)
    matcher.add("preventa", [ 
            
            #para ver si es preventa
            [{"LOWER":{"IN": palabraPreVenta}}],
            [{"LOWER": "pre"}, {"LOWER": "venta"}],

            #para ver si se habla en futuro o similar
            [{"LOWER":{"IN": palabrasFuturoExactas}}],
            [{"LOWER": "primeras"}, {"LIKE_NUM": True}, {"LOWER": "unidades"}],

            #no necesarias porque ya me conformo solo con encontrar la palabra posesión
            #[{"LOWER": "posesión"}, {"LOWER": "futura"}],
            #[{"LOWER": "posesión"}, {"LOWER": "a"}, {"LIKE_NUM": True}, {"LOWER": {"IN": tiempo}}],

        ])#defino los patrones para encontrar cierto campo
    
    prediccion = False
    matches = matcher(doc)#mostramos lo que encontramos con el patron
    if len(matches) > 0:
        prediccion: True

    print("------------------------------------------------------------")
    print("")
    print(f"\nDescripcion numero", index+1)
    print("")
    print(description) #para ver el texto normal, aunque lo podríamos ver en el edit-csv.net
    print("")
    #for token in doc: print(token.text, token.pos_, token.dep_, token.head.text) #para ver más a fondo la descripción de cada token    mostrar = False
    print("")
    print("esperado: " + str(resultado))
    print("")
    print("prediccion: " + str(prediccion))
    print("")
