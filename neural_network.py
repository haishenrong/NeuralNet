from functions import sigmoid, sigmoid_prime, alpha_decay
from random import random


# initializes NN with corresponding input variables, hidden nodes, output variables:
# For each weight, w(i,j) = small number including bias weights
def initialize_network(numInputs, numHidden, numOutputs):
    network = []
    hidden_layer = []
    for i in range(numHidden):
        data = { 'weights':[] }
        for i in range(numInputs + 1):
            data['weights'].append(random())
        hidden_layer.append(data)
    network.append(hidden_layer)

    output_layer = []
    for i in range(numOutputs):
        data = { 'weights':[] } 
        for i in range(numHidden + 1):
            data['weights'].append(random())
        output_layer.append(data)
    network.append(output_layer)
    return network

# Activate neuron from inputs 
def activate(weights, inputs):
    last = len(weights)-1
    activation = weights[last] # bias weight
    for i in range(last):
        activation += weights[i] * inputs[i]
    return activation

# Propagate the inputs forward / copy input vector example to nodes of network
def forward_propagate(net, inputs):
    # for each layer l in NN
    dummy_inputs = inputs
    for l in net:
        next_input = []
        # for each node in layer l
        for node in l:
            node['output'] = sigmoid(activate(node['weights'], dummy_inputs)) # inj = SUMi of w(i,j) * ai
            next_input.append(node['output'])
        dummy_inputs = next_input
    return dummy_inputs

# Propagate delta backwards from output layer to input layer
def back_propagate(net, desired):
    # output layer delta[j] = g'(inj) * (yj - aj)
    output_layer = net[1]
    for j in range(len(output_layer)):
        node = output_layer[j]
        node['delta'] = sigmoid_prime(node['output'])*(desired[j] - node['output'])
    # hidden layer delta[i] = g'(ini) * sumj w(i,j) delta[j]
    hidden_layer = net[0]
    for i in range(len(hidden_layer)):
        error = 0.0
        for node in net[1]:
            error += (node['weights'][i]*node['delta'])
        node = hidden_layer[i]
        node['delta'] = sigmoid_prime(node['output'])*error
# Update every weight in the network using deltas
# For each weight in network: w(i,j) = w(i,j) + alpha * ai * delta[j]
def update_weights(net, inputs, step):
    # Hidden Layer
    hidden_outputs = []
    for node in net[0]:
        for i in range(len(inputs)):
            node['weights'][i] += step*inputs[i]*node['delta']
        node['weights'][len(node['weights'])-1] += step*node['delta'] # missing ai
        hidden_outputs.append(node['output'])
    # Outer Layer
    for node in net[1]:
        for j in range(len(hidden_outputs)):
            node['weights'][j] += step*hidden_outputs[j]*node['delta']
        node['weights'][len(node['weights'])-1] += step*node['delta'] # missing ai

def train_nn (net, data, step, epoch):
    for iteration in range(epoch):
        error = 0
        for row in data:
            outputs = forward_propagate(net, row)
            possible = [0] * 2
            possible[row[-1]] = 1
            #print(possible)
            for i in range(2):
                error += (possible[i]-outputs[i])**2
            #error += (possible[1]-outputs[1])**2
            back_propagate(net, possible)
            update_weights(net, row, step)
        print('epoch#:'+str(iteration)+' step:'+str(step)+' error:'+str(error))
        #step = alpha_decay(step)

def test(net, row):
    results = forward_propagate(net, row)
    return results.index(max(results))

file1 = open('.\\WDBC\\train.txt', 'r')
lines = file1.readlines()
file1.close()
data = [] 
for line in lines:
    line = line.replace('\n', '')
    one = line.split(' ')
    one = [float(i) for i in one]
    one[-1] = int(one[-1])
    data.append(one)

file2 = open('.\\WDBC\\test.txt', 'r')
lines2 = file2.readlines()
file2.close()
data_test = [] 
for line in lines2:
    line = line.replace('\n', '')
    one = line.split(' ')
    one = [float(i) for i in one]
    one[-1] = int(one[-1])
    data_test.append(one)

input_len = len(data[0]) - 1
output_len = len(set([row[-1] for row in data]))
network = initialize_network(input_len, 30, output_len)
train_nn(network, data, 0.30, 500)  

ones = 0
zero = 0
for layer in network:
    print(layer)
print(len(network[0]), len(network[1]))
correct = 0
total = 0
for row in data:
    prediction = test(network, row)
    total+=1
    if row[-1] == prediction:
        correct+=1
    if row[-1] == 0:
        zero+=1
    else:
        ones+=1
print('Training Set: Correct=%d, Total=%d, Ratio=%f'% (correct, total, correct/total))

correct2 = 0
total2 = 0
for row in data_test:
    prediction = test(network, row)
    total2+=1
    if row[-1] == prediction:
        correct2+=1
    if row[-1] == 0:
        zero+=1
    else:
        ones+=1
print('Test Set: Correct=%d, Total=%d, Ratio=%f'% (correct2, total2, correct2/total2))
print(zero, ones)
# f = open("neural_net.txt", "w")
# for layer in network:
#     for node in layer:
#         weights = []
#         for weight in node['weights']:
#             weights.append(str(weight)+' ')
#         output = str(node['output'])
#         delta = str(node['delta'])
#         f.writelines(weights)
#         f.write(' '+output)
#         f.write(' '+delta)
#         f.write('\n')
# f.close()


# # test backpropagation of error
# network = [[{'output': 0.7105668883115941, 'weights': [0.13436424411240122, 0.8474337369372327, 0.763774618976614]}],
#         [{'output': 0.6213859615555266, 'weights': [0.2550690257394217, 0.49543508709194095]}, {'output': 0.6573693455986976, 'weights': [0.4494910647887381, 0.651592972722763]}]]
# expected = [0, 1]
# back_propagate(network, expected)
# for layer in network:
#     print(layer)

# # test forward propagation
# network = [[{'weights': [0.13436424411240122, 0.8474337369372327, 0.763774618976614]}],
#         [{'weights': [0.2550690257394217, 0.49543508709194095]}, {'weights': [0.4494910647887381, 0.651592972722763]}]]
# row = [1, 0, None]
# output = forward_propagate(network, row)
# print(output)