import sys

import pygame

import constants
from game.plane import Plane, OurPlane, SmallEnemyPlane
from game.war import PlaneWar


def main():
    """游戏入口，main方法"""
    war = PlaneWar()
    # 添加敌方飞机
    war.add_small_enemies(6)
    war.run_game()

if __name__ == '__main__':
    main()

    # print(pygame.font.get_fonts())