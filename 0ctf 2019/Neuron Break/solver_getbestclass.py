import numpy as np
from matplotlib import pyplot as plt
from networks.lenet import LeNet

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def predictimg(path,lenet):
	image = plt.imread(path)
	confidence = lenet.predict(image)[0]
	predicted_class = np.argmax(confidence)
	for i in range(10):
		print(class_names[i], confidence[i]*100)
	return  predicted_class, class_names[predicted_class], confidence[predicted_class]

id = 0 #imageid
	
if __name__ == "__main__":
	lenet = LeNet()
	print(predictimg('./static/%s.jpg' % id, lenet))