import math
from random import uniform, randint
from const import *
from device import Device


class ASP():
    def __init__(self):
        self.bandwidth = ASP_BANDWIDTH
        self.device_list = []
        self.num_of_normal_users = randint(ASP_NUM_OF_NORMAL_USERS_LOWER, ASP_NUM_OF_NORMAL_USERS_UPPER)
        self.num_of_malicious_users = randint(ASP_NUM_OF_MALICIOUS_USERS_LOWER, ASP_NUM_OF_MALICIOUS_USERS_UPPER)

    def set_users(self):
        for i in range(self.num_of_normal_users):
            self.device_list.append(Device(self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))

a = ASP()
