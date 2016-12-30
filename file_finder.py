#coding=utf-8
"""
�ļ���ȡ
"""
import os

# ����ļ����Ƿ����
def check_folder_exists(folder='data'):
    if not os.path.exists(folder):
        os.mkdir(folder)

# ���ļ��л�ȡ����
def get_iter_no(folder='data', filename='output_', extension='.csv'):
    iter_name = 0
    while os.path.exists(os.path.join(folder, filename+str(iter_name)+extension)):
        iter_name += 1
    return iter_name

# �����ļ��л�ȡ���·����
def get_relative_filename(iter_name, folder='data', filename='output_', extension='.csv'):
    fileoutname = filename + str(iter_name) + extension
    fileoutname = os.path.join(folder, fileoutname)
    return fileoutname

# ������ļ��л�ȡ�����µ��ļ�����
def get_new_filename(folder='data', filename='output_', extension='.csv'):
    check_folder_exists(folder)
    iter_name = get_iter_no(folder=folder, filename=filename, extension=extension)
    return get_relative_filename(iter_name, folder=folder, filename=filename, extension=extension) 

# ��ȡ���µ�����ļ���
def get_latest_filename(folder='data', filename='output_', extension='.csv'):
    check_folder_exists(folder)
    iter_name = get_iter_no(folder=folder, filename=filename, extension=extension) - 1
    if iter_name == -1:
        raise IOError('No file found!')
    return get_relative_filename(iter_name, folder=folder, filename=filename, extension=extension) 