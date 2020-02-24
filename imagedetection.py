import numpy as np
import cv2
def imagedetection(b,img):
    height=b[0]
    width=b[1]
    #print("Height (Vert) x Width (Horiz) = "+str(height)+" x "+str(width))
    #These rows have data, ie atleast 1 pixel does not match background color
    dataRows=[]

    # Start from 1,1 since we used 0,0 for background
    for i in range(0,height):
        datainRow=False
        backgroundPixel=img[i,0]
        for j in range(1,width):
            pixelToCheck=img[i,j]
            if np.array_equal(pixelToCheck,backgroundPixel):
                datainRow=False
            else:
                if (abs(int(pixelToCheck[0])-int(backgroundPixel[0]))>100) or (abs(int(pixelToCheck[1])-int(backgroundPixel[1]))>100) or (abs(int(pixelToCheck[2])-int(backgroundPixel[2]))>100):
                    print("Data Found",i,pixelToCheck,backgroundPixel)
                    #time.sleep(1)
                    datainRow=True
                    break;        
        if(datainRow):
            dataRows.append(i)
            
    #print(dataRows)
    ranges = sum((list(t) for t in zip(dataRows, dataRows[1:]) if t[0]+1 != t[1]), [])
    iranges = dataRows[0:1] + ranges +dataRows[-1:]
    #print('iranges',iranges)
    ex2=[]
    for i in range(1,len(iranges),2):
        ex1=[]
        ex1.append(iranges[i-1])
        ex1.append(iranges[i])
        ex2.append(ex1)
    print('ex2=',ex2)
    ex3=[]
    for i in range(0,len(ex2)):
        ex1=ex2[i]
        if (ex1[-1]-ex1[0])>=55:
            ex3.append(ex1)
    print("ex3",ex3)
    if(len(ex3)>1):
        for i in range(0,len(ex3)):
            ex4=ex3[i]
            cv2.rectangle(img,(0,ex4[0]),(b[0],ex4[1]),(255,0,0),2)
            font =cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,'IMAGE'+str(i+1),(0,ex4[0]), font, 1,(255,0,0),1)
    elif len(ex3)==1:
        ex5=ex3[0]
        cv2.rectangle(img,(0,ex5[0]),(b[0],ex5[1]),(255,0,0),2)
        font =cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'IMAGE'+str(1),(0,ex5[0]), font, 1,(255,0,0),1)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
