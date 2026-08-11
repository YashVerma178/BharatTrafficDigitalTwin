class ActuatedController:
    def __init__(self, min_green=10, max_green=60, threshold=1.25):
        self.min_green = min_green
        self.max_green = max_green
        self.threshold = threshold

    def choose(self, ns_queue, ew_queue, elapsed):
        if elapsed < self.min_green:
            return "hold"
        if elapsed >= self.max_green:
            return "switch"
        if ns_queue > self.threshold * max(ew_queue, 1):
            return "extend_ns"
        if ew_queue > self.threshold * max(ns_queue, 1):
            return "extend_ew"
        return "hold"
