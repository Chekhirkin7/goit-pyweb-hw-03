from time import time

def factorize (*numbers):
	result = []
	for num in numbers:
		factors = []
		for i in range(1, abs(num) + 1):
			if num % i == 0:
				factors.append(i)
		result.append(factors)
	return result

start = time()
a, b, c, d, e, f, g, h  = factorize(128, 255, 99999, 10651060, 125000, 999800, 1000000, 123456789)
end = time()

ex_time = end - start

print(a, b, c, d, e, f, g, h)
print(ex_time)
