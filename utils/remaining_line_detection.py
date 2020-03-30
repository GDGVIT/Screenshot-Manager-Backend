import cv2
def line_detection(key_list,headerrownumber,rows,dd,g,img,b):
    for i in range(0,len(key_list)):
        key_list[i]-=1
    #print("key_list",key_list)
    # print("rows",rows)
    # print("headerrownumber",headerrownumber)
    key_list=set(key_list)
    rows=set(rows)
    headerrownumber=set(headerrownumber)

    #Lines list will be storing the lines which have not been accessing yet i.e the lines which 
    # have not been included in neither header nor paragraph
    lines=key_list-rows
    lines=list(lines-headerrownumber)
    lines.sort()
    print("lines number are",lines)

    #In order to draw a rectangle we need the top left index and the maximum height so that we can
    #get the corner right point.

    for i in range(0,len(lines)):
        left1=int(dd[int(lines[i])])
        height1=int(g[int(lines[i])])
        total_height1=left1+height1
        cv2.rectangle(img,(0,left1),(b[1],total_height1),(0,0,0),1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Line'+str(i+1),(0,left1), font, 1,(255,100,127),1)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
