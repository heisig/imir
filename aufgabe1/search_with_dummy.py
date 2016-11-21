docs = {"buch0": "eins zwei Drei Vier", "buch1": " fünf lol heros", "buch2": "Vier Vier eins heros eins heros heros"}
inverted_dict = {'drei': {'buch0': [2]}, 'eins': {'buch0': [0], 'buch2': [2, 4]},
                 'vier': {'buch0': [3], 'buch2': [0, 1]}, 'heros': {'buch1': [2], 'buch2': [3, 5, 6]},
                 'lol': {'buch1': [1]}, 'fünf': {'buch1': [0]}, 'zwei': {'buch0': [1]}}

print(docs)
print(inverted_dict)


# returnt ein True wenn sich pos mindestens ein mal in positionsList befindet
def checkForPosition(positionList, pos):
    i = False
    for p in positionList:
        if pos == p:
            i = True
    return i


# returns set of all document identifiers
def get_doc_set(inverted_dict):
    set_of_docs = set()
    for word in inverted_dict.keys():
        for doc in inverted_dict[word].keys():
            set_of_docs.add(doc)
    return set_of_docs


"""
function reads input and splits it in single terms. Cases with oprators OR, AND, NOT
search in inverted index and join the single terms.
"""


def binary_search():
    query = input("Your Query: ")
    occurences = 0
    query_or_split = query.split(' OR ')  # list of all OR terms
    documents_set = get_doc_set(inverted_dict)
    or_set = set()
    or_not_set = set()  # set with documents for NOT terms within simple OR terms, to be deleted out of answer
    for term in query_or_split:
        # case with AND terms
        if ' AND ' in term:
            query_and_split = term.split(' AND ')
            and_set = set()  # set with documents for simple AND terms
            and_terms = {}
            not_set = set()  # set with documents for NOT terms within AND terms, to be deleted out of answer
            for andterm in query_and_split:
                not_term = None
                # if "NOT" within AND terms
                if ' NOT ' in andterm:
                    not_term = andterm.replace(' NOT ', "")
                elif 'NOT ' in andterm:
                    not_term = andterm.replace('NOT ', "")
                # if no phrase within NOT term, add the documents with term to not_set
                if not_term is not None and ' ' not in not_term and not_term.lower() in inverted_dict.keys():
                    not_set.update(inverted_dict[not_term.lower()].keys())
                # if phrase within NOT term, add all documents with phrase to not_set
                elif not_term is not None and ' ' in not_term:
                    not_set.update(set(phrase_search(not_term.lower(), inverted_dict).keys()))
                # if no NOT terms within AND term, check, if it is phrase, add terms and considering docs to and_terms
                elif not_term is None:
                    if ' ' in andterm:
                        phrases = phrase_search(andterm.lower(), inverted_dict).keys()
                        if phrases:
                            and_terms[andterm.lower()] = phrases
                        # if no phrases, break AND loop, clear and_set and and_terms
                        else:
                            and_terms.clear()
                            and_set.clear()
                            break
                    #cases with simple and term
                    elif andterm.lower() in inverted_dict.keys():
                        and_terms[andterm.lower()] = inverted_dict[andterm.lower()].keys()
                    else:
                        return print("No resources found!")
            # go through and_set to check occurences
            for andterm in and_terms.keys():
                if not and_set:
                    and_set.update(set(and_terms[andterm.lower()]))
                else:
                    and_set.intersection_update(set(and_terms[andterm.lower()]))

            # delete all documents with NOT terms out of and_set.
            # More efficient than intersection of all NOT answers with normal AND terms!
            for not_doc in not_set:
                for and_doc in and_set.copy():
                    if not_doc == and_doc:
                        and_set.remove(and_doc)
            or_set.update(and_set)

            # calculate occurences for all remaind AND results
            for andterm in and_terms:
                for doc in and_set:
                    if ' ' in andterm:
                        occurences = occurences + phrase_search(andterm.lower(), inverted_dict)[doc]
                    else:
                        occurences = occurences + len(inverted_dict[andterm.lower()][doc])

        # if there are no AND terms, check for NOTs and phrases
        else:
            not_term = None
            if ' NOT ' in term:
                not_term = term.replace(' NOT ', "")
            elif 'NOT ' in term:
                not_term = term.replace('NOT ', "")
            # simple OR with phase search
            elif ' ' in term:
                phrases = phrase_search(term.lower(), inverted_dict).keys()
                or_set.update(set(phrases))
                for source in phrases:
                    occurences = occurences + phrase_search(term.lower(), inverted_dict)[source]
            # simple OR
            elif ' ' not in term and term.lower() in inverted_dict.keys():
                or_set.update(inverted_dict[term.lower()].keys())
                for key in inverted_dict[term.lower()].keys():
                    occurences = occurences + len(inverted_dict[term.lower()][key])
            # cases with simple NOT terms and NOT phrases within OR terms
            if not_term is not None and ' ' not in not_term and not_term.lower() in inverted_dict.keys():
                or_not_set.update(set(inverted_dict[not_term.lower()].keys()))
            # make sure that or_not_set without valid documents and not empty
            elif not_term is not None and ' ' not in not_term and not_term.lower() not in inverted_dict.keys():
                or_not_set.add("")
            elif not_term is not None and ' ' in not_term:
                or_not_set.update(set(phrase_search(not_term.lower(), inverted_dict).keys()))
                # if phrase not in dict, make sure that or_not_set without valid documents and not empty
                if not or_not_set:
                    or_not_set.add("")
    # case with NOT term within OR
    if or_not_set:
        # build complement set for not_set and add to OR result
        not_result_set = documents_set.difference(or_not_set)
        print("not result set", not_result_set)
        or_set.update(not_result_set)

    if or_set:
        print("query answer: ids of found sources: ",
              or_set)  # prints query with OR and AND. Needed case to print only AND
        print("query answer: number of found sources: ", len(or_set))
        print("query answer: number of occurrences: ", occurences)
    else:
        print("No resources found!")


