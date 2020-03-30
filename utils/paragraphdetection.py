import cv2

def paragraphdetection(min_top_number,min_top_list,each_line_info,headerrownumber,image_shape,img,max_height_list):
    
    diff=[]
    allrowsnumber=[]
    paragraph_coordinates=[]
    for i in range(0,min_top_number):
        allrowsnumber.append(i)

    for i in range(1,min_top_number):
        f=min_top_list[i]-min_top_list[i-1]
        diff.append(abs(f))
    #print("length of diff is",len(diff))
    #print('diff is',diff)

    """
    Now we will create a dictionary my_dict that contains the line number as keys and the 
    difference in the number of rows to the next line as value.
    """

    keys=[x for x in range(1,len(each_line_info))]
    my_dict=dict(zip(keys, diff))
    #print("mydict",my_dict)
    key_list = list(my_dict.keys()) 
    #print("length of key list is",len(key_list))
    #print("key list is",key_list)
    val_list = list(my_dict.values())
    #print("val list is",val_list) 
    
    #para_rows contains the row number around which paragraphs has to be drawn 
    para_rows=[]

    for i in range(1,len(val_list)-1):
        #if the difference between heights of two consecutive rows is less than equal to 5
        #5 is a generalized value(have used after passing through a number of test cases)
        if int(abs(val_list[i+1]-val_list[i]))<=5:
            para_rows.append(i+1)
            para_rows.append(i)

    #To elimate the Repeating Values we have converted to sets
    para_rows=set(para_rows)
    headerrownumber=set(headerrownumber)
    
    #We are subtracting header rows number from the para_rows list because if a header is of more than 
    #2 lines so this algorithm will classify this header also as paragraph so inorder to avoid this 
    #we need to subtract these rows number from the para_rows list.
    
    para_rows=list(para_rows-headerrownumber)
    #print("para rows after deletion=",para_rows)
    ranges = sum((list(t) for t in zip(para_rows, para_rows[1:]) if t[0]+1 != t[1]), [])
    iranges = para_rows[0:1] + ranges + para_rows[-1:]
    #print('iranges',iranges)
    #ex2 contains the starting row number and the ending row number of a block classified as paragraph.

    ex2=[]

    for i in range(1,len(iranges),2):
        iranges[i]+=1
        para_rows.append(iranges[i])
        ex1=[]
        ex1.append(iranges[i-1])
        ex1.append(iranges[i])
        ex2.append(ex1)
    #print("rows=",rows)
    #print('iranges=',iranges)
    #print('ex2=',ex2)

    for i in range(0,len(ex2)):
        each_paragraph_coordinates=[]
        ex3=ex2[i]
        #Min_Top 1 is the row number of the first letter of the line containg text
        min_top1=int(min_top_list[ex3[0]])
        #print(min_top1)
        max_height1=int(min_top_list[ex3[-1]])+int(max_height_list[ex3[-1]])
        if max_height1<=image_shape[0]:
            max_height2=max_height1
            #print(max_height2)
        width=int(image_shape[1])
        #print(x)
        cv2.rectangle(img,(0,min_top1),(width,max_height2),(0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'PARAGRAPH'+str(i+1),(0,min_top1), font, 1,(255,0,0),1)
        each_paragraph_coordinates.append((0,min_top1))
        each_paragraph_coordinates.append((width,max_height2))
        paragraph_coordinates.append(each_paragraph_coordinates)
    
    #UNCOMMENT FOR DEBUGGING
    # cv2.imshow('image',img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    list2=[]
    list2.append(para_rows)
    list2.append(key_list)

    return [list2,paragraph_coordinates]