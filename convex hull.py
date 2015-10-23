###############################################################################
# CPSC 335 Project 1
# Spring 2015
#
# Author: Phillip Stewart
###############################################################################

# constant parameters
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
CANVAS_MARGIN = 20
BOX_OUTLINE_COLOR = 'green'
BOX_FILL_COLOR = 'white'
HULL_OUTLINE_COLOR = 'black'
HULL_FILL_COLOR = 'blue'
INTERIOR_POINT_COLOR = 'black'
POINT_RADIUS = 2
OUTLINE_WIDTH = 2

import math, random, time, tkinter

# Class representing one 2D point.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# input: a list of Point objects
# output: a 4-tuple (x_min, y_min, x_max, y_max)
def bounding_box(points):
	#trivial case
	if len(points) == 0:
		return None
	x_min = points[0].x
	x_max = points[0].x
	y_min = points[0].y
	y_max = points[0].y
	#check each in one for loop, but
	#if it's the highest, don't check for lowest too...
	#similar for left/right
	for point in points:
		if point.x > x_max:
			x_max = point.x
		elif point.x < x_min:
			x_min = point.x
		if point.y > y_max:
			y_max = point.y
		elif point.y < y_min:
			y_min = point.y
	return x_min, y_min, x_max, y_max

# input: a list of Point objects
# output: a list of the Point objects on the convex hull boundary
def convex_hull(points):
	# trivial cases
	if len(points) == 0:
		return None
	elif len(points) < 3:
		return points[:]
	
	# find highest point
	highest = points[0]
	for point in points:
		if point.y > highest.y:
			highest = point
	
	# find outer hull:
	# start with highest point
	current = highest
	hull = [highest]
	previous = 0
	searching = True
	while (searching):
		# find the next point on the hull
		# -may go clockwise or counterclockwise depending on which point
		#	is selected in the first iteration
		# nph = next_possible_hull_point
		for nph in points:
			if nph is previous or nph is current:
				continue
			#find line and check that it is on the hull
			m = (current.y - nph.y) / (current.x - nph.x)
			b = current.y - (m * current.x)
			#assert nph.y = m*nph.x + b
			num_above = 0
			num_below = 0
			for point in points:
				if point is current or point is nph:
					continue
				if point.y == (m * point.x + b):
					print('colinear point encountered!')
					#resolve...
				elif point.y > (m * point.x + b):
					num_above += 1
				else:
					num_below += 1
			# if nph is on the hull, add it and continue
			if num_above == 0 or num_below == 0:
				#-unless we encounter the first point - then we are done!
				if nph is highest:
					searching = False
					break
				hull.append(nph)
				previous = current
				current = nph
	return hull

###############################################################################
# The following code is reponsible for generating instances of random
# points and visualizing them. You can leave it unchanged.
###############################################################################

# input: an integer n >= 0
# output: n Point objects with all coordinates in the range [0, 1]
def random_points(n):
    return [Point(random.random(), random.random())
            for i in range(n)]

# translate coordinates in [0, 1] to canvas coordinates
def canvas_x(x):
    return CANVAS_MARGIN + x * (CANVAS_WIDTH - 2*CANVAS_MARGIN)
def canvas_y(y):
    return CANVAS_MARGIN + y * (CANVAS_HEIGHT - 2*CANVAS_MARGIN)

# extract the x-coordinates (or y-coordinates respectively) from a
# list of Point objects
def xs(points):
    return [p.x for p in points]
def ys(points):
    return [p.y for p in points]

# input: a non-empty list of numbers
# output: the mean average of the list
def mean(numbers):
    return sum(numbers) / len(numbers)

# input: list of Point objects
# output: list of the same objects, in clockwise order
def clockwise(points):
    if len(points) <= 2:
        return points
    else:
        center_x = mean(xs(points))
        center_y = mean(ys(points))
        return sorted(points,
                      key=lambda p: math.atan2(p.y - center_y,
                                               p.x - center_x),
                      reverse=True)

