import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
advertisement = "eat some banana sirloin steak"
doc = nlp(advertisement)
displacy.serve(doc, style="ent")

# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)