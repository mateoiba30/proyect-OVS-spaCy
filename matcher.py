import spacy
from spacy.matcher import DependencyMatcher as DependencyMatcherSpacy
from spacy.matcher import Matcher as MatcherSpacy

from src.helper import (
    procesar_barrio,
    procesar_direccion,
    procesar_fot,
    procesar_frentes,
    procesar_irregular,
    procesar_medidas,
)

NLP = spacy.load("es_core_news_lg")


class Matcher:

    def __init__(self) -> None:
        if Matcher.matcher is None:
            Matcher.initialize_matcher()

    matcher = None
    dependencyMatcher = None
    
    @staticmethod
    def initialize_matcher():
        dimension = ["frente", "fondo", "lateral", "ancho", "alto", "profundidad", "largo", "anchura", "longitud", "espesor"]
        conectoresMedidas = ["x", "y", "por", "de", "con"]
        medidas = ["metro", "m", "mt", "mts", "ms"] #el LEMMA no funciona con "m" porque cree que es un número en lugar de una palabra
        relleno = ["ADP", "ADV", "PROPN", "NOUN", "DET", "ADJ"] # sacarle el DET y ADJ? -> por ahora da buenos resultados sin perjudicar
        
        Matcher.matcher = MatcherSpacy(NLP.vocab)
        Matcher.matcher.add(
            "medidas",
            [ 
            #2 medidas:
            [{"LIKE_NUM":True},{"LEMMA": {"IN":medidas}}, {"POS":{"IN":relleno}, "OP":"*"},{"LOWER":{"IN":conectoresMedidas}}, {"LIKE_NUM":True, "OP":"+"}, {"LOWER": {"IN":medidas}, "OP":"?"}],
            [{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN":conectoresMedidas}}, {"LIKE_NUM":True, "OP":"+"}, {"LOWER": {"IN":medidas}}],
 
            #intentos fallidos:
            #[{"LIKE_NUM": True}, {"POS":"PUNCT", "OP":"?"},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectores}, "OP":"?"}, {"POS":"PUNCT", "OP":"?"}, {"LIKE_NUM": True},{"POS":"PUNCT", "OP":"?"}, {"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectores}, "OP":"?"},{"POS": {"IN": relleno}, "OP": "*"}, {"POS":"PUNCT", "OP":"?"}, {"LIKE_NUM": True}],         
            #[{"LEMMA": {"IN": dimension}},{"LOWER": "de"},{"LIKE_NUM":True},{"ORTH":",", "OP":"?"}, {"LEMMA":{"IN":relleno}, "POS":"?"},{"LEMMA": {"IN": dimension}},{"LOWER": "de"},{"LIKE_NUM":True},{"ORTH":",", "OP":"?"}, {"LEMMA":{"IN":relleno}, "POS":"?"},{"LEMMA": {"IN": dimension}},{"LOWER": "de"},{"LIKE_NUM":True},{"ORTH":",", "OP":"?"}],
            
            #3 medidas, lo hago varias veces para asegurarme que en algún lado se diga la medida
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}],
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}],
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}}],


            #4 medidas, que tenga la medida en algún lado
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}],     
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}],     
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}],     
            [{"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"},{"LOWER":{"IN": conectoresMedidas}, "OP":"*"}, {"LIKE_NUM": True},{"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}, "OP":"?"}, {"POS": {"IN": relleno}, "OP": "*"}, {"LOWER": {"IN": conectoresMedidas}, "OP":"*"},{"LIKE_NUM": True}, {"LEMMA": {"IN": medidas}}],     

        ]
        )
        Matcher.matcher.add(
            "pileta",
            [
                [
                    {"LEMMA": {"IN": ["piscina", "pileta"]}},
                ]
            ],
        )
        Matcher.matcher.add(
            "esquina",
            [
                [
                    {"LOWER": "esquina"},
                ]
            ],
        )
        Matcher.matcher.add(
            "irregular",
            [
                [{"LEMMA": "irregular"}],
                [{"LOWER": {"IN": ["lote", "forma"]}}, {"POS": "ADJ"}],
            ],
        )

        fotSinonimos = ['fot', 'f.o.t']
        Matcher.matcher.add(
            "fot",
            [
            [{'LOWER': {'IN':fotSinonimos}},{"POS": {"IN":["ADJ", "PROPN"]}, "OP":"*"},{"LIKE_NUM": True}],
            [{"LOWER": "factor"},{"LOWER": "de"},{"LOWER": "ocupacion"},{"LOWER": "total"},{'POS': "ADP", 'OP':'?'},{'LIKE_NUM': True}],
            ]
        )

        barrioSinonimos = ["barrio", "lote", "zona", "finca", "sector", "urbanizacion"]
        Matcher.matcher.add(
            "barrio",
            [
                [{"LEMMA": {"IN":barrioSinonimos}}, {"POS": {"IN":["PROPN"]}}],
                [{"LEMMA": {"IN":barrioSinonimos}},{"LIKE_NUM":True, "OP":"?"},{"POS": {"IN":["PRON", "VERB", "ADP", "NOUN"]}, "OP":"*"},{"POS": {"IN": ["NOUN", "ADP", "PROPN", "DET"]}, "OP":"+"},{"POS": {"IN":["PROPN"]}}],
                [{"LEMMA": {"IN":barrioSinonimos}},{"LIKE_NUM":True, "OP":"?"},{"POS": {"IN":["PRON", "VERB", "ADP", "NOUN"]}, "OP":"*"},{"POS": {"IN":["PROPN"]}}],
            ]
        )

        nombreLargo = ["PROPN", "DET", "ADP", "NOUN"]
        conectores = ["e", "e/", "entre", "y", "a", "a/"]
        calleSinonimos = ["Av", "av", "calle", "Calle", "ruta", "Ruta", "avenida", "Avenida", "carrera", "Carrera", "diagonal", "Diagonal", "dg", "Dg", "diag", "Diag"]
        manzanaSinonimos = ["manzana", "Manzana", "mz", "Mz", "mza", "Mza"]
        numeroSinonimos = ["numero", "nro", "número", "número", "n", "n°", "nº", "nº", "n°", "nro."]

        calleSinonimos2 = ["avs", "av", "calle", "calles", "ruta", "rutas", "avenida", "avenidas", "carrera", "carreras", "diagonal", "diagonales", "dg", "dgs", "diag", "diags"]
        manzanaSinonimos2 = ["manzana", "Manzana", "mz", "Mz", "mza", "Mza"]
        numeroSinonimos2 = ["numero", "nro", "número", "número", "n", "n°", "nº", "nº", "n°", "nro."]

        Matcher.matcher.add(
            "dir_nro",[
                [{"LIKE_NUM": True}, {"POS": "ADJ"}, {"LIKE_NUM": True},{"TEXT":"y"}, {"LIKE_NUM": True}],
                [{"LOWER": {"IN":calleSinonimos2}},{'TEXT': '.', 'OP':'?'},{"LIKE_NUM": True},{"LOWER":"bis", "OP":"?"},{"LOWER": {"IN": conectores}, "OP":"+"},{"LIKE_NUM":True, "OP":"+"}],
                [{"LOWER": {"IN":calleSinonimos2}},{'TEXT': '.', 'OP':'?'},{"LIKE_NUM": True},{"LOWER":"bis", "OP":"?"},{"LOWER": {"IN": conectores}, "OP":"*"},{"LIKE_NUM":True, "OP":"?"},{"LOWER":"bis", "OP":"?"},{"TEXT":"y"},{"POS": "PROPN", "OP":"?"},{"LIKE_NUM": True, "OP":"+"}],
                [{"LOWER": {"IN":calleSinonimos2}},{'TEXT': '.', 'OP':'?'},{"LIKE_NUM": True},{"LOWER":"bis", "OP":"?"},{"LOWER": {"IN": conectores}, "OP":"*"},{"LIKE_NUM":True, "OP":"?"},{"LOWER":"bis", "OP":"?"},{"TEXT":"y"},{"POS": "PROPN", "OP":"?"},{"LIKE_NUM": True, "OP":"?"},{"LOWER":"bis", "OP":"?"},{"POS": "ADP", "OP": "*"},{"POS": "PROPN", "OP": "+"}],     
            ]
        )
        Matcher.matcher.add(
            "dir_interseccion",
            [
                [{"LOWER": {"IN":calleSinonimos2}},{'TEXT': '.', 'OP':'?'},{"POS":{"IN":nombreLargo}, "OP":"+"},{"TEXT": "al", "OP":"?"},{"LIKE_NUM": True, "OP":"+"}],
                [{"LOWER": {"IN":calleSinonimos2}},{'TEXT': '.', 'OP':'?'},{"POS":{"IN":nombreLargo}, "OP":"+"},{"LOWER": {"IN": conectores}},{"LEMMA": {"IN":calleSinonimos}, "OP":"?"},{'TEXT': '.', 'OP':'?'},{"POS":{"IN":nombreLargo}, "OP":"+"},{"TEXT":"y"},{"LOWER": {"IN":calleSinonimos2}, "OP":"?"},{'TEXT': '.', 'OP':'?'},{"POS":{"IN":nombreLargo}, "OP":"+"}],
            ],
        )
        Matcher.matcher.add(
            "dir_entre", #los nuevos que agregué
            [
                [{"LEMMA": {"IN":calleSinonimos}},{'TEXT': '.', 'OP':'?'},{"LIKE_NUM": True},{"LOWER": "km"},{"LIKE_NUM": True}],
                [{"POS":{"IN":nombreLargo}, "OP":"+"},{"LIKE_NUM": True, "OP": "?"},{"LOWER": "km"},{"LIKE_NUM": True}],
                #[{"LEMMA": {"IN":calleSinonimos}},{'TEXT': '.', 'OP':'?'},{"POS":"PROPN", "OP":"+"},{"LOWER": "y"},{"POS":{"IN":nombreLargo}, "OP":"+"}],#supuestamente baja presición, pero es culpa del header
                #[{"LEMMA": {"IN":calleSinonimos2}},{"POS":{"IN":nombreLargo}, "OP":"+"},{"LOWER": "entre"},{"POS":{"IN":nombreLargo}, "OP":"+"},{"TEXT":"y"},{"POS":{"IN":nombreLargo}, "OP":"+"}],#supuestamente baja presición, pero es culpa del header
                [{"LEMMA": {"IN":calleSinonimos}},{'TEXT': '.', 'OP':'?'},{"POS":{"IN":nombreLargo}, "OP":"+"},{"TEXT": "al", "OP":"?"},{"LIKE_NUM": True, "OP":"+"},{"LOWER": "entre"},{"POS":{"IN":nombreLargo}, "OP":"+"},{"TEXT":"y"},{"POS":{"IN":nombreLargo}, "OP":"+"}],
                [{"POS":{"IN":nombreLargo}, "OP":"+"},{"LIKE_NUM": True, "OP": "?"},{"LOWER":"bis"}],
                #[{"LEMMA": {"IN":calleSinonimos}},{'TEXT': '.', 'OP':'?'},{"LIKE_NUM": True},{"LOWER":"bis"}] #no aporta nada

            ],
        )
        Matcher.matcher.add(
            "dir_lote", [
                [{"LOWER": "lote"}, {"POS": {"IN": ["NUM", "PROPN"]}}],
                [{"LOWER": "lote"}, {"POS": {"IN": ["NUM", "PROPN"]}}, {"LOWER": {"IN": ["en","sobre"]}, "OP":"?"}, {"LEMMA": {"IN": manzanaSinonimos}},{"LOWER": {"IN":numeroSinonimos}, "OP":"?"},{"LIKE_NUM": True}],
                [{"LEMMA": {"IN": manzanaSinonimos}},{"LOWER": {"IN":numeroSinonimos}, "OP":"?"},{"LIKE_NUM": True}, {"LOWER": {"IN": ["en","sobre"]}, "OP":"?"},{"LOWER": "lote"}, {"POS": {"IN": ["NUM", "PROPN"]}}],
            ]
        )

        Matcher.dependencyMatcher = DependencyMatcherSpacy(NLP.vocab)
        Matcher.dependencyMatcher.add(
            "frentes",
            patterns=[
                [
                    {
                        "RIGHT_ID": "frentes",
                        "RIGHT_ATTRS": {"LOWER": {"IN": ["frente", "frentes"]}},
                    },
                    {
                        "LEFT_ID": "frentes",
                        "REL_OP": ">",
                        "RIGHT_ID": "num",
                        "RIGHT_ATTRS": {"DEP": {"IN": ["nummod", "amod"]}},
                    },
                ],
                [
                    {"RIGHT_ID": "frentes", "RIGHT_ATTRS": {"LOWER": "salida"}},
                    {
                        "LEFT_ID": "frentes",
                        "REL_OP": ">",
                        "RIGHT_ID": "calles",
                        "RIGHT_ATTRS": {"DEP": "obl"},
                    },
                    {
                        "LEFT_ID": "calles",
                        "REL_OP": ">",
                        "RIGHT_ID": "num",
                        "RIGHT_ATTRS": {"DEP": "nummod"},
                    },
                ],
            ],
        )
        Matcher.dependencyMatcher.add(
            "fot",
            patterns=[
                [
                    {
                        "RIGHT_ID": "fot",
                        "RIGHT_ATTRS": {"LOWER": {"IN": ["fot", "f.o.t"]}},
                    },
                    {
                        "LEFT_ID": "fot",
                        "REL_OP": ">",
                        "RIGHT_ID": "num",
                        "RIGHT_ATTRS": {"DEP": "nummod"},
                    },
                ]
            ],
        )

    def __get_matches(self, text, prev_result):
        doc = NLP(text)

        matches = Matcher.matcher(doc)
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            prev_result[NLP.vocab.strings[match_id]].append(matched_span.text)

    def __get_dep_matches(self, text, prev_result):
        doc = NLP(text)
        matches_dep = Matcher.dependencyMatcher(doc)
        for match_id, token_ids in matches_dep:
            palabra = []
            for token_id in sorted(token_ids):
                token = doc[token_id]
                palabra.append(token.text)
            prev_result[NLP.vocab.strings[match_id]].append(" ".join(palabra))

    def __merge(self, dic1, dic2):
        for clave, valores in dic1.items():
            if clave in dic2:
                dic2[clave].extend(valores)
            else:
                dic2[clave] = valores

        return dic2

    def obtener_mejor_resultado(self, predichos):
        return {
            "direccion": procesar_direccion(predichos),
            "fot": procesar_fot(predichos["fot"]) if predichos["fot"] else "",
            "irregular": (
                procesar_irregular(predichos["irregular"])
                if len(predichos["irregular"]) > 0
                else ""
            ),
            "medidas": (
                procesar_medidas(predichos["medidas"]) if predichos["medidas"] else ""
            ),
            "esquina": True if len(predichos["esquina"]) > 0 else "",
            "barrio": (
                procesar_barrio(predichos["barrio"]) if predichos["barrio"] else ""
            ),
            "frentes": (
                procesar_frentes(predichos["frentes"]) if predichos["frentes"] else ""
            ),
            "pileta": True if len(predichos["pileta"]) > 0 else "",
        }

    def get_pairs(self, text: str):
        prev_result = {
            "medidas": [],
            "dir_nro": [],
            "dir_interseccion": [],
            "dir_entre": [],
            "dir_lote": [],
            "fot": [],
            "irregular": [],
            "pileta": [],
            "barrio": [],
            "esquina": [],
            "frentes": [],
        }
        self.__get_matches(text, prev_result)
        self.__get_dep_matches(text, prev_result)

        a = self.obtener_mejor_resultado(prev_result)
        return a
