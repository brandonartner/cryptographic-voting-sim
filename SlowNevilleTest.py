from SlowNeville import SlowNeville


def find_congruence_with_divisibility(soln,p):
	
	num = soln.numerator % p
	den = soln.denominator % p

	i = 0
	z = (p*i+num)/den

	while z != int(z):
		i += 1
		z = (p*i+num)/den

	return z

p = 1004137

sn = SlowNeville(5)

keys = [(11, 382368), (8, 426359), (12, 343044), (2, 962623), (14, 929131)]

for i in range(len(keys)):
	soln = sn.addKey(keys[i])
	print(sn.values)
 	
print(find_congruence_with_divisibility(soln[0],p))

for i in range(len(keys)):
	soln = sn.addKey(keys[i])
	print(sn.values)


print(find_congruence_with_divisibility(soln[0],p))

