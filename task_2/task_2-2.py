from multiprocessing import Pool, cpu_count
import logging
from time import time

logging.basicConfig(
	format = '%(message)s',
	level= logging.DEBUG,
	handlers=[
		logging.StreamHandler()
	]
)

def factorize (num):
	factors = []
	for i in range(1, abs(num) + 1):
		if num % i == 0:
			factors.append(i)
	return factors


if __name__ == "__main__":
	numbers = [128, 255, 99999, 10651060, 125000, 999800, 1000000, 123456789]
	start = time()
	with Pool (cpu_count()) as pool:
		result = pool.map(factorize, numbers)
	end = time()
	ex_time = end - start
	logging.debug(result)
	logging.debug(ex_time)