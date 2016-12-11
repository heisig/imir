from PIL import Image
import numpy
import math


def rgb_to_ycc((r, g, b)): # in (0,255) range
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

a = Image.open("a.jpg")
pix = a.load()


#step 1,2: rgb to ycc, devided in 8x8 fields: ycc_values[matrix_raw, matrix_col] = list of values
ycc_values={}
for x in range(0, a.size[0]):
    for y in range(0,a.size[1]):
        #ycc_values[x,y]=rgb_to_ycc(pix[x,y])
        #for i in range(0,8):
        #    for j in range(0,8):
        if x<a.size[0]/8:
            i = 0
        elif x >=a.size[0] / 8 and x< 2*a.size[0]/8:
            i = 1
        elif x >= 2*a.size[0] / 8 and x < 3 * a.size[0] / 8:
            i = 2
        elif x >= 3*a.size[0] / 8 and x < 4 * a.size[0] / 8:
            i = 3
        elif x >= 4*a.size[0] / 8 and x < 5 * a.size[0] / 8:
            i = 4
        elif x >= 5*a.size[0] / 8 and x < 6 * a.size[0] / 8:
            i = 5
        elif x >= 6*a.size[0] / 8 and x < 7 * a.size[0] / 8:
            i = 6
        elif x >= 7*a.size[0] / 8 and x < 8 * a.size[0] / 8:
            i = 7

        if y<a.size[1]/8:
            j = 0
        elif y >=a.size[1] / 8 and y< 2*a.size[1]/8:
            j = 1
        elif y >= 2*a.size[1] / 8 and y < 3 * a.size[1] / 8:
            j = 2
        elif y >= 3*a.size[1] / 8 and y < 4 * a.size[1] / 8:
            j = 3
        elif y >= 4*a.size[1] / 8 and y < 5 * a.size[1] / 8:
            j = 4
        elif y >= 5*a.size[1] / 8 and y < 6 * a.size[1] / 8:
            j = 5
        elif y >= 6*a.size[1] / 8 and y < 7 * a.size[1] / 8:
            j = 6
        elif y >= 7*a.size[1] / 8 and y < 8 * a.size[1] / 8:
            j = 7

        if (i, j) not in ycc_values.keys():
            ycc_values[(i, j)] = []
        ycc_values[(i,j)].append(rgb_to_ycc(pix[x,y]))





#step 3: estimate dominant (average) color of each matrix field
ycc_average_values ={}
for i in range(0, 8):
     for j in range(0,8):
        ycc_average_values[(i, j)] = (estimate_average_values(list=ycc_values[(i,j)]))
        print "average ycc in matrix field",   i, j, ":  ", ycc_average_values[(i,j)]



#step 4: apply DCT --Implementierung der bescheuerten Formel

dct_values_y = numpy.zeros((8,8))
dct_values_cb = numpy.zeros((8,8))
dct_values_cr = numpy.zeros((8,8))
for i in range(0,8):
    for j in range(0,8):
        sum_x = 0.0
        for x in range(0,8):
            sum_y= 0.0
            for y in range(0,8):
                #only for y-value of ycc
                sum_y = sum_y + ycc_average_values[x,y][0]*math.cos(math.pi*(2*x+1)*i/16)*math.cos(math.pi*(2*x+1)*j/16)
            sum_x = sum_x + sum_y

        dct_values_y[i,j] = alpha(i)*alpha(j)*sum_x
print dct_values_y