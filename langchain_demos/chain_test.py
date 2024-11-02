from constraint_gen import *
import cv2
import os

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    generator = LaTeXGenerator()
    img = cv2.imread('latex.png')
    generator.generate(img)
