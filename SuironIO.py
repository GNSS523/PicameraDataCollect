#coding=utf-8
#图片采集与数据采集
import time
import random
import numpy as np
import pandas as pd
import cv2, os, serial, csv
import matplotlib.pyplot as plt

from functions import cnn_to_raw
from img_serializer import serialize_image
from file_finder import get_new_filename


"""读取摄像头数据读取串口数据并保存在本地"""
class SuironIO:

    def __init__(self, width=72, height=48, depth=3, serial_location='/dev/ttyUSB0', baudrate=57600):
        #图像设置
        self.width = int(width)
        self.height = int(height)
        self.depth = int(depth)
        self.cap =  cv2.VideoCapture(0) #使用本地摄像头

        #读取串口IO数据
        self.ser = None
        if os.path.exists(serial_location):
            print('Found %s, starting to read from it...' % serial_location)
            self.ser = serial.Serial(serial_location, baudrate)        
        self.outfile = None        

        #将数据记录在内存中防止IO操作过于频繁
        self.frame_results = []
        self.servo_results = []
        self.motorspeed_results = [] 
    

    #初始化保存设置
    def init_saving(self, folder='data', filename='output_', extension='.csv'):
        fileoutname = get_new_filename(folder=folder, filename=filename, extension=extension)

        #打开数据保存的文件
        outfile = open(fileoutname, 'w') # Truncate file first
        self.outfile = open(fileoutname, 'a')

    #保存2个输入，图片和串口数据
    def record_inputs(self):
        frame = self.get_frame()

        #串口数据servo和motor'
        serial_inputs = self.get_serial()

        if serial_inputs:
            servo = serial_inputs['servo'] 
            motor = serial_inputs['motor'] 

            # 在内存中追加
            self.frame_results.append(serialize_image(frame))
            self.servo_results.append(servo)
            self.motorspeed_results.append(motor)

    # 获取motor输入
    def get_serial(self):
        serial_raw = '-1,-1\n'
        if self.ser:
            #轮询数据
            self.ser.write('d')
            serial_raw = self.ser.readline()
        serial_processed = self.normalize_serial(serial_raw)
        return serial_processed

    #获取图像
    def get_frame(self):
        ret, frame = self.cap.read()

        #图像获取成功就保存
        if not ret:
            raise IOError('No image found!')

        frame = self.normalize_frame(frame)
        return frame

    #获取图像做预测用
    def get_frame_prediction(self):
        ret, frame = self.cap.read()
        if not ret:
            raise IOError('No image found!')

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        frame = frame.astype('uint8')

        return frame
    

    # 归一化串口数据
    def normalize_serial(self, line):
        try:
            line = line.replace('\n', '').split(',')
            line_dict = {'servo': int(line[0]), 'motor': int(line[1])}
            return line_dict
        except:
            return None

    # 归一化图像数据
    def normalize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        frame = frame.flatten()
        frame = frame.astype('uint8')
        return frame

    #保存文件
    def save_inputs(self):
        raw_data = {
            'image': self.frame_results, 
            'servo': self.servo_results,
            'motor': self.motorspeed_results
        }
        df = pd.DataFrame(raw_data, columns=['image', 'servo', 'motor'])
        df.to_csv(self.outfile)

   
    # 神经网络控制输出
    def servo_write(self, np_y):
        servo_out = cnn_to_raw(np_y)

        if (servo_out < 90):
            servo_out *= 0.85

        elif (servo_out > 90):
            servo_out *= 1.15

        self.ser.write('steer,' + str(servo_out) + '\n') 
        time.sleep(0.02)

    # 设置电机为固定速度
    def motor_write_fixed(self):    
        self.ser.write('motor,80\n')
        time.sleep(0.02)

    # 关闭电机
    def motor_stop(self):      
        self.ser.write('motor,90\n')
        time.sleep(0.02)

    # 设置伺服
    def servo_straighten(self):
        self.ser.write('steer,90')
        time.sleep(0.02)
        
    def __del__(self):
        if self.outfile:
            self.outfile.close()