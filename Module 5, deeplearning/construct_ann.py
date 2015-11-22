"""
construct_ann.py
Created by Neshat Naderi on 05/11/15.

References: http://cs231n.github.io/neural-networks-2
"""
import theano
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np
from mnist_basics import *
import sys, time
from math import ceil, floor, sqrt

''' Running command: THEANO_FLAGS=device=gpu,floatX=float32 python3 construct_ann.py '''

# Numpy printing options
np.set_printoptions(threshold=1000, edgeitems=38, linewidth=159)

''' Running command: THEANO_FLAGS=device=gpu,floatX=float32 python3 construct_ann.py '''
# measure process time
t0 = time.clock()
stop = minutes = seconds = 0

theano.config.exception_verbosity='high' # prints out the error message and what caused the error.
# raise Exception ('X:', X)

class Construct_ANN(object):

    """docstring for Construct_ANN"""
    def __init__(self, hidden_nodes, functions, lr, input_units=784, output_units=10):
        super(Construct_ANN, self).__init__()
        self.hidden_nodes = hidden_nodes
        self.learning_rate = lr
        self.functions = functions
        self.build_ann(hidden_nodes, self.learning_rate)


    def build_ann(self, hidden_nodes, lr):
        ann_weights, biases = get_net_weights(hidden_nodes)
        # functions = get_functions(len(hidden_nodes)+1)
        signals = T.fmatrix() # input signals
        lables = T.fmatrix() # input lables

        params = []
        for i in range(len(biases)):
            params.append(ann_weights[i])
            params.append(biases[i])

        p_outputs = model(signals, ann_weights, biases, self.functions)# probability outputs given input signals
        noisy = add_noise(signals, ann_weights, biases, self.functions)
        # print('p_out dim:',(p_outputs.broadcastable))

        max_predict = T.argmax(p_outputs, axis=1) # chooses the maximum prediction over the probabilities

        # maximizes the value there is there and minimizes the other values
        # classification metric to optimize
        # cost = T.mean(T.nnet.categorical_crossentropy(p_outputs, lables)) # without dropout
        cost = T.mean(T.nnet.categorical_crossentropy(noisy, lables)) # with dropout, but doesn't work :/
        # print('cost dim', cost.broadcastable)

        # cost = T.sum((signals - p_outputs)**2)

        # updates = sgd(cost, params, lr) # sgd:model1 without dropout
        updates = acc_sgd(cost, params, lr) #accelerated w/ momentum

        self.train = theano.function(inputs=[signals, lables], outputs=cost, updates=updates, allow_input_downcast=True)
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

# sgd : Stochastic Gradient Descent
# lr= 0.01 for zero mean gradient, larger migth give a worse final model
def sgd(cost, params, lr, momentum=0.8):
    grads = T.grad(cost=cost, wrt=params) # computes gradient of loss w/respect to params
    updates = []
    # Back propagation act
    for p, g in zip(params, grads):
        # param_update = theano.shared(p.get_value()*0., broadcastable=p.broadcastable)
        updates.append([p, p - g * lr])
        # updates.append((param_update, momentum*param_update + (1. - momentum)*g)) #gradient scaling
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

# ref: http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
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
        # updates.append((param_update, momentum*param_update + (1. - momentum)*g)) #gradient scaling
    return updates

# with dropout regularization, not regulizes biases
def add_noise(X, weights, biases, functions, p_drop_in=0.2, p_drop_out=0.5):
    # w/ acc_sgd & dropout
    # h = dropout(X, p_drop_in)
    h = functions[0]( T.dot(dropout(X, p_drop_in), weights[0])+biases[0] )
    # outputs = []
    for i in range(1,len(weights)):
        if functions[i] == T.nnet.sigmoid:
            weights[i] *= 4
        h = dropout(h, p_drop_out)
        h = functions[i](T.dot(h, weights[i])+biases[i])
        # outputs.append(h)
    # prediction = functions[-1]( T.dot(h, weights[-1])+biases[-1] )
    return h

def dropout(X, p=0.0):
    # X: input data
    # p: probability of keeping a unit active. higher = less dropout
    if p > 0:
        retain_prob = 1 - p
        noise = RandomStreams().binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
        X = X * (noise/retain_prob) # X w/noise
    return X

