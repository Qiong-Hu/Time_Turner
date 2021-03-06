# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import get_backend
import time
import numpy as np
import winsound
import json

class Time_Turner(object):
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']

        # Params for plot
        self.linewidth = 6
        self.gap = 0.17
        self.base_pos = [[1, 1], [2.5, 1], [4.5, 1], [6, 1]]

        self.register_rules()
        self.register_turning_point()
        self.register_exempt_time()

    def register_rules(self):
        with open("time_turner_content.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            if not line.startswith("#") and len(line) > 0:
                if line.lstrip('{"').startswith("rule_turning_point"):
                    self.rule_turning_point = json.loads(line)["rule_turning_point"]
                if line.lstrip('{"').startswith("rule_ref_turning_point"):
                    self.rule_ref_turning_point = json.loads(line)["rule_ref_turning_point"]
                if line.lstrip('{"').startswith("rule_speed"):
                    self.rule_speed = json.loads(line)["rule_speed"]
                if line.lstrip('{"').startswith("rule_name"):
                    self.rule_name = json.loads(line)["rule_name"]
                if line.lstrip('{"').startswith("rule_exempt_period"):
                    self.rule_exempt_period = json.loads(line)["rule_exempt_period"]

    # map num 0-9 to index in digital display
    def num_to_lineindex(self, num):
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

    def lineindex_to_line(self, index):
        gap = self.gap
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
    def num_to_digit(self, ax, num, digit):
        for each_index in self.num_to_lineindex(num):
            xlist, ylist = self.lineindex_to_line(each_index)
            ax.plot(np.array(xlist) + self.base_pos[digit][0], np.array(ylist) + self.base_pos[digit][1], 'k', linewidth = self.linewidth)

    # hour = 0-23, minute = 00-59
    def plot_time(self, ax, hour, minute, task_name = ""):
        # Plot four digit
        self.num_to_digit(ax, int(hour/10), 0)
        self.num_to_digit(ax, int(hour%10), 1)
        self.num_to_digit(ax, int(minute/10), 2)
        self.num_to_digit(ax, int(minute%10), 3)

        # Two points in the middle of clock
        ax.plot(4, 1.5, 'ok', markersize = self.linewidth)
        ax.plot(4, 2.5, 'ok', markersize = self.linewidth)

        # Write the task name
        ax.text(4, 0, task_name, fontsize = 15, horizontalalignment = "center", verticalalignment = "center")

    def ax_standard(self, ax):
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

    def hour_to_minute(self, hour, minute):
        return 60*hour+minute

    def minute_to_hour(self, minute):
        return int(int(minute/60)%24), int(minute%60)

    def time_transform(self, hour, minute):
        time_cal = self.hour_to_minute(hour, minute)
        time_new = 0

        hour_new = 0
        minute_new = 0
        task_name = ""

        for rule_idx in range(len(self.real_turning_point) - 1):
            if self.real_turning_point[rule_idx] <= time_cal < self.real_turning_point[rule_idx + 1]:
                time_new = self.rule_speed[rule_idx] * (time_cal - self.real_turning_point[rule_idx]) + self.ref_turning_point[rule_idx]
                if len(self.rule_name) > 0:
                	task_name = self.rule_name[rule_idx] + "????????????" + self.rule_name[rule_idx] + "??????????????????"
                break

        hour_new, minute_new = self.minute_to_hour(time_new)
        return hour_new, minute_new, task_name

    def register_turning_point(self):
        self.real_turning_point = []
        for each in self.rule_turning_point:
            self.real_turning_point.append(self.hour_to_minute(each[0], each[1]))

        self.ref_turning_point = []
        for each in self.rule_ref_turning_point:
            self.ref_turning_point.append(self.hour_to_minute(each[0], each[1]))

    def register_exempt_time(self):
        self.exempt_time = []
        # exempt_time format = [weekday, start time (minute), end time (minute)]
        for each in self.rule_exempt_period:
            self.exempt_time.append([each[0], self.hour_to_minute(each[1], each[2]), self.hour_to_minute(each[3], each[4])])

    # print(time.localtime(time.time()))
    # tm_mon=7, tm_mday=12
    # tm_hour=1, tm_min=29
    # tm_wday=6

    # Main function begins here
    def main(self):
        fig, ax = plt.subplots(1, 1, figsize=(4,2))
        fig.canvas.set_window_title("Time Turner")
        
        mngr = plt.get_current_fig_manager()
        if get_backend() == "Qt5Agg":
            fig.canvas.manager.window.move(625, 0)
            fig.canvas.toolbar.setVisible(False)
        elif get_backend() == "TkAgg":
            fig.canvas.manager.window.wm_geometry("+880+0")
            fig.canvas.toolbar.pack_forget()

        fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

        while True:
            plt.cla()

            hour = time.localtime(time.time()).tm_hour
            minute = time.localtime(time.time()).tm_min

            hour_new = 0
            minute_new = 0
            task_name = ""

            exempt_flag = False
            for each_exempt in self.exempt_time:
                # tm_wday = weekday - 1 (because start from 0)
                if time.localtime(time.time()).tm_wday+1 == each_exempt[0] and each_exempt[1] <= self.hour_to_minute(hour, minute) < each_exempt[2]:
                    hour_new = hour
                    minute_new = minute
                    exempt_flag = True
                    break
            if exempt_flag == False:
                hour_new, minute_new, task_name = self.time_transform(hour, minute)

            self.plot_time(ax, hour_new, minute_new, task_name)
            if minute == 0:
                winsound.Beep(440, 200)
            if self.hour_to_minute(hour, minute) in self.real_turning_point:
                if minute == 0:
                    [winsound.Beep(440, 200) for _ in range(3)]
                else:
                    [winsound.Beep(440, 200) for _ in range(4)]

            self.ax_standard(ax)
            
            fig.tight_layout()
            fig.set_size_inches((4, 2))

            plt.pause(20)
        plt.ioff()

time_turner = Time_Turner()
time_turner.main()
