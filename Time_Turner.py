import matplotlib.pyplot as plt
import time
import numpy as np
import winsound

# params for plot
linewidth = 6
gap = 0.17
base_pos = [[1, 1], [2.5, 1], [4.5, 1], [6, 1]]


# map num 0-9 to index in digital display
def num_to_lineindex(num):
    index = []
    if num == 0:
        index = [0, 1, 2, 4, 5, 6]
    elif num == 1:
        index = [2, 5]
    elif num == 2:
        index = [0, 2, 3, 4, 6]
    elif num == 3:
        index = [0, 2, 3, 5, 6]
    elif num == 4:
        index = [1, 2, 3, 5]
    elif num == 5:
        index = [0, 1, 3, 5, 6]
    elif num == 6:
        index = [0, 1, 3, 4, 5, 6]
    elif num == 7:
        index = [0, 2, 5]
    elif num == 8:
        index = [0, 1, 2, 3, 4, 5, 6]
    elif num == 9:
        index = [0, 1, 2, 3, 5, 6]
    return index

def lineindex_to_line(index):
    xlist = []
    ylist = []

    if index == 0:
        xlist = [0+gap, 1-gap]
        ylist = [2, 2]
    elif index == 1:
        xlist = [0, 0]
        ylist = [1+gap, 2-gap]
    elif index == 2:
        xlist = [1, 1]
        ylist = [1+gap, 2-gap]
    elif index == 3:
        xlist = [0+gap, 1-gap]
        ylist = [1, 1]
    elif index == 4:
        xlist = [0, 0]
        ylist = [0+gap, 1-gap]
    elif index == 5:
        xlist = [1, 1]
        ylist = [0+gap, 1-gap]
    elif index == 6:
        xlist = [0+gap, 1-gap]
        ylist = [0, 0]
    return xlist, ylist

# num = 0-9, digit = 0-3 (set position)
def num_to_digit(ax, num, digit):
    for each_index in num_to_lineindex(num):
        xlist, ylist = lineindex_to_line(each_index)
        ax.plot(np.array(xlist)+base_pos[digit][0], np.array(ylist)+base_pos[digit][1], 'k', linewidth = linewidth)

# hour = 0-23, minute = 00-59
def plot_time(ax, hour, minute):
    # Plot four digit
    num_to_digit(ax, int(hour/10), 0)
    num_to_digit(ax, int(hour%10), 1)
    num_to_digit(ax, int(minute/10), 2)
    num_to_digit(ax, int(minute%10), 3)

    # Two points in the middle of clock
    ax.plot(4, 1.5, 'ok', markersize=linewidth)
    ax.plot(4, 2.5, 'ok', markersize=linewidth)

def ax_standard(ax):
    # Plot a square as edge
    xlim = [0, 8]
    ylim = [0, 4]
    kwarg = {'linewidth': 5, 'color': 'grey', 'alpha': 1}
    ax.plot(xlim, [ylim[0], ylim[0]], **kwarg)
    ax.plot(xlim, [ylim[1], ylim[1]], **kwarg)
    ax.plot([xlim[0], xlim[0]], ylim, **kwarg)
    ax.plot([xlim[1], xlim[1]], ylim, **kwarg)

    ax.set_facecolor('lightgrey')
    ax.axis('equal')
    ax.axis("off")

def hour_to_minute(hour, minute):
    return 60*hour+minute

def minute_to_hour(minute):
    return int(int(minute/60)%24), int(minute%60)

def time_transform(hour, minute):
    time_cal = hour_to_minute(hour, minute)
    time_new = 0

    hour_new = 0
    minute_new = 0

    if 0 <= hour < 7:
        time_new = time_cal + hour_to_minute(5,30)
    elif 7 <= hour < 8:
        time_new = (time_cal - hour_to_minute(7,0)) * 2.5 + hour_to_minute(12,30)
    elif 8 <= hour < 11:
        time_new = (time_cal - hour_to_minute(8,0)) * 2/3 + hour_to_minute(2,30)
    elif 11 <= hour < 12:
        time_new = (time_cal - hour_to_minute(11,0)) * 2.5 + hour_to_minute(12,30)
    elif 12 <= hour < 16:
        time_new = (time_cal - hour_to_minute(12,0)) / 2 + hour_to_minute(2,30)
    elif hour_to_minute(16,0) <= time_cal < hour_to_minute(17,30):
        time_new = (time_cal - hour_to_minute(16,0)) * 4/3 + hour_to_minute(18,0)
    elif hour_to_minute(17,30) <= time_cal < hour_to_minute(19,0):
        time_new = time_cal - hour_to_minute(17,30) + hour_to_minute(20,0)
    elif 19 <= hour < 20:
        time_new = (time_cal - hour_to_minute(19,0)) * 3 + hour_to_minute(21,30)
    elif hour_to_minute(20,0) <= time_cal < hour_to_minute(22,30):
        time_new = (time_cal - hour_to_minute(20,0)) * 1.8 + hour_to_minute(0,30)
    elif hour_to_minute(22,30) <= time_cal < hour_to_minute(24,00):
        time_new = (time_cal - hour_to_minute(22,30)) / 3 + hour_to_minute(5,0)

    hour_new, minute_new = minute_to_hour(time_new)
    return hour_new, minute_new

time_rule_turning_point = []
time_rule_turning_point.append(hour_to_minute(0,0))
time_rule_turning_point.append(hour_to_minute(7,0))
time_rule_turning_point.append(hour_to_minute(8,0))
time_rule_turning_point.append(hour_to_minute(11,0))
time_rule_turning_point.append(hour_to_minute(12,0))
time_rule_turning_point.append(hour_to_minute(16,0))
time_rule_turning_point.append(hour_to_minute(17,30))
time_rule_turning_point.append(hour_to_minute(19,0))
time_rule_turning_point.append(hour_to_minute(20,0))
time_rule_turning_point.append(hour_to_minute(22,30))

# print(time.localtime(time.time()))
# tm_mon=7, tm_mday=12
# tm_hour=1, tm_min=29
# tm_wday=6

# Main function begins here
fig, ax = plt.subplots(figsize=(4,2))
fig.canvas.set_window_title("Time Turner")
while True:
    plt.cla()

    hour = time.localtime(time.time()).tm_hour
    minute = time.localtime(time.time()).tm_min

    hour_new = 0
    minute_new = 0

    if time.localtime(time.time()).tm_wday == 4 and 0 <= hour_to_minute(hour, minute) < hour_to_minute(13,0):
        hour_new = hour
        minute_new = minute
    else:
        hour_new, minute_new = time_transform(hour, minute)

    plot_time(ax, hour_new, minute_new)
    if hour_to_minute(hour, minute) in time_rule_turning_point:
        [winsound.Beep(440, 200) for _ in range(4)]
    
    ax_standard(ax)
    fig.tight_layout()

    plt.pause(20)
plt.ioff()


