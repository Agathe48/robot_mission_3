class Cleaning(object):
    def __init__(self):
        super().__init__()
        print("cleaning")

    def update(self):
        print("update_cleaning")

class Green(Cleaning):
    def __init__(self):
        super().__init__()
        print("green")

class Chief(Cleaning):
    def __init__(self):
        super().__init__()
        print("chief")

    def update(self):
        super().update()
        print("update chief")

class ChiefGreen(Chief, Green):
    def __init__(self):
        super().__init__()
        print("cg")

cg = ChiefGreen()
cg.update()