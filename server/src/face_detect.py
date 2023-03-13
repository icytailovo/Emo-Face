import cv2
import sys
import numpy as np
from PIL import Image

from image_utils import Rotation


def detect_face(image_path, rotation):
    '''
    detect the boundary boxes of human faces in the input image and saves the output to 'masked.png';
    the saved output will contain a resized version of the original image with the human faces boxed out
    and made transparent.
    
    returns the path of the saved image
    '''
    
    # the image must be stored in rgba format
    image = cv2.imread(image_path, -1)
    
    # need to mannually rotate the image h as cv2 doesn't read the EXIF info
    print(rotation, Rotation.ROTATE_90)
    if rotation == Rotation.HORIZONTAL.value:
        pass
    elif rotation == Rotation.MIRROR_HORIZONTAL.value:
        image = cv2.flip(image, 1)
    elif rotation == Rotation.ROTATE_180.value:
        image = cv2.rotate(image, cv2.ROTATE_180)
    elif rotation == Rotation.MIRROR_VERTICAL.value:
        image = cv2.flip(image, 0)
    elif rotation == Rotation.MIRROR_AND_ROTATE_270.value:
        image = cv2.flip(image, 1)
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rotation == Rotation.ROTATE_90.value:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif rotation == Rotation.MIRROR_AND_ROTATE_90.value:
        image = cv2.flip(image, 1)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif rotation == Rotation.ROTATE_270.value:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        raise Exception("unrecognized rotation code")
        
    cv2.imwrite("tmp/received.png", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    alpha = 0.0
    beta = 1 - alpha
    gamma = 0.0

    # __________ detecting faces through eigenfaces _________
    # faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # faces = faceCascade.detectMultiScale(
    #         gray,
    #         scaleFactor=1.3,
    #         minNeighbors=3,
    #         minSize=(30, 30)
    # ) 
    
    
    # __________ detecting faces through finetuned resnet _________
    ## [initialize_FaceDetectorYN]
    image1 = cv2.imread(image_path)
    detector = cv2.FaceDetectorYN.create(
        "face_detection_yunet_2022mar.onnx",    # face detection model
        "",
        (320, 320),
        0.9,                                    # score threshold, filtering out faces of score < score_threshold.
        0.3,                                    # nms threshold, suppress bounding boxes of iou >= nms_threshold
        5000                                    # top k
    )
    
    detector.setInputSize((image1.shape[1], image1.shape[0]))
    faces = detector.detect(image1)
    
    if faces:
        print("Found {0} Faces!".format(len(faces)))
        for idx, face in enumerate(faces[1]):
            print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))
            x = int(face[0])
            y = int(face[1])
            w = int(face[2])
            h = int(face[3])
            
            sub_img = image[y:y+h, x:x+w]
            white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0

            res = cv2.addWeighted(sub_img, alpha, white_rect, beta, gamma)

            # Putting the image back to its position
            image[y:y+h, x:x+w] = res

    

    # for (x, y, w, h) in faces:
    #     sub_img = image[y:y+h, x:x+w]
    #     white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0

    #     res = cv2.addWeighted(sub_img, alpha, white_rect, beta, gamma)

    #     # Putting the image back to its position
    #     image[y:y+h, x:x+w] = res

    cv2.imwrite("tmp/before_resize.png", image)
    # resize to square image
    size = min(int(image.shape[1]), int(image.shape[0]))
    size = min(size, 512)
    dim = (size, size)

    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    print('Resized Dimensions : ',resized.shape)

    output_path = 'tmp/masked.png'
    status = cv2.imwrite(output_path, resized)
    print("Image masked.png written to filesystem: ",status)

    return output_path


