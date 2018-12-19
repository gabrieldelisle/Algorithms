from math import log
from random import randint


def sieve(n_max) :
	# returns a list of all prime number below n
	integers = list(range(n_max))
	integers[1]=0
	i = 2
	while i*i <= n_max :
		if integers[i]!=0 :
			for j in range(2,(n_max-1)//i+1) :
				integers[j*i] = 0

		i+=1
	return [u for u in integers if u!=0]


def Primalitytest(n) :
	# if n is prime, returns True
	# else, returns False

	# case n even number
	if n==2: 
		return True
	if n%2==0 or n==1:
		return False

	i=3
	while i**2<=n :
		if n%i == 0 :
			return False
		i+=2
	return True



def FermatPrimalityTest(n, k=80):
	# if n is prime, returns True
	# else, returns False with probability 1-1/2**k
	if n==2 or n==3 :
		return True
	if n%2==0 or n==1 :
		return False

	# try for different witnesses a:
	# if a does not pass the test, n is composed
	# ferma test: a**(n-1) = 1 [n]
	for times in range(k):
		a = random.randint(2, n-2)-1
		if ( pow(a, n-1, n) != 1 ):
			return False
	return True


def MillerRabinPrimalityTest(n, k=40):
	# if n is prime, returns True
	# else, returns False with probability 1-1/4**k

	# case n<=3
	if n==2 or n==3 :
		return True
	if n%2==0 or n==1 :
		return False

	# decomp n = 2**r * d (d odd number)
	r=0
	while (n-1)%2**r==0 :
		r+=1
	r-=1
	d = n//2**r

	# try for different witnesses a : 
	# if a does not pass one of the tests, n is composed
	# tests: a**d = 1 [n] and for all 1<=k<=r a**(kd) = n-1 [n]
	for _ in range(k) :
		isWitness = True

		a = randint(2,n-2)
		x = pow(a,d,n)
		if x==1 :
			isWitness = False

		for _ in range(r) :
			if x==n-1 :
				isWitness = False
				break
			x = x**2%n
			
		if isWitness :
			return  False
	return True


def decomp(n) :
	dec = []
	i=2
	while n!=1 and i*i<=n :
		if n%i==0 :
			dec.append(i)
			n//=i
		else :
			i+=1
	if i*i>n :
		dec.append(n)
	return dec

if __name__ == '__main__':
	def is_prime(n) :
		if MillerRabinPrimalityTest(n, k=20) :
			print(n, "is prime")
		else :
			print(n, "is not prime")

	n=31*97*1399*4177
	print("decomposition of", n,":",decomp(n))
	is_prime(2**31-1)
	is_prime(2**37-1)
	primes = sieve(200000)
	print("10,000th prime number is", primes[10000])
