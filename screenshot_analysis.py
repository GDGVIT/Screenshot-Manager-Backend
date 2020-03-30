import json

import cv2
import numpy as np

from .utils.api import *
from .utils.imagedetection import *
from .utils.headerdetection import *
from .utils.paragraphdetection import *
from .utils.buttondetection import *
from .utils.line_detection import *

def annotate_screenshot(image_data,image_name):

    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
    #print("image name is",image_name)
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

    test_file = ocr_space_file(image_data,image_name, language='eng')
    test_file = json.loads(test_file)

    #img reads the image in the coloured(1->colored,0->grayscale)
    image_shape = image.shape
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

    min_top_number = len(min_top_list)

    #IMAGE DETECTION
    image_coordinates=imagedetection(image_shape,image)
    #print("The image coordinates are",image_coordinates)
    
    #HEADER BUILDING
    headerrownumber = headerdetection(max_height_list,lowerlimit,upperlimit,min_top_list,image_shape,image)[0]
    header_coordinates=headerdetection(max_height_list,lowerlimit,upperlimit,min_top_list,image_shape,image)[1]
    #print("The header_coordinates are",header_coordinates)
    
    #PARAGRAPH BUILDING
    list2=paragraphdetection(min_top_number,min_top_list,each_line_info,headerrownumber,image_shape,image,max_height_list)[0]
    paragraph_coordinates=paragraphdetection(min_top_number,min_top_list,each_line_info,headerrownumber,image_shape,image,max_height_list)[1]
    #print("The paragraph coordinates are",paragraph_coordinates)

    #BUTTON DETECTION
    button_coordinates=buttondetection(image)
    #print("The coordinates for buttons are",button_coordinates)

    #For making lines,we will be refering to the line number starting from 0 i.e line number 1 will be zero etc

    #Key_list stores the line numbers from 1 to last row number
    key_list = list2[1]

    #rows stores the rows number that have been classified as paragraphs
    rows = list2[0]

    #Line Detection
    final_image = line_detection(key_list,headerrownumber,rows,min_top_list,max_height_list,image,image_shape)[0]
    line_coordinates=line_detection(key_list,headerrownumber,rows,min_top_list,max_height_list,image,image_shape)[1]
    #print("The line coordinates are",line_coordinates)
    #UNCOMMENT FOR SEEING THE FINAL IMAGE
    # cv2.imshow('image',final_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    coordinates={'Image':image_coordinates,'Header':header_coordinates,
    'Paragraph':paragraph_coordinates,'Button':button_coordinates,
    'Line':line_coordinates}
    


    return coordinates
