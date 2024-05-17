medidas = ["m2", "metro", "m", "mt", "m^2", "m²", "metros", "mts", "mts2", "ms2", "ms"]
medidas2D = ["m2", "m^2", "mts2", "ms2", "m²"]

[{"LIKE_NUM":True},
 {"LOWER": {"IN":medidas}},
 {"POS":{"IN":["ADP", "ADV", "PROPN", "NOUN"]}, "OP":"*"},
 {"LOWER":{"IN":["x", "y", "por"]}},
 {"LIKE_NUM":True, "OP":"+"},
 {"LOWER": {"IN":medidas}, "OP":"?"}]

[{"LIKE_NUM":True},
 {"LOWER": {"IN":medidas}, "OP":"?"},
 {"POS":{"IN":["ADP", "ADV","PROPN", "NOUN"]}, "OP":"*"},
 {"LOWER":{"IN":["x", "y", "por"]}},
 {"LIKE_NUM":True, "OP":"+"},
 {"LOWER": {"IN":medidas}}]

[{"LIKE_NUM":True},
 {"LOWER": {"IN":medidas2D}}]
