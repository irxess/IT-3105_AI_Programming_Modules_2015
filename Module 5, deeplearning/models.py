import mnist_basics as mb
import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import numpy as np
import matplotlib.pyplot as plt
import theano.tensor.nnet as Tann

''' Learning is based on a comparison of recent firing rates of neuron pairs.

    Number of hidden units = DxD_h (recall D is the number of 
    inputs and D_h is the number of hidden units).
    Learning rate =  a constant rate    
    Goal = minimize total error across all output nodes
    Method = modify weights throughout the network (i.e., at all levels) 
    to follow the route of steepest descent in error space.
    Each node = a pixel in mnist 

    '''
learning_rate = 0.001
units = 748
hidden_nodes = 500 #maybe in first hidden_layer
# topologi : ex. => 3 hidden_layers of sizes [20, 50, 30].

class models():
#training:
    def __init__(self, units, hidden_layers, learning_rate):
	
        self.training_cases = mb.load_mnist()
        self.testing_cases = mb.load_mnist(type='testing')

        self.learning_rate = learning_rate
        self.build_ann(units, hidden_layers)

    # def floatX(X):
    # 	return np.asarray(X, dypet=theano.config.floatX)

    def initialize(self, shape):
    	return theano.shared( np.random.uniform( -.1, .1, size=shape) )

    # Not testet
    def build_ann1(self, units, hidden_layers):
        
        parameters = []
        
        # input_layer 
    	input_matrix = T.fmatrix('input')
        weight_input = self.initialize( units, hidden_layers[0])
        # theano.shared( np.random.uniform( -.1,.1,size=(units,hidden_nodes) ) )
        biases_input = self.initialize(hidden_layers[0])
        # theano.shared(np.random.uniform(-.1,.1,size=hidden_nodes))
        
        # append the first layer parameters
        parameters.append( weight_input )
        parameters.append( biases_input )
        
        w1 = weight_input
        b1 = biases_input

        #build multilayers
        for i in range(1, len(hidden_layers)-1):

            weight_hidden = self.initialize( hidden_layers[i], units )
            biases_hidden = self.initialize(units)

        	# weight_hidden = theano.shared( np.random.uniform( -.1, .1, size=(hidden_layers, hidden_nodes) ) )
         #    biases_hidden = theano.shared( np.random.uniform(-.1, .1, size=units) )

            w2 = weight_hidden
            b2 = biases_hidden

        	# sigmoid, the activation function and its outputs== the neuron’s(node's) firing rate
            x_input = Tann.sigmoid(T.dot(input_vector, w1) + b1)
       		x_hidden = Tann.sigmoid( T.dot(x1, w2) + b2 )

       		# calculate the error = cost function
       		error = T.sum( (input_vector - x2)**2 )

       		# append parameters for each hidden layer
            parameters.append( weight_hidden )
            parameters.append( biases_hidden )

            # learning signal for parameter
            gradients = T.grad( error, parameters )
            
            # updates based on learning signal
            backprop_acts = [(p, p - self.learning_rate*g) for p,g in zip(parameters,gradients)]

            self.predictor = theano.function( [input], [x_hidden, x_input])

            self.trainer = theano.function( [input], error, updates=backprop_acts )

            #change variables to calculate for next hidden layers
            w1 = w2
            b1 = b2
            units = hidden_layers[i]


    def do_training(self, epochs=100, test_interval=None):
    	#converts each case into a vector of features (length = 28 x 28 = 784) and a class (0-9).
    	self.training_cases = reconstruc_flat_cases( mb.gen_flat_cases() )

        errors = []

        if test_interval:
        	self.avg_vector_distances = []

        for i in range(epochs):
            error = 0
            for c in self.training_cases:
                error += self.trainer(c)
            errors.append(error)
            if test_interval: 
            	self.consider_interim_test(i, test_interval)

        # graph.simple_plot(errors,xtitle="Epoch",ytitle="Error",title="")
        # TODO=>Draw the graph
        if test_interval:
            graph.newfig()
            graph.simple_plot(self.avg_vector_distances,xtitle='Epoch', \
                              ytitle='Avg Hidden-Node Vector Distance',title='')

    def do_testing(self, scatter=True):
    	#converts each case into a vector of features (length = 28 x 28 = 784) and a class (0-9).
    	self.testing_cases = reconstruc_flat_cases( mb.gen_flat_cases(cases=self.testing_cases) )

        hidden_activations = []
        for c in self.testing_cases:
            _, hact = self.predictor(c)
            hidden_activations.append(hact)
        
        # TODO => 
        # if scatter: 
        # 	graph.simple_scatter(hidden_activations,radius=8)

        return hidden_activations
        
    def consider_interim_test(self,epoch,test_interval):
    	# test in given interval
        if epoch % test_interval == 0:
            self.avg_vector_distances.append(calc_avg_vect_dist(self.do_testing(scatter=False)))
    	
    	
def test(units=748, hidden_layers=[30, 50, 20], learning_rate=0.001, epoches=100):
    model = models(units, hidden_layers, learning_rate)
    model.do_training(epochs)
    return model.do_testing()


    # def build_ann2(self, units, hidden_nodes, learning_rate):
    # 	# vector eller matrix???
    # 	input_vector = T.dvector('input')

    # 	weight_input = theano.shared( np.random.uniform( -.1,.1,size=(units,hidden_nodes) ) )
    #     biases_input = theano.shared(np.random.uniform(-.1,.1,size=hidden_nodes))

    #     weight_hidden = theano.shared( np.random.uniform( -.1,.1,size=(units,hidden_nodes) ) )
    #     biases_hidden = theano.shared(np.random.uniform(-.1,.1,size=units))

    #     biases_output = theano.shared( np.random.uniform(-.1) )

    # 	# Compute hidden layer
    # 	hidden = T.tanh( T.dot(input_vector, weight_input) + biases_hidden)

    # 	# compute output probability from hidden layer
    # 	output = Tann.softmax( T.dot(hidden, weight_hidden) + biases_output)
        
    #     # activation functions = output = the neuron’s firing rate
    #     x1 = Tann.sigmoid(T.dot(input_vector, w1) + b1)
    #     x2 = Tann.sigmoid( T.dot(x1, w2) + b2 )