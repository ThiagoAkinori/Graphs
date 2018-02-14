import os

count = 1
for i in range(20893614, 20956483):
	try:
		os.rename('art_and_culture-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20906848, 20956841):
	try:
		os.rename('business-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')


for i in range(20920852, 20956778):
	try:
		os.rename('crime-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20858793, 20955083):
	try:
		os.rename('fashion-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20905216, 20955731):
	try:
		os.rename('health-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20809566, 20955150):
	try:
		os.rename('politics_us-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20802892, 20979458):
	try:
		os.rename('politics_world-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20860321, 20955108):
	try:
		os.rename('science-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20934852, 20956865):
	try:
		os.rename('sports-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')

for i in range(20916454, 20955348):
	try:
		os.rename('tech-'+str(i)+'.txt',"texto"+str(count)+'.txt')
		count = count + 1
	except:
		print ('not found')
