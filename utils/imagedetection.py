import numpy as np
import cv2

def imagedetection(image_shape,img):
    
    image_coordinates=[]
    height=image_shape[0]
    width=image_shape[1]
    #print("Height (Vert) x Width (Horiz) = "+str(height)+" x "+str(width))
    
    #These rows have data, ie atleast 1 pixel does not match background color
    dataRows=[]

    # Start from 1,1 since we used 0,0 for background
    for i in range(0,height):
        datainRow=False
        #backgroundpixel is the pixel value of the ith row
        backgroundPixel=img[i,0]

        for j in range(1,width):
            #pixeltocheck is the pixel to be checked against the background pixel.
            pixelToCheck=img[i,j]

            if np.array_equal(pixelToCheck,backgroundPixel):
                datainRow=False

            else:
                if (abs(int(pixelToCheck[0])-int(backgroundPixel[0]))>100) or (abs(int(pixelToCheck[1])-int(backgroundPixel[1]))>100) or (abs(int(pixelToCheck[2])-int(backgroundPixel[2]))>100):
                    #print("Data Found",i,pixelToCheck,backgroundPixel)
                    datainRow=True
                    break;   


        if(datainRow):
            dataRows.append(i)
            
    #print(dataRows)
    
    #ranges_of_each_box stores the upper row number and bottom row number of the each box formed
    ranges_of_each_box = sum((list(t) for t in zip(dataRows, dataRows[1:]) if t[0]+1 != t[1]), [])
    dataRows[-1:]

    #iranges add the first element which was excluded in ranges_of_each_box
    iranges = dataRows[0:1] + ranges_of_each_box +dataRows[-1:]
    #print('iranges',iranges)

    #list_of_ranges stores two consecutive numbers of iranges as they specify the upper bound and 

    #lower bound of one box.
    list_of_ranges=[]

    for i in range(1,len(iranges),2):
        ex1=[]
        ex1.append(iranges[i-1])
        ex1.append(iranges[i])
        list_of_ranges.append(ex1)
    #print("list_of_ranges",list_of_ranges)
    
    #image_box stores the upper row number and lower row number(which satisfies a condition) of 

    # a box for drawing the rectangle
    image_box=[]

    for i in range(0,len(list_of_ranges)):
        #A temporary variable for checking the condition.
        ex1=list_of_ranges[i]
        #55 is the difference between the upper bound and lower bound of a box.We have chosen 
        #55 because in a screenshot the maximum height of the text will be that of H1 that is 55.
        #So if the difference is greater than 55 then it will be image only.
        if (ex1[-1]-ex1[0])>=55:
            image_box.append(ex1)
    #print("image_box",image_box)

    if(len(image_box)>1):

        for i in range(0,len(image_box)):

            each_image_coordinate=[]
            #ex4 contains the rows number about which rectangle should be drawn
            ex4=image_box[i]
            cv2.rectangle(img,(0,ex4[0]),(image_shape[0],ex4[1]),(255,0,0),2)
            font =cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,'IMAGE'+str(i+1),(0,ex4[0]), font, 1,(255,0,0),1)

            each_image_coordinate.append((0,ex4[0]))
            each_image_coordinate.append((image_shape[0],ex4[1]))
        image_coordinates.append(each_image_coordinate)

    elif len(image_box)==1:
        #ex5 contains the rows number about which rectangle should be drawn
        each_image_coordinate=[]

        ex5=image_box[0]
        cv2.rectangle(img,(0,ex5[0]),(image_shape[0],ex5[1]),(255,0,0),2)
        font =cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'IMAGE'+str(1),(0,ex5[0]), font, 1,(255,0,0),1)
        each_image_coordinate.append((0,ex5[0]))
        each_image_coordinate.append((image_shape[0],ex5[1]))
        image_coordinates.append(each_image_coordinate)

    #UNCOMMENT FOR DEBUGGING
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image_coordinates

