
import matplotlib.pyplot as p
from project2b import *

print('Starting...')

# TSP
#x = range(3, 10)

# Prim
x = range(50, 301, 50)

# Kruskal
#x = range(100, 1501, 100)

y = []
num_trials = 3

for i in x:
	times = []
	for _ in range(num_trials):
		points = generate_points(i)
		start = time.perf_counter()
		graph = euclidean_mst(points)
		#path = euclidean_tsp(points)
		end = time.perf_counter()
		times.append(end - start)
	y.append(sum(times)/float(num_trials))
	print('Input size: {0:5d}, Time = {1:10.6f} seconds'.format(i, y[-1]))

p.plot(x, y, 'k', lw=2)
p.plot(x, y, 'b^', lw=2)

p.axis([0, max(x)*1.05, 0, max(y)*1.05])
p.show()

	