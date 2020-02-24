import pygame
import sys

import constants
from game.plane import OurPlane, SmallEnemyPlane
from store.result import PlayRest


class PlaneWar(object):
    """飞机大战"""

    # 游戏状态 0.准备中，1.游戏中，2.游戏结束
    READY = 0
    PLAYING = 1
    OVER = 2
    status = READY

    # 实例化飞机对象
    our_plane = None

    frame = 0  # 播放帧数

    # 敌方小飞机精灵组，可以属于多个精灵组，便于碰撞检测
    small_enemies = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    # 游戏结果
    rest = PlayRest()


    def __init__(self):
        # 初始化游戏
        pygame.init()

        # 指定屏幕高度、宽度
        self.width, self.height = 480, 852

        # 屏幕对象
        self.screen = pygame.display.set_mode((self.width, self.height))

        # 设置窗口标题
        pygame.display.set_caption('飞机大战')

        # 加载背景图片
        self.bg = pygame.image.load(constants.BG_IMG)
        self.bg_over = pygame.image.load(constants.BG_IMG_OVER)

        # 加载游戏标题
        self.img_game_title = pygame.image.load(constants.IMG_GAME_TITLE)
        self.img_game_title_rect = self.img_game_title.get_rect()
        # 标题高度和宽度
        self.t_width, self.t_height = self.img_game_title.get_size()

        self.img_game_title_rect.topleft = (int((self.width - self.t_width) / 2),
                                            int(self.height / 2 - self.t_height))

        # 开始按钮
        self.btn_start = pygame.image.load(constants.IMG_GAME_START_BTN)
        self.btn_start_rect = self.btn_start.get_rect()
        self.btn_width, self.btn_height = self.btn_start.get_size()
        self.btn_start_rect.topleft = (int((self.width - self.btn_width) / 2),
                                       int(self.height / 2 + self.btn_height))

        # 游戏文字对象
        self.score_font = pygame.font.SysFont('arial', 32)

        # 加载背景音乐
        pygame.mixer.music.load(constants.BG_MUSIC)
        # 无限循环播放
        pygame.mixer.music.play(-1)
        # 设置音量
        pygame.mixer.music.set_volume(0.3)

        # 上次按的键盘
        self.key_down = None

        # 实例化飞机对象
        self.our_plane = OurPlane(self.screen, speed=8)

        self.clock = pygame.time.Clock()

    def bind_event(self):
        # 1.监听事件
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #         鼠标点击进入游戏
                # 游戏正在准备中才能进入游戏
                if self.status == self.READY:
                    self.status = self.PLAYING
                elif self.status == self.OVER:
                    self.status = self.READY
                    self.add_small_enemies(6)
            elif event.type == pygame.KEYDOWN:
                #         键盘事件
                # 游戏正在游戏中，才需要控制键盘 ASWD
                self.key_down = event.key
                if self.status == self.PLAYING:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.our_plane.move_up()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.our_plane.move_down()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.our_plane.move_left()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.our_plane.move_right()
                    elif event.key == pygame.K_SPACE:
                        # 发射子弹
                        self.our_plane.shoot()

    def add_small_enemies(self, num):
        # 随机添加num架小飞机
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, 4)
            plane.add(self.small_enemies, self.enemies)

    def run_game(self):
        """游戏主循环部分"""
        while True:
            # 设置帧速率
            self.clock.tick(60)
            self.frame += 1
            if self.frame >= 60:
                self.frame = 0
            # 绑定事件
            self.bind_event()

            # 2.更新游戏的状态
            if self.status == self.READY:
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 游戏正在准备中，绘制开始画面，绘制标题
                self.screen.blit(self.img_game_title, self.img_game_title_rect)
                # 开始按钮
                self.screen.blit(self.btn_start, self.btn_start_rect)
                # 重置按键
                self.key_down = None

            elif self.status == self.PLAYING:
                #     游戏进行中
                self.screen.blit(self.bg, self.bg.get_rect())
                #     绘制飞机
                self.our_plane.update(self)
                #     绘制子弹
                self.our_plane.bullets.update(self)
                #     绘制敌方飞机
                self.small_enemies.update()
                #     游戏分数
                score_text = self.score_font.render('Score:{0}'.format(self.rest.score), False,
                                                    constants.TEXT_SCORE_COLOR)
                self.screen.blit(score_text, score_text.get_rect())

            elif self.status == self.OVER:
                #     游戏背景
                self.screen.blit(self.bg_over, self.bg_over.get_rect())
                # 分数统计
                # 1.本次总分
                score_text = self.score_font.render('{0}'.format(self.rest.score), False, constants.TEXT_SCORE_COLOR)
                score_text_rect = score_text.get_rect()
                text_w, text_h = score_text.get_size()
                # 改变文字的位置
                score_text_rect.topleft = (
                    int((self.width - text_h) / 2),
                    int(self.height / 2)
                )
                self.screen.blit(score_text, score_text_rect)
                # 2.历史最高分
                score_hist = self.score_font.render(
                    '{0}'.format(self.rest.get_max_core()), False,
                                 constants.TEXT_SCORE_COLOR
                )
                self.screen.blit(score_hist, (150, 40))
                # 刷新屏幕

            pygame.display.flip()
