from sys import argv, exit, stdout
from cPickle import load
from tensorflow import keras
from pinet import PiNet
import numpy as np

def main():
    if len(argv) < 4:
        exit(1)

    model_file = argv[1]
    recording_files = argv[2:]

    feature_extractor = PiNet()

    stdout.write("Loading")
    xs = []
    ys = []
    class_count = {}

    for i, filename in enumerate(recording_files):
        stdout.write(' %s' % filename)
        stdout.flush()
        with open(filename, 'rb') as f:
            x = load(f)
            features = [feature_extractor.features(f) for f in x]
            label = np.zeros((len(recording_files),))
            label[i] = 1.          
            xs += features         
            ys += [label] * len(x) 
            class_count[i] = len(x)
    stdout.write('\n')

    classifier = make_classifier(xs[0].shape, len(recording_files))

    classifier.fit([np.array(xs)], [np.array(ys)], epochs=20, shuffle=True)

    classifier.save(model_file)


def make_classifier(input_shape, num_classes):

    net_input = keras.layers.Input(input_shape)

    noise = keras.layers.GaussianNoise(0.3)(net_input)
    flat = keras.layers.Flatten()(noise)
    net_output = keras.layers.Dense(num_classes, activation='softmax')(flat)

    net = keras.models.Model([net_input], [net_output])

    net.compile(optimizer=keras.optimizers.Adam(),
                loss='categorical_crossentropy',
                metrics=['accuracy'])
    return net


if __name__ == '__main__':
    main()
