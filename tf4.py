import tensorflow as tf
from numpy.random import RandomState

batch_size = 8


def get_weight(shape, lamb):
    var = tf.Variable(tf.random_normal(shape), dtype=tf.float32)
    tf.add_to_collection(
        'losses', tf.contrib.layers.l2_regularizer(lamb)(var)
    )
    return var


def main():
    x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
    y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

    # 定义网络参数
    lamb = 0.001
    # 每层神经元个数
    layer_dimension = [2, 2, 2, 2, 1]
    # 神经网络层数
    n_layers = len(layer_dimension)
    # 网络结构
    cur_layer = x
    in_dimension = layer_dimension[0]
    for i in range(1, n_layers):
        out_dimension = layer_dimension[i]
        weight = get_weight([in_dimension, out_dimension], lamb)
        bias = tf.Variable(tf.constant(0.1, shape=[out_dimension]))
        cur_layer = tf.nn.relu(tf.matmul(cur_layer, weight) + bias)
        in_dimension = layer_dimension[i]
    y = cur_layer

    # 定义损失函数与反向传播算法
    cross_entropy = -tf.reduce_mean(
        y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
        + (1 - y_) * tf.log(tf.clip_by_value(1 - y, 1e-10, 1.0))
    )
    tf.add_to_collection('losses', cross_entropy)

    # 最终的损失函数
    loss = tf.add_n(tf.get_collection('losses'))
    #loss = cross_entropy

    # cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y)
    global_step = tf.Variable(0)
    learning_rate = tf.train.exponential_decay(
        0.001, global_step, 5000, 0.96, staircase=True
    )
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)

    # 数据集
    rdm = RandomState(1)
    dataset_size = 128
    X = rdm.rand(dataset_size, 2)
    Y = [[int(x1 + x2 < 1)] for (x1, x2) in X]

    valid_size = 128
    Xvalid = rdm.rand(valid_size, 2)
    Yvalid = [[int(x1 + x2 < 1)] for (x1, x2) in X]

    # tensorflow训练
    with tf.Session() as sess:
        # 初始化所有变量
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        # 设置训练迭代次数
        STEPS = 5000
        for i in range(STEPS):
            # 每次选取一个patch来训练
            start = (i * batch_size) % dataset_size
            end = min(start + batch_size, dataset_size)

            # 通过选取的样本来更新网络参数
            sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})

            if i % 1000 == 0:
                total_cross_entropy = sess.run(
                    cross_entropy, feed_dict={x: X, y_: Y}
                )
                valid_cross_entropy = sess.run(
                    cross_entropy, feed_dict={x: Xvalid, y_: Yvalid}
                )
                print("After %d training step(s), cross entropy on all data is %g" % (i, total_cross_entropy))
                print("After %d training step(s), cross entropy on valid is %g" % (i, valid_cross_entropy))
                print()

if __name__ == '__main__':
    main()
