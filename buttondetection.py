import cv2
import numpy as np

def buttondetection(image,img):
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
        
        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
        
        # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha

        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
        (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # Find contours for image, which will detect all the boxes
        #im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort all the contours by top to bottom.
        (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
        idx = 0

        #print("Total Identified: ",len(contours))
        #list1=[]#for storing the x,y,width,height.

        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            
            # If the box height is greater then 20, widht is >80, then only save it as a box image in folder.
            # IMPORTANT ASSUMPTION about how button looks
            if (w > 80 and h > 20 and x!=0 and y!=0) and w > 2.0*h:
                #If x,y,w,h satisfy the above conditions append it into points
                points=[]
                points.append(x)
                points.append(y)
                points.append(w)
                points.append(h)
                idx += 1
                #print("Matches rules on H & W",x,y,w,h)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                total_points.append(points)

    total_points=[]#for storing the x,y,width,height.It is neccessary to store these values as it will be
            #required for drawing rectangles around buttons
    box_extraction(image, "./")

    for i in range(0,len(total_points)):
        list2=total_points[i]
        cv2.rectangle(img,(list2[0],list2[1]),(list2[0]+list2[2],list2[1]+list2[3]),(0,255,0),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'BUTTON'+str(i+1),(list2[0],list2[1]), font, 1,(255,0,0),1)
        
    # UNCOMMENT FOR DEBUGGING
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
