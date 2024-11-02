from constraint_gen import *
import cv2
if __name__ == '__main__':
    generator = LaTeXGenerator()
    img = cv2.imread('latex.png')
    generator.generate(img)