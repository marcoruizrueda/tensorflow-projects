#from PIL import Image                                                            
import numpy                                                                     
import glob
from skimage import io


imageFolderPath = 'tensorflow-projects/cnn1/bears/'
imagePath = glob.glob(imageFolderPath + '/*.jpeg')

#im_array = []
for img in imagePath:
	im = io.imread(img)
	#im = numpy.array(Image.open(img).convert('L'), 'f')
	#print(im[:,:,0])	
	#print("-------------------------")	
	#print(im[:,:,0].ravel())
	#im_array[0] = im[:,:,0].ravel()	
	#numpy.expand_dims(im_array, 0)	
	#numpy.append(im_array, im[:,:,0].ravel(),0)
	#numpy.append(im_array, im[:,:,1].ravel(),1)
	#numpy.append(im_array, im[:,:,2].ravel(),2)
	im1 = im.reshape((1,im.shape[0]*im.shape[1],3))	
	print(img)
	print(im1.shape)	
	break
#im_array = numpy.array( [numpy.array(Image.open(img).convert('L'), 'f') for img in imagePath] )

