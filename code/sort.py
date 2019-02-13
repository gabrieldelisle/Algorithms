import numpy as np
from time import time

global N_min
N_min = 12

def selection_sort(l, key=lambda x: x) :
	N = np.size(l)
	for i in range(N) :
		for j in range(i+1,N) :
			if key(l[j])<key(l[i]) :
				l[j],l[i] = l[i],l[j]

def insertion_sort(l, key=lambda x: x) :
	N = np.size(l)
	for i in range(N) :
		z = l[i]
		j = i
		while j>0 and l[j-1]>l[j] :
			l[j-1], l[j] = l[j], l[j-1]
			j-=1


def quick_sort(l, key=lambda x: x) :
	N = np.size(l)
	if N>N_min :
		#pivot: median of 3 randoms indexes
		select = l[np.random.randint(0,N-1,3)]
		insertion_sort(select)
		pivot = select[1]

		left = 0
		right = N-1
		while left <= right :
			if key(l[left]) <= key(pivot) :
				left+=1
			else :
				l[left],l[right] = l[right],l[left]
				right-=1
		quick_sort(l[:left])
		quick_sort(l[left:])
	else :
		insertion_sort(l, key=key)


def merge_sort(l, key=lambda x: x) :
	N = np.size(l)
	if N>N_min :
		a = l[0:N//2]
		b = l[N//2:N]
		merge_sort(a)
		merge_sort(b)

		i,j = 0,0
		newl = np.zeros(N)
		while i+j<N :
			if i==N//2 :
				newl[i+j] = b[j]
				j+=1
			elif j==N-N//2 :
				newl[i+j] = a[i]
				i+=1
			elif key(a[i]) <= key(b[j]) :
				newl[i+j] = a[i]
				i+=1
			else :
				newl[i+j] = b[j]
				j+=1
		l = newl
	else :
		insertion_sort(l, key=key)


if __name__ == '__main__':
	def test(sort_func) :
		T=0
		for _ in range(100) :
			l = np.arange(1000)
			np.random.shuffle(l)
			t1 = time()
			sort_func(l)
			t2 = time()
			T += t2-t1
		return T

	print("quick sort:", test(quick_sort))
	print("merge sort:", test(merge_sort))
