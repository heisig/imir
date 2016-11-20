import re
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

    glossary = {}
    re_word = re.compile('\w+', re.UNICODE)
    for entry in entries:
        words = re_word.findall(entry.abstract)
        #words = [word.lower() for word in words]
        for word in words:
            word = word.lower();
            if word in glossary:
                glossary[word].append(entry.id)
            else:
                glossary[word] = [entry.id]

    with open('output.txt', 'w', encoding='utf-8') as output:
        for key, value in glossary.items():
            output.write('%s: ' % key)
            output.write(','.join(str(x) for x in value))
            output.write('\n')
