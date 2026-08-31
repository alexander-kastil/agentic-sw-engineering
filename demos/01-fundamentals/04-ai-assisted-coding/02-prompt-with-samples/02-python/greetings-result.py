from datetime import datetime


def get_greeting(time=None):
    if time is None:
        time = datetime.now()
    
    hour = time.hour
    
    if 5 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 20:
        return "Good Afternoon!"
    else:
        return "Good Evening!"


if __name__ == "__main__":
    print(get_greeting())
