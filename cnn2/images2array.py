
import  numpy
import glob
from skimage import io
import numpy.matlib
import os


def flat_pixels(imageFolderPath, ext):
	"""---."""
	imagePath = glob.glob(imageFolderPath + ext)
	featues_path = []
	for img in imagePath:
		im = io.imread(img)
		feat_im = im.reshape(1,im.shape[0]*im.shape[1],3)	
		if featues_path==[]:
			featues_path = feat_im
		else:
			featues_path = numpy.vstack((featues_path, feat_im))
		#print(img)

	#Return flatten pixels from images of path
	return featues_path


def do_labels(num_imagens, label):
	"""---."""
	labels_path = numpy.full((num_imagens, 1), label)	
	
	return labels_path


def main(folderPath, ext):
	"""---."""
	label = 0
	labels = []
	features = []
	
	for root,dirs,_ in os.walk(folderPath):
		for d in dirs:
			label = label+1
			path = os.path.join(root,d)			
			features_path = flat_pixels(path+os.sep, ext)
			labels_path = do_labels(len(features_path), label)
			
			if features==[]:
				features = features_path
				labels = labels_path
			else:
				features = numpy.vstack((features, features_path))
				labels = numpy.vstack((labels, labels_path))
	
	return features, labels

if __name__ == "__main__":
	features = main(folderPath='bears/train/', ext='*.jpg')
	
