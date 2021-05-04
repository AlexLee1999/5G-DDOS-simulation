import math
from random import randint
from const import *



class MPO():
    def __init__(self):
        self.price_per_vm = None
        self.asp_lst = []
        self.num_of_asp = randint(MPO_NUM_OF_ASP_LOWER, MPO_NUM_OF_ASP_UPPER)
        self.set_asp()

    def set_asp(self):
        for i in range(self.num_of_asp):
            self.asp_lst.append(ASP())

    def set_price_per_vm(self, price):
        self.price_per_vm = price
        for asp in self.asp_lst:
            asp.set_mpo_price(price)
