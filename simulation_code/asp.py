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
        self.z_v = None
        self.z_h = None
        self.mpo_price = None

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

    def process_time(self):
        return 1 / ((self.z_v - self.z_h) * self.service_rate - self.arrival_rate + asp_H(self.z_h))

    def utility(self):
        util = 0
        for dev in self.device_list:
            if self.process_time() + dev.transmission_time_to_asp >= dev.latency_requirement:
                util += dev.price_per_task
        return util - self.mpo_price * self.z_v
