import math

def get_network(file):
    file1 = open(file, 'r')
    lines = file1.readlines()
    file1.close()
    network = []
    layer = []
    for i in range(len(lines)-2):
        node = {
            "weights":[],
            "output":0.0,
            "delta":0.0
        }
        one = lines[i].replace('\n', '')
        one = one.split(' ')
        one = [float(i) for i in one]
        node["delta"] = one.pop()
        node["output"] = one.pop()
        node["weights"] = one
        layer.append(node)
    network.append(layer)
    layer2 = []
    for i in range(len(lines)-2, len(lines)):
        node = {
        "weights":[],
        "output":0.0,
        "delta":0.0
        }
        two = lines[i].replace('\n', '')
        two = two.split(' ')
        two = [float(i) for i in two]
        node["delta"] = two.pop()
        node["output"] = two.pop()
        node["weights"] = two
        layer2.append(node)
    network.append(layer2)
    return network

def sigmoid(x):
    return 1.0/(1.0+math.exp(-x))

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

def test(net, row):
    results = forward_propagate(net, row)
    return results.index(max(results))


network = get_network('neural_net.txt')
# for layer in network:
#     print('hi')
#     for node in layer:
#         print(node)
for layer in network:
    print(layer)

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

correct2 = 0
total2 = 0
for row in data_test:
    print(row)
    prediction = test(network, row)
    total2+=1
    if row[-1] == prediction:
        correct2+=1
print('Test Set: Correct=%d, Total=%d, Ratio=%f'% (correct2, total2, correct2/total2))