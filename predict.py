import cv2
import easyocr
import re
import base64
import numpy as np


def predict(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
        if len(approx) == 4:
            location = approx
            break

    (x, y, w, h) = cv2.boundingRect(location)
    cropped_image = gray[y:y+h, x:x+w]

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    plate_text = ' '.join([res[1] for res in result])

    split_text = plate_text.split()
    if len(split_text) > 3:
         del split_text[3:6]  
    clean_plate_text = ' '.join(split_text).strip()

    return clean_plate_text

def predict64(image):
    base64Image = image
    base64Image = re.sub('^data:image/.+;base64,', '', base64Image)
    base64Image = base64Image.replace(' ', '+')
    base64Image = base64Image.encode()
    base64Image = base64.b64decode(base64Image)

    np_arr = np.frombuffer(base64Image, dtype=np.uint8)
    img = cv2.imdecode(np_arr, flags=cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
        if len(approx) == 4:
            location = approx
            break

    (x, y, w, h) = cv2.boundingRect(location)
    cropped_image = gray[y:y+h, x:x+w]

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    plate_text = ' '.join([res[1] for res in result])

    split_text = plate_text.split()
    if len(split_text) > 3:
            del split_text[3:6]
    clean_plate_text = ' '.join(split_text).strip()

    return clean_plate_text, base64Image