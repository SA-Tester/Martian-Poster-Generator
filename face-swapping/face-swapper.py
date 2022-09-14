#Source Image: One we take the face 
#Destination Image: Where we put the image

import cv2
import dlib

img_source = cv2.imread("images/Matthew-McConaughey.jpg")
img_source_gray = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)

img_destination = cv2.imread("images/Niel-Armstrong.jpg")
img_destination_gray = cv2.cvtColor(img_destination, cv2.COLOR_BGR2GRAY)

#Loading Face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#Face 1: Source