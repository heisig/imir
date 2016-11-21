import re
import pickle
from collections import namedtuple
#responsible for creating an inverted index abd parsing the results into a file

Entry = namedtuple('Entry', 'id URI abstract')

#create an entry from a line
def line_to_entry(i, line):
    return Entry(
        i,
        re.match(r'<([^>]+)>', line).group(1),
        re.search(r'"([^"]+)"', line).group(1)
    )

#get each line and execute
def get_entries(path):
    with open(path, encoding='utf-8') as file:
        i = 0
        list = []
        for line in file:
            i += 1
            if line.startswith('<'):
                list.append(line_to_entry(i, line))
        return list

#start with the file given here
if __name__ == '__main__':
    query = input("File name (or location relativ to the current folder): ")
    print("Creating inverted index. This may take several minutes depending on the initial file size.")
    entries = get_entries(query)

    tmp = 1
    glossary = {}
    re_word = re.compile('\w+', re.UNICODE)
    #get all words
    for entry in entries:
        words = re_word.findall(entry.abstract)
        #for all words in the entry
        for position,word in enumerate(words):
            # lower the word, get entry id
            word = word.lower();
            docID = entry.id
            #put word, docid and position in the glossary depending on what is already existing in the glossary
            if word in glossary:
                if docID in glossary[word]:
                    glossary[word][docID].append(position)
                else:
                    glossary[word].update({docID : [position]})
            else:
                glossary[word] = {docID : [position]}
    #serialize the finished glossary
    #this may take several minutes (depending on input file size)
    with open('output.txt', 'wb') as output:
        pickle.dump(glossary, output)
    print("Success. output.txt created.")
    input("Press any key to continue...")
#         output.write(str(glossary))
#        output.write('{')
#        for key, value in glossary.items():
#            output.write('\'%s\':{' % key)
#            for key2, value2 in value.items():
#                output.write('\'%s\':' % key2 + '[' + ','.join(str(x) for x in value2) + ']')
#            output.write('}\n')
#        output.write('}')