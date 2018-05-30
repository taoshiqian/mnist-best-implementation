import tensorflow as tf
from numpy.random import RandomState

batch_size = 8

def main():
    # 定义网络参数
    w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))
    w3 = tf.Variable(tf.random_normal([3, 3], stddev=1, seed=1))

    x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
    y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

    a = tf.matmul(x, w1)
    a = tf.sigmoid(a)
    b = tf.matmul(a, w3)
    #b = tf.sigmoid(b)
    y = tf.matmul(b, w2)
    y = tf.sigmoid(y)

    # 定义损失函数与反向传播算法
    cross_entropy = -tf.reduce_mean(
        y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
        + (1 - y_) * tf.log(tf.clip_by_value(1 - y, 1e-10, 1.0))
    )+ tf.contrib.layers.l2_regularizer(0.0005)(w3)

    #cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y)
    global_step = tf.Variable(0)
    learning_rate = tf.train.exponential_decay(
        0.001, global_step, 5000, 0.96, staircase=True
    )
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step=global_step)

    # 数据集
    rdm = RandomState(1)
    dataset_size = 128
    X = rdm.rand(dataset_size, 2)
    Y = [[int(x1 + x2 < 1)] for (x1, x2) in X]

    # tensorflow训练
    with tf.Session() as sess:
        # 初始化所有变量
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        # 训练之前的参数
        print(sess.run(w1))
        print(sess.run(w2))

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
                print("After %d training step(s), cross entropy on all data is %g" % (i, total_cross_entropy))

        print(sess.run(w1))
        print(sess.run(w2))


if __name__ == '__main__':
    main()
