import os
import pickle
import webbrowser
import xml.etree.ElementTree

base_path = "PlantCLEF2016Test"
#base_path = "testData"

def search(search_id, num_closest):
    with open("index.txt", "rb") as index_file:
        index = pickle.load(index_file)
        
    root = xml.etree.ElementTree.parse(
        os.path.join(base_path, search_id + ".xml")
    ).getroot()
    try:
        search_type = root.findall('Content')[0].text
    except KeyError:
        search_type = None
    search_coeffs = index[search_type][search_id]

    distances = []
    for type in index:
        if type == search_type:
            for id in index[type]:
                if id != search_id:
                    coeffs = index[type][id]

                    distance = 0
                    for pair in zip(coeffs, search_coeffs):
                        distance += abs(pair[0] - pair[1])
                    distances.append((distance, id))

    distances.sort()
    return distances[:num_closest]

print("ID of the reference picture: ", end="")
search_id = input()
print("How many results do you want to find (nearest neighbours): ", end="")
max_results = int(input())
distances = search(search_id, max_results)
#print(distances)

with open("results_template.html", "r") as template, \
    open("results.html", "w") as output:
    text = template.read()

    search_image_path = os.path.join(base_path, search_id + ".jpg")
    search_tag = '<img class="img-responsive" src="{0}">'.format(search_image_path)

    result_tags = []
    for distance, id in distances:
        image_path = os.path.join(base_path, id + ".jpg")
        result_tags.append(
            '<img class="img-responsive" src="{0}">'.format(image_path)
        )
    result_tag = '\n'.join(result_tags)

    output.write(text.format(search_tag, result_tag))
    print("output.html created. Showing in browser.")
    webbrowser.open_new_tab("results.html")
