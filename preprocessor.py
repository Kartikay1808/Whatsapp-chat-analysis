import regex
import pandas as pd




def preprocess(data):
    def date_time(s):
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        result = regex.match(pattern, s)
        if result:
            return True
        return False

    def find_author(s):
        s = s.split(":")
        if len(s) == 2:
            return True
        else:
            return False

    def getDatapoint(line):
        splitline = line.split(' - ')
        dateTime = splitline[0]
        date, time = dateTime.split(", ")
        message = " ".join(splitline[1:])
        if find_author(message):
            splitmessage = message.split(": ")
            author = splitmessage[0]
            message = " ".join(splitmessage[1:])
        else:
            author = None
        return date, time, author, message

    df = []
    conversation = 'Heavy Drivers.txt'
    with open(conversation, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    df.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDatapoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)
    df = pd.DataFrame(df, columns=["date", 'time', 'user', 'message'])
    df['date'] = pd.to_datetime(df['date'])
    df["time"] = pd.to_datetime(df["time"])
    df["month"] = df.date.dt.month_name()
    df["year"] = df.date.dt.year
    df["day"] = df.date.dt.day
    df["hour"] = df.time.dt.hour
    df["minute"] = df.time.dt.minute
    df = df.drop(columns=["date", "time"])

    return df