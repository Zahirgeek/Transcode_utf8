import os
import codecs
import chardet


# 将文件转换成UTF-8编码
def convert(file_name, file_path, in_code="GBK", out_code="UTF-8"):
    '''
    :param file_name: 文件名
    :param file_path: 文件路径
    :param in_code: 输入文件格式，默认GBK
    :param out_code: 输出文件格式，默认UTF-8
    :return:
    '''
    if in_code == "UTF-8":
        return 0
    # 文件位置
    file = os.path.join(file_path, file_name)
    try:
        with codecs.open(file, "rb", in_code) as f_in:
            new_content = f_in.read()
            out_path = "transform"
            file_out = os.path.join(file_path, out_path)
            isExists = os.path.exists(file_out)
            if not isExists:
                os.makedirs(file_out)

            file_out = os.path.join(file_out, file_name)
            # 转换后文件默认保存在当前目录的transform目录中
            with codecs.open(file_out, "w", out_code) as f_out:
                f_out.write(new_content)

    except IOError as err:
        print("I/O error: {}".format(err))


# 返回路径该级所有文件名和文件路径
def list_folders_files(path):
    '''
    :param path: 输入的文件路径
    :return:
    '''

    # 文件夹路径列表
    list_folders = []
    # 文件路径列表
    list_files = []

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_folders.append(file_path)
        else:
            if file.endswith('.lrc'):
                list_files.append(file)

    return list_files, list_folders


# 遍历输入文件路径下所有文件和路径并执行转换
def transform(path):

    list_file_name, list_folder_name = list_folders_files(path)
    current_path = path

    # 批量转换当前路径下的文件
    for file_name in list_file_name:
        file_path = os.path.join(current_path, file_name)
        with open(file_path, 'rb') as f_in:
            data = f_in.read()
            code_type = chardet.detect(data)['encoding']
            code_type = code_type.upper()

        if code_type == 'UTF-8':
            continue
        if code_type == 'GB2312':
            convert(file_name, current_path)
        else:
            convert(file_name, current_path, in_code=code_type)


# 判断用户输入, 返回转换目录
def user_input():

    file_path = input(">>请输入你需要转换的文件所在目录，默认为该程序当前目录,转换后的文件在该目录的transform文件夹下\n"
                      ">>Please input your convert directory, the default directory is current directory of this program,"
                      "the converted file is under the transform folder in current directory\n")

    if not file_path:
        file_path = os.path.abspath('transcode.py')
        file_path = file_path.split("\\")[:-1]
        file_path = "\\".join(file_path)
    else:
        if not os.path.exists(file_path):
            print("不存在该目录，程序退出")

    return file_path


if __name__ == '__main__':
    file_path = user_input()
    transform(file_path)
