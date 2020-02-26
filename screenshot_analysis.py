import json

import cv2
import numpy as np

from utils.ocr_api_fetch import *
from utils.imagedetection import *
from utils.headerdetection import *
from utils.paragraphdetection import *
from utils.buttondetection import *
from utils.line_detection import *

#Global Variable for Storing the Image Name. If you want to change the image just change here
image='Test Images/screenshot2.jpeg'

#THE HEIGHT DICTIONARY STORES THE HEIGHT OF THE HEADER TAGS(H1...H6).HEIGHTS STORES THE VALUES OF THE DICTIONARY
height={'Header1': 58.0, 'Header2': 44.0, 'Header3': 35.0, 'Header4': 30.0, 'Header5': 24.0, 'Header6': 21.0}
heights=list(height.values())
limit=[]

#THE FOLLOWING LINES OF CODE DEFINES A RANGE OF HEIGHTS FOR CLASSIFYING A LINE AS HEADER AND STORES THE LIMITS IN LIMIT LIST
upperlimit=int(heights[0]+4.0)
lowerlimit=int(heights[3]-2.0)
limit.append(lowerlimit)
limit.append(upperlimit)
#print("upper limit and lower limit for heading is",upperlimit,lowerlimit)

test_file = ocr_space_file(filename=image, language='eng')
test_file=json.loads(test_file)

#img reads the image in the coloured(1->colored,0->grayscale)
img=cv2.imread(image,1)
image_shape=img.shape
#print(image_shape)

#each_line_info is a list of length equal to the number of rows having text in them.
#It contains the informartion like line text,word text maximum height of a word in a
#line which we will use in the future.
each_line_info=test_file["ParsedResults"][0]['TextOverlay']['Lines']
#print(len(each_line_info))

#min_top_list stores the left topmost point of the text in the row
min_top_list=[]

#max_height_list stores the height of the each row(having text) in the screenshot
max_height_list=[]

#left list stores how much left the first word of the line is
left=[]

for i in range(len(each_line_info)):
    left.append(each_line_info[i]['Words'][0]['Left'])
    min_top_list.append(each_line_info[i]['MinTop'])
    max_height_list.append(each_line_info[i]['MaxHeight'])
    #print(i)

Min_Top_number=len(min_top_list)

#IMAGE DETECTION
imagedetection(image_shape,img)

#HEADER BUILDING
headerrownumber=headerdetection(max_height_list,lowerlimit,upperlimit,min_top_list,image_shape,img)

#PARAGRAPH BUILDING
list2=paragraphdetection(Min_Top_number,min_top_list,each_line_info,headerrownumber,image_shape,img,max_height_list)

#BUTTON DETECTION
buttondetection(image,img)

#For making lines,we will be refering to the line number starting from 0 i.e line number 1 will be zero etc

#Key_list stores the line numbers from 1 to last row number
key_list=list2[1]

#rows stores the rows number that have been classified as paragraphs
rows=list2[0]

#Line Detection
final_image=line_detection(key_list,headerrownumber,rows,min_top_list,max_height_list,img,image_shape)


#UNCOMMENT FOR SEEING THE FINAL IMAGE
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
