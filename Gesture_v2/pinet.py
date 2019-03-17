import tensorflow as tf
import numpy as np

class PiNet:
    def __init__(self):
        with tf.gfile.GFile('mnet.pb', 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def)

        self.x = graph.get_operations()[0].outputs[0]
        self.y = graph.get_operations()[-1].outputs[0]
        self.session = tf.Session(graph=graph)
        _ = self.features(np.zeros((128, 128, 3)))

    def features(self, image):
        preprocessed = ((np.array(image, dtype=np.float32) / 255.) - 0.5) * 2.
        features = self.session.run(self.y, feed_dict={self.x: [image]})[0]
        return features


if __name__ == '__main__':
    darkness = np.zeros((128, 128, 3))
    net = PiNet()
    z = net.features(darkness)[0]
    print(z.shape)
    print(z)
