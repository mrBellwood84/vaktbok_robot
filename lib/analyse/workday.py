class Workday:
    def __init__(self, date, code, start, end, timestamp):
        self.date = date
        self.code = code
        self.start = start
        self.end = end
        self.start_n = self.to_numeric_time(start)
        self.end_n = self.to_numeric_time(end)
        self.timestamp = timestamp

        self.worktime = self.end_n - self.start_n
        self.below_8 = self.worktime < 8
        self.above_8 = self.worktime > 8

    def to_numeric_time(self, timestring:str):
        s = timestring.split(":")
        h = int(s[0])
        m = float(s[1]) / 60
        return h + m
