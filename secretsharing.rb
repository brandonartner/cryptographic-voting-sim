class Polynomial
    def initialize(coefficients)
        @coefficients = coefficients
    end

    def evaluate(x)
        value = 0
        for i in 0..@coefficients.size-1
            subvalue = @coefficients[i] * x ** (@coefficients.size - (i+1))
            value += subvalue
        end
        return value
    end

    def add_coeff(coeff)
        @coefficients << coeff
    end
end

def prime_generator(lo, hi)
=begin
    Generates a random prime number
    
    lo: Low bound for searching
    hi: High bound for searching
        
    Returns: Random prime within bounds
=end
    
    return 1237 # totally random
end

def random_distinct(lo, hi, size)
=begin
    Used to get lists of distinct random numbers,
    
    lo: Low bound for searching
    hi: High bound for searching
        
    Returns: Random numbers within bounds
=end

    v = Array.new

    while v.size < size
        randint = rand lo..hi
        
        if not v.include? randint
            v << randint
        end
    end

    return v
end

def sample(xs, size)
    copy = Array.new(xs)
    ys = Array.new

    for i in 0..size
        idx = rand 0..(copy.size-1)
        ys << copy[idx]
        copy.delete_at(idx)
    end

    return ys
end

def generate_polynomial(data, k)
=begin
=end
    p = prime_generator(nil, nil)

    coefficients = random_distinct(0, p, k-1)
    polynomial = Polynomial.new(coefficients)
    polynomial.add_coeff(data)

    return polynomial, p
end

def generate_keys(n, poly, p)
    xs = 1..(n+1)
    ys = Array.new

    for x in xs
        ys << poly.evaluate(x) % p
    end

    return xs.zip(ys)
end

def decrypt(keys, p)
    a, b = keys.transpose
    value = Rational(0)

    for i in 0..(b.size-1)
        subvalue = Rational(b[i])

        for j in 0..(a.size-1)
            if i != j
                subvalue *= Rational(a[j])/Rational(a[i]-a[j])
            end
        end

        value += subvalue
    end

    num = value.numerator % p
    den = value.denominator % p

    i = 0
    z = (p*i+num)/den

    while z != z.floor
        i += 1
        z = (p*i+num)/den
    end

    return z % p
end

    
n = 100000
k = 50001
d = rand 1..1236
poly, p = generate_polynomial(d, k)
keys = generate_keys(n, poly, p)

#puts poly
#puts keys

puts d
puts decrypt(keys, p)
