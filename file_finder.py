#coding=utf-8
"""
文件获取
"""
import os

# 检查文件夹是否存在
def check_folder_exists(folder='data'):
    if not os.path.exists(folder):
        os.mkdir(folder)

# 从文件中获取号码
def get_iter_no(folder='data', filename='output_', extension='.csv'):
    iter_name = 0
    while os.path.exists(os.path.join(folder, filename+str(iter_name)+extension)):
        iter_name += 1
    return iter_name

# 从新文件中获取相对路径名
def get_relative_filename(iter_name, folder='data', filename='output_', extension='.csv'):
    fileoutname = filename + str(iter_name) + extension
    fileoutname = os.path.join(folder, fileoutname)
    return fileoutname

# 从输出文件中获取到最新的文件名字
def get_new_filename(folder='data', filename='output_', extension='.csv'):
    check_folder_exists(folder)
    iter_name = get_iter_no(folder=folder, filename=filename, extension=extension)
    return get_relative_filename(iter_name, folder=folder, filename=filename, extension=extension) 

# 获取最新的输出文件名
def get_latest_filename(folder='data', filename='output_', extension='.csv'):
    check_folder_exists(folder)
    iter_name = get_iter_no(folder=folder, filename=filename, extension=extension) - 1
    if iter_name == -1:
        raise IOError('No file found!')
    return get_relative_filename(iter_name, folder=folder, filename=filename, extension=extension) 