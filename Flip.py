'''
作者：逋逋
b站账号：逋逋噗逋逋

'''

import cv2
import os

src = 'left'
dst = 'right'
action = 'special'
print(src, '->', dst, ': ', action)

src_path = os.path.join('deskpet', src, action)
filelist = os.listdir(src_path)
for idx, filename in enumerate(filelist):
    old_dir = os.path.join(src_path, filename)
    if os.path.isdir(old_dir):
        continue
    new_dir = os.path.join(src_path, str(idx) + '.png')
    # os.rename(old_dir, new_dir)
    # image_src = cv2.imread(old_dir, -1)
    # cv2.imwrite(new_dir, image_src)
    dst_path = os.path.join('deskpet', dst, action, str(idx) + '.png')
    image_src = cv2.imread(new_dir, -1)
    image_dst = cv2.flip(image_src, 1)
    cv2.imwrite(dst_path, image_dst)
