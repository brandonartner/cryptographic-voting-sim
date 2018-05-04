from fractions import Fraction
from Crypto.PublicKey import DSA
from Crypto.Util import number
from Crypto.Random import random
from sympy.abc import x
from Toolkit import *
import hashlib

import sympy

class Voter:
	"""	Voter implements a (n,k)-threshold scheme which is capable of submiting 
		a signature.
	"""

	def __init__(self, node, n, k, prime_size=1024):
		"""
            :Parameter node: A reference back to the node this voter belongs to.
            :Type node: TreeNode

            :Parameter n: The number of key to generate for this voter.
            :Type n: int

            :Parameter k: The number of vote required to pass a vote.
            :Type k: int

            :Parameter prime_size: The number of bits for the prime number.
            						default: 1024
            						Must be a multiple of 128 between 512 and 1024.
            :Type prime_size: int

            :Return: None

            :TODO 
        """

		self.prime_size = prime_size
		self.p = number.getStrongPrime(prime_size,false_positive_prob=1e-10)
		self.n = n
		self.k = k
		self.values = [[], []]
		self.pubKey = None
		self.node = node

	def generate_scheme(self, data=None):
		"""Generates the private-public key pair, the polynomial, and the keys
			for this voter.

            :Parameter data: The data to be used as the secret data. 
        						(Note: None means the voter is for root node.)
            :Type data: long or int

            :Return: list of 2-tuples, each tuple is a key pair for the Shamir's Scheme.

            :TODO Implement non-root DSA key pairs. This is to allow for signing of sub-root
            		document sets. Problem consists of being given a private key and having to 
        			generate a public key.
        """

		if not data:
			print('Creating new DSA pair.')
			# Generate the DSA public-private key pair for signing with
			key = DSA.generate(self.prime_size)
			# Set the prime equal to the modulus from the DSA key set
			self.pubKey = key.publickey()
			self.p = self.pubKey.p
			# Set the public key to the public key from the DSA key set
			data = key.x
		'''
		else:
			print('Creating new DSA pair.')
			# Generate the DSA public-private key pair for signing with
			key = DSA.importKey(convert_to_format(data))
			# Set the prime equal to the modulus from the DSA key set
			self.p = key.p
			# Set the public key to the public key from the DSA key set
			self.pubKey = key.y
			data = key.x
		'''

		# Generate a polynomial
		poly = self.generate_polynomial(data%self.p)
		# Reutrn a set of keys generated from the polynomial
		return self.generate_keys(poly)

	def random_distinct(self, lower_bound, upper_bound, size):
		"""Generates lists of distinct random numbers,

            :Parameter lower_bound: Low bound for searching
            :Type lower_bound: long or int

            :Parameter upper_bound: High bound for searching
            :Type upper_bound: long or int

            :Parameter size: Length of list of numbers
            :Type size: long or int

            :Return: List of random numbers within given bounds

            :TODO 
        """

		v = []

		while len(v) < size:
			rand = random.randint(lower_bound, upper_bound)
		    
			if rand not in v:
				v.append(rand)
		        
		return v

	def generate_polynomial(self, data):
		"""Makes a random polynomial with data as the coeficient term.

            :Parameter data: The data as a numeric value to be split
            :Type data: long or int

            :Return: polynomial as a lambda function

            :TODO 
        """

		# Shamir's algorithms requires each coefficient to be distinct
		#coefficients = random.sample((x for x in range(self.p)), self.k-1) 
		coefficients =  self.random_distinct(0, self.p, self.k-1)

		# start building our polynomial
		polynomial = ''
		power = self.k-1

		while power > 0:
			# each a_i*x^i for i from k-1 to 1
			polynomial = polynomial + '{}*x**{}+'.format(coefficients[-power], power)
			power -= 1

		# set a_0 to data
		polynomial = polynomial + '{}'.format(data)

		# convert polynomial string to lambda function
		f = sympy.utilities.lambdify(x, sympy.sympify(polynomial))

		return f

	def generate_keys(self, poly):
		"""Creates the keys for distributing.

            :Parameter poly: Polynomial function to create the keys
            :Type poly: a lambda function

            :Return: list of key pairs.

            :TODO 
        """

		# create distinct x values because f(a)=f(b) iff a=b 
		# implies less than n keys will be made
		#X = random_distinct(1, p, n)
		X = range(1, self.n+1)

		# get corresponding y values
		Y = [poly(x) % self.p for x in X]

		return list(zip(X, Y))


	def add_key_to_signature(self, key, doc):
		"""Add given key to the in progress vote 

            :Parameter key: The key being added to the LIP
            :Type key: 2-tuple of ints

            :Parameter doc: The document being voted on.
            :Type doc: String 2-tuple

            :Return: DSA Signature, if the vote is completed, i.e. k keys have been submitted.

            :TODO 
        """

		# splitting the key across first two lists
		self.values[0].append(key[0])
		self.values[1].append(key[1])

		
		# generate the as far forward as possible in the Neville list
		# ie. if 3 keys have been submitted, 3 entries in the list can be made
		for idx, lst in enumerate(self.values[1:]):
			# for every sublist that has 2 elements, generate the corresponding  LIP
		    if len(lst) == 2:
		        val = self.firstOrderLag(idx)
		        
		        if idx == len(self.values)-2:
		            self.values.append([self.find_divisible_congruency(val)])
		        else:
		            self.values[idx+2].append(self.find_divisible_congruency(val))
		            
				# remove now unnecessary value from current sublist
		        self.values[idx+1].pop(0)

		# if there are k elements, than we are done, delete all elements and return the last value
		if len(self.values[0]) == self.k:
			signature = self.sign(doc, self.values[-1][0])
			for i in range(len(self.values)):
				self.values[i] = []
			return signature, True

		return None, False


	def firstOrderLag(self, idx):
		"""Calculates the (idx)th-ordered Lagrangian Interpolating Polynomial, evaluated at 0.

            :Parameter idx: The order of the next LIP
            :Type idx: int

            :Return: A Fraction class, containing the value of the (idx)th LIP, evaluated at 0

            :TODO I think the name of this function is missleading, should't it be nOrdLag.
        """

		j = -1
		i = j - (idx + 1)

		x1 = self.values[0][i]
		x2 = self.values[0][j]

		y1 = self.values[idx+1][-2]
		y2 = self.values[idx+1][-1]

		num = (0-x2)*y1-(0-x1)*y2
		den = x1-x2
		return Fraction(num, den)


	def find_divisible_congruency(self, fraction):
		"""Calculates a congruent integer to the numerator that is divisible by the denominator.

            :Parameter fraction: fraction, the fraction in question.
            :Type fraction: a Fraction object

            :Return: The z such that z = (num + i*prime)/den and z is an integer (without trunction).

            :TODO 
        """

		# Fracction class is used here because float division can't handle crypto-secure sized numbers,
		#  but Fraction uses integers, which can handle effectively infinite numbers
		num = Fraction(fraction.numerator % self.p,1)
		den = Fraction(fraction.denominator % self.p,1)

		i = 0
		z = (self.p*i+num)/den

		while z != int(z):
			i += 1
			z = (self.p*i+num)/den

		return int(z)

	def sign(self, doc, private_key):
		"""Function creates the digital signature for a given document with this voter's private key.

            :Parameter doc: The document that is being signed.
            :Type doc: String tuple

            :Parameter private_key: The private key for the DSA pair. (Comes from add_key_to_signature)
            :Type private_key: long or int

            :Return: A signature if this node has a public key, else None.

            :TODO Right now the doc param is a string 2-tuple, this might be better as just a String
            		since all that is needed is the document text and it would be more intuitive 
            		for future users.
        """

		if self.node.parent:
			# If voter is a subvoter, also send key to parent.
			self.node.vote(doc, key=data_to_key(private_key,self.n))

		if self.pubKey:
			# Sign the document. 
			key = DSA.construct((self.pubKey.y, self.pubKey.g, self.pubKey.p, self.pubKey.q, private_key))

			m = hashlib.sha256()
			m.update(doc[1].encode())
			h = m.digest()
			k = random.StrongRandom().randint(1,key.q-1)

			signature = key.sign(h,k)

			return signature

		return None

		
	def verify(self,doc, signature):
		"""Function verifies a digital signature. for a given document with this voter's public key.

            :Parameter doc: The document that is being signed.
            :Type doc: String

            :Parameter signature: DSA signature being verified.
            :Type signature: long 2-tuple

            :Return: True if the voter has a public key and the signature is correct, False otherwise.

            :TODO 
        """

		if self.pubKey:
			m = hashlib.sha256()
			m.update(doc.encode())
			h = m.digest()

			return self.pubKey.verify(h,signature)

		return False