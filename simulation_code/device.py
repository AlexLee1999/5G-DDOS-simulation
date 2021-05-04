import math
import random
from const import *


class Device():
    def __init__(self):
        self.latency_requirement = uniform(DEVICE_LATENCY_LOWER, DEVICE_LATENCY_UPPER)
        self.tx_power = DEVICE_TX_POWER
        self.distance = uniform(DEVICE_DISTANCE_LOWER, DEVICE_DISTANCE_UPPER)
        self.required_cpu_cycle = uniform(DEVICE_REQUIRED_CPU_CYCLE_LOWER, DEVICE_REQUIRED_CPU_CYCLE_UPPER)
