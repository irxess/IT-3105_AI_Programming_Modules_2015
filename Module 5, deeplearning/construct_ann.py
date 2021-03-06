"""
construct_ann.py
Created by Neshat Naderi on 05/11/15.

References: http://cs231n.github.io/neural-networks-2
"""
import sys
import theano
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np
from mnist_basics import *
import sys, time
from math import ceil, floor, sqrt

# Numpy printing options
np.set_printoptions(threshold=1000, edgeitems=38, linewidth=159)

theano.config.exception_verbosity='high' # prints out the error message and what caused the error.

class Construct_ANN(object):

    """docstring for Construct_ANN"""
    def __init__(self, hidden_nodes, functions, lr, input_units=784, output_units=10, max_of_outputs=True):
        super(Construct_ANN, self).__init__()
        self.hidden_nodes = hidden_nodes
        self.learning_rate = lr
        self.functions = functions
        self.build_ann(hidden_nodes, self.learning_rate, input_units, output_units, max_of_outputs)


    def build_ann(self, hidden_nodes, lr, input_units, output_units, max_of_outputs):
        ann_weights, biases = get_net_weights(hidden_nodes, input_units, output_units)
        signals = T.fmatrix() # input signals
        labels = T.fmatrix() # input labels

        params = []
        for i in range(len(biases)):
            params.append(ann_weights[i])
            params.append(biases[i])

        p_outputs = model(signals, ann_weights, biases, self.functions)# probability outputs given input signals
        # p_outputs = model2(signals, ann_weights, biases, self.functions) #w/dropout
        if max_of_outputs:
            max_predict = T.argmax(p_outputs, axis=1) # chooses the maximum prediction over the probabilities
        else:
            max_predict = p_outputs[0]

        # classification metric to optimize
        # cost = T.mean(T.nnet.categorical_crossentropy(p_outputs, labels)) # without dropout
        cost = T.mean(T.nnet.categorical_crossentropy(p_outputs, labels)) # with dropout, but doesn't work :/
        # cost = T.sum((signals - p_outputs)**2)#different cost function

        # updates = sgd(cost, params, lr) # sgd:model1 without dropout
        updates = acc_sgd(cost, params, lr) #accelerated w/ momentum

        self.train = theano.function(inputs=[signals, labels], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[signals], outputs=max_predict, allow_input_downcast=True)


    def blind_test(self, test_input):
        test_cases = np.array(test_input)/255.0
        test_count = len(test_input)

        predictions = []
        pred_index = 0

        prediction = self.predict(test_cases)
        for ele in prediction:
            predictions.append( int(ele) )
            pred_index += 1

        # return predictions
        return predictions[:pred_index]

