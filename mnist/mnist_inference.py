# coding:utf-8
'''
定义神经网络结构
可以进行一次前馈
'''
import tensorflow as tf

INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500


# 创建神经网络连接参数，并将他们的正则化项加入loss
def get_weight_variable(shape, regularizer):
    weights = tf.get_variable(
        'weights', shape=shape,
        initializer=tf.truncated_normal_initializer(stddev=0.1)
    )
    # loss中加入正则化项
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))

    return weights


# 网络的前向传播
def inference(input_tensor, regularizer):
    # 声明第一层神经网络，同tf.get_Variable tf.Variable
    with tf.variable_scope('layer1'):
        weights = get_weight_variable([INPUT_NODE, LAYER1_NODE], regularizer)
        biases = tf.get_variable("biases", [LAYER1_NODE], initializer=tf.constant_initializer(0.0))
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights) + biases)

    # 声明第2层神经网络
    with tf.variable_scope('layer2'):
        weights = get_weight_variable([LAYER1_NODE, OUTPUT_NODE], regularizer)
        biases = tf.get_variable("biases", [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))
        layer2 = tf.nn.relu(tf.matmul(layer1, weights) + biases)

    return layer2

if __name__ == '__main__':
    from numpy.random import RandomState
    rdm = RandomState(1)
    X = rdm.rand(5,784)
    print(inference(X,None))