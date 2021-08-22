from math import sqrt
from random import uniform
from const import *
from device import *
import matplotlib
matplotlib.use('agg') 
import matplotlib.pyplot as plt

"""
bandwidth : total bandwidth of ASP_
frequency : CPU frequency of a VM
"""


class ASP():
    def __init__(self, ratio, num, ASP_type):
        self.type = ASP_type
        self.bandwidth = ASP_BANDWIDTH / MPO_NUM_OF_ASP
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
        self.chi = uniform(ASP_CHI_LOWER, ASP_CHI_UPPER)
        self.gamma = 30
        self.phi = 0
        if self.service_rate < GLOBAL_ETA:
            self.sqrt_coff = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)))
            self.coff = self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
        else:
            self.sqrt_coff = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.service_rate))
            self.coff = self.arrival_rate / self.service_rate
        self.queue_coff = (self.gamma + self.arrival_rate) / self.service_rate
        self.set_boundary()

    """
    set_users : initial users
    """
    def set_users(self):
        if self.type == load_type.AVERAGE:
            for i in range(self.num_of_normal_users):
                self.device_list.append(Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
            for i in range(self.num_of_malicious_users):
                self.mal_device_list.append(Malicious_Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
        elif self.type == load_type.HIGH:
            for i in range(self.num_of_normal_users):
                self.device_list.append(Device_high_load(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
            for i in range(self.num_of_malicious_users):
                self.mal_device_list.append(Malicious_Device_high_load(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
        elif self.type == load_type.LOW:
            for i in range(self.num_of_normal_users):
                self.device_list.append(Device_low_load(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
            for i in range(self.num_of_malicious_users):
                self.mal_device_list.append(Malicious_Device_low_load(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
    """
    total_pay : calculate the total payment from device
    """
    def total_pay(self):
        self.total_payment = 0
        for dev in self.device_list:
            self.total_payment += dev.price_per_task
    """
    set_service_rate : initial the service rate
    """
    def set_service_rate(self):
        tot_cpu_cycle = 0
        for dev in self.device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        for dev in self.mal_device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        self.service_rate = self.frequency / (tot_cpu_cycle / (self.num_of_normal_users + self.num_of_malicious_users))
    """
    set_arrival_rate : initial the arrival rate
    """
    def set_arrival_rate(self):
        self.arrival_rate = 0
        self.malicious_arrival_rate = 0
        self.normal_rate = 0
        for dev in self.device_list:
            self.arrival_rate += dev.arrival_rate
            self.normal_rate += dev.arrival_rate
        for dev in self.mal_device_list:
            self.arrival_rate += dev.arrival_rate
            self.malicious_arrival_rate += dev.arrival_rate
    """
    set_mpo_price : get mpo price from mpo
    """
    def set_mpo_price(self, price):
        self.mpo_price = price
    """
    set_malicious_ratio : set malicious ratio of an ASP
    """
    def set_malicious_ratio(self, ratio):
        self.malicious_ratio = ratio
    """
    set_utility : calculate the utility
    """
    def set_utility(self):
        util = 0
        for dev in self.device_list:
            util += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.process_time - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
        self.utility = util - self.mpo_price * self.z_v
        return
    """
    time : calculate processing time with z_v and z_h
    """
    def time(self, z_v, z_h):
        return 1 / ((z_v - z_h) * self.service_rate - (self.arrival_rate - ASP_H(z_h, self.malicious_arrival_rate)))
    """
    set_boundary : calculate the boundary
    """
    def set_boundary(self):
        z_v = (self.arrival_rate + self.gamma) / self.service_rate
        z_h = self.chi * z_v
        util1 = 0
        util2 = 0
        util3 = 0
        for dev in self.device_list:
            util1 += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.time(z_v, z_h) - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
            util2 += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.time(z_v, 0) - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
            util3 += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.time(z_v, self.malicious_arrival_rate / GLOBAL_ETA) - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
        if GLOBAL_ETA > self.service_rate: # case 2 & 4
            bound_case2 = util1 / z_v
            bound_case4 = util3 / z_v
            qbound_case2 = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)) / (z_v - self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)) ** 2
            qbound_case4 = self.total_payment / (self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)) * ((self.malicious_arrival_rate + self.gamma) / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA) ** (-2)
            if bound_case4 < qbound_case4: # No queuing
                A = 0
                for dev in self.device_list:
                    A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
                B = self.total_payment / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                C = self.service_rate
                D = self.malicious_arrival_rate * self.service_rate / GLOBAL_ETA + self.arrival_rate - self.malicious_arrival_rate
                phi = (A * C * D + 2 * B * C - 2 * C * sqrt(B ** 2 + A * B * D)) / (D ** 2)
                z_v_zero = sqrt(self.total_payment / ((self.arrival_rate) * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * phi)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                if z_v_zero < (self.malicious_arrival_rate / (GLOBAL_ETA * self.chi)):
                    self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (self.chi * GLOBAL_ETA) - self.normal_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA) ** (-2)
                    A = 0
                    for dev in self.device_list:
                        A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
                    B = self.total_payment / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                    C = self.service_rate * (1 - self.chi) + self.chi * GLOBAL_ETA
                    D = self.arrival_rate
                    self.bound = (A * C * D + 2 * B * C - 2 * C * sqrt(B ** 2 + A * B * D)) / (D ** 2)
                    self.qbound = None
                    # print(4)
                    self.case = 4
                else:
                    self.bound = phi
                    self.change_point = phi
                    self.qbound = None
                    # print(2)
                    self.case = 2
            else:
                if (self.arrival_rate + self.gamma) / self.service_rate > (self.malicious_arrival_rate / (GLOBAL_ETA * self.chi)):
                    self.bound = bound_case4
                    self.qbound = qbound_case4
                    self.change_point = bound_case4
                    # print(1)
                    self.case = 1
                else:
                    self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (self.chi * GLOBAL_ETA) - self.normal_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA) ** (-2)
                    self.bound = bound_case2
                    self.qbound = qbound_case2
                    # print(3)
                    self.case = 3

        else: # case3
            bound = util2 / z_v
            qbound = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1) * self.service_rate)) / (z_v - self.arrival_rate / ((1) * self.service_rate)) ** 2
            if bound < qbound:
                A = 0
                for dev in self.device_list:
                    A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
                B = self.total_payment / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                C = self.service_rate
                D = self.arrival_rate
                self.qbound = None
                self.bound = (A * C * D + 2 * B * C - 2 * C * sqrt(B ** 2 + A * B * D)) / (D ** 2)
            else:
                self.bound = bound
                self.qbound = qbound
        return
    """
    set_process_time : set the process_time with existing z_v and z_h
    """
    def set_process_time(self):
        self.process_time = 1 / ((self.z_v - self.z_h) * self.service_rate - (self.arrival_rate - ASP_H(self.z_h, self.malicious_arrival_rate)))
    """
    optimize_zv : set the optimize z_v and calculate utility
    """
    def optimize_zv(self):
        if GLOBAL_ETA > self.service_rate:
            if self.case == 1:
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                    self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
                self.z_h = self.malicious_arrival_rate / GLOBAL_ETA
                self.set_process_time()
                self.set_utility()
                if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                    print('infeasible')
                if self.utility < 0:
                    self.z_v = 0
                    self.z_h = 0
                    self.utility = 0
            elif self.case == 2:
                
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                self.z_h = self.malicious_arrival_rate / GLOBAL_ETA
                self.set_process_time()
                self.set_utility()
                if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                    print('infeasible')
                if self.utility < 0:
                    self.z_v = 0
                    self.z_h = 0
                    self.utility = 0
            elif self.case == 3:
                
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                if self.z_v < self.malicious_arrival_rate / (self.chi * GLOBAL_ETA):
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                    self.z_h = self.malicious_arrival_rate / GLOBAL_ETA
                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0
                else:
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
                    self.z_h = self.chi * self.z_v
                    if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                        self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
                        self.z_h = self.chi * self.z_v

                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0
            elif self.case == 4:
                
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                if self.z_v > self.malicious_arrival_rate / (self.chi * GLOBAL_ETA):
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA + self.normal_rate / self.service_rate
                    self.z_h = self.malicious_arrival_rate / GLOBAL_ETA
                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                        print('infeasible')
                else:
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
                    self.z_h = self.chi * self.z_v
                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0
            
        else:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
            self.z_h = 0
            if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                print('infeasible')
            self.set_process_time()
            self.set_utility()
            if self.utility < 0:
                self.z_v = 0
                self.z_h = 0
                self.utility = 0

    def optimize_zv_without_constraint(self):
        if GLOBAL_ETA > self.service_rate:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
            self.z_h = self.chi * self.z_v
            self.set_process_time()
            self.set_utility()
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                print('infeasible')
        else:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
            self.z_h = 0
            self.set_process_time()
            self.set_utility()
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                print('infeasible')
        
    def report_asp(self, price):
        self.mpo_price = price
        case = 'e'
        if GLOBAL_ETA > self.service_rate:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
            if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
                case = 'q'
            self.z_h = self.chi * self.z_v
            self.set_process_time()
            self.set_utility()
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                print('infeasible')
            if self.utility < 0:
                self.z_v = 0
                self.utility = 0
                case = 'z'
        else:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
            self.z_h = 0
            if self.z_v < ((self.gamma + self.arrival_rate) / self.service_rate):
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
                case = 'q'
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
                print('infeasible')
                self.z_h = 0
            self.set_process_time()
            self.set_utility()
            if self.utility < 0:
                self.z_v = 0
                self.utility = 0
                case = 'z'
        return case

    def res(self, price):
        if price > self.bound:
            return 'z'
        elif self.qbound and price > self.qbound:
            return 'q'
        else:
            return 'e'
    """
    set_zv_zh : set the asp with chi
    """
    def set_zv_zh(self, chi):
        self.chi = chi
        self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA)
        if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
            self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
        self.z_h = self.chi * self.z_v
        self.set_process_time()
        self.set_utility()
        if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate):
            print('infeasible')
        if self.utility < 0:
            self.z_v = 0
            self.utility = 0
            self.z_h = 0
            

    def plot_max(self):
        mpo_lst = [100, 300, 500, 700, 900]
        color_dict = {100: 'red', 300: 'darkorange', 500: 'indigo', 700: 'darkgreen', 900: 'darkblue'}
        if GLOBAL_ETA > self.service_rate:
            plt.figure(figsize=(45, 25), dpi=400)
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
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_case1.pdf')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_case1.jpg')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_case1.eps')
            plt.close()
        else:
            plt.figure(figsize=(45, 25), dpi=400)
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
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_case2.pdf')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_case2.jpg')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_case2.eps')
            plt.close()

    def plot_max_zh(self):
        if GLOBAL_ETA > self.service_rate:
            self.mpo_price = 100
            ut = []
            z_h = []
            plt.figure(figsize=(45, 25), dpi=400)
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
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_z_h_case1.pdf')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_z_h_case1.jpg')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_z_h_case1.eps')
            plt.close()
        else:
            self.mpo_price = 100
            ut = []
            z_h = []
            plt.figure(figsize=(45, 25), dpi=400)
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
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_z_h_case2.pdf')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_z_h_case2.jpg')
            plt.savefig('./image/asp/5GDDoS_Game_asp_utility_z_h_case2.eps')
            plt.close()
