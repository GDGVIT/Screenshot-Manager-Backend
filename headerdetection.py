import cv2
def headerdetection(g,lowerlimit,upperlimit,dd,b,img):
    headerrownumber=[]
    for i in range(0,len(g)):
        if(g[i]>=lowerlimit and g[i]<=upperlimit):
            headerrownumber.append(i)
    if len(headerrownumber)!=1:
            if(headerrownumber[1]-headerrownumber[0]!=1):
                t=headerrownumber[0]
                headerrownumber=[]
                headerrownumber.append(t)
    if(len(headerrownumber)==1):
        maxheight1=g[headerrownumber[0]]
        MinTop1=int(dd[headerrownumber[0]])
        height1=int(maxheight1)+int(MinTop1)
        x=int(b[1])
        cv2.rectangle(img,(0,MinTop1),(x,height1),(0,255,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'HEADER'+str(1),(0,MinTop1), font, 1,(255,0,0),1)

    else:
        MinTop1=int(dd[headerrownumber[0]])
        MaxTop1=int(dd[headerrownumber[-1]])
        maxheight=MaxTop1+int(g[headerrownumber[-1]])
        x=int(b[1])
        cv2.rectangle(img,(0,MinTop1),(x,maxheight),(0,255,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'HEADER'+str(1),(0,MinTop1), font, 1,(255,0,0),1)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return headerrownumber