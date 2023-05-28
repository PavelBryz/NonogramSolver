import cv2
import numpy as np

"""
Here I test how recognition works.
"""

#######   training part    ###############
samples = np.loadtxt('generalsamples.data', np.float32)
responses = np.loadtxt('generalresponses.data', np.float32)
responses = responses.reshape((responses.size, 1))

model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)
# model.train(samples, responses)

############################# testing part  #########################

im = cv2.imread('images/tp.png')
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
out = np.zeros(im.shape, np.uint8)
# gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

processed_contours = []

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) > 18:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if h > 15 and len([pc for pc in processed_contours if x + 5 > pc[0] > x - 5 and y + 5 > pc[1] > y - 5]) == 0:
            processed_contours.append((x, y))
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = thresh[y:y + h, x:x + w]
            roismall = cv2.resize(roi, (10, 10))
            roismall = roismall.reshape((1, 100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
            string = str(int((results[0][0])))
            cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))

cv2.imshow('im', im)
cv2.imshow('out', out)
cv2.waitKey(0)
