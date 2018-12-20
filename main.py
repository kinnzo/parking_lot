from imutils.video import VideoStream
from imutils.video import FPS
from numpy import genfromtxt
#from scipy import label
import imutils
import time
import cv2
import sys
import numpy as np

# Pretrained classes in the model
classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}


def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

mymap = genfromtxt("map.csv",delimiter=",")
#print(mymap[0][0],mymap[39][29])
# Loading model
model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                      'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
print("[INFO] Starting to read the image..")
in_name="image.jpeg"
out_name="image_box_text.jpeg"
if(len(sys.argv)>2):
    in_name = sys.argv[1]
    out_name = sys.argv[2]
image = cv2.imread(in_name)
image = cv2.resize(image,(640,480))
arr = np.zeros((40,30))

image_height, image_width, _ = image.shape

fps = FPS().start()

model.setInput(cv2.dnn.blobFromImage(image, size=(320, 240), swapRB=True))
output = model.forward()
# print(output[0,0,:,:].shape)
area = 0
num = 0
for detection in output[0, 0, :, :]:
    confidence = detection[2]
    if confidence > .4:
        class_id = detection[1]
        class_name=id_class_name(class_id,classNames)
        print(str(str(class_id) + " " + str(detection[2])  + " " + class_name))
        box_x = detection[3] * image_width
        box_y = detection[4] * image_height
        box_width = detection[5] * image_width
        box_height = detection[6] * image_height
        print(box_x,box_y,box_width,box_height)
        bx=int(box_x//16)
        by=int(box_y//16)
        bw=int(box_width//16)
        bh=int(box_height//16)
        area = area + (bw-bx)*(bh-by)
        num=num+1
        print(bx,by,bw,bh)
        for i in range(bx,bw):
            for j in range(by,bh):
                arr[i][j]=1
        cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
        cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))
        fps.update()

np.savetxt('procimg.csv',arr,delimiter=",")
arr1 = np.logical_xor(mymap,arr)
arr2 = np.logical_not(arr)
arr3 = np.logical_and(arr2,arr1)
np.savetxt('reslt.csv',arr3,delimiter=",")

fps.stop()
print("[INFO] Elapsed Time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx FPS: {:.2f}".format(fps.fps()))

ctr = 0
for i in range(40):
    for j in range(30):
        if arr3[i][j]==1:
            ctr = ctr + 1

eslots = ctr*num/(area)
print("[INFO] Number of empty slots: ",round(eslots))
#cv2.imshow('image', image)
cv2.imwrite(out_name,image)
#labeled_array, num_features=label(arr3)
#print("Number of available slots is:")
#print(num_features-1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.waitKey(1)
