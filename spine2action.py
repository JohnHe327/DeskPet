import os
import cv2

"""
============================
    cv2只支持纯英文路径！
============================
 """
rootpath = os.path.join(r'C:\Users\kaihong\Desktop\DeskPet\nothing')

filelist = os.listdir(rootpath + '/spine/')
for filename in filelist:
    if os.path.isdir(rootpath + '/spine/' + filename):
        continue
    new_filename = filename.split('_')[-1]
    if 'Interact' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'poke'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/poke/'+new_filename)
    elif 'Move' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'move'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/move/'+new_filename)
    elif 'Relax' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'relax'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/relax/'+new_filename)
    elif 'Skill_Start' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'skill_begin'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/skill_begin/'+new_filename)
    elif 'Skill_Loop' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'skill_loop'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/skill_loop/'+new_filename)
    elif 'Skill_End' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'skill_end'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/skill_end/'+new_filename)
    elif 'Sit' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'sit'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/sit/'+new_filename)
    elif 'Sleep' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'sleep'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/sleep/'+new_filename)
    elif 'Special' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'special'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/special/'+new_filename)
    elif 'Die' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'die'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/die/'+new_filename)
    elif 'Charge Idle' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'charge_idle'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/charge_idle/'+new_filename)
    elif 'Idle_Charge' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'idle_charge'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/idle_charge/'+new_filename)
    elif 'Idle_2_' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'idle_2'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/idle_2/'+new_filename)
    elif 'Idle' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'idle'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/idle/'+new_filename)
    elif 'Start' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'start'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/start/'+new_filename)
    elif 'Stun' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'stun'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/stun/'+new_filename)
    elif 'Attack' in filename:
        os.makedirs(os.path.join(rootpath, 'spine', 'attack'), exist_ok=True)
        os.rename(rootpath+'/spine/'+filename, rootpath+'/spine/attack/'+new_filename)

os.makedirs(os.path.join(rootpath, 'right'), exist_ok=True)
os.makedirs(os.path.join(rootpath, 'left'), exist_ok=True)
for folder_name in os.listdir(rootpath + '/spine/'):
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
