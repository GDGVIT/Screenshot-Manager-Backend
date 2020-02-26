from api import *
import json
import cv2
test_file = ocr_space_file(filename='screenshot20.png', language='pol')
d=json.loads(test_file)
a=d["ParsedResults"][0]['TextOverlay']['Lines']
heights=[]
limit=[]
for i in range(0,len(a)):
    heights.append(a[i]['MaxHeight'])
upperlimit=int(heights[0]+4.0)
lowerlimit=int(heights[3]-2.0)
limit.append(lowerlimit)
limit.append(upperlimit)
sublimit=[]
subheadingul=int(heights[3]-3.0)
subheadingll=int(heights[5]-4)
sublimit.append(subheadingul)
sublimit.append(subheadingll)

print("upper limit and lower limit for heading is",upperlimit,lowerlimit)
#print("upper limit and lower limit for subheading is",subheadingul,subheadingll)

headers=['Header1','Header2','Header3','Header4','Header5','Header6']
dictionary=dict(zip(headers,heights))
print(dictionary)
test_file = ocr_space_file(filename='screenshot2.jpeg', language='pol')
d=json.loads(test_file)
img=cv2.imread('screenshot2.jpeg',1)
b=img.shape
print(b)

a=d["ParsedResults"][0]['TextOverlay']['Lines']
#print(a)
print(len(a))
dd=[]#Min Top List
g=[]#Max Height List
left=[]#Left list
for i in range(len(a)):
    print(a[i])
    q=[]#a list that stores the 'MaxHeight' and 'MinTop'
    left.append(a[i]['Words'][0]['Left'])
    q.append(a[i]['MinTop'])
    dd.append(a[i]['MinTop'])
    q.append(a[i]['MaxHeight'])
    g.append(a[i]['MaxHeight'])
    #cv2.rectangle(img,(0,int(q[0])),(int(b[1]),int(q[0]+q[1])),(0,255,0))
    print(i)
    #print(q)
    #print(q[0]+q[1])
print("MaxHeight List=",g)
print("MinTop=",dd)
print("Left list",left)  
Min_Top_number=len(dd)
print(Min_Top_number)
print("The total number of rows in the image is",len(a))
#HEADER BUILDING
headerrownumber=[]
for i in range(0,len(g)):
    if(g[i]>=lowerlimit and g[i]<=upperlimit):
        headerrownumber.append(i)
print("header row number is",headerrownumber)
if len(headerrownumber)!=1:
    for i in range(0,1):
        if(headerrownumber[i+1]-headerrownumber[i]!=1):
            t=headerrownumber[i]
            headerrownumber=[]
            headerrownumber.append(t)

        
print("header row number is",headerrownumber)
if(len(headerrownumber)==1):
    maxheight1=g[headerrownumber[0]]
    MinTop1=int(dd[headerrownumber[0]])
    print("MinTop1",MinTop1)
    height1=int(maxheight1)+int(MinTop1)
    print("maxheight1",maxheight1)
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

# for i in range(0,len(headerrownumber)):
#     headerrownumber[i]+=1
# print("Updated value of headerrownumber",headerrownumber)

#PARAGRAPH BUILDING
diff=[]
allrowsnumber=[]
for i in range(0,Min_Top_number):
    allrowsnumber.append(i)
for i in range(1,Min_Top_number):
    f=dd[i]-dd[i-1]
    diff.append(abs(f))
print("length of diff is",len(diff))
print('diff is',diff)
#Now we will create a dictionary that contains the line number as keys and the 
#difference in the number of rows to the next line as value.
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
rows=set(rows)
rows=list(rows)
print("1st time rows is ",rows)
print(rows)
rows.sort()
print("rows number",rows)
rows=set(rows)
headerrownumber=set(headerrownumber)
rows=list(rows-headerrownumber)
print("rows after deletion=",rows)
ranges = sum((list(t) for t in zip(rows, rows[1:]) if t[0]+1 != t[1]), [])
iranges = rows[0:1] + ranges + rows[-1:]
print('iranges',iranges)
w=iranges[-1]
ex2=[]
for i in range(1,len(iranges),2):
    iranges[i]+=1
    rows.append(iranges[i])
    ex1=[]
    ex1.append(iranges[i-1])
    ex1.append(iranges[i])
    ex2.append(ex1)
rows=set(rows)
rows=list(rows)
print("rows=",rows)
print('iranges=',iranges)
print('ex2=',ex2)
Max_Height=g
Min_Top=dd
# ht=dict(zip(Max_Height,Min_Top))
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

#BOX DETECTION
import cv2
import numpy as np


def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0       
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    
    # For DEBUG, uncomment below
    #cv2.imwrite("Image_bin.jpg",img_bin)
   
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//40
     
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    
    # For DEBUG, uncomment below
    #cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    
    # For DEBUG, uncomment below
    #cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
    
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    #cv2.imwrite("img_final_bin.jpg",img_final_bin)
    
    
    # Find contours for image, which will detect all the boxes
    #im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    idx = 0
    print("Total Identified: ",len(contours))
    #list1=[]#for storing the x,y,width,height.
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
        
        # If the box height is greater then 20, widht is >80, then only save it as a box image in folder.
        # IMPORTANT ASSUMPTION about how button looks
        if (w > 80 and h > 20 and x!=0 and y!=0) and w > 2.0*h:
            list2=[]
            list2.append(x)
            list2.append(y)
            list2.append(w)
            list2.append(h)
            idx += 1
            new_img = img[y:y+h, x:x+w]
            cv2.imwrite(str(idx) + '.png', new_img)
            print("Matches rules on H & W",x,y,w,h)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            list1.append(list2)
          
list1=[]#for storing the x,y,width,height.
box_extraction("screenshot2.jpeg", "./")
for i in range(0,len(list1)):
    list2=list1[i]
    cv2.rectangle(img,(list2[0],list2[1]),(list2[0]+list2[2],list2[1]+list2[3]),(0,255,0),2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'BUTTON'+str(i+1),(list2[0],list2[1]), font, 1,(255,0,0),1)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#For making lines
for i in range(0,len(key_list)):
    key_list[i]-=1
print("key_list",key_list)
key_list=set(key_list)
rows=list(rows)
print("rows",rows)
print("headerrownumber",headerrownumber)
rows=set(rows)
headerrownumber=set(headerrownumber)
lines=key_list-rows
lines=list(lines-headerrownumber)
lines.sort()
print("lines number are",lines)
for i in range(0,len(lines)):
    lines[i]=lines[i]-1
for i in range(0,len(lines)):
    left1=int(dd[int(lines[i])+1])
    height1=int(g[int(lines[i])+1])
    total_height1=left1+height1
    cv2.rectangle(img,(0,left1),(b[1],total_height1),(0,0,0),1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Line'+str(i+1),(0,left1), font, 1,(255,100,127),1)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
