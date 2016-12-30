#coding=utf-8
"""
�����л��ͷ����л���ͼ��ת��Ϊ����֡��ʽ
"""
import cv2
import numpy as np

# �������з����л���ͼ���ļ�
def deserialize_image(df_dump, width=72, height=48, depth=3):
    df_dump = np.fromstring(df_dump[1:-1], sep=', ', dtype='uint8')
    df_dump = np.resize(df_dump, (height, width, depth))

    return df_dump


def serialize_image(frame):
    return frame.tolist()