def softmax(X):
    # numerically more stable than tensor.nnet.softmax
    # suggested in theano doc.
    e_x = T.exp(X - X.max(axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)

def get_func_names(funcs):
    names=[]
    for f in funcs:
        if f==T.tanh: names.append('tanh')
        elif f==T.nnet.relu: names.append('relu')
        elif f==T.nnet.softmax or f==softmax: names.append('softmax')
        else: names.append(f.name)
    return names

# Stochastic Gradient Descent
def sgd(cost, params, lr, momentum=0.8):
    grads = T.grad(cost=cost, wrt=params) # computes gradient of loss w/respect to params
    updates = []
    # Back propagation act
    for p, g in zip(params, grads):
        updates.append([p, p - g * lr])
    return updates

def model(X, weights, biases, functions):
    """ Calculate the activation function for each layer. """
    # w/ sgd
    h = X
    for i in range(len(weights)):
        if functions[i] == T.nnet.sigmoid:
            weights[i] *= 4
        h = functions[i](T.dot(h, weights[i])+biases[i])
    return h

def acc_sgd(cost, params, lr=0.001, momentum=0.9, epsilon=1e-6):
    # this function accelerates convergence by momentum
    grads = T.grad(cost=cost, wrt=params) # computes gradient of loss w/respect to params
    updates = []
    # Back propagation act
    for p, g in zip(params, grads):
        accumulator = theano.shared(p.get_value()*0., broadcastable=p.broadcastable)
        acc_new = momentum * accumulator + (1 - momentum) * g ** 2
        gradient_scaling = T.sqrt(acc_new + epsilon)
        g = g / gradient_scaling
        updates.append((p, p - g * lr))
        updates.append((accumulator, acc_new))
    return updates

# with dropout regularization, not regulizes biases
def model2(X, weights, biases, functions, p_drop_in=0.2, p_drop_out=0.5):
    h = functions[0]( T.dot(dropout(X, p_drop_in), weights[0])+biases[0] )
    for i in range(1,len(weights)):
        if functions[i] == T.nnet.sigmoid:
            weights[i] *= 4
        h = dropout(h, p_drop_out)
        h = functions[i](T.dot(h, weights[i])+biases[i])
    return h

def dropout(X, p=0.0):
    # X: input data
    # p: probability of keeping a unit active. higher = less dropout
    if p > 0:
        retain_prob = 1 - p
        noise = RandomStreams().binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
        X = X * (noise/retain_prob)
    return X

# converts labels to a 2D numpy array of 0's & 1's
def one_hot_encoding(x,n):
    if type(x) == list:
        x = np.array(x)
    x = x.flatten()
    lbls = np.zeros((len(x),n))
    lbls[np.arange(len(x)),x] = 1
    return lbls

def get_functions(length, funcs=[T.tanh, T.nnet.sigmoid]):
    if len(funcs) == length:
        return funcs
    print('Length not matching function list length')
    return False

def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

#ReLU units will have a positive mean.
def init_weights(shape, n):
    return theano.shared(floatX(np.random.uniform( -.1, .1, size=shape) * (sqrt(2.0/n)) ))

def init_bias(shape):
    return theano.shared(floatX(np.random.uniform( -.1, .1, size=shape)))

def get_net_weights(hidden_nodes, input_units, output_units):
    network_weights = []
    biases = []
    if len(hidden_nodes)==0:
        network_weights.append(init_weights((input_units, output_units), n=input_units))
        biases.append(init_bias(output_units))
        return network_weights, biases

    n0 = hidden_nodes[0]

    # append first hidden layer
    network_weights.append(init_weights((input_units, n0), n=input_units))
    biases.append( init_bias(n0) )

    for n_next in hidden_nodes[1:]:
        network_weights.append(init_weights((n0, n_next), n=n0))
        biases.append(init_bias(n_next))
        n0 = n_next

    # append output layer
    network_weights.append(init_weights((hidden_nodes[-1], output_units), n=hidden_nodes[-1]))
    biases.append(init_bias(output_units))

    # returns weights for all layers in the network
    return network_weights, biases


def load_cases():
    # load both training & testing cases
    # training_cases = load_all_flat_cases('training')
    # testing_cases = load_all_flat_cases('testing')
    training_cases = load_flat_text_cases('all_flat_mnist_training_cases_text.txt')
    testing_cases = load_flat_text_cases('all_flat_mnist_testing_cases_text.txt')
    # seperate cases into images and their labels
    training_signals = np.array(training_cases[0])/255.0
    training_labels = training_cases[1]
    testing_signals  = np.array(testing_cases[0])/255.0
    testing_labels  = testing_cases[1]

    # Modify to 2D(lable arrays)numpy arrays of zeros & ones of length 10
    testing_labels  = one_hot_encoding(testing_labels, 10)
    training_labels = one_hot_encoding(training_labels, 10)

    return training_signals, training_labels, testing_signals, testing_labels


def train_on_batches(epochs, hidden_nodes, funcs, lr, batch_size=128):
    ann = Construct_ANN(hidden_nodes, funcs, lr)
    # traning_signals, training_labels, testing_signals, testing_labels = load_cases()
    tr_sig, tr_lbl, te_sig, te_lbl = load_cases()

    # Write results and statistics to a file
    # orig_stdout = sys.stdout
    # f = open('testResults2.txt', 'a')
    # sys.stdout = f
    # print('***********************************************************************')
    # print('functions = ', get_func_names(ann.functions), '\nlearning rate = ', ann.learning_rate)
    # print('hidden nodes = ',ann.hidden_nodes)
    # print ('epoch', '|','   occuracy', '\n---------------------')

    for i in range(epochs):
        for start, end in zip(range(0, len(tr_sig), 128), range(128, len(tr_sig), 128)):
            cost = ann.train(tr_sig[start:end], tr_lbl[start:end])
            # sys.exit(0)
        occuracy = np.mean(np.argmax(te_lbl, axis=1) == ann.predict(te_sig))
        # print(occuracy)
    answers = np.argmax(te_lbl, axis=1)
    predictions = ann.predict(te_sig)
    total = int(te_sig.size/784)
    # print(sum(answers==predictions), 'out of', total, 'correct.')
    print('functions = ', get_func_names(ann.functions), '\nlearning rate = ', ann.learning_rate)
    print(hidden_nodes)

    # sys.stdout = orig_stdout
    # f.close()
    return ann

def parse_input(envir=globals()):
    functions = eval('[' + sys.argv[1] + ']', envir)
    layer_sizes = eval('[' + sys.argv[2] + ']', envir)
    learning_rate = eval(sys.argv[3], envir)
    return (functions, layer_sizes, learning_rate)

# only run this if we're not being imported
if __name__ == "__main__":
    # train 20 times, 2 hidden layers with 625 nodes
    funct, layrs, lrt = parse_input()
    trained_ann = train_on_batches(epochs=20, hidden_nodes=layrs, funcs=funct, lr=lrt)
    # trained_ann = train_on_batches(epochs=20, hidden_nodes=[625, 625], \
    #                 funcs=[T.nnet.relu, T.nnet.relu, softmax], lr=0.001)
    minor_demo(trained_ann)
