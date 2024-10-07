import random
import math

def time():
    time = random.randint(0, 7200000)
    # time = random.randint(3600000, 7200000) <- set time between 1 and 2 hours
    hour = math.floor(time / 3600000)
    minute = math.floor((time % 3600000) / 60000)
    second = math.floor((time % 60000) / 1000)
    millisecond = time % 1000
    hour = str(hour).zfill(1)
    minute = str(minute).zfill(2)
    second = str(second).zfill(2)
    millisecond = str(millisecond).zfill(3)
    digt_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    digit_str = hour + minute + second + millisecond
    for digit in digit_str:
        digt_counts[int(digit)] += 1
    for count in digt_counts:
        if count > 1:
            return False
    return True

success_count = 0
for i in range(1000000):
    if time():
        success_count += 1

print("Total successes:", success_count)
print("Success rate:", success_count / 1000000)


