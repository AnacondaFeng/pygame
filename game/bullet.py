import pygame

import constants


class Bullet(pygame.sprite.Sprite):
    """子弹类"""

    # 子弹状态，True：活的
    active = True

    def __init__(self, screen, plane, speed=None):
        super().__init__()
        self.screen = screen
        # 速度
        self.speed = speed or 10
        self.plane = plane

        # 加载子弹的图片
        self.image = pygame.image.load(constants.BULLET_IMG)
        # 改变子弹位置
        self.rect = self.image.get_rect()
        self.rect.centerx = plane.rect.centerx
        self.rect.top = plane.rect.top

        # 发射的音乐效果
        self.shoot_sound = pygame.mixer.Sound(constants.BULLET_SHOOT_SOUND)
        self.shoot_sound.set_volume(0.3)
        self.shoot_sound.play()

    def update(self, *args):
        """ 更新子弹位置 """
        self.rect.top -= self.speed
        # 超出屏幕范围
        if self.rect.top < 0:
            self.remove(self.plane.bullets)
            print(self.plane.bullets)
        # 绘制子弹
        self.screen.blit(self.image, self.rect)
