# Lab 2 Linear Regression
import tensorflow as tf

tf.random.set_seed(777)
# X and Y data
x_train = [1, 2, 3]
y_train = [1, 2, 3]

# Try to find values for W and b to compute y_data = x_data * W + b
# We know that W should be 1 and b should be 0
# But let TensorFlow figure it out
W = tf.Variable(tf.random.normal([1]), name='weight')
b = tf.Variable(tf.random.normal([1]), name='bias')

h = x_train * W + b

cost = tf.reduce_mean(tf.square(h - y_train))

learning_rate = 0.01
for step in range(2001):
    with tf.GradientTape() as tape:
        h = x_train * W + b
        cost = tf.reduce_mean(tf.square(h - y_train))

        dc_dW, dc_db = tape.gradient(cost, [W, b])
        W.assign_sub(learning_rate * dc_dW)
        b.assign_sub(learning_rate * dc_db)

        if step % 20 == 0:
            print(step, cost.numpy(), W.numpy(), b.numpy())