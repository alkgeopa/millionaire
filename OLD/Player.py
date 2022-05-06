class Player:
    def __init__(
        self,
        username: str = 'Player',
        money: int = 0,
        totalTime: float = 0,
        meanTime: float = 0,
        score: float = 0
    ) -> None:

        self.username = username
        self.money = money
        self.totalTime = totalTime
        self.meanTime = meanTime
        self.score = score