#coding=utf-8
#ͼƬ�ɼ������ݲɼ�
import time
import random
import numpy as np
import pandas as pd
import cv2, os, serial, csv
import matplotlib.pyplot as plt

from functions import cnn_to_raw
from img_serializer import serialize_image
from file_finder import get_new_filename


"""��ȡ����ͷ���ݶ�ȡ�������ݲ������ڱ���"""
class SuironIO:

    def __init__(self, width=72, height=48, depth=3, serial_location='/dev/ttyUSB0', baudrate=57600):
        #ͼ������
        self.width = int(width)
        self.height = int(height)
        self.depth = int(depth)
        self.cap =  cv2.VideoCapture(0) #ʹ�ñ�������ͷ

        #��ȡ����IO����
        self.ser = None
        if os.path.exists(serial_location):
            print('Found %s, starting to read from it...' % serial_location)
            self.ser = serial.Serial(serial_location, baudrate)        
        self.outfile = None        

        #�����ݼ�¼���ڴ��з�ֹIO��������Ƶ��
        self.frame_results = []
        self.servo_results = []
        self.motorspeed_results = [] 
    

    #��ʼ����������
    def init_saving(self, folder='data', filename='output_', extension='.csv'):
        fileoutname = get_new_filename(folder=folder, filename=filename, extension=extension)

        #�����ݱ�����ļ�
        outfile = open(fileoutname, 'w') # Truncate file first
        self.outfile = open(fileoutname, 'a')

    #����2�����룬ͼƬ�ʹ�������
    def record_inputs(self):
        frame = self.get_frame()

        #��������servo��motor'
        serial_inputs = self.get_serial()

        if serial_inputs:
            servo = serial_inputs['servo'] 
            motor = serial_inputs['motor'] 

            # ���ڴ���׷��
            self.frame_results.append(serialize_image(frame))
            self.servo_results.append(servo)
            self.motorspeed_results.append(motor)

    # ��ȡmotor����
    def get_serial(self):
        serial_raw = '-1,-1\n'
        if self.ser:
            #��ѯ����
            self.ser.write('d')
            serial_raw = self.ser.readline()
        serial_processed = self.normalize_serial(serial_raw)
        return serial_processed

    #��ȡͼ��
    def get_frame(self):
        ret, frame = self.cap.read()

        #ͼ���ȡ�ɹ��ͱ���
        if not ret:
            raise IOError('No image found!')

        frame = self.normalize_frame(frame)
        return frame

    #��ȡͼ����Ԥ����
    def get_frame_prediction(self):
        ret, frame = self.cap.read()
        if not ret:
            raise IOError('No image found!')

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        frame = frame.astype('uint8')

        return frame
    

    # ��һ����������
    def normalize_serial(self, line):
        try:
            line = line.replace('\n', '').split(',')
            line_dict = {'servo': int(line[0]), 'motor': int(line[1])}
            return line_dict
        except:
            return None

    # ��һ��ͼ������
    def normalize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        frame = frame.flatten()
        frame = frame.astype('uint8')
        return frame

    #�����ļ�
    def save_inputs(self):
        raw_data = {
            'image': self.frame_results, 
            'servo': self.servo_results,
            'motor': self.motorspeed_results
        }
        df = pd.DataFrame(raw_data, columns=['image', 'servo', 'motor'])
        df.to_csv(self.outfile)

   
    # ������������
    def servo_write(self, np_y):
        servo_out = cnn_to_raw(np_y)

        if (servo_out < 90):
            servo_out *= 0.85

        elif (servo_out > 90):
            servo_out *= 1.15

        self.ser.write('steer,' + str(servo_out) + '\n') 
        time.sleep(0.02)

    # ���õ��Ϊ�̶��ٶ�
    def motor_write_fixed(self):    
        self.ser.write('motor,80\n')
        time.sleep(0.02)

    # �رյ��
    def motor_stop(self):      
        self.ser.write('motor,90\n')
        time.sleep(0.02)

    # �����ŷ�
    def servo_straighten(self):
        self.ser.write('steer,90')
        time.sleep(0.02)
        
    def __del__(self):
        if self.outfile:
            self.outfile.close()