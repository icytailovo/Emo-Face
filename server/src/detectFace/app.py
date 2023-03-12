import cv2
import sys
import numpy as np
from PIL import Image

imagePath = sys.argv[1]

# convert to rgba
image = Image.open(imagePath)
image.convert("RGBA").save('image.png')

image = cv2.imread("image.png", -1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

alpha = 0.0
beta = 1 - alpha
gamma = 0.0

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
) 

print("Found {0} Faces!".format(len(faces)))

for (x, y, w, h) in faces:
    sub_img = image[y:y+h, x:x+w]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0

    res = cv2.addWeighted(sub_img, alpha, white_rect, beta, gamma)

    # Putting the image back to its position
    image[y:y+h, x:x+w] = res

# resize to square image
size = min(int(image.shape[1]), int(image.shape[0]))
dim = (size, size)

resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
print('Resized Dimensions : ',resized.shape)

status = cv2.imwrite('faces_resized.png', resized)
print ("Image faces_resized.jpg written to filesystem: ",status)



