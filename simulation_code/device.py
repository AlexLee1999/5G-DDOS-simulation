import math
from random import uniform
from const import *


class Device():
    def __init__(self, bandwidth):
        self.tx_power = DEVICE_TX_POWER
        self.distance = uniform(DEVICE_DISTANCE_LOWER, DEVICE_DISTANCE_UPPER)
        self.frequency = DEVICE_FREQUENCY
        self.bandwidth = bandwidth
        self.task_size = uniform(DEVICE_TASK_SIZE_LOWER, DEVICE_TASK_SIZE_UPPER) * 8 * 10E3 ##change to bits
        self.arrival_rate = uniform(DEVICE_ARRIVAL_RATE_LOWER, DEVICE_ARRIVAL_RATE_UPPER)
        self.required_cpu_cycle = uniform(DEVICE_REQUIRED_CPU_CYCLE_LOWER, DEVICE_REQUIRED_CPU_CYCLE_UPPER)
        self.log_snr = math.log2(1 + self.tx_power * 10**10 * 10 ** (-(22 * math.log10(self.distance) + 28 + 20 * math.log10(self.frequency)) / 10))
        self.shannon_rate = self.bandwidth * self.log_snr
        self.transmission_time_to_asp = self.arrival_rate * self.task_size / self.shannon_rate
        self.price_per_task = uniform(DEVICE_PRICE_PER_TASK_LOWER, DEVICE_PRICE_PER_TASK_UPPER)

    def __str__(self):
        return  f"tx_power : {self.tx_power}\n" \
                f"distance : {self.distance}\n" \
                f"frequency : {self.frequency}\n" \
                f"bandwidth : {self.bandwidth}\n" \
                f"task_size : {self.task_size}\n" \
                f"arrival_rate : {self.arrival_rate}\n" \
                f"required_cpu_cycle : {self.required_cpu_cycle}\n" \
                f"log_snr : {self.log_snr}\n" \
                f"shannon_rate : {self.shannon_rate}\n" \
                f"transmission_time_to_asp : {self.transmission_time_to_asp}\n" \
                f"price_per_task : {self.price_per_task}\n"