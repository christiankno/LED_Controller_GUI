import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
from itertools import chain
from functions import *
from skimage import io


mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

while 0:
    imgsct = sct.grab(mon)

    img=np.array(imgsct.pixels)
    average=img.mean(axis=0).mean(axis=0)

    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    rgb=[int(i)<<4 for i in dominant]

    print(rgb)
    send(rgb)

    #time.sleep(0.5)

    #img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    #cv2.imshow('test', np.array(img))
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    #    cv2.destroyAllWindows()
    #    break