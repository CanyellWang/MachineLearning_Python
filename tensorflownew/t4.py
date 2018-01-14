import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

minist = input_data.read_data_sets("./minist",one_hot = True)

print ("read complete")

x = tf.placeholder(tf.float32,[None,784])

W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x,W)+b)
y_ = tf.placeholder(tf.float32,[None,10])

cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.global_variables_initializer()
sess =tf.Session()
sess.run(init)
for i in range(1000):
    batch_xs ,batch_ys = minist.train.next_batch(100)
    sess.run([train_step,y],feed_dict={x:batch_xs,y_:batch_ys})
    #print ("y predicted is {0}".format(y))
    #print ("y is {0}".format(y_))

correct_prediction = tf.equal(tf.arg_max(y,1),tf.arg_max(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

print("Accuarcy on Test-dataset: ", sess.run(accuracy, feed_dict={x: minist.test.images, y_: minist.test.labels}))
