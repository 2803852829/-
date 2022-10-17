import os
import shutil
import subprocess
import glob

name = 'Obama'


def download_vedio(a, url):
    s = subprocess.Popen(a + url)
    if s.wait():
        print('下载完成')


def scene_split(a, b):
    cmd = r'scenedetect.exe -i {} -o {}\vid_{}\场景分割 detect-content split-video'.format(a, name, b)
    s = subprocess.Popen(cmd)
    if s.wait():
        print('分割完成')


def deldir(dir):
    all_dir = glob.glob(r'{}\*'.format(dir))
    for i in all_dir:
        if os.path.isdir(i):  # 判断是否为文件夹
            shutil.rmtree(i)
            print("%s目录 已删除" % i)
        else:  # 如果不是文件夹,则为文件
            os.remove(i)  # 该命令删除文件
            print("%s文件 已删除" % i)


# 获取视频时长
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


# 获取视频时长
def get_time_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def split_vedio(p, input_path, output_path):
    s = subprocess.Popen(
        r'ffmpeg -ss {} -t 15 -i {} -threads 5 -preset ultrafast -acodec copy {}'.format(p, input_path, output_path))
    print(p)
    if s.wait():
        print('分割完成')


def rename_vid_au():
    # -----------------------删除下载的视频音频分开的文件---------------------------------
    # -------------------------对剩下的文件进行重命名------------------------------------
    print('删除下载的视频音频分开的文件')
    i = 0
    all_dir = glob.glob(r'{}\*'.format(name))
    count = len(all_dir)
    while 1:
        if i >= count:
            break
        new_name = 'vid_' + str(i)
        os.rename(all_dir[i], r'{}\vid--{}'.format(name, i))  # 执行重命名
        i += 1
    # ----------------------------------------------------------------------------------
    i = 0
    all_dir = glob.glob(r'{}\*'.format(name))
    count = len(all_dir)
    while 1:
        if i >= count:
            break
        os.rename(all_dir[i], r'{}\vid_{}'.format(name, i))  # 执行重命名
        i += 1
    # ------------------------对au里面的文件进行重命名----------------------------------
    i = 0
    all_dir = glob.glob(r'{}\*'.format(name))
    count = len(all_dir)
    while 1:
        if i >= count:
            break
        dir_name = glob.glob(r'{}\vid_{}\au\*'.format(name, i))
        os.rename(dir_name[0], r'{}\vid_{}\au\{}.mp4'.format(name, i, i))  # 执行重命名
        i += 1


def del_split_vedio():
    record = []
    all_dir = glob.glob(r'{}\*'.format(name))
    count = len(all_dir)
    i = 0
    while 1:
        if i >= count:
            break
        handle_dir = glob.glob(r'{}\vid_{}\au\*'.format(name, i))
        if len(handle_dir) >= 2 or len(handle_dir) == 0:
            deldir(r'{}\vid_{}'.format(name, i))
            os.rmdir(r'{}\vid_{}'.format(name, i))
            print(r'视频音频分离{}\vid_{}'.format(name, i) + '文件已删除')
            record.append(i)
        i += 1
    with open('{}url.txt'.format(name)) as file1:
        with open('{}url1.txt'.format(name), 'w') as file2:
            i = 0
            while 1:
                content = file1.readline()
                if not content:
                    break
                if i not in record:
                    file2.write(content)
                i += 1
    os.remove('{}url.txt'.format(name))


def del_black_vedio():
    record = []
    i = 0
    all_dir = glob.glob(r'{}\*'.format(name))
    count = len(all_dir)
    while 1:
        if i >= count:
            break
        handle_dir = glob.glob(r'{}\vid_{}\场景分割\*'.format(name, i))
        if not handle_dir:
            deldir(r'{}\vid_{}'.format(name, i))
            os.rmdir(r'{}\vid_{}'.format(name, i))
            print(r'{}\vid_{}'.format(name, i) + '文件已删除')
            record.append(i)
        i += 1
    with open('{}url1.txt'.format(name)) as file1:
        with open('{}url.txt'.format(name), 'w') as file2:
            i = 0
            j = 0
            while 1:
                content = file1.readline()
                if not content:
                    break
                if i not in record:
                    file2.write('vid_{}:'.format(j) + content)
                    j += 1
                i += 1
    os.remove('{}url1.txt'.format(name))


def del_15s_vedio():
    x = 15
    i = 0
    while 1:
        useful_dir = glob.glob(r'{}\vid_{}\场景分割\*'.format(name, i))
        # 获取的都是完整的相对路径 ['input_dir\\0.mp4', 'input_dir\\list.txt', 'input_dir\\文件list.txt']
        all_dir = glob.glob(r'{}\*'.format(name))
        if i >= len(all_dir):
            break
        for vid in useful_dir:
            time = int(get_length(vid))  # 获取这个视频的总时长，单位S
            print('{}时长{}'.format(vid, time))
            if time < x:
                os.remove(vid)
        i += 1


def rename_15s():
    i = 0
    all_dir = glob.glob(r'{}\*'.format(name))
    len_i = len(all_dir)
    while 1:
        if i >= len_i:
            break
        handle_dir = glob.glob(r'{}\vid_{}\image\*'.format(name, i))  # 首先定义文件夹的路径
        len_j = len(handle_dir)
        j = 0
        while 1:
            if j >= len_j:
                break
            os.rename(handle_dir[j], r'{}\vid_{}\image\{}.mp4'.format(name, i, j))  # 执行重命名
            j += 1
        i += 1
