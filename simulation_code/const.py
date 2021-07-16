from math import exp
########################################
# These are the parameters of Global
# Prefix with GLOBAL_
########################################
GLOBAL_ETA = 50
########################################
# These are the parameters of Device
# Prefix with DEVICE_
########################################
# tx_power
DEVICE_TX_POWER = 199.5262315
# distance
DEVICE_DISTANCE_UPPER = 100
DEVICE_DISTANCE_LOWER = 50
# frequency
DEVICE_FREQUENCY = 2.1
# required cpu cycle
DEVICE_REQUIRED_CPU_CYCLE_UPPER = 0.9E8
DEVICE_REQUIRED_CPU_CYCLE_LOWER = 0.1E8
# task size
DEVICE_TASK_SIZE_UPPER = 50  # 5 kB
DEVICE_TASK_SIZE_LOWER = 40  # 4 kB
# arrival rate
DEVICE_ARRIVAL_RATE_UPPER = 3
DEVICE_ARRIVAL_RATE_LOWER = 1
# price per task
DEVICE_PRICE_PER_TASK_UPPER = 100
DEVICE_PRICE_PER_TASK_LOWER = 1

########################################
# These are the parameters of ASP
# Prefix with ASP_
########################################
# latency
ASP_DEVICE_LATENCY_UPPER = 1000E-3
ASP_DEVICE_LATENCY_LOWER = 5E-3

ASP_BANDWIDTH = 20 * 10E8


###################################################
# H function


def ASP_H(x):
    return GLOBAL_ETA * x

########################################
# These are the parameters of MPO
# Prefix with MPO_
########################################
MPO_NUM_OF_ASP_UPPER = 5
MPO_NUM_OF_ASP_LOWER = 5

MPO_NUM_OF_VM_LOWER = 150
MPO_NUM_OF_VM_UPPER = 300

MPO_CPU_FREQUENCY = 0.25 * 10E9

def MPO_cost(x):
    return 0.01 * x ** 2
