import datetime

# generate a python code that takes the current time as input using the datetime module
# and returns the appropriate greeting message based on the current time.

# Example 1: Greeting message for morning
#Input: 9 AM
#Output: "Good Morning!"

# Example 2: Greeting message for afternoon
# Input: 2 PM
# Input: 7 PM
#Output: "Good Afternoon!"

# Example 3: Greeting message for evening
# Input: 9 PM
# Output: "Good Evening!"

def get_greeting_message():
    current_time = datetime.datetime.now().time()
    
    if current_time.hour < 12:
        return "Good Morning!"
    elif current_time.hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

greeting_message = get_greeting_message()
print(greeting_message)