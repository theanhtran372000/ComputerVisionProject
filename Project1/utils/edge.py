import cv2
import numpy as np

def edge_detector(image, thresh):
    canny_image = cv2.Canny(image, 70, 200)
    lines = cv2.HoughLines(canny_image, 1, np.pi/180, thresh)
    return lines
