'''
原版桌面宠物红
作者：守陵人渊云
b站：python降临到我身边
转载时请注明出处

修改版桌面宠物麦哲伦
作者：逋逋
b站：逋逋噗逋逋

修改版桌面宠物安洁莉娜
重构全部动作逻辑
作者：JohnHe
'''
import os
import random
import sys
import win32api
import win32con
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QPainter, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu

class MainWindows(QWidget):

    def __init__(self):
        # 调用父类初始化函数
        super(MainWindows, self).__init__()
        #去掉边框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
                            | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 当前宠物
        self.resource = 'deskpet'

        # 初始化菜单，托盘与右键人物用同一套菜单
        self.menu_init()
        self.tray_init()
        self.right_press_menu()

        # flags
        self.end_drop_flag = False  # 落地动作
        self.relax_flag = False
        self.Geocentric_travel_notes = False  # 人为拖下去
        self.poke_flag = False  # 戳一戳
        self.sit_flag = False
        self.sleep_flag = False
        self.attack_flag = False
        self.skill_begin_flag = False
        self.skill_loop_flag = False
        self.skill_end_flag = False
        self.special_flag = False
        # 运动方向与长度
        self.move_direction = 0  # 1,-1
        self.move_distance = 0
        self.die_flag = False
        self.idle_flag = False

        self.left_press_flag = False
        self.right_press_flag = False  # 右键是否按下

        # 动作重复次数上下限
        self.MAX_RELAX_LOOP = 3

        self.MIN_SIT_LOOP = 3
        self.MAX_SIT_LOOP = 10

        self.MIN_SLEEP_LOOP = 3
        self.MAX_SLEEP_LOOP = 7

        self.MIN_ATTACK_LOOP = 5
        self.MAX_ATTACK_LOOP = 10

        self.MIN_SKILL_LOOP = 3
        self.MAX_SKILL_LOOP = 10

        self.image_index = 0  # 播放序列第几张图
        self.img_repeat_count = 0  # 当前图片重复播放了几次
        self.MAX_REPEAT_COUNT = 1  # 同一张图重复播放多少次

        # 扫描各图像包图像量
        self.RELAX_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'relax')))
        self.DROP_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'drop')))
        self.MOVE_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'move')))
        self.POKE_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'poke')))
        self.SIT_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'sit')))
        self.SLEEP_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'sleep')))
        self.ATTACK_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'attack')))
        self.SKILL_BEGIN_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'skill_begin')))
        self.SKILL_LOOP_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'skill_loop')))
        self.SKILL_END_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'skill_end')))
        self.SPECIAL_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'special')))
        self.DIE_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'die')))
        self.IDLE_MAX_INDEX = len(
            os.listdir(os.path.join(self.resource, 'left', 'idle')))

        # 图像刷新频率(ms)
        self.image_refresh_rate = 1

        # 当前动作重复次数
        self.action_loop_count = 0
        self.ACTION_MAX_LOOP = 0

        # 步长
        self.step_length = 2

        # 牛顿棺材板部分
        self.delta_x = 0
        self.delta_y = 0
        self.Gravity_velocity = 0  # 当前速度
        self.Gravitational_acceleration = 1  # 重力加速度

        # 设置窗口的尺寸
        self.resize(1920, 1080)

        # 边界
        # x: -260 ~ 1920-410
        # y: -400 ~ 1080-435
        # print(win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
        # TODO: how to ensure boundings?
        self.left_bound = -260
        self.right_bound = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) -410
        self.up_bound = -400
        self.down_bound = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) - 435

        # 当前图片位置(左上角)
        self.position_x = random.randint(self.left_bound, self.right_bound)
        self.position_y = self.up_bound

        self.face_direction = random.choice(['left', 'right'])
        self.path = os.path.join(self.resource, self.face_direction, 'skill_loop', '0.png')

        self.timer = QTimer()
        self.timer.start(self.image_refresh_rate)
        self.timer.timeout.connect(self.Central_processor)

    # 中心处理器
    # 优先级：
    # 是否die
    # 是否坠落
    # 是否落地
    # 是否relax
    # 是否sit
    # 是否sleep
    # 是否attack
    # 是否skill
    # 是否poke
    # 是否special
    # 是否move
    # 下一个动作判断
        # # 是否idle（idle是带装备的relax）
        # attack 以一个idle收尾
    def Central_processor(self):
        # die
        if self.die_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'die',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.DIE_MAX_INDEX:
                self.die_flag = False
                self.image_index = 0
                self.close()
                sys.exit()
                self.MAX_REPEAT_COUNT = 1
                self.clear_flags()
                self.relax_flag = True
                self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
        ###落地及后续动作###
        # 坠落
        elif self.sit_flag == False and self.position_y != self.down_bound:
            if self.position_y > self.down_bound:
                self.Geocentric_travel_notes = True
            self.the_coffin_board_of_Newton()
            self.repaint()
        
        # 落地
        elif self.end_drop_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction,
                                     'skill_loop',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SKILL_LOOP_MAX_INDEX:
                self.end_drop_flag = False
                self.skill_end_flag = True
                self.image_index = 0
        
        # skill end
        elif self.skill_end_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction,
                                     'skill_end',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SKILL_END_MAX_INDEX:
                self.skill_end_flag = False
                self.relax_flag = True
                self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                self.image_index = 0

        # relax
        elif self.relax_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'relax',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.RELAX_MAX_INDEX:
                self.action_loop_count += 1
                if self.action_loop_count >= self.ACTION_MAX_LOOP:
                    self.action_loop_count = 0
                    self.relax_flag = False
                self.image_index = 0

        # sit
        elif self.sit_flag == True:
            if self.img_repeat_count == 0:
                if self.image_index == 0 and self.action_loop_count == 0:
                    self.position_y -= 50
                    if self.face_direction == 'right':
                        self.position_x += 30
                    else:
                        self.position_x -= 30
                self.path = os.path.join(self.resource, self.face_direction, 'sit',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SIT_MAX_INDEX:
                self.action_loop_count += 1
                if self.action_loop_count >= self.ACTION_MAX_LOOP:
                    self.action_loop_count = 0
                    self.sit_flag = False
                    self.position_y += 50
                    if self.face_direction == 'right':
                        self.position_x -= 30
                    else:
                        self.position_x += 30
                    self.relax_flag = True
                    self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                self.image_index = 0
        
        # sleep
        elif self.sleep_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'sleep',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SLEEP_MAX_INDEX:
                self.action_loop_count += 1
                if self.action_loop_count >= self.ACTION_MAX_LOOP:
                    self.action_loop_count = 0
                    self.sleep_flag = False
                    self.relax_flag = True
                    self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                self.image_index = 0
        
        # attack_flag
        elif self.attack_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'attack',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.ATTACK_MAX_INDEX:
                self.action_loop_count += 1
                if self.action_loop_count >= self.ACTION_MAX_LOOP:
                    self.action_loop_count = 0
                    self.attack_flag = False
                    self.idle_flag = True
                self.image_index = 0

        # idle
        elif self.idle_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction,
                                     'idle',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.IDLE_MAX_INDEX:
                self.idle_flag = False
                self.relax_flag = True
                self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                self.image_index = 0

        # skill begin
        elif self.skill_begin_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'skill_begin',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SKILL_BEGIN_MAX_INDEX:
                self.skill_begin_flag = False
                self.skill_loop_flag = True
                self.image_index = 0

        # skill loop
        elif self.skill_loop_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'skill_loop',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SKILL_LOOP_MAX_INDEX:
                self.action_loop_count += 1
                if self.action_loop_count >= self.ACTION_MAX_LOOP:
                        self.action_loop_count = 0
                        self.skill_loop_flag = False
                        self.skill_end_flag = True
                self.image_index = 0

        # poke
        elif self.poke_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'poke',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.POKE_MAX_INDEX:
                self.poke_flag = False
                self.relax_flag = True
                self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                self.image_index = 0

        # special
        elif self.special_flag == True:
            if self.img_repeat_count == 0:
                self.path = os.path.join(self.resource, self.face_direction, 'special',
                                     str(self.image_index) + '.png')
                self.repaint()
            self.img_repeat_count += 1
            self.same_image_repeat_check()
            if self.image_index >= self.SPECIAL_MAX_INDEX:
                self.special_flag = False
                self.relax_flag = True
                self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                self.image_index = 0

        # move
        elif self.move_direction != 0:
            if self.move_distance > 0:
                if self.img_repeat_count == 0:
                    if self.image_index >= self.MOVE_MAX_INDEX:
                        self.image_index = 0
                    self.path = os.path.join(self.resource, self.face_direction,
                                                'move',
                                                str(self.image_index) + '.png')
                self.position_x = self.position_x + self.step_length * self.move_direction
                self.move_distance -= self.step_length
                if self.position_x >= self.right_bound:
                    self.move_distance = 0
                    self.position_x = self.right_bound
                elif self.position_x <= self.left_bound:
                    self.move_distance = 0
                    self.position_x = self.left_bound
                self.repaint()
                self.img_repeat_count += 1
                self.same_image_repeat_check()
            else:
                next_step = random.randint(1, 10)
                if 1 <= next_step <= 7:
                    self.move_distance = 0
                    self.move_direction = 0
                    self.relax_flag = True
                    self.ACTION_MAX_LOOP = random.randint(1, self.MAX_RELAX_LOOP)
                    self.image_index = 0
                else:
                    # 可能转向继续走
                    dst_positionx = random.randint(self.left_bound, self.right_bound)
                    if dst_positionx < self.position_x:
                        self.move_direction = -1
                        self.face_direction = 'left'
                        self.move_distance = self.position_x - dst_positionx
                    elif dst_positionx > self.position_x:
                        self.move_direction = 1
                        self.face_direction = 'right'
                        self.move_distance = dst_positionx - self.position_x
                    else:
                        self.move_direction = 0
        # next action
        else:
            choices = ['sit', 'sleep', 'attack', 'skill', 'special', 'move_left', 'move_right']
            # # debug use
            # choices = ['sit', 'move_left', 'move_right']

            if self.right_bound - self.position_x < self.step_length * self.MOVE_MAX_INDEX:
                choices.remove('move_right')
            if self.position_x - self.left_bound < self.step_length * self.MOVE_MAX_INDEX:
                choices.remove('move_left')

            next_action = random.choice(choices)

            if next_action == 'sit':
                self.sit_flag = True
                self.ACTION_MAX_LOOP = random.randint(self.MIN_SIT_LOOP, self.MAX_SIT_LOOP)
            elif next_action == 'sleep':
                self.sleep_flag = True
                self.ACTION_MAX_LOOP = random.randint(self.MIN_SLEEP_LOOP, self.MAX_SLEEP_LOOP)
            elif next_action == 'attack':
                self.attack_flag = True
                self.ACTION_MAX_LOOP = random.randint(self.MIN_ATTACK_LOOP, self.MAX_ATTACK_LOOP)
            elif next_action == 'skill':
                self.skill_begin_flag = True
                self.ACTION_MAX_LOOP = random.randint(self.MIN_SKILL_LOOP, self.MAX_SKILL_LOOP)
            elif next_action == 'special':
                self.special_flag = True
            elif next_action == 'move_left':
                self.face_direction = 'left'
                self.move_direction = -1
                dst_positionx = random.randint(self.left_bound, self.position_x-self.step_length*self.MOVE_MAX_INDEX)
                self.move_distance = self.position_x - dst_positionx
            elif next_action == 'move_right':
                self.face_direction = 'right'
                self.move_direction = 1
                dst_positionx = random.randint(self.position_x+self.step_length*self.MOVE_MAX_INDEX, self.right_bound)
                self.move_distance = dst_positionx - self.position_x

    def the_coffin_board_of_Newton(self):
        self.position_x = self.position_x + self.delta_x
        self.position_y = self.position_y + self.delta_y + self.Gravity_velocity
        self.Gravity_velocity += self.Gravitational_acceleration
        if self.Geocentric_travel_notes == False:
            if self.position_y >= self.down_bound:
                self.position_y = self.down_bound
                self.end_drop_flag = True
                self.the_coffin_board_of_Newton_flag = False
                self.delta_x = 0
                self.delta_y = 0
                self.Gravity_velocity = 0
                self.image_index = 0
        else:
            if self.position_y > self.down_bound + 300:
                self.position_y = self.up_bound
                self.Geocentric_travel_notes = False
        # 左右穿墙
        if self.position_x > self.right_bound:
            self.position_x = self.left_bound
        elif self.position_x < self.left_bound:
            self.position_x = self.right_bound

    def clear_flags(self):
        self.image_index = 0
        self.img_repeat_count = 0
        self.end_drop_flag = False
        self.relax_flag = False
        self.Geocentric_travel_notes = False 
        self.poke_flag = False
        self.sit_flag = False
        self.sleep_flag = False
        self.attack_flag = False
        self.skill_begin_flag = False
        self.skill_loop_flag = False
        self.skill_end_flag = False
        self.special_flag = False
        self.move_direction = 0
        self.move_distance = 0
        self.Gravity_velocity = 0
        self.left_press_flag = False
        self.right_press_flag = False
        self.idle_flag = False
    
    # 鼠标相关代码
    # 一次性（检测鼠标按下）
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.buttons() == QtCore.Qt.LeftButton:  # 左键 绑定
            # self.mouse_drag_pos = ev.globalPos() - self.pos()
            self.left_press_flag = True
        elif ev.buttons() == QtCore.Qt.RightButton:  # 右键 绑定
            self.right_press_flag = True

    # 只要鼠标按下循环触发
    def mouseMoveEvent(self, event):
        self.timer.stop()
        self.poke_flag = False
        self.delta_x = int((QCursor.pos().x() - 332 - self.position_x) / 5)
        self.delta_y = int((QCursor.pos().y() - 231 - self.position_y) / 5)
        self.position_x = QCursor.pos().x() - 332
        self.position_y = QCursor.pos().y() - 231
        if self.delta_x > 0:
            self.face_direction = 'right'
        elif self.delta_x < 0:
            self.face_direction = 'left'
        self.path = os.path.join(self.resource, self.face_direction, 'skill_loop',
                                 '0.png')
        self.repaint()

    # 重写鼠标抬起事件
    def mouseReleaseEvent(self, event):
        if self.position_y == self.down_bound:
            self.clear_flags()
            self.poke_flag = True
        else:
            self.clear_flags()
        
        self.timer.start(self.image_refresh_rate)

    def paintEvent(self, event):
        qp = QPainter(self)
        # 装载图像
        image = QImage(self.path)
        rect3 = QRect(self.position_x, self.position_y,
                      int(image.width() * 1 / 4),
                      int(image.height() * 1 / 4))  #修改小人大小
        qp.drawImage(rect3, image)

    def menu_init(self):
        quit_action = QAction('退出', self,
                              triggered=self.quit)  # 设置右键点开能看到的选项与相应功能
        # quit_action.setIcon(QIcon('deskpet\\0.png'))  # 设置右键点开时左边的图片
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)  # 添加功能（猜的）

    def tray_init(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('deskpet\\0.png'))  # 托盘图案
        self.tray_icon.setContextMenu(self.tray_icon_menu)  # 绑定功能
        self.tray_icon.show()  # show

    def right_press_menu(self):
        # 将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)

    def showMenu(self):
        self.tray_icon_menu.exec_(QCursor.pos())  # 在鼠标位置显示

    def same_image_repeat_check(self):
        if self.img_repeat_count >= self.MAX_REPEAT_COUNT:
            self.image_index += 1
            self.img_repeat_count = 0

    def quit(self):
        self.MAX_REPEAT_COUNT = 50
        self.die_flag = True
        self.clear_flags()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('deskpet\\0.png'))

    main = MainWindows()
    main.show()
    # 进入程序主循环
    sys.exit(app.exec_())
