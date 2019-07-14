from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
import imutils

class Text_Recognition:
	def decode_predictions(self, scores, geometry):
		(numRows, numCols) = scores.shape[2:4]
		rects = []
		confidences = []

		for y in range(0, numRows):
			scoresData = scores[0, 0, y]
			xData0 = geometry[0, 0, y]
			xData1 = geometry[0, 1, y]
			xData2 = geometry[0, 2, y]
			xData3 = geometry[0, 3, y]
			anglesData = geometry[0, 4, y]

			for x in range(0, numCols):
				# if our score does not have sufficient probability,
				# ignore it
				if scoresData[x] < self.args["min_confidence"]:
					continue

				(offsetX, offsetY) = (x * 4.0, y * 4.0)

				angle = anglesData[x]
				cos = np.cos(angle)
				sin = np.sin(angle)

				h = xData0[x] + xData2[x]
				w = xData1[x] + xData3[x]

				endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
				endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
				startX = int(endX - w)
				startY = int(endY - h)

				rects.append((startX, startY, endX, endY))
				confidences.append(scoresData[x])

		# return a tuple of the bounding boxes and associated confidences
		return (rects, confidences)

	def start(self, filename, target_word, is_rotated):
		self.args = {'image': filename, 'east': 'frozen_east_text_detection.pb',
		'width': 320, 'height': 320, 'min_confidence': 0.5, 'padding': 0.0}

		# load the input image rotate if needed
		if(is_rotated == '1'):
			image = imutils.rotate(cv2.imread(self.args["image"]), 90)
		else:
			image = cv2.imread(self.args["image"])

		orig = image.copy()
		(origH, origW) = image.shape[:2]

		(newW, newH) = (self.args["width"], self.args["height"])
		rW = origW / float(newW)
		rH = origH / float(newH)

		image = cv2.resize(image, (newW, newH))
		(H, W) = image.shape[:2]

		layerNames = [
			"feature_fusion/Conv_7/Sigmoid",
			"feature_fusion/concat_3"]

		# load EAST text detector
		print("[INFO] loading EAST text detector...")
		net = cv2.dnn.readNet(self.args["east"])

		blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
			(123.68, 116.78, 103.94), swapRB=True, crop=False)
		net.setInput(blob)
		(scores, geometry) = net.forward(layerNames)

		(rects, confidences) = self.decode_predictions(scores, geometry)
		boxes = non_max_suppression(np.array(rects), probs=confidences)

		results = []

		for (startX, startY, endX, endY) in boxes:
			startX = int(startX * rW)
			startY = int(startY * rH)
			endX = int(endX * rW)
			endY = int(endY * rH)

			dX = int((endX - startX) * self.args["padding"])
			dY = int((endY - startY) * self.args["padding"])

			startX = max(0, startX - dX)
			startY = max(0, startY - dY)
			endX = min(origW, endX + (dX * 2))
			endY = min(origH, endY + (dY * 2))

			roi = orig[startY:endY, startX:endX]

			# config for tesseract
			config = ("-l eng --oem 1 --psm 7")
			text = pytesseract.image_to_string(roi, config=config)

			results.append(((startX, startY, endX, endY), text))

		# sort the results bounding box coordinates from top to bottom
		results = sorted(results, key=lambda r:r[0][1])

		successfulInFindingTarget = False
		for ((startX, startY, endX, endY), text) in results:
			# output the text found
			print("OCR TEXT")
			print("========")
			print("{}\n".format(text))
			print()

			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			output = orig.copy()
			cv2.rectangle(output, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(output, text, (startX, startY - 20),
				cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

			# show the output image

			current_text = text.lower()

			if(target_word.lower() in current_text):
				successfulInFindingTarget = True
				cv2.imshow("Text Detection", output)
				cv2.waitKey(0)
		if(successfulInFindingTarget == False):
			failed_img = cv2.imread(self.args["image"])
			cv2.imshow('image', failed_img)
			cv2.waitKey(0)
