import constants


class PlayRest(object):
    """记录游戏结果"""
    __score = 0  # 总分
    __life = 3  # 生命数量
    __blood = 1000  # 生命值

    @property
    def score(self):
        """返回分数，私有变量"""
        return self.__score

    @score.setter
    def score(self, value):
        """设置分数"""
        if value < 0:
            return None
        self.__score = value

    def set_history(self):
        """记录最高分"""
        # 1.读取文件中存储的分数
        # 2.对比，更新最大数
        # 3.分数不是追加， 是替换
        if int(self.get_max_core()) < self.score:
            with open(constants.PLAY_RESULT_STORE_FILE, 'w') as f:
                f.write('{0}'.format(self.score))

    def get_max_core(self):
        """读取历史最高分"""
        rest = 0
        with open(constants.PLAY_RESULT_STORE_FILE, 'r') as f:
            r = f.read()
            if r:
                rest = r
        return rest
