import math
from random import uniform, randint
from const import *
from device import Device


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
        self.z_v = 150
        self.mpo_price = 1
        self.process_time = None
        self.eta = uniform(ASP_ETA_LOWER, ASP_ETA_UPPER) ## system parameters
        self.phi = uniform(ASP_PHI_LOWER, ASP_PHI_UPPER) ## system parameters

    def __str__(self):
        return_str = ""
        for dev in self.device_list:
            return_str += f"{dev}\n\n"
        return return_str

    def set_users(self):
        for i in range(self.num_of_normal_users):
            self.device_list.append(Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))

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

    def utility(self):
        util = 0
        for dev in self.device_list:
            util += (dev.price_per_task * (1 - ((dev.transmission_time_to_asp + self.process_time - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))))
        return util - self.mpo_price * self.z_v

    def optimize(self):
        z_h = asp_G(self.service_rate)
        if z_h > self.eta * self.z_v:
            self.process_time = 1 / ((1 - self.eta) * self.service_rate * self.z_v - (self.arrival_rate - asp_H(self.eta * self.z_v)))
            print('case2')
            print(self.utility())
            return
        else:
            if self.phi * self.service_rate * self.z_v >= ((self.z_v - z_h) * self.service_rate - self.arrival_rate + asp_H(z_h)):
                self.process_time = 1/(self.phi * self.z_v * self.service_rate)
                print('case3')
                print(self.utility())
                return
            else:
                print('case1')
                self.process_time = 1 / ((self.z_v - asp_G(self.service_rate)) * self.service_rate - self.arrival_rate + asp_H(asp_G(self.service_rate)))
                print(self.utility())
                return

asp = ASP()
asp.optimize()