# Hungs Funktion zur Phrasensuche
# prüft mithilfe eines dictionarys, wie oft eine phrase oder ein wort in einem Dokument vorkommt
def phrase_search(phrase, dictionary):
    # spalte phrase in einzelne Wörter
    # speichere anzahl der wörter
    # speichere das erste Wort
    # lege neues dictionary an

    wordList = phrase.split()

    # if any word of phrase not in dictionary, return empty dictionary
    for word in wordList:
        if word not in inverted_dict.keys():
            return {}

    wordCount = len(wordList)
    startWord = wordList[0]
    docList = {}

    # Für alle Dokumente in denen das erste Wort vorkommt
    for docs in dictionary[startWord]:

        # für alle Positionen des ersten Wortes im Dokument
        for startPos in dictionary[startWord][docs]:

            # counter: Wird jedes Mal erhöht, wenn sich ein Wort an der richtigen Position befindet
            counter = 1

            i = 1
            while i < wordCount:
                # nextWord : das i-te Wort in der Phrase
                nextWord = wordList[i]

                # prüfe ob nextWord im Dokument überhaupt vorkommt
                if docs in dictionary[nextWord]:
                    nextPos = dictionary[nextWord][docs]
                    # prüfe ob sich das Wort i-Stellen nach der StartPosition befindet. Erhöht in dem Fall den counter
                    if checkForPosition(nextPos, startPos + i):
                        counter += 1
                i += 1
            # Wenn die Phrase sich in einem Dokument befindet, wurde der Counter für jedes einzelne Wort um 1 erhöht und ist genauso groß wie die Wortlänge
            if counter == wordCount:
                # print ('HORAY')

                # lege den Eintrag im Dictionary an bzw aktualisiere es.
                if docs in docList:
                    docList[docs] += 1
                else:
                    docList[docs] = 1
    return docList


# Start of Program

# testPhrase = input('phrase eingeben:')
# print (phrase_search(testPhrase, inverted_dict))

binary_search()
