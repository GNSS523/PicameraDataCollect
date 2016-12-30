#coding=utf-8
"""
相关数据处理方法
"""
import numpy as np

#从arduino映射的方法
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# 将原始数据转化为CNN输入所需数据
def raw_to_cnn(y, min_arduino=40.0, max_arduino=150.0):
    y_ = arduino_map(y, min_arduino, max_arduino, 0.0, 1.0)
    return [y_] 

# 将卷积神经网络输出转化为原始输出
def cnn_to_raw(y, min_arduino=40.0, max_arduino=150.0):
    #获取到最大的索引值并映射到后面
    y_ = y[np.argmax(y)]

    y_ = arduino_map(y_, 0.0, 1.0, min_arduino, max_arduino)

    return y_

# 根据速度设置MOTOR RGB颜色
def raw_motor_to_rgb(x):
    if x <= 90:
        if x < 70:
            return (255, 0, 0)        
        elif x < 80:
            return (255, 165, 0)
        else:
            return (0, 255, 0)
    elif x > 90:
        if x > 120:
            return (255, 0, 0)
        elif x > 110:
            return (255, 165, 0)
        else:
            return (0, 255, 0)