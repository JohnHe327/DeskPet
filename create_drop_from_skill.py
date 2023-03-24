import os
import shutil

rootpath = os.path.join('tmp', 'spine')

drop_path = os.path.join(rootpath, 'drop')
os.makedirs(drop_path)

loop_path = os.path.join(rootpath, 'skill_loop')
end_path = os.path.join(rootpath, 'skill_end')
loop_len = len(os.listdir(loop_path))

for filename in os.listdir(end_path):
    shutil.copyfile(src=os.path.join(end_path, filename),
                    dst=os.path.join(drop_path, str(int(filename[:-4]) + loop_len).rjust(3,'0')+filename[-4:]))
for filename in os.listdir(loop_path):
    shutil.copyfile(src=os.path.join(loop_path, filename),
                    dst=os.path.join(drop_path, filename[:-4].rjust(3,'0')+filename[-4:]))
