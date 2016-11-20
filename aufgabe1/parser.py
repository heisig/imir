import re
import pickle
from collections import namedtuple

Entry = namedtuple('Entry', 'id URI abstract')


def line_to_entry(i, line):
    return Entry(
        i,
        re.match(r'<([^>]+)>', line).group(1),
        re.search(r'"([^"]+)"', line).group(1)
    )


def get_entries(path):
    with open(path, encoding='utf-8') as file:
        i = 0
        list = []
        for line in file:
            i += 1
            if line.startswith('<'):
                list.append(line_to_entry(i, line))
        return list

if __name__ == '__main__':
    entries = get_entries("test.ttl")

    tmp = 1
    glossary = {}
    re_word = re.compile('\w+', re.UNICODE)
    for entry in entries:
        words = re_word.findall(entry.abstract)
        for position,word in enumerate(words):
            word = word.lower();
            docID = entry.id
            if word in glossary:
                if docID in glossary[word]:
                    glossary[word][docID].append(position)
                else:
                    glossary[word].update({docID : [position]})
            else:
                glossary[word] = {docID : [position]}

    with open('output.txt', 'wb') as output:
        pickle.dump(glossary, output)
#         output.write(str(glossary))
#        output.write('{')
#        for key, value in glossary.items():
#            output.write('\'%s\':{' % key)
#            for key2, value2 in value.items():
#                output.write('\'%s\':' % key2 + '[' + ','.join(str(x) for x in value2) + ']')
#            output.write('}\n')
#        output.write('}')