#Image manipulation for webscraped imgs

import sys
from PySide2.QtWidgets import (QApplication, QLabel, QWidget, 
                                QPushButton, QLineEdit, QVBoxLayout, QComboBox)
from PySide2.QtCore import Slot

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for

import numpy as np
import cv2

from pprint import pprint
from PIL import Image

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.my_list = ["Pick a manipulation", "Sepia", "Grayscale", "Negative", "Thumbnail", "None", "Winter"]
        self.my_combo_box = QComboBox()
        self.my_combo_box.addItems(self.my_list)
        self.my_label = QLabel("")

        vbox = QVBoxLayout()
        vbox.addWidget(self.my_combo_box)
        vbox.addWidget(self.my_label)

        self.setLayout(vbox)
        self.my_combo_box.currentIndexChanged.connect(self.update_ui)

    @Slot()
    def update_ui(self):
        my_text = self.my_combo_box.currentText()
        my_index = self.my_combo_box.currentIndex()
        self.my_label.setText(f'You chose {self.my_list[my_index]}.')        

        #Open Sawyer image
        print(my_text)
        im = Image.open('SawyerOG.jpg')

        if my_text == "Sepia":
            
            sepia_list = [(255 + pixel[0], pixel[1], pixel[2])
                for pixel in im.getdata()]
            im.putdata(sepia_list)
            im.show()
            ##############
            #def map_sepia(pixel):
            #    return (pixel[0], pixel[1]//2, pixel[2]//2)
            #
            #new_list = map(map_sepia, im.getdata())
            ###############
        if my_text == "Grayscale":
            grayscale_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                  for a in im.getdata() ]
            #grayscale_list = [(255 - a[0], 255 - a[0], 255 - a[0])
            #    for a in im.getdata()]
            im.putdata(grayscale_list)
            im.show()
        if my_text == "Negative":
            negative_list = [(255 - p[0], 255 - p[1], 255 - p[2])
                for p in im.getdata()]
            im.putdata(negative_list)
            im.show()
        if my_text == "Thumbnail":
            source = Image.open('SawyerOG.jpg')

            w,h = source.width, source.height

            target = Image.new('RGB', (w, h), 'rosybrown')

            target_x = 0
            for source_x in range(0, source.width, 2):
                target_y = 0
                for source_y in range(0, source.height, 2):
                    pixel = source.getpixel((source_x, source_y))
                    target.putpixel((target_x, target_y), pixel)
                    target_y += 1
                target_x += 1

            target.show('SawyerOG-Smaller.jpg')
            
        if my_text == "None":
            im.show()

        if my_text == "Winter":
            image_winter = cv2.imread(
                'SawyerOG.jpg',
                cv2.IMREAD_GRAYSCALE
            )
            image_remap = cv2.applyColorMap(
                image_winter,
                cv2.COLORMAP_WINTER
            )
            cv2.imshow("Image in Winter", image_remap)
            cv2.waitKey()

            # def map_red(pixel):
            #     return (pixel[0], pixel[1], pixel[2]*2)
            # new_list = map(map_red, im.getdata())
            # im.putdata(list(new_list))
            # im.show()


#Negative code
# def map_neg(pixel):
#     im = Image.open('Sawyer.jpg')

#     orig_data = im.getdata()
#     new_data = [ ]

#     for p in orig_data:
#         new_data.append((255-p[0], 255-p[1], 255-p[2]))

#     im.putdata(new_data)
#     im.save('SawyerNeg.jpg')
#End Negative code


#Sepia
# def map_sepia(pixel):
#     if pixel[0] < 63:
#         r,g,b = int(pixel[0]*1.1), pixel[1], int(pixel[2]*.9)
#     elif pixel[0]>62 and pixel[0]<192:
#         r,g,b = int(pixel[0]*1.15), pixel[1], int(pixel[2]*.85)
#     else:
#         r = int(pixel[0]*1.08)
#         if r>255: r=255
#         g,b = pixel[1], pixel[2]//2
#     return r,g,b

#new_list = map(map_sepia, im.getdata())
#End sepia

app = QApplication([])
my_win = MyWindow()
my_win.show()
app.exec_()