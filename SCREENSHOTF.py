from api import *
import json
import cv2
import cv2
import numpy as np
from imagedetection import *
from headerdetection import *
from paragraphdetection import *
from buttondetection import *
from line_detection import *

#Global Variable for Storing the Image Name. If you want to change the image just change here
image='screenshot17.jpeg'

height={'Header1': 58.0, 'Header2': 44.0, 'Header3': 35.0, 'Header4': 30.0, 'Header5': 24.0, 'Header6': 21.0}
heights=list(height.values())
limit=[]

#THE FOLLOWING LINES OF CODE DEFINES A RANGE OF HEIGHTS FOR CLASSIFYING A LINE AS HEADER 
upperlimit=int(heights[0]+4.0)
lowerlimit=int(heights[3]-2.0)
limit.append(lowerlimit)
limit.append(upperlimit)

print("upper limit and lower limit for heading is",upperlimit,lowerlimit)
test_file = ocr_space_file(filename=image, language='eng')
d=json.loads(test_file)
img=cv2.imread(image,1)
b=img.shape
print(b)
a=d["ParsedResults"][0]['TextOverlay']['Lines']
print(len(a))
dd=[]#Min Top List
g=[]#Max Height List
left=[]#Left list
for i in range(len(a)):
    q=[]#a list that stores the 'MaxHeight' and 'MinTop'
    left.append(a[i]['Words'][0]['Left'])
    q.append(a[i]['MinTop'])
    dd.append(a[i]['MinTop'])
    q.append(a[i]['MaxHeight'])
    g.append(a[i]['MaxHeight'])
    #print(i)
Min_Top_number=len(dd)

#IMAGE DETECTION
imagedetection(b,img)

#HEADER BUILDING
headerrownumber=headerdetection(g,lowerlimit,upperlimit,dd,b,img)

#PARAGRAPH BUILDING
list2=paragraphdetection(Min_Top_number,dd,a,headerrownumber,b,img,g)


#BUTTON DETECTION
buttondetection(image,img)


#For making lines,we will be refering to the line number starting from 0 i.e line number 1 will be zero etc
key_list=list2[1]
rows=list2[0]

#Line Detection
line_detection(key_list,headerrownumber,rows,dd,g,img,b)
