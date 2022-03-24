import cv2
import sys
import os
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import imutils

imagePath_face = "images\DG.jpeg"
imagePath_sign = "images\DG_sign.jpeg"

image_face = cv2.imread(imagePath_face)
image_sign = cv2.imread(imagePath_sign)

class Helper():
    def __init__(self):
        pass
    
    def find_face(self,imagePath_face):
        image = cv2.imread(imagePath_face)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=3,
                minSize=(30, 30)
        ) 
        print("Found {0} Faces!".format(len(faces)))
        if len(faces)==0 or len(faces)>1:
            return False
        if len(faces)==1:
            return True

    def detect_sign(self,image):
        orig = image.copy()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(5,5),0)
        plt.imshow(gray,'gray')
        edged = cv2.Canny(gray,80,200)
        plt.imshow(edged,'gray')
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key= cv2.contourArea, reverse=True)[:1]
        for c in cnts:
            peri = cv2.arcLength(c,True)
            apprx = cv2.approxPolyDP(c, 0.2*peri, True)
            x,y,w,h = cv2.boundingRect(apprx)
            cv2.rectangle(orig,(x,y),(x+w,y+h),(255,0,0),2)
            #print(c)
        plt.imshow(orig)

    def convert_sign(self,image):
        lower = np.array([90, 38, 0])
        upper = np.array([145, 255, 255])
        mask = cv2.inRange(image, lower, upper)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        
        boxes = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            boxes.append([x,y, x+w,y+h])

        boxes = np.asarray(boxes)
        left = np.min(boxes[:,0])
        top = np.min(boxes[:,1])
        right = np.max(boxes[:,2])
        bottom = np.max(boxes[:,3])
        plt.imshow(mask)

    def sign_extract(self):
                
        import cv2
        import matplotlib.pyplot as plt
        from skimage import measure, morphology
        from skimage.color import label2rgb
        from skimage.measure import regionprops
        import numpy as np

        # the parameters are used to remove small size connected pixels outliar 
        constant_parameter_1 = 84
        constant_parameter_2 = 250
        constant_parameter_3 = 100

        # the parameter is used to remove big size connected pixels outliar
        constant_parameter_4 = 18

        # read the input image
        img = cv2.imread('./images/DG_sign.jpeg', 0)
        img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary

        # connected component analysis by scikit-learn framework
        blobs = img > img.mean()
        blobs_labels = measure.label(blobs, background=1)
        image_label_overlay = label2rgb(blobs_labels, image=img)

        fig, ax = plt.subplots(figsize=(10, 6))

        '''
        # plot the connected components (for debugging)
        ax.imshow(image_label_overlay)
        ax.set_axis_off()
        plt.tight_layout()
        plt.show()
        '''

        the_biggest_component = 0
        total_area = 0
        counter = 0
        average = 0.0
        for region in regionprops(blobs_labels):
            if (region.area > 10):
                total_area = total_area + region.area
                counter = counter + 1
            # print region.area # (for debugging)
            # take regions with large enough areas
            if (region.area >= 250):
                if (region.area > the_biggest_component):
                    the_biggest_component = region.area

        average = (total_area/counter)
        print("the_biggest_component: " + str(the_biggest_component))
        print("average: " + str(average))

        # experimental-based ratio calculation, modify it for your cases
        # a4_small_size_outliar_constant is used as a threshold value to remove connected outliar connected pixels
        # are smaller than a4_small_size_outliar_constant for A4 size scanned documents
        a4_small_size_outliar_constant = ((average/constant_parameter_1)*constant_parameter_2)+constant_parameter_3
        print("a4_small_size_outliar_constant: " + str(a4_small_size_outliar_constant))

        # experimental-based ratio calculation, modify it for your cases
        # a4_big_size_outliar_constant is used as a threshold value to remove outliar connected pixels
        # are bigger than a4_big_size_outliar_constant for A4 size scanned documents
        a4_big_size_outliar_constant = a4_small_size_outliar_constant*constant_parameter_4
        print("a4_big_size_outliar_constant: " + str(a4_big_size_outliar_constant))

        # remove the connected pixels are smaller than a4_small_size_outliar_constant
        pre_version = morphology.remove_small_objects(blobs_labels, a4_small_size_outliar_constant)
        # remove the connected pixels are bigger than threshold a4_big_size_outliar_constant 
        # to get rid of undesired connected pixels such as table headers and etc.
        component_sizes = np.bincount(pre_version.ravel())
        too_small = component_sizes > (a4_big_size_outliar_constant)
        too_small_mask = too_small[pre_version]
        pre_version[too_small_mask] = 0
        # save the the pre-version which is the image is labelled with colors
        # as considering connected components
        plt.imsave('pre_version.png', pre_version)

        # read the pre-version
        img = cv2.imread('pre_version.png', 0)
        # ensure binary
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # save the the result
        cv2.imwrite("output.png", img)

    def download_img(self,url):
        urllib.request.urlretrieve(url,"./images/temp.jpg")
        

models = Helper()
url = "https://firebasestorage.googleapis.com/v0/b/dsc-club-management-app.appspot.com/o/Yash%20Srivastava.jpg?alt=media&token=1c80a8cf-25c5-4b52-8902-08f7596a8f01"
models.download_img(url)
models.find_face("./images/temp.jpg")
#models.convert_sign(image_sign)
models.sign_extract()