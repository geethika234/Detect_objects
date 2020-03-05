import json 
import numpy as np
import cv2

def detect(image):
	# initialize the list of class labels MobileNet SSD was trained to detect
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]

	pro="MobileNetSSD_deploy.prototxt.txt"
	ca="MobileNetSSD_deploy.caffemodel"
	# load the model from disk
	net = cv2.dnn.readNetFromCaffe(pro, ca)

	# load the input image and construct an input blob for the image
	# by resizing to a fixed 300x300 pixels and then normalizing it
	image = cv2.imread(image)
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and predictions
	net.setInput(blob)
	detections = net.forward()
	items=[]
	k=[0,0,0]

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence of the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > 0.2:
			# extract the index of the class label from the `detections`
			idx = int(detections[0, 0, i, 1])
			if CLASSES[idx] not in items:
				items.append(CLASSES[idx])

			if idx == 15:
				k[0]=k[0]+1
			elif idx == 8 or idx == 10 or idx == 12 or idx == 13 or idx == 17:
				k[1]=k[1]+1
			else:
				k[2]=k[2]+1 

	dictionary ={ 
	    "items" : items, 
	    "humans" : k[0], 
	    "animals" : k[1], 
	    "others" : k[2]
	} 
	  
	# Serializing json  
	json_object = json.dumps(dictionary, indent = 4) 
	  
	# Writing to sample.json 
	return(json_object)
