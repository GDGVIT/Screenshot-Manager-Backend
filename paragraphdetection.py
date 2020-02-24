import cv2
def paragraphdetection(Min_Top_number,dd,a,headerrownumber,b,img,g):
    diff=[]
    allrowsnumber=[]
    for i in range(0,Min_Top_number):
        allrowsnumber.append(i)
    for i in range(1,Min_Top_number):
        f=dd[i]-dd[i-1]
        diff.append(abs(f))
    print("length of diff is",len(diff))
    print('diff is',diff)
    """
    Now we will create a dictionary that contains the line number as keys and the 
    difference in the number of rows to the next line as value.
    """
    keys=[x for x in range(1,len(a))]
    my_dict=dict(zip(keys, diff))
    print(my_dict)
    key_list = list(my_dict.keys()) 
    print("length of key list is",len(key_list))
    print("key list is",key_list)
    val_list = list(my_dict.values())
    print("val list is",val_list) 
    rows=[]
    for i in range(1,len(val_list)-1):
        if int(abs(val_list[i+1]-val_list[i]))<=5:
            rows.append(i+1)
            rows.append(i)
    rows=set(rows)#To elimate the Repeating Values
    headerrownumber=set(headerrownumber)
    # rows=set(rows)
    #headerrownumber=set(headerrownumber)
    rows=list(rows-headerrownumber)
    print("rows after deletion=",rows)
    ranges = sum((list(t) for t in zip(rows, rows[1:]) if t[0]+1 != t[1]), [])
    iranges = rows[0:1] + ranges + rows[-1:]
    print('iranges',iranges)
    ex2=[]
    for i in range(1,len(iranges),2):
        iranges[i]+=1
        rows.append(iranges[i])
        ex1=[]
        ex1.append(iranges[i-1])
        ex1.append(iranges[i])
        ex2.append(ex1)
    print("rows=",rows)
    print('iranges=',iranges)
    print('ex2=',ex2)
    Max_Height=g
    Min_Top=dd
    for i in range(0,len(ex2)):
        ex3=ex2[i]
        Min_Top1=int(Min_Top[ex3[0]])
        print(Min_Top1)
        Max_Height1=int(Min_Top[ex3[-1]])+int(Max_Height[ex3[-1]])
        if Max_Height1<=b[0]:
            Max_Height2=Max_Height1
            print(Max_Height2)
        x=int(b[1])
        print(x)
        cv2.rectangle(img,(0,Min_Top1),(x,Max_Height2),(0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'PARAGRAPH'+str(i+1),(0,Min_Top1), font, 1,(255,0,0),1)

    cv2.imshow('image',img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    list2=[]
    list2.append(rows)
    list2.append(key_list)
    return list2