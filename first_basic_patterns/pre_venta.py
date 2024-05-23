#importamos todo
import spacy#para el nlp()
import pandas as pd#para manipular el csv mas facil
from spacy.matcher import Matcher #para hacer los patrones
from spacy.tokens import Doc, Span

nlp = spacy.load("es_core_news_lg")#importamos la info entrenada en español con muchos datos

gt = pd.read_csv("DBPreVenta.csv")#abrimos el csv -> lo hacemos una DataFrame
gt = gt.fillna("")

rangeRows = gt.iloc[17:18]

minimosMatcheos = 2 #es lo mismo a poner 1 y sacar lo de las cuotas

TP = 0
TN = 0
FN = 0
FP = 0

for index, row in rangeRows.iterrows():#gracias a pandas, recorremos sencillamente el csv

    description = row["DESCRIPCION"]#pedimos una columna especifica segun el nombre de la columna, indicada en la 1er linea del csv
    resultado = row["PREVENTA"]
    doc = nlp(description)# el doc tiene cada palabra/token

    tiempo = ["año", "años", "mes", "meses"]
    #para usar con LOWER
    palabraPreVenta = ["preventa", "pre-venta"]
    palabrasFuturoExactas = ["concretará", "contará","propuesta", "construcción", "construccion", "proyecto", "entregará", "entregarán", "entrega", "posesión", "posesión", "obra", "desarrollo"]#las palabras en futuro deben tener los acentos obligatoriamente
    cuotasIndicadorExacto = ["cuota", "cuotas", "cta", "ctas", "plan", "pozo", "anticipo", "fideicomiso"]
    cuotasIndicadorAproximado = ["financiar", "financiado", "financiación", "financiacion"]#encontrarla en cualquier conjugación o palabra de la familia

    matcherAsegurado = Matcher(nlp.vocab)
    matcherAsegurado.add("asegurados", [ #si matcheo algo de acá seguro es una preventa
            [{"LOWER":{"IN": palabraPreVenta}}],
            [{"LOWER": "pre"}, {"LOWER": "venta"}],
        ])#defino los patrones para encontrar cierto campo
    
    matcherPosible = Matcher(nlp.vocab)
    matcherPosible.add("posibles", [ #si matcheo algo de acá tal vez es una preventa
            [{"LOWER":{"IN": palabrasFuturoExactas}}],
            [{"LOWER": "primeras"}, {"LIKE_NUM": True}, {"LOWER": "unidades"}],
            #distingo si encuentro 'posesión' de 'posesión futura' ya que si ocurre la última el contador quedará en 2
            [{"LOWER": "posesión"}, {"LOWER": "futura"}],
            [{"LOWER": "posesión"}, {"LOWER": "a"}, {"LIKE_NUM": True}, {"LOWER": {"IN": tiempo}}],
        ])
    
    matcherCuotas = Matcher(nlp.vocab)
    matcherCuotas.add("cuotas", [ #si matcheo algo de acá tal vez es una preventa
            [{"LOWER": {"IN": cuotasIndicadorExacto}}],
            [{"LOWER": {"IN": cuotasIndicadorAproximado}}],
        ])
    
    mostrar = True #cambiar si queiro ver todo o solo lo que no matchea bien
    matcheos = 0
    matcherAsegurado = matcherAsegurado(doc)#mostramos lo que encontramos con el patron
    for match_id, start, end in matcherAsegurado: #para lo que encontramos vamos a mostrar solo eso
        matcheos += minimosMatcheos+1

    matcherPosible = matcherPosible(doc)#mostramos lo que encontramos con el patron
    for match_id, start, end in matcherPosible: #para lo que encontramos vamos a mostrar solo eso
        matcheos += 1

    matcheosCuotas =0
    matcherCuotas = matcherCuotas(doc)#mostramos lo que encontramos con el patron
    for match_id, start, end in matcherCuotas: #para lo que encontramos vamos a mostrar solo eso
        matcheosCuotas += 1
    if matcheosCuotas > 0:
        matcheos += 1

    prediccion = False
    if matcheos >= minimosMatcheos:
        prediccion = True
        if resultado:
            TP+=1
        else:
            FP+=1
            mostrar = True
    else:
        if not resultado:
            TN+=1
        else:
            FN +=1
            mostrar = True   

    if mostrar:
        print("------------------------------------------------------------")
        print("")
        print(f"\nDescripcion numero", index+1)
        print("")
        print(description) #para ver el texto normal, aunque lo podríamos ver en el edit-csv.net
        print("")
        for token in doc: print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text) #para ver más a fondo la descripción de cada token    mostrar = False
        print("")
        print("esperado: " + str(resultado))
        print("")
        print("prediccion: " + str(prediccion))
        print("")
        print("matcheos: ")
        for match_id, start, end in matcherAsegurado:
            print(doc[start:end].text)
        for match_id, start, end in matcherPosible:
            print(doc[start:end].text)
        for match_id, start, end in matcherCuotas:
            print(doc[start:end].text)
        print("")

print("")
print("----------------MEDIDAS----------------")
print("")
if TP + FP != 0:
    precision = TP/(TP+FP)
else:
    precision = 0
if TP + FN != 0:
    recall = TP/(TP+FN)
else:
    recall = 0

f1 = 2*(precision*recall)/(precision+recall)
print("tp: " + str(TP))
print("fp: " + str(FP))
print("fn: " + str(FN))
print("tn: " + str(TN))
print("precision: " + str(precision))
print("recall: " + str(recall))
print("f1: " + str(f1))