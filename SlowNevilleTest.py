from SlowNeville import SlowNeville


p = 1004137

sn = SlowNeville(5,p)

keys = [(11, 382368), (8, 426359), (12, 343044), (2, 962623), (14, 929131)]

for i in range(len(keys)):
	soln = sn.addKey(keys[i])
	print(sn.values)
 	
print(soln[0])