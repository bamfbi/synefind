import random
from scipy.io.wavfile import read as wav_read, write as wav_write
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as pltclr
import matplotlib.gridspec as gridspec
from scipy.signal import spectrogram
import keras
import os 
import traceback as tb

def autoencode(
    data,
    name,
    epochs=10,
    batch_size=1,
    neck_dim=2,
    intermediate_dims=[], 
    validation_split=0.3,
    load_if_possible=True,
    callbacks=[],
):
    sample_size,input_size = data.shape
    input_shape = (input_size,)

    inputs = keras.layers.Input(shape=input_shape, name='encoder_input')

    if len(intermediate_dims) > 0:
        interms1 = []
        interms1.append(keras.layers.Dense(intermediate_dims[0], activation='relu')(inputs))
        for i,dim in enumerate(intermediate_dims[1:]):
            interms1.append(keras.layers.Dense(dim, activation='relu')(interms1[i - 1]))
    else:
        interms1 = [inputs]

    encoded = keras.layers.Dense(neck_dim, activation='relu')(interms1[-1])

    encoder = keras.models.Model(inputs, encoded, name='encoder')
    encoder.summary()

    decode_inputs = keras.layers.Input(shape=(neck_dim,), name='decoder_input')

    if len(intermediate_dims) > 0:
        interms2 = []
        interms2.append(keras.layers.Dense(intermediate_dims[0], activation='relu')(decode_inputs))
        for i,dim in enumerate(intermediate_dims[1:]):
            interms2.append(keras.layers.Dense(dim, activation='relu')(interms2[i - 1]))
    else:
        interms2 = [decode_inputs]

    outputs = keras.layers.Dense(input_size, activation='tanh')(interms2[-1])

    decoder = keras.models.Model(decode_inputs, outputs, name='decoder')
    decoder.summary()

    outputs = decoder(encoder(inputs))
    autoencoder = keras.models.Model(inputs, outputs, name='vae')
    autoencoder.summary()

    loss = keras.losses.mean_squared_error(
        inputs,
        outputs,
    )

    autoencoder.add_loss(loss)
    autoencoder.compile(optimizer='adam')

    npath = '/{}/model.h5'.format(name)
    npath = os.path.abspath(os.curdir) + npath
    if os.path.exists(npath) and load_if_possible:
        print("loading weights from npath: " + npath)
        autoencoder.load_weights(npath)
    else:
        autoencoder.fit(
            data,
            epochs=epochs,
            # batch_size=batch_size, 
            verbose=True,
            validation_split=validation_split,
            steps_per_epoch=int(np.ceil(sample_size*(1-validation_split)/batch_size)),
            validation_steps=int(np.ceil(sample_size*validation_split/batch_size)),
            callbacks=callbacks
            )
        autoencoder.save_weights(npath)

    return locals()

def autoencode_conv(
    data,
    name,
    epochs=10,
    batch_size=512,
    neck_dim=15,
    intermediate_dims=[200], 
    validation_split=0.3
):
    sample_size,input_size = data.shape
    input_shape = (input_size,)

    inputs = keras.layers.Input(shape=input_shape, name='encoder_input')

    if len(intermediate_dims) > 0:
        interms1 = []
        interms1.append(keras.layers.Dense(intermediate_dims[0], activation='relu')(inputs))
        for i,dim in enumerate(intermediate_dims[1:]):
            interms1.append(keras.layers.Dense(dim, activation='relu')(interms1[i - 1]))
    else:
        interms1 = [inputs]

    encoded = keras.layers.Dense(neck_dim, activation='relu')(interms1[-1])

    encoder = keras.models.Model(inputs, encoded, name='encoder')
    encoder.summary()

    decode_inputs = keras.layers.Input(shape=(neck_dim,), name='decoder_input')

    if len(intermediate_dims) > 0:
        interms2 = []
        interms2.append(keras.layers.Dense(intermediate_dims[0], activation='relu')(decode_inputs))
        for i,dim in enumerate(intermediate_dims[1:]):
            interms2.append(keras.layers.Dense(dim, activation='relu')(interms2[i - 1]))
    else:
        interms2 = [decode_inputs]

    outputs = keras.layers.Dense(input_size, activation='tanh')(interms2[-1])

    decoder = keras.models.Model(decode_inputs, outputs, name='decoder')
    decoder.summary()

    outputs = decoder(encoder(inputs))
    autoencoder = keras.models.Model(inputs, outputs, name='vae')
    autoencoder.summary()

    loss = keras.losses.mse(
        inputs,
        outputs,
    )

    autoencoder.add_loss(loss)
    autoencoder.compile(optimizer='adam')

    npath = '{}.h5'.format(name)
    if os.path.exists(npath):
        autoencoder.load_weights(npath)
    else:
        autoencoder.fit(data, epochs=epochs, batch_size=batch_size, verbose=True, validation_split=validation_split)
        autoencoder.save_weights(npath)

    return locals()
