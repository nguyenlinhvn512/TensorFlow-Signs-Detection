import math
import numpy as np
import h5py
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
from tf_utils import load_dataset, random_mini_batches, convert_to_one_hot, predict
from forward_propagation import *
from compute_cost import *

tf.compat.v1.disable_eager_execution()

# %matplotlib inline
np.random.seed(1)

# Loading the dataset
X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()

# Example of a picture
index = 0
plt.imshow(X_train_orig[index])
print("y = " + str(np.squeeze(Y_train_orig[:, index])))

# Flatten the training and test images
X_train_flatten = X_train_orig.reshape(X_train_orig.shape[0], -1).T
X_test_flatten = X_test_orig.reshape(X_test_orig.shape[0], -1).T
# Normalize image vectors
X_train = X_train_flatten/255.
X_test = X_test_flatten/255.
# Convert training and test labels to one hot matrices
Y_train = convert_to_one_hot(Y_train_orig, 6)
Y_test = convert_to_one_hot(Y_test_orig, 6)

print("number of training examples = " + str(X_train.shape[1]))
print("number of test examples = " + str(X_test.shape[1]))
print("X_train shape: " + str(X_train.shape))
print("Y_train shape: " + str(Y_train.shape))
print("X_test shape: " + str(X_test.shape))
print("Y_test shape: " + str(Y_test.shape))


def create_placeholders(n_x, n_y):
    # """
    # Creates the placeholders for the tensorflow session.

    # Arguments:
    # n_x -- scalar, size of an image vector (num_px * num_px = 64 * 64 * 3 = 12288)
    # n_y -- scalar, number of classes (from 0 to 5, so -> 6)

    # Returns:
    # X -- placeholder for the data input, of shape [n_x, None] and dtype "tf.float32"
    # Y -- placeholder for the input labels, of shape [n_y, None] and dtype "tf.float32"

    # Tips:
    # - You will use None because it let's us be flexible on the number of examples you will for the placeholders.
    #   In fact, the number of examples during test/train is different.
    # """

    ### START CODE HERE ### (approx. 2 lines)
    X = tf.compat.v1.placeholder(tf.float32, shape=(n_x, None))
    Y = tf.compat.v1.placeholder(tf.float32, shape=(n_y, None))
    ### END CODE HERE ###

    return X, Y


def initialize_parameters():
    # """
    # Initializes parameters to build a neural network with tensorflow. The shapes are:
    #                     W1 : [25, 12288]
    #                     b1 : [25, 1]
    #                     W2 : [12, 25]
    #                     b2 : [12, 1]
    #                     W3 : [6, 12]
    #                     b3 : [6, 1]

    # Returns:
    # parameters -- a dictionary of tensors containing W1, b1, W2, b2, W3, b3
    # """

    # so that your "random" numbers match ours
    tf.compat.v1.set_random_seed(1)

    ### START CODE HERE ### (approx. 6 lines of code)
    W1 = tf.compat.v1.get_variable(
        "W1", [25, 12288], initializer=tf.compat.v1.keras.initializers.glorot_normal(seed=1))
    b1 = tf.compat.v1.get_variable("b1", [25, 1], initializer=tf.zeros_initializer())
    W2 = tf.compat.v1.get_variable(
        "W2", [12, 25], initializer=tf.compat.v1.keras.initializers.glorot_normal(seed=1))
    b2 = tf.compat.v1.get_variable("b2", [12, 1], initializer=tf.zeros_initializer())
    W3 = tf.compat.v1.get_variable(
        "W3", [6, 12], initializer=tf.compat.v1.keras.initializers.glorot_normal(seed=1))
    b3 = tf.compat.v1.get_variable(
        "b3", [6, 1], initializer=tf.zeros_initializer())
    ### END CODE HERE ###

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2,
                  "W3": W3,
                  "b3": b3}

    return parameters



def model(X_train, Y_train, X_test, Y_test, learning_rate=0.0001,
          num_epochs=1500, minibatch_size=32, print_cost=True):
    # """
    # Implements a three-layer tensorflow neural network: LINEAR->RELU->LINEAR->RELU->LINEAR->SOFTMAX.
    
    # Arguments:
    # X_train -- training set, of shape (input size = 12288, number of training examples = 1080)
    # Y_train -- test set, of shape (output size = 6, number of training examples = 1080)
    # X_test -- training set, of shape (input size = 12288, number of training examples = 120)
    # Y_test -- test set, of shape (output size = 6, number of test examples = 120)
    # learning_rate -- learning rate of the optimization
    # num_epochs -- number of epochs of the optimization loop
    # minibatch_size -- size of a minibatch
    # print_cost -- True to print the cost every 100 epochs
    
    # Returns:
    # parameters -- parameters learnt by the model. They can then be used to predict.
    # """

    # to be able to rerun the model without overwriting tf variables
    ops.reset_default_graph()
    # to keep consistent results
    tf.compat.v1.set_random_seed(1)
    seed = 3                                          # to keep consistent results
    # (n_x: input size, m : number of examples in the train set)
    (n_x, m) = X_train.shape
    n_y = Y_train.shape[0]                            # n_y : output size
    costs = []                                        # To keep track of the cost

    # Create Placeholders of shape (n_x, n_y)
    ### START CODE HERE ### (1 line)
    X, Y = create_placeholders(n_x, n_y)
    ### END CODE HERE ###

    # Initialize parameters
    ### START CODE HERE ### (1 line)
    parameters = initialize_parameters()
    ### END CODE HERE ###

    # Forward propagation: Build the forward propagation in the tensorflow graph
    ### START CODE HERE ### (1 line)
    Z3 = forward_propagation(X, parameters)
    ### END CODE HERE ###

    # Cost function: Add cost function to tensorflow graph
    ### START CODE HERE ### (1 line)
    cost = compute_cost(Z3, Y)
    ### END CODE HERE ###

    # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.
    ### START CODE HERE ### (1 line)
    optimizer = tf.compat.v1.train.AdamOptimizer(
        learning_rate=learning_rate).minimize(cost)
    ### END CODE HERE ###

    # Initialize all the variables
    init = tf.compat.v1.global_variables_initializer()

    # Start the session to compute the tensorflow graph
    with tf.compat.v1.Session() as sess:

        # Run the initialization
        sess.run(init)

        # Do the training loop
        for epoch in range(num_epochs):

            epoch_cost = 0.                       # Defines a cost related to an epoch
            # number of minibatches of size minibatch_size in the train set
            num_minibatches = int(m / minibatch_size)
            seed = seed + 1
            minibatches = random_mini_batches(
                X_train, Y_train, minibatch_size, seed)

            for minibatch in minibatches:

                # Select a minibatch
                (minibatch_X, minibatch_Y) = minibatch

                # IMPORTANT: The line that runs the graph on a minibatch.
                # Run the session to execute the "optimizer" and the "cost", the feedict should contain a minibatch for (X,Y).
                ### START CODE HERE ### (1 line)
                _, minibatch_cost = sess.run([optimizer, cost], feed_dict={
                                             X: minibatch_X, Y: minibatch_Y})
                ### END CODE HERE ###

                epoch_cost += minibatch_cost / minibatch_size

            # Print the cost every epoch
            if print_cost == True and epoch % 100 == 0:
                print("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)

        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per fives)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        # lets save the parameters in a variable
        parameters = sess.run(parameters)
        print("Parameters have been trained!")

        # Calculate the correct predictions
        correct_prediction = tf.equal(tf.argmax(Z3), tf.argmax(Y))

        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        print("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))

        return parameters


parameters = model(X_train, Y_train, X_test, Y_test)
