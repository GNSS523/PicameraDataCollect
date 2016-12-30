#coding=utf-8
"""
将序列化和反序列化的图像转化为数据帧格式
"""
import cv2
import numpy as np

# 从序列中反序列化出图像文件
def deserialize_image(df_dump, width=72, height=48, depth=3):
    df_dump = np.fromstring(df_dump[1:-1], sep=', ', dtype='uint8')
    df_dump = np.resize(df_dump, (height, width, depth))

    return df_dump


def serialize_image(frame):
    return frame.tolist()