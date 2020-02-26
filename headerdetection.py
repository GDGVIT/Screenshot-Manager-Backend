import cv2

def headerdetection(max_height_list,lowerlimit,upperlimit,min_top_list,image_shape,img):
    
    #for classifying some part of the image as header we had defined upper limit and lower limit
    #if the i th row's height falls in between this range(by checking with help of max_height_list)
    #we append it to headerrownumber list
    headerrownumber=[]

    for i in range(0,len(max_height_list)):
        if(max_height_list[i]>=lowerlimit and max_height_list[i]<=upperlimit):
            headerrownumber.append(i)

    if len(headerrownumber)!=1:
            #we have defined below condition because the header rows number should be continuous.
            if(headerrownumber[1]-headerrownumber[0]!=1):
                t=headerrownumber[0]
                headerrownumber=[]
                headerrownumber.append(t)

    if(len(headerrownumber)==1):
        maxheight1=max_height_list[headerrownumber[0]]
        MinTop1=int(min_top_list[headerrownumber[0]])
        height1=int(maxheight1)+int(MinTop1)
        width=int(image_shape[1])
        cv2.rectangle(img,(0,MinTop1),(width,height1),(0,255,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'HEADER'+str(1),(0,MinTop1), font, 1,(255,0,0),1)

    else:
        MinTop1=int(min_top_list[headerrownumber[0]])
        MaxTop1=int(min_top_list[headerrownumber[-1]])
        maxheight=MaxTop1+int(max_height_list[headerrownumber[-1]])
        width=int(image_shape[1])
        cv2.rectangle(img,(0,MinTop1),(width,maxheight),(0,255,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'HEADER'+str(1),(0,MinTop1), font, 1,(255,0,0),1)
    
    # UNCOMMENT FOR DEBUGGING
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return headerrownumber
