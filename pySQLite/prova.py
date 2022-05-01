from ast import In
import math
import time
import cv2
import numpy as np
import cvlib as cv
import matplotlib.pyplot as plt
from cvlib.object_detection import draw_bbox

thres = 0.5
nms_threshold = 0.2


def take_photo(In):
    cap = cv2.VideoCapture(In)
    ret, frame = cap.read()
    (grabbed, frame) = cap.read()
    time.sleep(0.3)  # Wait 300 miliseconds
    image = '.\capture' + str(In) + '.png'
    cv2.imwrite(image, frame)
    cap.release()
    return image


def count(path):
    img = cv2.imread(path)
    classNames = []
    classFile = 'coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    ### rilevazione nei due modi ###
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    box, label, count = cv.detect_common_objects(img)

    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)

    Nperson = 0
    for i in indices:
        Nperson += 1
        # box = bbox[i]
        # x,y,w,h = box[0],box[1],box[2],box[3]
        # cv2.rectangle(img, (x,y),(x+w,h+y), color=(0, 255, 0), thickness=2)
        # cv2.putText(img,classNames[classIds[i][0]-1].upper(),(box[0]+10,box[1]+30),
        # cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    persone = 0
    for obj in label:
        if (obj == 'person'):
            persone += 1

    ### disegna il rettangolo con il nome dell'oggeto ###
    # out = draw_bbox(img, box, label, count)
    # out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(10, 10))
    # plt.axis("off")
    # plt.imshow(out)
    # plt.show()

    per = math.floor(((Nperson + persone) / 2))
    return per