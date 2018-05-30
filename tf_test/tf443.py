import tensorflow as tf

# 用于计算滑动平均的变量
v1 = tf.Variable(0, dtype=tf.float32)

# 神经网络迭代次数，可以用于动态控制衰减率
step = tf.Variable(0, trainable=False)

# 定义一个滑动平均的类
ema = tf.train.ExponentialMovingAverage(0.99, step)

# 滑动平均的操作。每次执行操作时，列表里面的变量都会被更新
maintain_average_op = ema.apply([v1])

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    # 初始化v1 与 滑动平均值
    print(sess.run([v1, ema.average(v1)]))

    # 更新v1为5
    sess.run(tf.assign(v1, 5))
    # 更新v1的滑动平均值。衰减率为min{0.99,(1+step)/(10+step)}=0.1
    # 0.1*0+0.9*5=4.5
    sess.run(maintain_average_op)
    print(sess.run([v1, ema.average(v1)]))

    # 更新step的值为1000
    sess.run(tf.assign(step, 1000))

    # 更新v1的值为10
    sess.run(tf.assign(v1, 10))
    # 更新v1的滑动平均值。衰减率为min{0.99,(1+step)/(10+step)}=0.99
    # 0.99*4.5+0.01*10=4.555
    sess.run(maintain_average_op)
    print(sess.run([v1, ema.average(v1)]))

    # 更新v1的滑动平均值。衰减率为min{0.99,(1+step)/(10+step)}=0.99
    # 0.99*4.555+0.01*10=4.60945
    sess.run(maintain_average_op)
    print(sess.run([v1, ema.average(v1)]))
