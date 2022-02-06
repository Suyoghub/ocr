import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract

#global constats 
IMAGE_HEIGHT = 720
IMAGE_WIDTH = 720

# cap = cv2.VideoCapture("./../sample_pics/video1.mp4")
# cap = cv2.VideoCapture("http://192.168.120.112:8080/")
# cap = cv2.VideoCapture("rtsp://192.168.120.112:8080/h264_ulaw.sdp")

# def get_paper_boundaries() -> np.array:
#     '''
#     This function takes the input frame and then determines the border of th paper. 

#     Input parameters: 
#         None
    
#     return np array of the cropped image.
#     '''

#     # Getting the base image from source
#     _, base_image = cap.read()

#     #TODO: REMOVE LATER: ADDED FOR STATIC FILES TEST! 
#     # base_image = cv2.imread("./../sample_pics/1.jpg")

#     #resizing the image to a specified size
#     resized_image = cv2.resize(base_image,(IMAGE_HEIGHT,IMAGE_WIDTH))

#     #converting to hsv color space to detect white color 
#     hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

#     # specifying the mask; the hsv values for lower limt and upper limit were figured using a script
#     mask = cv2.inRange(hsv_image,(0,0,100),(179,30,255))

#     # bitwise and operation using the mask
#     result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

#     #converting the obtained image back to RGB color scheme
#     result_rgb = cv2.cvtColor(result,cv2.COLOR_HSV2BGR)
#     result_gray = cv2.cvtColor(result_rgb,cv2.COLOR_BGR2GRAY)

#     #Image thresholding (Otsu, binary etc)
#     #Image dilation and erosion
#     #Find contours only on thresholded/binarized image

#     # finding the contours of the image after applying the mask
#     contours, _ = cv2.findContours(result_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#     #comparint the area of each contour because only the largest one is the Paper which has an area of ~200k
#     for each_contour in contours:
#         if cv2.contourArea(each_contour) > 100000:
#             # print(cv2.contourArea(each_contour))
#             (x,y,w,h) = cv2.boundingRect(each_contour)
#             cv2.rectangle(resized_image,(x,y),(x+w,y+h),(0,255,0),2)
    
#     return resized_image


def get_paper(image,edges):
    cropped_image  = four_point_transform(image, edges.reshape(4, 2))
    return cropped_image


while True:
    # _, base_image = cap.read()
    # base_image  = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)

    #color incase of RGB
    base_image = cv2.imread("./../sample_pics/1.jpg")
    resized_image = cv2.resize(base_image,(IMAGE_HEIGHT,IMAGE_WIDTH))

    #using simple image threshold
    # _, threshold_segmented_image = cv2.threshold(resized_image,127,255,cv2.THRESH_BINARY_INV)

    #using adaptive threshold 
    # threshold_segmented_image_adaptive_c = cv2.adaptiveThreshold(resized_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # threshold_segmented_image_gussian = cv2.adaptirveThreshold(resized_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,157,20)
    
    # roi1 = threshold_segmented_image_gussian[651:677,60:220]
    # cv2.imshow("Resized Image",resized_image)
    # cv2.imshow("Segmented Image Using Threshold",threshold_segmented_image)
    # cv2.imshow("Segmented Image Using Adaptive Thres Mean C",threshold_segmented_image_adaptive_c)
    # cv2.imshow("Segmented Image Using Adaptive Thres Gaussian",threshold_segmented_image_gussian)

    #finding countours 
    # contours, hierarchy = cv2.findContours(threshold_segmented_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(threshold_segmented_image, contours, -1, (0,255,0), 1)

    # contours, hierarchy = cv2.findContours(threshold_segmented_image_gussian, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(resized_image, contours, -1, (0,255,0), 1)

    # for contour in contours:
    #     (x,y,w,h) = cv2.boundingRect(contour)
    #     cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0,255,0), 2)
    #     break

    # print(f"No of Contours Detected: {len(contours)}")
    # adding median blur to remove salt and pepper noise
    # img_median = cv2.medianBlur(threshold_segmented_image, 5) 
    # contours, _ = cv2.findContours(img_median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print(f"No of Contours Detected: {len(contours)}")

    # for each_contour in contours:
    #     if cv2.contourArea(each_contour) > 2000:
    #         (x,y,w,h) = cv2.boundingRect(each_contour)
    #         cv2.rectangle(resized_image,(x,y),(x+w,y+h),(0,255,0),3)

    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image,(0,0,100),(179,30,255))
    result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    result_rgb = cv2.cvtColor(result,cv2.COLOR_HSV2BGR)
    result_gray = cv2.cvtColor(result_rgb,cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(result_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print(f"No of Contours Detected: {len(contours)}")

    #loop to get cropped image from the detected paper
    for each_contour in contours:
        if cv2.contourArea(each_contour) > 100000:
            # print(cv2.contourArea(each_contour))
            perimeter = cv2.arcLength(each_contour, True)
            approximate = cv2.approxPolyDP(each_contour, 0.02 * perimeter, True)

            if len(approximate) == 4:
                paper_boundaries = approximate
                (x,y,w,h) = cv2.boundingRect(each_contour)
                cv2.rectangle(resized_image,(x,y),(x+w,y+h),(0,255,0),2)
                x = get_paper(resized_image,paper_boundaries)
                name = x[90:135,20:200]
                name = cv2.cvtColor(name, cv2.COLOR_BGR2GRAY)

                ret3,th3 = cv2.threshold(name,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


                cv2.imshow("x",x)
                cv2.imshow("unsharpened",th3)
                print(pytesseract.image_to_string(x))
                cv2.imshow("y",resized_image)
                break
        
    # cropped_image  = four_point_transform(resized_image, paper_boundaries.reshape(4, 2))
    # cv2.imshow("as",cropped_image)
    # cv2.imshow("img.jpg",resized_image)
    
    # compare = np.concatenate((resized_image,cropped_image), axis=1)
    # cv2.imshow("Original-Resized",resized_image)
    # cv2.imshow("Gaussian Threshold",threshold_segmented_image_gussian)
    
    # cv2.imshow("Comparision",compare)
    # cv2.imshow("ROi",roi1)

    # e = get_paper_boundaries()
    # cv2.imshow("Paper Detection",e)

    # cv2.imwrite("regular_vs_mean_c_text.jpg",compare)
    # cv2.imwrite("roi_regular_vs_mean_c_text.jpg",roi1)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# cap.release()
cv2.destroyAllWindows()




