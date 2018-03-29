from SlowNeville import SlowNeville

sn = SlowNeville(5)

keys = [(11, 382368), (8, 426359), (12, 343044), (2, 962623), (14, 929131)]

for i in range(len(keys)):
	sn.addKey(keys[i])
	print(sn.values)
 	

p = 1004137

num = sn.values[-1][0].numerator % p
den = sn.values[-1][0].denominator % p

i = 0
z = (p*i+num)/den
    
while z != int(z):
    i += 1
    z = (p*i+num)/den

print(z)