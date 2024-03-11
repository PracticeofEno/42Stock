"""이평선 클래스"""

class MovingAverage:
    """이평선 클래스"""
    def __init__(self, mov_avg: int = 5):
        self.mov_avg = mov_avg
        self.list = []

    def push_data(self, data: float):
        """이평선에 데이터 추가"""
        if len(self.list) >= self.mov_avg:
            self.list.pop(0)
            self.list.append(data)
        else:
            self.list.append(data)

    def check(self):
        """이동평균선을 만들 수 있는지 확인"""
        if len(self.list) == self.mov_avg:
            return True
        return False

    def get_moving_average(self):
        """이동평균선 계산"""
        if self.check():
            return sum(self.list) / self.mov_avg
        return 0
