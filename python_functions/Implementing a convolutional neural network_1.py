import tensorflow as tf
from tensorflow.keras import layers, models

def create_cnn(input_shape, num_classes):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))

    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))

    return model

input_shape = (32, 32, 3) # Assuming RGB images of size 32x32
num_classes = 10 # Assuming 10 classes to classify

model = create_cnn(input_shape, num_classes)
print(model.summary())

# Now, you can compile the model, train it on your dataset, and use it for predictions. For full implementation, see: https://www.tensorflow.org/tutorials/images/cnn