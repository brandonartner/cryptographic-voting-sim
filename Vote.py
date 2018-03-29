from fractions import Fraction
from Crypto.PublicKey import DSA
from Crypto.Util import number


class Voter:
	"""	Voter implements a (n,k)-threshold scheme which is capable of submiting 
		a signature.
	"""

	def __init__(self, n, k, prime_size=1024):
		'''	
			n: total number of keys for the voter
			k: the required number of votes
			prime_size: number of bits for the prime number, default:1024
		'''
		self.p = number.getStrongPrime(prime_size,false_positive_prob=1e-10)
		self.n = n
		self.k = k
		self.values = [[], []]
		self.pubKey = None

	def generate_scheme(self, data):
		'''	Generates the private-public key pair, the polynomial, and the keys
			for this voter
		'''
		pass

	def generate_polynomial(self):
		'''	Creates a polynomial of degree k.
			Return: A kth degree polynomial
		'''
		pass

	def generate_keys(self, poly):
		'''	Generates keys based off the entered polynomial.
			poly: The polynomial used to generate the keys.
			Return: A list of n key pairs
		'''
		pass


	def add_key_to_signature(self, key):
		''' Adds given key and feeds forward 
		'''

        # splitting the key across first two lists
		self.values[0].append(key[0])
		self.values[1].append(key[1])
        
        # 
		for idx, lst in enumerate(self.values[1:]):
			if len(lst) == 2:
				val = self.firstOrderLag(idx)

				if idx == len(self.values)-2:
					self.values.append([val])
				else:
					self.values[idx+2].append(val)

				# remove value from 
				self.values[idx+1].pop(0)

		if len(self.values[0]) == self.k:
			for i in range(len(self.values)-1):
				self.values[i] = []

	def firstOrderLag(self, idx):
		j = -1
		i = j - (idx + 1)

		x1 = self.values[0][i]
		x2 = self.values[0][j]

		y1 = self.values[idx+1][-2]
		y2 = self.values[idx+1][-1]

		num = (0-x2)*y1-(0-x1)*y2
		den = x1-x2
		return Fraction(num, den)

	def sign(self, doc):
		'''
			Function creates the digital signature for the scheme.
			doc: Data that is being signed
			Return: Digital Signature
		'''
		pass


if __name__ == '__main__':
	voter = Voter(5)