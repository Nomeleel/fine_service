# 1. Read iamge, async start neural network.
# 2. Find 9 * 9 cells.
# 3. Each split to cell, and erase border.
# 4. Recognize numbers in cells.
# 5. Sudoku.
# 6. If not solve will save image.

import cv2
import numpy as np

class Sudoku:

    image = None

    def __init__(self, image_source):
        self.loadImage(image_source)
        image = self.findSudoku()
        self.helpers.show(image, 'image')

    def loadImage(self, image_source):
        # image source is path.
        if isinstance(image_source, str):
            self.image = cv2.imread(image_source)
        # image source from network byte stream.
        elif isinstance(image_source, bytes):
            self.image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        else:
            raise Exception('Invalid image source.')

    def saveImage(self, image_name):
        cv2.imwrite(image_name, self.image)

    def findSudoku(self):
        # The default is BGR format. Only the conversion to GRAY format can perform the following processing.
        image = cv2.cvtColor(self.image.copy(), cv2.COLOR_BGR2GRAY)
        # Binarize and invert.
        image = 255 - cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 1)
        # Find all contours.
        img, contours, hierarchy = cv2.findContours(self.image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # The biggest contour is ours targrt.
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        # Crop out the target sudoku part.
        image = image[y:y + h, x:x + w]

        return image

    def splitToCells(self, image):
        pass

    def recognitionToDigit(self, image):
        pass