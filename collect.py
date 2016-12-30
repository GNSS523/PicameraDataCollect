#coding=utf-8
import cv2
import os
import time
import json
import numpy as np

from SuironIO import SuironIO

#����ͼ������
with open('settings.json') as d:
    SETTINGS = json.load(d)

suironio = SuironIO(width=SETTINGS['width'], height=SETTINGS['height'], depth=SETTINGS['depth'])
suironio.init_saving()

#Ԥ������ͷ
print('Warming up...')
time.sleep(5)

raw_input('Press any key to conitnue')
print('Recording data...')
while True:
    try:
        suironio.record_inputs()#��¼������Ϣ
    except KeyboardInterrupt:
        break
    

print('Saving file...')
suironio.save_inputs()