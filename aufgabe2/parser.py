from PIL import Image
import numpy, math, pickle, glob, os, re, xml.etree.ElementTree, time, sys

def rgb_to_ycc(r, g, b): # in (0,255) range
    y = 0.299*r + 0.587*g + 0.114*b
    cb = 128 -0.168736*r -0.331364*g + 0.5*b
    cr = 128 +0.5*r - 0.418688*g - 0.081312*b
    return y, cb, cr

def estimate_average_values(list):
    sum_y = 0
    sum_cr = 0
    sum_cb = 0
    for elem in list:
        sum_y = sum_y + elem[0]
        sum_cb = sum_cb + elem[1]
        sum_cr = sum_cr + elem[2]
    return int(round(sum_y/len(list), 0)), int(round(sum_cb/len(list), 0)), int(round(sum_cr/len(list), 0))

def alpha(u):
    if u==0:
        return math.sqrt(2)/4
    else:
        return 0.5

start = time.time()

#pictureDirectory = "PlantCLEF2016Test"
pictureDirectory = "testData"
pictureCount = 0
index = {}
pictureList = []
estimate = "time left: ?"

# traverse over the given directory
for file in glob.glob(os.path.join(pictureDirectory,"*.jpg")):
    filename = os.path.basename(file)
    # find matching objects and save its ID (leave out the one with ._ at the start)
    file = re.match("([^._]*).jpg$", filename)
    pictureID = file.group(1)

    pictureList.append(pictureID)

print(str(len(pictureList)) + " pictures found, starting to build the index ...")