# Run one trial of one or both of the algorithms.
#
# 1. Generates an instance of n random points.
# 2. If do_box is True, run the bounding_box algorithm and display its output.
# 3. Likewise if do_hull is True, run the convex_hull algorithm and display
#    its output.
# 4. The run-times of the two algorithms are measured and printed to standard
#    output.
def trial(do_box, do_hull, n):
    print('generating n=' + str(n) + ' points...')
    points = random_points(n)
    hull = []
    
    if do_box:
        print('bounding box...')
        start = time.perf_counter()
        (x_min, y_min, x_max, y_max) = bounding_box(points)
        end = time.perf_counter()
        print('elapsed time = {0:10.6f} seconds'.format(end - start))

    if do_hull:
        print('convex hull...')
        start = time.perf_counter()
        hull = convex_hull(points)
        end = time.perf_counter()
        print('elapsed time = {0:10.6f} seconds'.format(end - start))

    w = tkinter.Canvas(tkinter.Tk(),
                       width=CANVAS_WIDTH, 
                       height=CANVAS_HEIGHT)
    w.pack()

    if do_box:
        w.create_polygon([canvas_x(x_min), canvas_y(y_min),
                          canvas_x(x_min), canvas_y(y_max),
                          canvas_x(x_max), canvas_y(y_max),
                          canvas_x(x_max), canvas_y(y_min)],
                         outline=BOX_OUTLINE_COLOR,
                         fill=BOX_FILL_COLOR,
                         width=OUTLINE_WIDTH)

    if do_hull:
        vertices = []
        for p in clockwise(hull):
            vertices.append(canvas_x(p.x))
            vertices.append(canvas_y(p.y))

        w.create_polygon(vertices,
                         outline=HULL_OUTLINE_COLOR,
                         fill=HULL_FILL_COLOR,
                         width=OUTLINE_WIDTH)
    #to aid in debug...
    for p in hull:
        w.create_oval(canvas_x(p.x) - POINT_RADIUS,
                      canvas_y(p.y) - POINT_RADIUS,
                      canvas_x(p.x) + POINT_RADIUS,
                      canvas_y(p.y) + POINT_RADIUS,
                      fill='magenta')
    
    for p in points:
        if p not in hull:
            w.create_oval(canvas_x(p.x) - POINT_RADIUS,
                      canvas_y(p.y) - POINT_RADIUS,
                      canvas_x(p.x) + POINT_RADIUS,
                      canvas_y(p.y) + POINT_RADIUS,
                      fill=INTERIOR_POINT_COLOR)

    tkinter.mainloop()


# Input: (int) num_trials - number of times to run each algorithm for input n
# Output: no return value,
#	creates a matplotlib.pyplot window
def time_trials(num_trials):
	"""Uses matplotlib to plot runs of various n values against time"""
	import matplotlib.pyplot as p
	print('Running time trials, be patient...')
	bb_data_points = []
	ch_data_points = []
	x_max = 0
	y_max = 0
	
	for n in [25,50,100,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000,2250,2500]:
	#for n in range(10,75,3): # <-for testing low values
		bb = []
		ch = []
		for i in range(num_trials):
			points = random_points(n)
			hull = []
			start = time.perf_counter()
			(x_min, y_min, x_max, y_max) = bounding_box(points)
			end = time.perf_counter()
			bb.append(end - start)
	
			start = time.perf_counter()
			hull = convex_hull(points)
			end = time.perf_counter()
			ch.append(end - start)
		
		bb_time = sum(bb)/float(num_trials)
		ch_time = sum(ch)/float(num_trials)
		bb_data_points.append(Point(n, bb_time))
		ch_data_points.append(Point(n, ch_time))
		if n > x_max:
			x_max = n
		if bb_time > y_max:
			y_max = bb_time
		if ch_time > y_max:
			y_max = ch_time
		
		print('Input size: ', n)
		print('Bounding box time = {0:10.6f} seconds'.format(bb_time))
		print('Convex hull time  = {0:10.6f} seconds'.format(ch_time))
	
	p.plot(xs(bb_data_points), ys(bb_data_points), 'k', lw=2)
	p.plot(xs(bb_data_points), ys(bb_data_points), 'b^', lw=2)
	p.plot(xs(ch_data_points), ys(ch_data_points), 'k', lw=1)
	p.plot(xs(ch_data_points), ys(ch_data_points), 'g^', lw=2)
	p.axis([0,x_max*1.05,0,y_max*1.05])
	p.show()

		

###############################################################################
# This main() function runs multiple trials of the algorithms to
# gather empirical performance evidence. You should rewrite it to
# gather the evidence you need.
###############################################################################
def main():
	trial(True, True, 20)
#	trial(True, True, 200)
#	trial(True, False, 20000)
#	trial(True, False, 1000000)
#	time_trials(10)



if __name__ == '__main__':
    main()
