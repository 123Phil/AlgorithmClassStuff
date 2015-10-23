import sys
import time


def n2_sort(lines):
	for i in range(len(lines)-1):
		best = i
		for j in range(i, len(lines)):
			if lines[j].lower() < lines[best].lower():
				best = j
		lines[i], lines[best] = lines[best], lines[i]
	return lines


def nlogn_sort(lines):
	n = len(lines)
	if n <= 1:
		return lines
	# Modified to enhance lowest recursive calls
	elif n == 2:
		if lines[1].lower() > lines[0].lower():
			return [lines[1], lines[0]]
		else:
			return lines
	else:
		half = len(lines) // 2
		return merge(nlogn_sort(lines[:half]), nlogn_sort(lines[half:]))


def merge(A, B):
	S = []
	ai = 0
	bi = 0
	while ai < len(A) and bi < len(B):
		if A[ai].lower() <= B[bi].lower():
			x = A[ai]
			ai += 1
		else:
			x = B[bi]
			bi += 1
		S.append(x)
	return S + A[ai:] + B[bi:]


def main(args):
	if len(args) != 3:
		print('Usage  $ ' + args[0] + ' beowulf.txt' + ' <num_lines>')
		sys.exit(0)
	else:
		filename = args[1]

	num_lines = int(args[2])
	if num_lines > 40707:
		num_lines = 40707
	
	print("Reading n = %d lines" %num_lines)
	lines = []
	with open(filename, 'r') as f:
		for i in range(num_lines):
			lines.append(f.readline().strip())

	print("First 10 words:")
	print(lines[:10])
	#print("Running python merge sort...")
	#print("Running python selection sort...")

	start = time.perf_counter()
	lines = sorted(lines, key=str.lower)
	#lines = nlogn_sort(lines)
	#lines = n2_sort(lines)
	end = time.perf_counter()
	
	print("First 10 words:")
	print(lines[:10])
	print("elapsed time: " + str(end-start) + " seconds")



if __name__ == "__main__":
	main(sys.argv)

