#from PIL import Image
import  numpy
import glob
from skimage import io


imageFolderPath = 'bears/'
imagePath = glob.glob(imageFolderPath + '/*.jpeg')

im_array = numpy.zeros(1,1,3)
for img in imagePath:
	im = io.imread(img)
	feat = im.reshape(1,im.shape[0]*im.shape[1],3)	
	im_array = numpy.vstack([im_array, feat])
	print(img)
	print(im.shape)
	print(feat.shape)
	print(im)
	print('------')
	print(feat)
	print('------')
	print(im_array)
	#print(im1[:,:,2].item(15026))	
	break
#im_array = numpy.array( [numpy.array(Image.open(img).convert('L'), 'f') for img in imagePath] )

