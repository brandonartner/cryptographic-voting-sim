import numpy as np
from Crypto.Util import number
import math

from fractions import Fraction

class Polynomial:
    ''' Class to evaluate simulated polynomials '''

    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(self.coefficients) - 1

    def evaluate(self, x):
        value = 0

        for i, c in enumerate(self.coefficients):
            value += c * x ** (self.degree - i)

        return value

    def stringify(self):
        s = ''

        for i, c in enumerate(self.coefficients):
            s = s + '{}*x**{}'.format(c, self.degree - i)

            if i < self.degree:
                s = s + '+'

        return s

def prime_generator(lo, hi):
    ''' Generates a random prime number
    
        lo: Low bound for searching
        hi: High bound for searching
        
        Returns: Random prime within bounds
    '''
    
    return 1004137 # totally random
    #return number.getStrongPrime(prime_size,false_positive_prob=1e-10) # totally random (yes... yes it is)

def random_distinct(lo, hi, size):
    ''' Used to get lists of distinct random numbers,
    
        lo: Low bound for searching
        hi: High bound for searching
        
        Returns: Random numbers within bounds
    '''
    
    v = []
    
    while len(v) < size:
        rand = np.random.randint(lo, hi)
        
        if rand not in v:
            v.append(rand)
            
    return v

def sample(xs, size):
    copy = [ x for x in xs ]
    ys = []
    
    for i in range(size):
        idx = np.random.randint(0, len(copy)-1)
        ys.append(copy.pop(idx))
        
    return ys

def generate_polynomial(data, k):
    ''' Makes a random polynomial
    
        data: The data as a numeric value to be split
        degree: The degree of the polynomial, and the minimum number of keys needed to decrypt
        
        Returns: polynomial as a function
    '''
    
    # will eventually give random primes greater than max{n, data}
    p = prime_generator(None, None)
    
    # Shamir's algorithms requires each coefficient to be distinct
    coefficients = random_distinct(0, p, k-1)
    # set data as 0th degree term
    coefficients.append(data)

    polynomial = Polynomial(coefficients)
    
    return polynomial, p

def generate_keys(n, poly, p):
    ''' Creates the keys
    
        n: Number of keys to be created
        poly: Polynomial function to create the keys
        p: Prime number for modular arithmetic
        
        Returns: n 2-tuples of keys
    '''
    
    # create distinct x values because f(a)=f(b) iff a=b 
    # implies less than n keys may be made
    X = range(1, n+1)
    
    # get corresponding y values
    Y = [poly.evaluate(x) % p for x in X]
    
    return list(zip(X, Y))

def find_congruence_with_divisibility(soln, p):

    num = soln.numerator % p
    den = soln.denominator % p

    i = 0
    z = (p*i+num)/den

    while z != int(z):
        i += 1
        z = (p*i+num)/den

    return int(z)

def decrypt(keys, p):
    ''' Uses Lagrange interpolation to decrypt data
    
        keys: List of keys to use in the decryption
        p: Prime number used to create finite field
        
        Returns: Decrypted data
    '''
    
    x, y = zip(*keys)
    value = Fraction(0)
    
    for i in range(len(y)):   
        product = Fraction(y[i])
        
        for j in range(len(x)):      
            if i == j:
                continue
                
            product *= Fraction(x[j], x[j]-x[i])

        value += product
        
    return find_congruence_with_divisibility(value, p)

def key_to_data(key, p):
    x, y = key
    
    xbin = bin(x)[2:]
    ybin = bin(y)[2:]

    # This now pads to make the first number the same bit length of the prime
    databin = '1' +xbin.zfill(len(bin(p)[2:])) + ybin
    data = int(databin, 2)

    return data

def data_to_key(data,p):
    databin = bin(data)[2:]
    prime_bit_len = len(bin(p)[2:])

    xbin = databin[1:prime_bit_len+1]
    #xbin = databin[:len(databin)/2]
    ybin = databin[prime_bit_len+1:]

    x = int('0b'+xbin, 2)
    y = int('0b'+ybin, 2)

    key = (x, y)

    return key

def next_multiple_of_128(data):
    '''Calculates the smallest number of bits bigger than the length of data and a multiple of 128.
    '''
    bin_data_len = len(bin(data)[2:]) 

    return math.ceil(bin_data_len/128)*128

def convvert_to_PEM(private_key):
    ''' Converts a private key integer to PEM format
    '''
    base64_key = 0

if __name__ == '__main__':
    from SlowNeville import SlowNeville

    np.random.seed(0)

    n = 8
    k = 5
    print('({}, {})-thresholding scheme'.format(n, k))

    D = 10
    print('Original data:', D)

    polynomial, p = generate_polynomial(D, k)
    print('Arithmetic modulo', p)
    print('Created polynomial:', polynomial.stringify())

    keys = generate_keys(n, polynomial, p)
    for key in keys:
        print('Generated key:', key)

    not_enough_keys = sample(keys, k-1)
    enough_keys = sample(keys, k)

    print('Incorrectly decrypted data:', decrypt(not_enough_keys, p))
    print('Correctly decrypted data:', decrypt(enough_keys, p))
