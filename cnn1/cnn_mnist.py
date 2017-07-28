from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Imports
import os
import numpy as np
import tensorflow as tf

from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

tf.logging.set_verbosity(tf.logging.INFO)


def cnn_model_fn(features, labels, mode):
  """Model function for CNN. 
     Example from: https://www.tensorflow.org/tutorials/layers#create_the_estimator"""
  
  # Input Layer
  input_layer = tf.reshape(features, [-1, 28, 28, 1])

  # Convolutional Layer #1
  conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=32,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #1
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2) #stride=[3, 6] for w and h, 50% reduction 

  # Convolutional Layer #2 and Pooling Layer #2
  conv2 = tf.layers.conv2d(
      inputs=pool1,
      filters=64,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2) 

  # Dense Layer
  pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64]) #Flat featMap:7(pool2 width)*7(pool2 height)*64(pool2 channels)=[batch_size, 3136]
  dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
  dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training = (mode == learn.ModeKeys.TRAIN) ) #40% of elements will be randomly dropped out during training.

  # Logits Layer
  logits = tf.layers.dense(inputs=dropout, units=10) #Raw values

  loss = None
  train_op = None

  # Calculate Loss (for both TRAIN and EVAL modes)
  if mode != learn.ModeKeys.INFER:
    onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
    loss = tf.losses.softmax_cross_entropy(
        onehot_labels=onehot_labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == learn.ModeKeys.TRAIN:
    train_op = tf.contrib.layers.optimize_loss(
        loss=loss,
        global_step=tf.contrib.framework.get_global_step(),
        learning_rate=0.001,
        optimizer="SGD")

  # Generate Predictions
  predictions = {
      "classes": tf.argmax(
          input=logits, axis=1),
      "probabilities": tf.nn.softmax(
          logits, name="softmax_tensor")
  }

  # Return a ModelFnOps object
  return model_fn_lib.ModelFnOps(
      mode=mode, predictions=predictions, loss=loss, train_op=train_op)


def main(unused_argv):
  # Load training and eval data
  mnist = learn.datasets.load_dataset("mnist")
  train_data = mnist.train.images # Returns np.array
  #print(train_data.shape)
  #print(train_data[1:5,240:280])
  train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
  #print(train_labels[1:10])
  eval_data = mnist.test.images # Returns np.array
  eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

  # Create the Estimator
  mnist_classifier = learn.Estimator(
      model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")

  # Set up logging for predictions
  tensors_to_log = {"probabilities": "softmax_tensor"}
  logging_hook = tf.train.LoggingTensorHook(
      tensors=tensors_to_log, every_n_iter=500)

  # Train the model
  mnist_classifier.fit(
    x=train_data,
    y=train_labels,
    batch_size=100,
    steps=20000,
    monitors=[logging_hook])

  # Configure the accuracy metric for evaluation
  metrics = {
    "accuracy":
        learn.MetricSpec(
            metric_fn=tf.metrics.accuracy, prediction_key="classes"),
	}

  # Evaluate the model and print results
  eval_results = mnist_classifier.evaluate(
    x=eval_data, y=eval_labels, metrics=metrics)
  print(eval_results)


if __name__ == "__main__":
  tf.app.run()

