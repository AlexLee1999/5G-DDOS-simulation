########################################
# These are the parameters of Device
# Prefix with DEVICE_
########################################
# latency
DEVICE_LATENCY_UPPER = 100E-3
DEVICE_LATENCY_LOWER = 5E-3
# tx_power
DEVICE_TX_POWER = 199.5262315
# distance
DEVICE_DISTANCE_UPPER = 100
DEVICE_DISTANCE_LOWER = 50
# frequency
DEVICE_FREQUENCY = 2.1
# required cpu cycle
DEVICE_REQUIRED_CPU_CYCLE_UPPER = 0.6E6
DEVICE_REQUIRED_CPU_CYCLE_LOWER = 0.5E6
# task size
DEVICE_TASK_SIZE_UPPER = 500 ##500 kB
DEVICE_TASK_SIZE_LOWER = 400 ##400 kB
# arrival rate
DEVICE_ARRIVAL_RATE_UPPER = 3
DEVICE_ARRIVAL_RATE_LOWER = 1
# price per task
DEVICE_PRICE_PER_TASK_UPPER = 5
DEVICE_PRICE_PER_TASK_LOWER = 1

########################################
# These are the parameters of ASP
# Prefix with ASP_
########################################
ASP_BANDWIDTH = 20 * 10E6

ASP_NUM_OF_NORMAL_USERS_UPPER = 100
ASP_NUM_OF_NORMAL_USERS_LOWER = 50

ASP_NUM_OF_MALICIOUS_USERS_UPPER = 100
ASP_NUM_OF_MALICIOUS_USERS_LOWER = 50

ASP_CPU_FREQUENCY_UPPER = 0.3 * 10E9
ASP_CPU_FREQUENCY_LOWER = 0.1 * 10E9
MU = 3
ALPHA = 0.5
def asp_H(z_ih):
    return ((z_ih + MU) ** (1 - ALPHA)) / (1 - ALPHA) - ((MU) ** (1 - ALPHA) / (1 - ALPHA))

########################################
# These are the parameters of MPO
# Prefix with MPO_
########################################
MPO_NUM_OF_ASP_UPPER = 50
MPO_NUM_OF_ASP_LOWER = 25
