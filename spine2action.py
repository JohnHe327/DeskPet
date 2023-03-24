import os
import cv2

"""
============================
    cv2只支持纯英文路径！
============================
 """
rootpath = os.path.join('tmp')

filelist = os.listdir(os.path.join(rootpath, 'spine'))
for filename in filelist:
    if os.path.isdir(os.path.join(rootpath, 'spine', filename)):
        continue
    if 'Default' in filename:
        continue
    new_filename = filename.split('-')[-1]
    folder_name = '_'.join(new_filename.split('_')[:-1]).lower()
    new_filename = filename.split('_')[-1]
    os.makedirs(os.path.join(rootpath, 'spine', folder_name), exist_ok=True)
    os.rename(src=os.path.join(rootpath, 'spine', filename),
              dst=os.path.join(rootpath, 'spine', folder_name, new_filename))

if os.path.isdir(os.path.join(rootpath, 'spine', 'interact')):
    os.rename(os.path.join(rootpath, 'spine', 'interact'), os.path.join(rootpath, 'spine', 'poke'))

expect_folders = ['relax', 'move', 'sit', 'sleep', 'special', 'poke', 'start', 'drop', 'idle', 'attack', 'skill_begin', 'skill_loop', 'skill_end', 'die']

os.makedirs(os.path.join(rootpath, 'right'), exist_ok=True)
os.makedirs(os.path.join(rootpath, 'left'), exist_ok=True)
for folder_name in os.listdir(os.path.join(rootpath, 'spine')):
    folder_path = os.path.join(rootpath, 'spine', folder_name)
    if os.path.isdir(folder_path):
        os.makedirs(os.path.join(rootpath, 'right', folder_name), exist_ok=True)
        os.makedirs(os.path.join(rootpath, 'left', folder_name), exist_ok=True)
        filelist = os.listdir(folder_path)
        filelist.sort()
        for idx, filename in enumerate(filelist):
            img_path = os.path.join(folder_path, filename)
            img_right = cv2.imread(img_path, -1)
            img_left = cv2.flip(img_right, 1)
            right_path = os.path.join(rootpath, 'right', folder_name, str(idx)+'.png')
            left_path = os.path.join(rootpath, 'left', folder_name, str(idx)+'.png')
            cv2.imwrite(right_path, img_right)
            cv2.imwrite(left_path, img_left)
        if folder_name in expect_folders:
            expect_folders.remove(folder_name)
if len(expect_folders):
    print('可能需要这些文件夹，但未自动生成: ', expect_folders)
