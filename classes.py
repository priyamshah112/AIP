class Counter:
    """
    Basic counter object
    """
    def __init__(self, value):
        self.value = value

    def reset(self):
        self.value = 0

    def increment(self):
        self.value += 1