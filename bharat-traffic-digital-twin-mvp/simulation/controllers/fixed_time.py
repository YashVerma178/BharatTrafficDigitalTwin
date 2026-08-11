class FixedTimeController:
    def __init__(self, green=30):
        self.green = green

    def choose(self, state):
        return "fixed"
