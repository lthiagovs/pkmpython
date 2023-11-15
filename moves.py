class Move:
    def __init__(self, animationLoop):
        self.animationLoop = animationLoop
        self.animationCount = 0
    def runMove(self):
        self.animationCount += 1
        if self.animationCount >= self.animationLoop:
            self.animationCount = 0
            return True
        return False