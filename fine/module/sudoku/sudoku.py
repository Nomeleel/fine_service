# 1. Read iamge, async start neural network.
# 2. Find 9 * 9 cells.
# 3. Each split to cell, and erase border, move to center.
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
        cv2.imshow('image', image)
        cells = self.splitToCells(image)
        cv2.imshow('Cells[2]', cells[2])
        cv2.waitKey(0)

    def loadImage(self, image_source):
        # image source is path.
        if isinstance(image_source, str):
            self.image = cv2.imread(image_source)
        # image source from network byte stream.
        elif isinstance(image_source, bytes):
            self.image = cv2.imdecode(np.frombuffer(
                image_source, np.uint8), cv2.IMREAD_COLOR)
        else:
            raise Exception('Invalid image source.')

    def saveImage(self, image_name):
        cv2.imwrite(image_name, self.image)

    def findSudoku(self):
        # The default is BGR format. Only the conversion to GRAY format can perform the following processing.
        image = cv2.cvtColor(self.image.copy(), cv2.COLOR_BGR2GRAY)
        # Binarize and invert.
        image = 255 - cv2.adaptiveThreshold(image.astype(
            np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 1)
        # Find target sudoku part.
        x, y, w, h = self.findMaxContour(image)
        # Crop out the target sudoku part.
        image = image[y: (y + h), x: (x + w)]

        return image

    def splitToCells(self, image):
        cells = []
        cell_side_length = image.shape[0] // 9
        # Guaranteed length is a multiple of 9, otherwise errors will accumulate.
        resized_side_length = cell_side_length * 9
        image = cv2.resize(image, (resized_side_length, resized_side_length))

        for r in range(0, resized_side_length, cell_side_length):
            for c in range(0, resized_side_length, cell_side_length):
                # Estimate border length, no border required for cropped cell.
                border_length = int(cell_side_length * 0.077)
                cell = image[(r + border_length): (r + cell_side_length - border_length),
                             (c + border_length): (c + cell_side_length - border_length)]

                # Because the border is not the same width, the digit are not necessarily in the center.
                cell = self.moveToCenter(cell)

                cells.append(cell)

        return cells

    def moveToCenter(self, cell):
        center_contour = self.findMaxContour(cell)
        if not center_contour is None:
            x, y = center_contour[0], center_contour[1]
            w, h = center_contour[2], center_contour[3]
            moved = np.zeros(cell.shape)

            offset_x = (cell.shape[0] - w) // 2 + 1
            offset_y = (cell.shape[1] - h) // 2 + 1

            moved[offset_y: (offset_y + h), offset_x: (offset_x + w)
                  ] = cell[y: (y + h), x: (x + w)]

            return moved

        return cell

    def recognitionToDigit(self, image):
        pass

    def findMaxContour(self, image):
        # Find all contours.
        img, contours, hierarchy = cv2.findContours(
            image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not hierarchy is None:
            # The biggest contour is ours targrt.
            return cv2.boundingRect(max(contours, key=cv2.contourArea))
