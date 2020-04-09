import os
import threading

from PIL import Image, ExifTags
from tqdm import tqdm
import time

def create_image(infile, overwrite):
    # 分离文件名与扩展名
    name, ext = os.path.splitext(infile) 
    img = Image.open(infile)

# 根据图片带有的方向信息，旋转图片
    try:
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(img._getexif().items())
        if   exif[orientation] == 3 : 
            img=img.rotate(180, expand = True)
        elif exif[orientation] == 6 : 
            img=img.rotate(270, expand = True)
        elif exif[orientation] == 8 : 
            img=img.rotate(90, expand = True)
    except:
        pass

    new_name = name + '.webp' #新文件的完整文件名取原文件名，后缀名变为webp
    img.save(str(new_name), "WEBP")

    if overwrite == "1":
        try:
            os.remove(infile)
        except:
            pass
""" 
获得文件夹内指定后缀名文件的列表
dir：文件夹   suf_list：指定后缀名列表    recur：是否迭代
迭代方法使用os.listdir方法
不迭代方法中使用os.walk方法
 """
def getFiles(dir, suf_list, recur):

    res = []    # 创建文件列表
    
    # os.walk方法，自动获取该文件夹下所有指定后缀文件(包括子文件夹)
    if recur == "1": 
        """
        os.walk方法返回一个三元组

        dirpath:遍历的目录路径
        directory:目录下所有文件夹
        filenames:目录下的所有的文件 
        """
        for dirpath, directory, filenames in os.walk(dir): 
            # 遍历该目录下所有的文件(不包含文件夹)
            for filename in filenames: 
                """ 
                先组装被读取的文件路径
                dirpath:目录路径    filename:文件名 
                os.path.join方法将路径与文件名接成文件绝对路径
                 """
                file_path = os.path.join(dirpath, filename) 

                # 将被读取文件的名字拆分成name:文件名及suf:后缀名
                name, suf = os.path.splitext(filename)
                
                # 将被读取文件的后缀名，依次与后缀名列表suf_list进行对比
                for suffix in suf_list:
                    if suf == suffix:
                        # 后缀名符合条件，则将其文件绝对路径加入到列表res
                        res.append(file_path)

    elif recur == "0":
        """
        os.listdir列出目录中所有的文件，返回列表数据
        """
        filenames = os.listdir(dir)
        # 获得被访问目录的路径
        dirpath = os.path.abspath(dir)
        # 遍历该目录下所有的文件(包含文件夹)
        for filename in filenames: 
            """ 
            先组装被读取的文件路径
            dirpath:目录路径    filename:文件名 
            os.path.join方法将路径与文件名接成文件绝对路径
             """
            file_path = os.path.join(dirpath, filename)
            # 将被读取文件的名字拆分成name:文件名及suf:后缀名
            name, suf = os.path.splitext(filename)
            # 将被读取文件的后缀名，依次与后缀名列表suf_list进行对比
            for suffix in suf_list: 
                if suf == suffix:
                    # 后缀名符合条件，则将其文件绝对路径加入到列表res
                    res.append(file_path)
                    
            # 若文件实际为文件夹，可以进行迭代，继续遍历子文件夹下的文件
            # if os.path.isdir(file_path):    
            #     """ 
            #     将该文件夹的路径再次带入getFiles函数进行迭代
            #     除了路径有变外，其他参数不变
            #     res.extend类似于res.append(列表末尾加入新数据)
            #     在列表末尾继续加入另一列表的数据
            #     即将迭代获得的子文件夹的文件列表加入总的文件列表
            #      """
            #     res.extend(getFiles(file_path, suf_list, recur))   

    return res

def start():

    print("本程序可将后缀名为:.jpg、.JPG、.png、.PNG 的图片文件均转为webp格式")
    print("webp格式可以近乎无损的提供很高的压缩率，在减小带宽消耗的目的上被许多网页及手机APP广泛应用")
    print("但是本地电脑的打开方法很麻烦，得用谷歌浏览器")
    print("本程序的核心算法均来源于PIL库 written by Virtual Circuit")

    print("\n转换后是否删除原图片？     1:是    0：否")
    print("请输入数字后，按下回车键")
    # 决定是否删除原图片
    overwrite = input() 

    print("\n是否将子目录的所有图片也转换？     1:是    0：否")
    print("请输入数字后，按下回车键")
    # 是否进行迭代，若迭代，则所有子文件夹（不论多少层）的图片也转换
    recur = input()

    # 根据后缀名判断文件是否为需要转换的文件
    suf_list = ['.jpg', '.JPG', 'png', 'PNG', 'bmp', 'BMP'] 

    """ 
    根据后缀名列表，是否进行迭代，查找程序所在文件夹 . 内的指定后缀名文件
    并将所有文件绝对路径加入列表img_list
     """
    img_list = getFiles(".", suf_list, recur)   

    # 获取所有图片的数量
    img_num = len(img_list)
    print("\n\n一共需要转换" + str(img_num) + "张图片数据")

    time.sleep(2)
    print("\n正在处理转换图片数据")

    # tqdm可以将遍历到列表第几个以进度条显示
    for img in tqdm(img_list, ncols=60):
        # 创建create_image线程，参数为(img, overwrite)
        img_conv = threading.Thread(target=create_image, args=(img, overwrite,))
        img_conv.start()
        img_conv.join()
        

    input("\n请按下回车键以结束此程序\nproduced by Vircuit Circuit")

if __name__ == "__main__":
    start()
