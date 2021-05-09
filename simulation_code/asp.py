from math import sqrt, floor
from random import uniform, randint
from const import *
from device import Device
import matplotlib.pyplot as plt


class ASP():
    def __init__(self):
        self.bandwidth = ASP_BANDWIDTH
        self.frequency = uniform(ASP_CPU_FREQUENCY_LOWER, ASP_CPU_FREQUENCY_UPPER)
        self.device_list = []
        self.num_of_normal_users = randint(ASP_NUM_OF_NORMAL_USERS_LOWER, ASP_NUM_OF_NORMAL_USERS_UPPER)
        self.num_of_malicious_users = randint(ASP_NUM_OF_MALICIOUS_USERS_LOWER, ASP_NUM_OF_MALICIOUS_USERS_UPPER)
        self.set_users()
        self.set_service_rate()
        self.set_arrival_rate()
        self.total_pay()
        self.mpo_price = None
        self.chi = 0.999
        self.gamma = 10000
        self.phi = 0.9

    def set_users(self):
        for i in range(self.num_of_normal_users):
            self.device_list.append(Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))

    def total_pay(self):
        self.total_payment = 0
        for dev in self.device_list:
            self.total_payment += dev.price_per_task

    def set_service_rate(self):
        tot_cpu_cycle = 0
        for dev in self.device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        self.service_rate = self.frequency / (tot_cpu_cycle / (self.num_of_normal_users + self.num_of_malicious_users))

    def set_arrival_rate(self):
        self.arrival_rate = 0
        for dev in self.device_list:
            self.arrival_rate += dev.arrival_rate

    def set_mpo_price(self, price):
        self.mpo_price = price

    def set_utility(self):
        util = 0
        for dev in self.device_list:
            util += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.process_time - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
        self.utility = util - self.mpo_price * self.z_v
        return

    # def optimize_zh(self):
    #     if self.z_v == 0:
    #         self.z_h = 0
    #         return
    #     elif GLOBAL_ETA > self.service_rate:
    #         if ASP_chi_lower(self.phi, self.z_v, self.service_rate, self.arrival_rate) > self.chi:
    #             print('infeasible')
    #         self.z_h = self.chi * self.z_v
    #         self.set_process_time()
    #         self.set_utility()
    #         return
    #     else:
    #         # self.phi = uniform(ASP_phi_lower_case2(self.z_v, self.service_rate, self.arrival_rate), ASP_phi_upper_case2(self.z_v, self.service_rate, self.arrival_rate))
    #         # self.z_h = ((self.phi - 1) * self.z_v * self.service_rate + self.arrival_rate) / (GLOBAL_ETA - self.service_rate)
    #         # print(self.z_h)
    #         self.z_h = 0
    #         self.set_process_time()
    #         self.set_utility()
    #         return

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
            if ASP_chi_lower(self.phi, self.z_v, self.service_rate, self.arrival_rate) > self.chi:
                print('infeasible')
            if self.utility < 0:
                self.z_v = 0
                return
        else:
            self.z_v = 1 / self.service_rate * sqrt(self.service_rate * self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price)) + self.arrival_rate / self.service_rate
            if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
            if ((self.phi - 1) * self.z_v * self.service_rate + self.arrival_rate) / (GLOBAL_ETA - self.service_rate) < 0:
                print("infeasible")
            self.z_h = 0
            self.set_process_time()
            self.set_utility()
            if self.utility < 0:
                self.z_v = 0
                return
    def plot_max(self):
        mpo_lst = [0.001, 0.003, 0.005, 0.007, 0.009]
        color_dict = {0.001 : 'red', 0.003 : 'darkorange', 0.005 : 'indigo', 0.007 : 'darkgreen', 0.009 : 'darkblue'}
        if GLOBAL_ETA > self.service_rate:
            for mpo_price in mpo_lst:
                self.mpo_price = mpo_price
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
                self.z_h = self.chi * self.z_v
                self.set_process_time()
                self.set_utility()
                plt.scatter(self.z_v, self.utility, color=color_dict[mpo_price], marker='^')
                extre = floor(self.z_v)
                ut = []
                z_v = []
                for i in range(1, 20):
                    self.z_v = i
                    self.z_h = self.chi * self.z_v
                    self.set_process_time()
                    self.set_utility()
                    z_v.append(self.z_v)
                    ut.append(self.utility)
                plt.plot(z_v, ut, marker='.', color=color_dict[mpo_price], linestyle='-.')
                z_v = []
                ut = []
            plt.savefig('./asp_utility_case1.jpg')
        else:
            for mpo_price in mpo_lst:
                self.mpo_price = mpo_price
                self.z_v = 1 / self.service_rate * sqrt(self.service_rate * self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price)) + self.arrival_rate / self.service_rate
                self.z_h = 0
                self.set_process_time()
                self.set_utility()
                plt.scatter(self.z_v, self.utility, color=color_dict[mpo_price], marker='^')
                extre = floor(self.z_v)
                ut = []
                z_v = []
                for i in range(1, 20):
                    self.z_v = i
                    self.z_h = self.chi * self.z_v
                    self.set_process_time()
                    self.set_utility()
                    z_v.append(self.z_v)
                    ut.append(self.utility)
                plt.plot(z_v, ut, marker='.', color=color_dict[mpo_price], linestyle='-.')
                ut = []
                z_v = []
            plt.savefig('./asp_utility_case2.jpg')
            plt.close()
