from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from networks.lenet import LeNet
from random import randint

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def predictimg(path,lenet):
	image = plt.imread(path)
	confidence = lenet.predict(image)[0]
	predicted_class = np.argmax(confidence)
	for i in range(10):
		print(class_names[i], confidence[i]*100)
	return  predicted_class, class_names[predicted_class], confidence[predicted_class]
	
def predictclass(path, lenet, id):
	image = plt.imread(path)
	confidence = lenet.predict(image)[0]
	return confidence[id]

am = 15
id = 3
targetclass = 2
	
if __name__ == "__main__":
	lenet = LeNet()
	print(predictclass('./static/%s.jpg' % id, lenet, targetclass))
	img = Image.open('./static/%s.jpg' % id)
	imp = np.array(img)
	plt.imsave('./static/tmp.jpg', imp)
	prob = predictclass('./static/tmp.jpg', lenet, targetclass)
	
	while prob < 0.5:
		x = randint(0, 31)
		y = randint(0, 31)
		z = randint(0, 2)
		img = Image.open('./static/tmp.jpg')
		iml = img.load()
		if z == 0:
			iml[x, y] = (iml[x, y][0] ^ am, iml[x, y][1], iml[x, y][2])
		elif z == 1:
			iml[x, y] = (iml[x, y][0], iml[x, y][1] ^ am, iml[x, y][2])
		else:
			iml[x, y] = (iml[x, y][0], iml[x, y][1], iml[x, y][2] ^ am)
		iml = np.array(img)
		plt.imsave('./static/tmp2.jpg', iml)
		
		prob2 = predictclass('./static/tmp2.jpg', lenet, targetclass)
		if (prob2 > prob):
			prob = prob2
			print(prob2)
			plt.imsave('./static/tmp.jpg', iml)
	
	print(predictimg('./static/tmp.jpg', lenet))