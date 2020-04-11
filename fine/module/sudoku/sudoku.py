# 1. Read iamge, async start neural network.
# 2. Find 9 * 9 cells.
# 3. Each split to cell, and erase border, move to center.
# 4. Recognize numbers in cells.
# 5. Sudoku.
# 6. If not solve will save image.

from module.neuralnetwork.digitalRecognizer import DigitalRecognizer
from module.sudoku import solvingSudoku
import cv2
import numpy as np
import os

class Sudoku:

    def __init__(self, image_source=None, sudoku_str=None):
        self.image_source =  image_source
        self.sudoku_str = sudoku_str

    def execute(self):

        if self.sudoku_str is None:
            self.parseToSudokuStr()

        result = self.solvingSudoku()
        
        if result:
            self.printSudokuResult()
        else:
            self.unSolvedAction()

        return result, self.sudoku_result

    def parseToSudokuStr(self):
        self.loadImage(self.image_source)
        
        #TODO async
        self.digital_recognizer = DigitalRecognizer()
        image = self.findSudoku()
        cells = self.splitToCells(image)

        self.sudoku_str = self.recognitionAllCell(cells)

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

    def recognitionToDigit(self, cell):
        digit = self.digital_recognizer.digitRecognition(cell)
        
        return digit if not digit is None else '0'

    def recognitionAllCell(self, cells):

        return ''.join(self.recognitionToDigit(cell) for cell in cells)

    def solvingSudoku(self):
        result = False
        try:
            result = solvingSudoku.solve(self.sudoku_str)
        except Exception as e:
            print('This sudoku unsolved!')
        if result:
            self.sudoku_result = ''.join(result)
            result = True
        else:
            self.sudoku_result = self.sudoku_str
        
        return result

    def printSudokuResult(self):
        if not self.sudoku_str is None and not self.sudoku_result is None and self.sudoku_str != self.sudoku_result:
            for i in range(9):
                for j in range(9):
                    # Background color: 41: red; 42: green; 44 blue;
                    offset = 4 if self.sudoku_str[9 * i + j] in '123456789' else ((i // 3 + j // 3) % 2 + 1)
                    print("\033[4;%sm %s \033[0m" % (str(40 + offset), self.sudoku_result[9 * i + j]), end='')
                print()

    # 图像模式下，得不到结果，可能是扫描出现问题，记录下来对训练数据集是有价值的。
    # 字符串模式下，得不到结果，那一定是因为字符串不合法。
    def unSolvedAction(self):
        if hasattr(self, 'image') and not self.image is None:
            # TODO format str
            self.saveImage(os.getcwd() + '\\module\\sudoku\\unsolvedlog\\' + self.sudoku_str + '.png')
            # 文件名可能不利于查看，建议输出到txt文件中

    def findMaxContour(self, image):
        # Find all contours.
        img, contours, hierarchy = cv2.findContours(
            image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not hierarchy is None:
            # The biggest contour is ours targrt.
            return cv2.boundingRect(max(contours, key=cv2.contourArea))
