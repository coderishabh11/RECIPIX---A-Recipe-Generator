import os
import cv2
import random
import imutils
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet import preprocess_input

from config import MODEL, CLASSES
from config import MIN_CONFIDENCE, WIDTH, PYR_SCALE, WIN_STEP, INPUT_SIZE

def sliding_window(image, step, ws):
    # slide a window across the image
    for y in range(0, image.shape[0] - ws[1], step):
        for x in range(0, image.shape[1] - ws[0], step):
            # yield the current window
            yield (x, y, image[y:y + ws[1], x: x + ws[0]])

def image_pyramid(image, scale=1.5, min_size=(224, 224)):
    # yield the original image
    yield image

    # keep looping over the image pyramid
    while True:
        # compute the dimensions of the next image in the pyramid
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)

        # if the resized image does not meet the supplied minimum size, then stop constructing the pyramid
        if image.shape[0] < min_size[1] or image.shape[1] < min_size[0]:
            break

        # yield the next image in the pyramid
        yield image

def detect_vegetables(img_path):
    # Load your model
    vegetable_model = load_model(MODEL)

    # Load the image
    orig = cv2.imread(img_path)

    # Class Names
    class_names = CLASSES

    # initialize the image pyramid
    pyramid = image_pyramid(orig, scale=PYR_SCALE, min_size=INPUT_SIZE)

    # initialize two lists, one to hold the ROIs generated from the image pyramid and sliding window,
    # and another list used to store the (x,y)-coordinate of where the ROI was in the original image
    rois = []
    locs = []

    # loop over the image pyramid
    for image in pyramid:
        # for each layer of the image pyramid, loop over the sliding window locations
        for (x, y, roi_orig) in sliding_window(image, WIN_STEP, INPUT_SIZE):
            # randomly change the size of the bounding box within a specified range
            # roi_size = (
            #     random.randint(100, 200),  # random width between 100 and 200 pixels
            #     random.randint(100, 200),  # random height between 75 and 150 pixels
            # )
            roi_size = (150,150)

            # take the ROI and pre-process it so we can later classify the region using Keras/Tensorflow
            roi = cv2.resize(roi_orig, (224, 224))  # Resize to a fixed size
            roi = img_to_array(roi)
            roi = preprocess_input(roi)

            # update our list of ROIs and associated coordinates
            rois.append(roi)
            locs.append((x, y, x + roi_size[0], y + roi_size[1]))

    # convert and ROIs to a Numpy array
    rois = np.array(rois, dtype='float32')

    # classify each of the proposal ROIs using your model
    predictions = vegetable_model.predict(rois)

    # initialize the list to store detected vegetables
    detected_vegetables = []

    # initialize a set to keep track of unique detected vegetable names
    unique_vegetable_names = set()

    # Loop over the predictions
    for i, pred in enumerate(predictions):
        # Get the predicted class index
        predicted_class_index = np.argmax(pred)

        # Get the class name
        predicted_class = class_names[predicted_class_index]

        # Get the confidence/probability score
        confidence = pred[predicted_class_index]

        # Filter out weak detections by ensuring the predicted probability is greater than the minimum probability
        if confidence >= MIN_CONFIDENCE:
            # Check if the vegetable name is not already present in the set
            if predicted_class not in unique_vegetable_names:
                # Add the detected vegetable to the list
                detected_vegetables.append({
                    'class': predicted_class,
                    'confidence': confidence,
                    'box': locs[i]
                })

                # Add the vegetable name to the set to avoid repetition
                unique_vegetable_names.add(predicted_class)

    # Create a list of detected vegetable names
    detected_vegetable_names = [veg['class'] for veg in detected_vegetables]

    # Print the list of detected vegetable names
    print("Detected Vegetable Names:", detected_vegetable_names)

    return detected_vegetable_names