"""
飞机的抽象
"""
import pygame

import constants
from game.bullet import Bullet


class Plane(pygame.sprite.Sprite):
    """
    飞机基础类
    """
    # list 保存飞机图片
    plane_images = []
    # 飞机爆炸的图片
    destroy_images = []
    # 坠毁的音乐地址
    down_sound_src = None

    # 飞机的状态:True,活的
    active = True
    # 飞机发射的子弹精灵组
    bullets = pygame.sprite.Group()

    def __init__(self, screen, speed=None):
        super().__init__()
        # 屏幕对象
        self.screen = screen
        # 加载静态资源
        self.img_list = []
        self._destroy_img_list = []
        self.down_sound = None
        self.load_src()
        # 设置飞机速度
        self.speed = speed or 10  # 默认给10
        #     获取飞机位置
        self.rect = self.img_list[0].get_rect()

        # 飞机的高度和宽度
        self.plane_w, self.plane_h = self.img_list[0].get_size()

        # 游戏窗口的高度和宽度
        self.width, self.height = self.screen.get_size()

        # 改变飞机初始化位置，放在屏幕下方
        self.rect.left = int((self.width - self.plane_w) / 2)
        self.rect.top = int(self.height / 2)

    def load_src(self):
        """加载静态资源"""
        # 飞机图像
        for img in self.plane_images:
            self.img_list.append(pygame.image.load(img))
        # 飞机坠毁图像
        for img in self.destroy_images:
            self._destroy_img_list.append(pygame.image.load(img))

        # 加载坠毁音乐
        if self.down_sound_src:
            self.down_sound = pygame.mixer.music.load(self.down_sound_src)

    @property
    def image(self):
        return self.img_list[0]

    # 自己画飞机
    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """飞机向上移动"""
        self.rect.top -= self.speed

    def move_down(self):
        """飞机向下移动"""
        self.rect.top += self.speed

    def move_left(self):
        """飞机向左移动"""
        self.rect.left -= self.speed

    def move_right(self):
        """飞机向右移动"""
        self.rect.left += self.speed

    def broken_down(self):
        """飞机坠毁效果"""
        # 1.播放坠毁音乐
        if self.down_sound:
            self.down_sound.play()
        # 2.播放坠毁动画
        for img in self._destroy_img_list:
            self.screen.blit(img, self.rect)
        # 3.坠毁后
        self.active = False

    def shoot(self):
        """飞机发射子弹"""
        bullet = Bullet(self.screen, self, 15)
        self.bullets.add(bullet)


class OurPlane(Plane):
    """我方飞机"""
    # list 保存飞机图片
    plane_images = [constants.OUR_PLANE_IMG_1, constants.OUR_PLANE_IMG_2]
    # 飞机爆炸的图片
    destroy_images = constants.OUR_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_sound_src = None

    def update(self, frame):
        """更新飞机的动画效果"""
        if frame % 5:
            self.screen.blit(self.img_list[0], self.rect)
        else:
            self.screen.blit(self.img_list[1], self.rect)

    def move_up(self):
        """向上移动超出范围后重置，重写方法"""
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        super().move_down()
        if self.rect.top >= self.height - self.plane_h:
            self.rect.top = self.height - self.plane_h

    def move_left(self):
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        super().move_right()
        if self.rect.left >= self.width - self.plane_w:
            self.rect.left = self.width - self.plane_w