for pictureID in pictureList:
    if pictureCount != 0:
        splitTime = time.time()
        seconds = splitTime - start
        estimate = seconds * len(pictureList)/pictureCount - seconds
        m, s = divmod(estimate, 60)
        h, m = divmod(m, 60)
        estimate = "time left: " + "%d:%02d:%02d" % (h, m, s)

    pictureCount += 1
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write("processing pictureID " + pictureID + " - (" + str(pictureCount) + "/" + str(len(pictureList)) + ") - " + estimate)

    # get category from xml file
    root = xml.etree.ElementTree.parse(pictureDirectory + "/" + pictureID + ".xml").getroot()
    for content in root.findall('Content'):
        category = content.text
        #print(category)

    picture = Image.open(pictureDirectory + "/" + pictureID + ".jpg")
    pix = picture.load()

    #step 1,2: rgb to ycc, devided in 8x8 fields: ycc_values[matrix_raw, matrix_col] = list of values
    ycc_values={}
    for x in range(0, picture.size[0]):
        for y in range(0,picture.size[1]):
            #ycc_values[x,y]=rgb_to_ycc(pix[x,y])
            #for i in range(0,8):
            #    for j in range(0,8):
            if x<picture.size[0]/8:
                i = 0
            elif x >=picture.size[0] / 8 and x< 2*picture.size[0]/8:
                i = 1
            elif x >= 2*picture.size[0] / 8 and x < 3 * picture.size[0] / 8:
                i = 2
            elif x >= 3*picture.size[0] / 8 and x < 4 * picture.size[0] / 8:
                i = 3
            elif x >= 4*picture.size[0] / 8 and x < 5 * picture.size[0] / 8:
                i = 4
            elif x >= 5*picture.size[0] / 8 and x < 6 * picture.size[0] / 8:
                i = 5
            elif x >= 6*picture.size[0] / 8 and x < 7 * picture.size[0] / 8:
                i = 6
            elif x >= 7*picture.size[0] / 8 and x < 8 * picture.size[0] / 8:
                i = 7

            if y<picture.size[1]/8:
                j = 0
            elif y >=picture.size[1] / 8 and y< 2*picture.size[1]/8:
                j = 1
            elif y >= 2*picture.size[1] / 8 and y < 3 * picture.size[1] / 8:
                j = 2
            elif y >= 3*picture.size[1] / 8 and y < 4 * picture.size[1] / 8:
                j = 3
            elif y >= 4*picture.size[1] / 8 and y < 5 * picture.size[1] / 8:
                j = 4
            elif y >= 5*picture.size[1] / 8 and y < 6 * picture.size[1] / 8:
                j = 5
            elif y >= 6*picture.size[1] / 8 and y < 7 * picture.size[1] / 8:
                j = 6
            elif y >= 7*picture.size[1] / 8 and y < 8 * picture.size[1] / 8:
                j = 7

            if (i, j) not in ycc_values.keys():
                ycc_values[(i, j)] = []
            ycc_values[(i,j)].append(rgb_to_ycc(pix[x,y][0], pix[x,y][1], pix[x,y][2]))





    #step 3: estimate dominant (average) color of each matrix field
    ycc_average_values ={}
    for i in range(0, 8):
         for j in range(0,8):
            ycc_average_values[(i, j)] = (estimate_average_values(list=ycc_values[(i,j)]))
            #print("average ycc in matrix field",   i, j, ":  ", ycc_average_values[(i,j)])



    #step 4: apply DCT
    dct_values_y = numpy.zeros((3,3))
    dct_values_cb = numpy.zeros((3,3))
    dct_values_cr = numpy.zeros((3,3))
    for i in range(0,3):
        for j in range(0,3):
            sum_x_y = 0.0
            sum_x_cb = 0.0
            sum_x_cr = 0.0
            for x in range(0,8):
                sum_y_y = 0.0
                sum_y_cb = 0.0
                sum_y_cr = 0.0
                for y in range(0,8):
                    #for y-value of ycc
                    sum_y_y = sum_y_y + ycc_average_values[x,y][0]*math.cos(math.pi*(2*x+1)*i/16)*math.cos(math.pi*(2*x+1)*j/16)
                    #for cb-value of ycc
                    sum_y_cb = sum_y_cb + ycc_average_values[x,y][1]*math.cos(math.pi*(2*x+1)*i/16)*math.cos(math.pi*(2*x+1)*j/16)
                    #for cr-value of ycc
                    sum_y_cr = sum_y_cr + ycc_average_values[x,y][2]*math.cos(math.pi*(2*x+1)*i/16)*math.cos(math.pi*(2*x+1)*j/16)
                sum_x_y = sum_x_y + sum_y_y
                sum_x_cb = sum_x_cb + sum_y_cb
                sum_x_cr = sum_x_cr + sum_y_cr

            dct_values_y[i,j] = alpha(i)*alpha(j)*sum_x_y
            dct_values_cb[i,j] = alpha(i)*alpha(j)*sum_x_cb
            dct_values_cr[i,j] = alpha(i)*alpha(j)*sum_x_cr

    #print(dct_values_y)
    #print(dct_values_cb)
    #print(dct_values_cr)

    # adding the DC and AC coefficients as a tuple
    dctValues = (
        dct_values_y[0,0],  #  Y DC Coeff (Position  1)
        dct_values_cb[0,0], # CB DC Coeff (Position  1)
        dct_values_cr[0,0], # CB DC Coeff (Position  1)
        dct_values_y[0,1],  #  Y AC Coeff (Position  2)
        dct_values_y[1,0],  #  Y AC Coeff (Position  9)
        dct_values_y[2,0],  #  Y AC Coeff (Position 17)
        dct_values_y[2,2],  #  Y AC Coeff (Position 10)
        dct_values_y[0,2],  #  Y AC Coeff (Position  3)
        dct_values_cb[0,1], # CB AC Coeff (Position  2)
        dct_values_cb[1,0], # CB AC Coeff (Position  9)
        dct_values_cr[0,1], # CR AC Coeff (Position  2)
        dct_values_cr[1,0], # CR AC Coeff (Position  9)
    )

    # adding the pictureID and its DCT Values in a dict to the right category
    if category not in index:
        index[category] = {pictureID : dctValues}
    else:
        index[category][pictureID] = dctValues

with open('index.txt', 'wb') as output:
        pickle.dump(index, output)

end = time.time()
seconds = end - start
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
elapsedTime = "%d:%02d:%02d" % (h, m, s)

print(" ")
print("Processed " + str(pictureCount) + " pictures in " + str(len(index)) + " categories")
print("Elapsed Time: " + elapsedTime)
print("Index created and written into index.txt")
input("Press any key to continue...")
