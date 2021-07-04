from math import sqrt, floor
from random import uniform, randint
from const import *
from device import Device, Malicious_Device
import matplotlib.pyplot as plt


class ASP():
    def __init__(self, ratio, num):
        self.bandwidth = ASP_BANDWIDTH
        self.frequency = MPO_CPU_FREQUENCY
        self.device_list = []
        self.mal_device_list = []
        self.malicious_ratio = ratio
        self.num_of_normal_users = num
        self.num_of_malicious_users = int(self.num_of_normal_users * self.malicious_ratio)
        self.set_users()
        self.set_service_rate()
        self.set_arrival_rate()
        self.total_pay()
        self.mpo_price = None
        self.chi = 0.999
        self.gamma = 100
        self.phi = 0

    def set_users(self):
        for i in range(self.num_of_normal_users):
            self.device_list.append(Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
        for i in range(self.num_of_malicious_users):
            self.mal_device_list.append(Malicious_Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))

    def total_pay(self):
        self.total_payment = 0
        for dev in self.device_list:
            self.total_payment += dev.price_per_task

    def set_service_rate(self):
        tot_cpu_cycle = 0
        for dev in self.device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        for dev in self.mal_device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        self.service_rate = self.frequency / (tot_cpu_cycle / (self.num_of_normal_users + self.num_of_malicious_users))

    def set_arrival_rate(self):
        self.arrival_rate = 0
        for dev in self.device_list:
            self.arrival_rate += dev.arrival_rate
        for dev in self.mal_device_list:
            self.arrival_rate += dev.arrival_rate

    def set_mpo_price(self, price):
        self.mpo_price = price

    def set_utility(self):
        util = 0
        for dev in self.device_list:
            util += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.process_time - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
        self.utility = util - self.mpo_price * self.z_v
        return

    def time(self, z_v, z_h):
        return 1 / ((z_v - z_h) * self.service_rate - (self.arrival_rate - ASP_H(z_h)))

    def set_boundary(self):
        z_v = (self.arrival_rate + self.gamma) / self.service_rate
        z_h = self.chi * z_v
        util1 = 0
        util2 = 0
        for dev in self.device_list:
            util1 += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.time(z_v, z_h) - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
            util2 += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.time(z_v, 0) - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
        if GLOBAL_ETA > self.service_rate:
            self.bound = util1 / z_v
            self.qbound = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)) / (z_v - self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)) ** 2
        else:
            self.bound = util2 / z_v
            self.qbound = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1) * self.service_rate)) / (z_v - self.arrival_rate / ((1) * self.service_rate)) ** 2
        return

    def set_process_time(self):
        self.process_time = 1 / ((self.z_v - self.z_h) * self.service_rate - (self.arrival_rate - ASP_H(self.z_h)))

    def optimize_zv(self):
        if GLOBAL_ETA > self.service_rate:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
            if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
            self.z_h = self.chi * self.z_v
            self.set_process_time()
            self.set_utility()
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h):
                print('infeasible')
            if self.utility < 0:
                self.z_v = 0
                self.utility = 0

        else:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
            self.z_h = 0
            if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h):
                print('infeasible')
                self.z_h = 0
            self.set_process_time()
            self.set_utility()
            if self.utility < 0:
                self.z_v = 0
                self.utility = 0


    def set_malicious_ratio(self, ratio):
        self.malicious_ratio = ratio

    def set_zv_zh(self, chi):
        self.chi = chi
        self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
        if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
            self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
        self.z_h = self.chi * self.z_v
        self.set_process_time()
        self.set_utility()
        if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h):
            print('infeasible')
        if self.utility < 0:
            self.z_v = 0
            self.utility = 0

    def plot_max(self):
        mpo_lst = [100, 300, 500, 700, 900]
        color_dict = {100: 'red', 300: 'darkorange', 500: 'indigo', 700: 'darkgreen', 900: 'darkblue'}
        if GLOBAL_ETA > self.service_rate:

            plt.figure(figsize=(42, 25), dpi=400)
            for mpo_price in mpo_lst:
                self.mpo_price = mpo_price
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
                self.z_h = self.chi * self.z_v
                ut = []
                z_v = []
                self.set_process_time()
                self.set_utility()
                plt.scatter(self.z_v, self.utility, color=color_dict[mpo_price], marker='^')
                for i in range(450, 1000):
                    self.z_v = i / 10
                    self.z_h = self.chi * self.z_v
                    self.set_process_time()
                    self.set_utility()
                    z_v.append(self.z_v)
                    ut.append(self.utility)
                plt.plot(z_v, ut, marker='.', color=color_dict[mpo_price], linestyle='-.', label=f"MPO price:{mpo_price}")
                plt.legend(loc="best")
                z_v = []
                ut = []
            plt.xlabel(r'$\bf{Purchased\ VM}$', fontsize=100)
            plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
            plt.xticks(fontsize=80)
            plt.yticks(fontsize=80)
            plt.legend(loc="best", fontsize=100)
            plt.savefig('./5GDDoS_Game_asp_utility_case1.pdf')
            plt.savefig('./5GDDoS_Game_asp_utility_case1.jpg')
            plt.close()
        else:
            plt.figure(figsize=(42, 25), dpi=400)
            for mpo_price in mpo_lst:
                self.mpo_price = mpo_price
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
                self.z_h = 0
                ut = []
                z_v = []
                self.set_process_time()
                self.set_utility()
                plt.scatter(self.z_v, self.utility, color=color_dict[mpo_price], marker='^')
                for i in range(450, 1000):
                    self.z_v = i /10
                    self.z_h = 0
                    self.set_process_time()
                    self.set_utility()
                    z_v.append(self.z_v)
                    ut.append(self.utility)
                plt.plot(z_v, ut, marker='.', color=color_dict[mpo_price], linestyle='-.', label=f"MPO price:{mpo_price}")
                plt.legend(loc="best")
                ut = []
                z_v = []
            plt.xlabel(r'$\bf{Purchased\ VM}$', fontsize=100)
            plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
            plt.xticks(fontsize=80)
            plt.yticks(fontsize=80)
            plt.legend(loc="best", fontsize=100)
            plt.savefig('./5GDDoS_Game_asp_utility_case2.pdf')
            plt.savefig('./5GDDoS_Game_asp_utility_case2.jpg')
            plt.close()

    def plot_max_zh(self):
        if GLOBAL_ETA > self.service_rate:
            self.mpo_price = 100
            ut = []
            z_h = []
            plt.figure(figsize=(42, 25), dpi=400)
            for z in range(1000, 1005, 1):
                self.z_v = z / 1000
                for i in range(11):
                    i = i / 10
                    self.z_h = self.z_v * i
                    self.set_process_time()
                    self.set_utility()
                    z_h.append(i)
                    ut.append(self.utility)
                plt.plot(z_h, ut, marker='.', linestyle='-.', label=f"VM :{self.z_v}", linewidth=7)
                ut = []
                z_h = []
            plt.xlabel(r'$\bf{IPS\ VM\ ratio}$', fontsize=100)
            plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
            plt.xticks(fontsize=80)
            plt.yticks(fontsize=80)
            plt.legend(loc="best", fontsize=100)
            plt.savefig('./5GDDoS_Game_asp_utility_z_h_case1.pdf')
            plt.savefig('./5GDDoS_Game_asp_utility_z_h_case1.jpg')
            plt.close()
        else:
            self.mpo_price = 100
            ut = []
            z_h = []
            plt.figure(figsize=(42, 25), dpi=400)
            for z in range(1000, 1005, 1):
                self.z_v = z / 1000
                for i in range(11):
                    i = i / 10
                    self.z_h = self.z_v * i
                    self.set_process_time()
                    self.set_utility()
                    z_h.append(i)
                    ut.append(self.utility)
                plt.plot(z_h, ut, marker='.', linestyle='-.', label=f"VM :{self.z_v}", linewidth=7)
                ut = []
                z_h = []
            plt.xlabel(r'$\bf{IPS\ VM\ ratio}$', fontsize=100)
            plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
            plt.xticks(fontsize=80)
            plt.yticks(fontsize=80)
            plt.legend(loc="best", fontsize=100)
            plt.savefig('./5GDDoS_Game_asp_utility_z_h_case2.pdf')
            plt.savefig('./5GDDoS_Game_asp_utility_z_h_case2.jpg')
            plt.close()
