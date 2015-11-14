import theano
from theano import tensor as T
import numpy as np
from mnist_basics import load_all_flat_cases, load_flat_cases
import sys, time
from math import ceil, floor

# measure process time
t0 = time.clock()
stop = minutes = seconds = 0

theano.config.exception_verbosity='high'
# raise Exception ('X:', X)

class Construct_ANN(object):

    """docstring for Construct_ANN"""
    def __init__(self, hidden_nodes, functions, lr, input_units=784):
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
        # print(ann_weights)
        max_predict = T.argmax(p_outputs, axis=1) # chooses the maximum prediction over the probabilities
        
        # maximizes the value there is there and minimizes the other values
        cost = T.mean(T.nnet.categorical_crossentropy(p_outputs, lables)) # classification metric to optimize
        # cost = T.sum((signals - p_outputs)**2)
        updates = sgd(cost, params, lr)
        self.train = theano.function(inputs=[signals, lables], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[signals], outputs=max_predict, allow_input_downcast=True)
        # self.blind_test = theano.function(inputs=[signals], outputs=max_predict, allow_input_downcast=True)


def get_func_names(funcs):
    names=[]
    for f in funcs:
        if f==T.tanh: names.append('tanh')
        elif f==T.nnet.relu: names.append('relu')
        elif f==T.nnet.softmax: names.append('softmax')
        else: names.append(f.name)
    return names

def model(X, weights, biases, functions):
    h = X
    # print(functions, len(functions))
    # print(weights, len(weights))
    for i in range(len(weights)):
        if functions[i] == T.nnet.sigmoid:
            weights[i] *= 4
        h = functions[i](T.dot(h, weights[i])+biases[i])
    return h     

# for usage with relu
def model2(X, weights, functions):
    h = X
    outputs = []
    for i in len(weights):
        h = functions[i](T.dot(h, weights[i]))
        outputs.append(h)
    return outputs  
    
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

def init_weights(shape):
    return theano.shared(floatX(np.random.uniform( -.1, .1, size=shape)))
    # return theano.shared(floatX(np.random.randn(*shape) * 0.01))


def get_net_weights(hidden_nodes):
    network_weights = []
    biases = []
    n0 = hidden_nodes[0]
    
    # append first hidden layer 
    network_weights.append(init_weights((784, n0)))
    biases.append( init_weights(n0) )
   
    for n_next in hidden_nodes[1:]:
        network_weights.append(init_weights((n0, n_next)))
        biases.append(init_weights(n_next))
        n0 = n_next

    # append output layer
    network_weights.append(init_weights((hidden_nodes[-1], 10)))
    biases.append(init_weights(10))

    
    # returns weights for all layers in the network
    return network_weights, biases

# sgd : Stochastic Gradient Descent
# lr= 0.01 for zero mean gradient, larger migth give a worse final model
def sgd(cost, params, lr):
    grads = T.grad(cost=cost, wrt=params) # computes gradient of loss w/respect to params
    updates = []
    # Back propagation act
    for p, g in zip(params, grads):
        updates.append([p, p - g * lr])
    return updates

def load_cases():
    # load both training & testing cases
    training_cases = load_all_flat_cases('training')
    testing_cases = load_all_flat_cases('testing')
  
    # seperate cases into images and their lables
    training_signals = np.array(training_cases[0])/255.0
    training_lables = training_cases[1]
    testing_signals  = np.array(testing_cases[0])/255.0
    testing_lables  = testing_cases[1]

    # Modify to 2D(lable arrays)numpy arrays of zeros & ones of length 10 
    testing_lables  = one_hot_encoding(testing_lables, 10)
    training_lables = one_hot_encoding(training_lables, 10)

    return training_signals, training_lables, testing_signals, testing_lables


def train_on_batches(nof_training, hidden_nodes, funcs, lr, batch_size=128):
    ann = Construct_ANN(hidden_nodes, funcs, lr)
    # traning_signals, training_lables, testing_signals, testing_lables = load_cases()
    tr_sig, tr_lbl, te_sig, te_lbl = load_cases()
    costs = []
    # Write results ans statistics to a file
    orig_stdout = sys.stdout
    f = open('testResults.txt', 'a')
    sys.stdout = f
    print('-------------------------------------------------------------------')
    print('With biases')
    print('functions = ', get_func_names(ann.functions), '\nlearning rate = ', ann.learning_rate)
    print('hidden nodes = ',ann.hidden_nodes)
    for i in range(nof_training):
        for start, end in zip(range(0, len(tr_sig), 128), range(128, len(tr_sig), 128)):
            cost = ann.train(tr_sig[start:end], tr_lbl[start:end])
        costs.append(cost)
        print ('i:', i+1,' ', np.mean(np.argmax(te_lbl, axis=1) == ann.predict(te_sig)) )
    # Calculate processing time:
    stop =  float(time.clock())
    minutes = (stop - t0)/60
    seconds = (stop - t0)%60
    print ('Running time: ', ceil(minutes), '(min)', ceil(seconds), '(s)')
    sys.stdout = orig_stdout
    f.close()
    return costs

### TODO ###
# implement correct blind_test, or ask??
def blind_testing(feature_sets):
    cases = np.array(load_cases(feature_sets))/255.0
    # signals = np.array(cases[0])/255.0
# test
# blind_testing()

train_on_batches(nof_training=20, hidden_nodes=[625, 625, 441], \
                funcs=[T.tanh, T.nnet.sigmoid, T.tanh, T.nnet.softmax], lr=0.02)



