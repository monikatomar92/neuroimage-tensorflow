import numpy as np
import tensorflow as tf
import nibabel as nib

# >>> img = nib.load(example_filename)

# PW 2017/03/01: Following along here:
#   http://warmspringwinds.github.io/tensorflow/tf-slim/2016/12/21/tfrecords-guide/

# test dataset
filename_pairs = [
('/home/paul/cmet/brainhack/neuroimage-tensorflow/bucker40/114/norm.nii.gz',
'/home/paul/cmet/brainhack/neuroimage-tensorflow/bucker40/114/aseg.nii.gz'),
('/home/paul/cmet/brainhack/neuroimage-tensorflow/bucker40/091/norm.nii.gz',
'/home/paul/cmet/brainhack/neuroimage-tensorflow/bucker40/091/aseg.nii.gz'),
('/home/paul/cmet/brainhack/neuroimage-tensorflow/bucker40/130/norm.nii.gz',
'/home/paul/cmet/brainhack/neuroimage-tensorflow/bucker40/130/aseg.nii.gz')
                 ]
def _bytes_feature(value):
	return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# PW 2017/03/01: Can/Should we get away in uint8?
def _int64_feature(value):
	return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

tfrecords_filename = 'buckner40.tfrecords'
writer = tf.python_io.TFRecordWriter(tfrecords_filename)
# To compare original to reconstructed images
original_images = []

for v_filename, l_filename in filename_pairs:

	# The volume, in nifti format	
	v_nii = nib.load(v_filename)
	# The volume, in numpy format
	v_np = v_nii.get_data()
	# The volume, in raw string format
	v_raw = v_np.tostring()

	# The label, in nifti format
	l_nii = nib.load(l_filename)
	# The label, in numpy format
	l_np = l_nii.get_data()
	# The label, in raw string format
	l_raw = l_np.tostring()

	# Dimensions
	x_dim = v_np.shape[0]
	y_dim = v_np.shape[1]
	z_dim = v_np.shape[2]

    # Put in the original images into array for future check for correctness
	original_images.append((v_np, l_np))

	data_point = tf.train.Example(features=tf.train.Features(feature={
		'x_dim': _int64_feature(x_dim),
		'y_dim': _int64_feature(y_dim),
		'z_dim': _int64_feature(z_dim),
		'image_raw': _bytes_feature(v_raw),
		'label_raw': _bytes_feature(l_raw)}))
    
	writer.write(data_point.SerializeToString())

writer.close()

##############################################################

# Reconstruct images from 'buckner40.tfrecords' can compare to originals

reconstructed_images = []

record_iterator = tf.python_io.tf_record_iterator(path=tfrecords_filename)

for string_record in record_iterator:
    
    example = tf.train.Example()
    example.ParseFromString(string_record)
    
    x_dim = int(example.features.feature['x_dim']
                                 .int64_list
                                 .value[0])
    
    y_dim = int(example.features.feature['y_dim']
                                .int64_list
                                .value[0])

    z_dim = int(example.features.feature['z_dim']
                                .int64_list
                                .value[0])
    
    image_raw = (example.features.feature['image_raw']
                                  .bytes_list
                                  .value[0])
    
    label_raw = (example.features.feature['label_raw']
                                .bytes_list
                                .value[0])
    
    img_1d = np.fromstring(img_string, dtype=np.uint8)
    reconstructed_img = img_1d.reshape((height, width, -1))
    
    annotation_1d = np.fromstring(annotation_string, dtype=np.uint8)
    
    # Annotations don't have depth (3rd dimension)
    reconstructed_annotation = annotation_1d.reshape((height, width))
    
    reconstructed_images.append((reconstructed_img, reconstructed_annotation))
    


# img =  nib.load(filename_pairs[0][0])













