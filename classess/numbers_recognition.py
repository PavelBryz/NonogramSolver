from enum import Enum
import cv2
import numpy as np
from PIL.Image import Image

from classess.scenarios import HardLevelScenario, MediumLevelScenario, BasicLevelScenario

# Load the training data for number recognition
samples = np.loadtxt('generalsamples.data', np.float32)
responses = np.loadtxt('generalresponses.data', np.float32)
responses = responses.reshape((responses.size, 1))

# Create a K-Nearest Neighbors model and train it with the data
model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)

def recognize_numbers(image: Image, size_of_number: int) -> list[tuple[int, int, int]: int]:
    # Convert the image to a numpy array
    im = np.array(image)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

    processed_contours = []
    fouded_numbers = []

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 18:
            [x, y, w, h] = cv2.boundingRect(cnt)
            # Check if the contour represents a number
            if h > size_of_number and len(
                    [pc for pc in processed_contours if x + 5 > pc[0] > x - 5 and y + 5 > pc[1] > y - 5]) == 0:
                processed_contours.append((x, y))
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                # Use the trained model to recognize the number
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                fouded_numbers.append([(x, y, x+w), int((results[0][0]))])
    return fouded_numbers

class Scenarios(Enum):
    # Define different scenarios and their corresponding image files and scenario classes
    HARD = ('images\hard.png', HardLevelScenario())
    MEDIUM = ('images\medium.png', MediumLevelScenario())
    EASY = ('images\easy.png', MediumLevelScenario())
    BASIC = ('images\\basic.png', BasicLevelScenario())

def get_scenario(image: Image):
    # Convert the image to a numpy array
    img_rgb = np.array(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    scenarios = [Scenarios.HARD, Scenarios.MEDIUM, Scenarios.EASY, Scenarios.BASIC]

    for sc in scenarios:
        # Load the template image for each scenario and convert it to grayscale
        template = cv2.imread(sc.value[0])
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Perform template matching to check if the scenario image matches the template
        res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            return sc.value[1]

    return None
