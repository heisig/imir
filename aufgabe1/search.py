import pickle

# für jedes recherchierbare Wort Position im
# Datenbestand in einen Index eintragen

#  Verarbeitungsschritte (Reihenfolge kann variieren):
# 1. Strukturelimination
# 2. Elimination von häufigen/seltenen Termen (Stoppwörter)
# 3. Text wird in Terme aufgebrochen (ohne Satzzeichen)
# 4. Reduktion der Terme auf Stammform / Grundform
# 5. Abbildung auf Indexterme


# Boolesches Retrieval
# – binärer Vektor d beschreibt Vorhandensein eines Terms:
# di=0  Term nicht vorhanden, di=1  Term vorhanden
# – Implementierung mittels Invertierter Listen
    #  zu jedem vorhandenen Attribut: Speicherung der Liste der Dokumente,
    # welche durch dieses beschrieben sind
    #  Dateibasierte Realisierung: für jeden Term separate Datei mit den IDs der
    # Dokumente
        # – Vorteil: einfache Implementierung, gute Performance
        # – Nachteil: keine Transaktionsgarantien (paralleles Suchen und Ändern)
        # – Herausforderungen: Kompression der Indexe, effizientes Modifizieren des
        # Indexes beim Einfügen/Ändern/Löschen von Dokumenten
    #  DB-basierte Real. : Dokumententabelle + Attributtabelle + Invertierte Liste
        # – Auswertung mittels geeigneter „Select“-Statements
        # – Vorteil: Transaktionen, Recovery, Caching, gute Performance, einfache
        # Implementierung
        # – Nachteil: nicht so effizient wie dateibasierte Lösung


#build list of terms (collect documents, turn each document into list of tokens, normalize tokes
#for each term as key store all documents that contain it to list as value
#here building inverted index
# list = []
# inverted_dict = {}
# for key in docs:
#     tokens = docs.get(key).split(' ')
#     for token in tokens:
#         list.append(token.lower())
#         if token.lower() not in inverted_dict.keys():
#
#              inverted_dict[token.lower()] = []   #for list without duplicates use set!
#         inverted_dict[token.lower()].append(key)
#
# #print("list of tokens", list)
# print("inverted dict", inverted_dict)
print("Loading data...")
inverted_dict = pickle.load(open('output.txt', 'rb'),encoding="utf-8")
#print("inverted dict ", inverted_dict)


query= input("Your Query: ")
# precedence: or--> and--> not
query_or_split = query.split(' OR ')
#print("query or split", query_or_split)
or_set = set()
for term in query_or_split:
    #and splitting
    query_and_split = term.split (' AND ')
    #print("query and split", query_and_split)
    and_set = set()
    not_set = set()
    for andterm in query_and_split:
        query_not_split = None
        if ' NOT ' in andterm:
            query_not_split = term.split (' NOT ')
            #print("not split", query_not_split)
            not_set.add(query_not_split)
        if 'NOT ' in andterm:
            query_not_split = andterm.replace('NOT ', "")
            #print("not split", query_not_split)
            not_set.add(query_not_split)
        if not query_not_split:
            if andterm in inverted_dict.keys():
                if not and_set:
                    and_set.update(set(inverted_dict[andterm].keys()))
                else:
                    and_set.intersection_update(set(inverted_dict[andterm].keys()))
            #else:
    #print("not set", not_set)
    for notterm in not_set:
        for andterm in and_set.copy():
            if andterm in set(inverted_dict[notterm].keys()):
                and_set.remove(andterm)
    #print("and_set", and_set)


            #print("and_set", and_set)
    or_set.update(and_set)

print("query answer: ids of found sources: ", or_set)   #prints query with OR and AND. Needed case to print only AND
print("query answer: number of found sources: ", len(or_set))
print("query answer: number of occurrences: toDo" )
#only OR
# query= input("Your Query: ")
# # precedence: or--> and--> not
# query_or_split = query.split(' OR ')
# #print("query or split", query_or_split)
# or_set = set()
# for term in query_or_split:
#     if term in inverted_dict.keys():
#         #print("term, docs", term, inverted_dict[term])
#         or_set.update(set(inverted_dict[term]))
#
# print(" query with or answer: ", or_set)