# converts lables to a 2D numpy array of 0's & 1's
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
    ''' paper on this topic, Delving Deep into Rectifiers:
    Surpassing Human-Level Performance on ImageNet Classification by He et al.,
    It derives an initialization specifically for ReLU neurons,
    reaching the conclusion that the variance of neurons
    in the network should be 2.0/n.'''
    # return theano.shared(floatX(np.random.uniform( -.1, .1, size=shape)))
    # shared variable of random floats sampled from a univariate “normal” (Gaussian) distribution of mean 0 and variance 1
    # return theano.shared(floatX(np.random.randn(*shape) * 0.01))
    # Initialize the weights by drawing them from a gaussian distribution with standard
    # deviation of sqrt(2/n), where n is the number of inputs to the neuron.
    return theano.shared(floatX(np.random.uniform( -.1, .1, size=shape) * (sqrt(2.0/n)) ))

def init_bias(shape):
    return theano.shared(floatX(np.random.uniform( -.1, .1, size=shape)))

def get_net_weights(hidden_nodes):
    network_weights = []
    biases = []
    if len(hidden_nodes)==0:
        network_weights.append(init_weights((784, 10), n=784))
        biases.append(init_bias(10))
        return network_weights, biases

    n0 = hidden_nodes[0]

    # append first hidden layer
    network_weights.append(init_weights((784, n0), n=784))
    biases.append( init_bias(n0) )

    for n_next in hidden_nodes[1:]:
        network_weights.append(init_weights((n0, n_next), n=n0))
        biases.append(init_bias(n_next))
        n0 = n_next

    # append output layer
    network_weights.append(init_weights((hidden_nodes[-1], 10), n=hidden_nodes[-1]))
    biases.append(init_bias(10))

    # returns weights for all layers in the network
    return network_weights, biases


def load_cases():
    # load both training & testing cases
    # training_cases = load_all_flat_cases('training')
    # testing_cases = load_all_flat_cases('testing')
    training_cases = load_flat_text_cases('all_flat_mnist_training_cases_text.txt')
    testing_cases = load_flat_text_cases('all_flat_mnist_testing_cases_text.txt')
    # seperate cases into images and their lables
    training_signals = np.array(training_cases[0])/255.0
    training_lables = training_cases[1]
    testing_signals  = np.array(testing_cases[0])/255.0
    testing_lables  = testing_cases[1]

    # Modify to 2D(lable arrays)numpy arrays of zeros & ones of length 10
    testing_lables  = one_hot_encoding(testing_lables, 10)
    training_lables = one_hot_encoding(training_lables, 10)

    return training_signals, training_lables, testing_signals, testing_lables


def train_on_batches(epochs, hidden_nodes, funcs, lr, batch_size=128):

    ann = Construct_ANN(hidden_nodes, funcs, lr)
    # traning_signals, training_lables, testing_signals, testing_lables = load_cases()
    tr_sig, tr_lbl, te_sig, te_lbl = load_cases()
    # Write results ans statistics to a file
    orig_stdout = sys.stdout
    f = open('testResults2.txt', 'a')
    sys.stdout = f
    print('***********************************************************************')
    print('With biases,', 'weights*sqrt(2/n),', 'noise/dropout, momentum' )
    print('functions = ', get_func_names(ann.functions), '\nlearning rate = ', ann.learning_rate)
    print('hidden nodes = ',ann.hidden_nodes)
    print ('epoch', '|','   occuracy', '\n---------------------')
    occuracy=0

    for i in range(epochs):
        for start, end in zip(range(0, len(tr_sig), 128), range(128, len(tr_sig), 128)):
            cost = ann.train(tr_sig[start:end], tr_lbl[start:end])
        occuracy = np.mean(np.argmax(te_lbl, axis=1) == ann.predict(te_sig))
        # if occuracy > occ:
        #     i -= 1
        # else:
        #     occuracy = occ
            # np.mean(np.argmax(te_lbl, axis=1) == ann.predict(te_sig))
        print (i+1,'       ', "{:.3f}".format(occuracy*100),'%' )
    answers = np.argmax(te_lbl, axis=1)
    predictions = ann.predict(te_sig)
    total = int(te_sig.size/784)
    print(sum(answers==predictions), 'out of', total, 'correct.')

    # Calculate processing time:
    stop = float(time.clock())
    minutes = (stop - t0)/60
    seconds = (stop - t0)%60
    print ('Running time: ', ceil(minutes), '(min)', ceil(seconds), '(s)')

    sys.stdout = orig_stdout
    f.close()
    return ann


# train 20 times, 2 hidden layers with 625 nodes,
trained_ann = train_on_batches(epochs=20, hidden_nodes=[625, 625], \
                funcs=[T.nnet.relu, T.nnet.relu, T.nnet.softmax], lr=0.001)

minor_demo(trained_ann)
