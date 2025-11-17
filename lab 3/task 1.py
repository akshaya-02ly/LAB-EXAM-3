# empty or existing content
"""Bubble Sort vs Insertion Sort timing demo.

This script implements bubble sort and insertion sort, verifies they
produce the same results as Python's built-in `sorted`, and compares
their execution times using the `time` module.

Usage: run the script directly. You can adjust sizes and repeats
by editing the DEFAULT_SIZES and DEFAULT_REPEATS constants or by
modifying the code below.
"""

import time
import random
import argparse
import sys


def bubble_sort(a):
	"""Return a new list that is the sorted version of a using bubble sort."""
	arr = a[:]
	n = len(arr)
	# Optimized bubble: stop early if no swaps
	for i in range(n):
		swapped = False
		for j in range(0, n - i - 1):
			if arr[j] > arr[j + 1]:
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
				swapped = True
		if not swapped:
			break
	return arr


def insertion_sort(a):
	"""Return a new list that is the sorted version of a using insertion sort."""
	arr = a[:]
	for i in range(1, len(arr)):
		key = arr[i]
		j = i - 1
		while j >= 0 and arr[j] > key:
			arr[j + 1] = arr[j]
			j -= 1
		arr[j + 1] = key
	return arr


def time_sort(sort_func, arr, repeats=1):
	"""Time `sort_func` on a copy of `arr`, averaged over `repeats` runs.

	Uses time.time() from the time module for measurement as requested.
	Returns average elapsed seconds.
	"""
	total = 0.0
	for _ in range(repeats):
		a_copy = arr[:]
		t0 = time.time()
		sort_func(a_copy)
		total += (time.time() - t0)
	return total / repeats


def make_random_list(n, seed=None, value_range=(0, 10_000)):
	if seed is not None:
		random.seed(seed)
	lo, hi = value_range
	return [random.randint(lo, hi) for _ in range(n)]


DEFAULT_SIZES = [100, 500, 1000]
DEFAULT_REPEATS = 3


def main(sizes=DEFAULT_SIZES, repeats=DEFAULT_REPEATS, seed=1):
	print("Bubble Sort vs Insertion Sort timing (averaged over {} runs)".format(repeats))
	print("Sizes: {}".format(sizes))
	print()

	header = "{:>8} | {:>12} | {:>12} | {:>8}"
	print(header.format("n", "bubble(s)", "insertion(s)", "ratio"))
	print("" + "-" * 52)

	for n in sizes:
		arr = make_random_list(n, seed=seed)

		# sanity check: both algorithms produce the same result as sorted()
		expected = sorted(arr)

		b_res = bubble_sort(arr)
		i_res = insertion_sort(arr)
		if b_res != expected or i_res != expected:
			print("ERROR: sorting algorithm produced incorrect result for n={}".format(n), file=sys.stderr)
			sys.exit(1)

		t_bubble = time_sort(bubble_sort, arr, repeats=repeats)
		t_insertion = time_sort(insertion_sort, arr, repeats=repeats)

		ratio = (t_bubble / t_insertion) if t_insertion > 0 else float('inf')
		print(header.format(n, "{:.6f}".format(t_bubble), "{:.6f}".format(t_insertion), "{:.2f}".format(ratio)))

	print("\nNotes: These are simple O(n^2) implementations for educational purposes.")
	print("For more reliable benchmarking, consider time.perf_counter() or the timeit module.")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Compare Bubble and Insertion sorts')
	parser.add_argument('--sizes', nargs='+', type=int, help='list of sizes to test', default=DEFAULT_SIZES)
	parser.add_argument('--repeats', type=int, help='repeats per size (average)', default=DEFAULT_REPEATS)
	parser.add_argument('--seed', type=int, help='random seed', default=1)
	args = parser.parse_args()

	main(sizes=args.sizes, repeats=args.repeats, seed=args.seed)

