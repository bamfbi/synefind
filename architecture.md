# **synefind architecture**
Updated Feburary 18th, 2019

## **1: problem statement**

It seems to boil down to this:


Given a sample `S` and a programmable instrument `I`, find the set of parameters `P` to apply to `I` such that it generates some `S_prime` which reconstructs `S` such that their MSE `(S - S_prime)**2.` is minimized.

noice. <br> <br>



## **2: problem variables**
two general approaches seem possible for reconstructing the synthesizer parameters for a given waveform. At its simplest, this task seems to be dependent on the following sets: 

- **synthesizer architecture** (oscillators, envelopes, general complexity): <br> With respect to machine learning, we may or may not need to understand the significance of each of these parameters depending on what we want our trained models to do. If we want to sample real instruments as well, that would fall under this category. <br> It is important to note that this might include an inadequate complexity for certain synthesizers. It is possible that tones made on really savage synths (moogs with plug boards or something) will be impossible to recreate on our shitty plugins. An added caveat to this is that we aren't really even able to guess at which synth is used to make shit (ex. live recs)
- **soundwave quality**: <br> pure sampling of synthesizers will probably be elusive for most natually-found tones (my man anomalie). Realistically we might need to train models with some amount of induced noise (i.e. drum/bass hits in background) so that these elements don't ruin the model during evaluation. 
- **sample compression**: <br> a direct sample (44000 Hz or whatever it is) is far too thick for any kind of virgin network we have the power to train/evaluate. the fourier analysis and subsequent compression of fourier analysis will be really important for this step - we can't lose too much data, but also can't dab on our computing resources too hard 
- **computing/training power**: <br> prolly won't be a problem, between the servers at our home schools/CERN. optimially we would have GPUs to work with but umich protects theirs and CERNs are for some reason hard to access   


This seems to sum up the problem variables as I see them. Add shit as necessary. 


## **3: possible solutions**

I think we have two sensical solutions thus far. In both cases, we need to construct an instrument model which basically reverses the usual instrument action. For our models, the output will need to determine the input, or parameters, of the instruments.  

- ### method 1: **train a new model for each instrument we want to predict**
    We all seem to understand this idea fairly well, but here's an outline anyways for documentation: 

    - pick a plugin or programmable instrument
    - generate or find a sample library for *that particular instrument*, with many examples of input parameters and their corresponding waveform FFT harmonics (whatever we deem usable)
    - train a neural network on this library such that for any processed waveform, we can attempt to predict the parameters which would generate that on our instrument
    - evaluate the trained model for a given waveform; predicted parameters are given as NN output 

    Pros:

    - very easy to understand 
    - will likely be easy to implement
    - will likely be successful for instruments with similar complexity to that of the considered sample
    - will be fast to evaluate once trained

    Cons: 

    - large training library required for each instrument we want to model
    - training will most likely be very expensive, and depending on FFT model neural network will be required
    - have to pick specific instruments we want to model 


- ### method 2: **train a master autoencoder model, with transformations to new instruments as needed**
    more complex. in this case the sample library would be the set of all samples of interest from any sources; the sampling would not have to be done only on the training instruments. <br> 
    Summary of the idea:

    - generate/gather sample library from multiple sources, targeting those similar to what we'll eventually want to target (i.e. anomalie synths, instruments with some background, etc.)
    - train autoencoder network (input trained to output, with a bottleneck) on this sample data. This should be quite expensive and will result in a trained network of (probably) large scale node architecture (i.e. 1000, 500, 200, 100, 50, then mirrored). 
    - once trained, the bottleneck nodes in the neural network will have essentially make up a new synthesizer, for which these central nodes serve as some abstract characterization of the input/output signal. there can be some form of display for this generated instrument, which users could then manipulate. 
    - with the trained network - which might have anywhere from 10-50 nodes as a characterizing "bottleneck" set of parameters - we can evaluate new signals on the network and immediately recieve as a return value both the "best" parameters for our new instrument and the output signal. Our new instrument would be the right half of the neural network; that is, input->bottleneck nodes, and output->right-hand-output signal nodes. 
    - train a mapping from the trained (autoencoder) instrument to the target simulative instrument. our network will likely not have any meaningful similarities to any actual synthesizers, except having a similar order of parameters - this makes a mapping from our 10-50 node "synth" to any number of plugins much easier than the mapping from signal to plugin. 
    - In this way, we have a "master key" for processed signal analysis. The translators will turn our master output into synth parameters. To train these translators, we can use a randomized, small sized sample library taken from the new instruments consisting of (parameter, waveform) pairs of the new instrument. We'll then evaluate each sample on our autoencoder network and take the bottleneck node values for each sample. This becomes the input for a new neural network, in which the training data is (bottleneck nodes, generative parameters on new instrument). After training this neural net, we will have a direct mapping from our abstract instrument's bottleneck nodes to parameters on our real world instrument. 
    - Putting it all together, we can then evaluate through both networks at once to acheive our goal: `signal -> bottleneck_node_parameters` via our master autoencoder, and then `bottleneck_node_parameters -> real_synth_parameters` via our much smaller and uniquely trained translator network. This gives us a signal to synth parameters network. 

    Pros: 

    - Training overhead is centralized in the autoencoder network; small training times for translator networks
    - translation networks can be generated client-side, for very niche (or even homemade) instruments/plugins. 
    - one big sample library with samples from any source. Huge imo because this makes our sample scraping easier. might even have something already avaliable. 
    - autoencoder network can be treated as its own synth with parameters optimized for whatever trait you want to train - i.e. train it entirely on MXXWLL and you get a synth which, no matter what you do with the dials, will be optimized for savagery. This seems really interesting as a kind of sample-library-in-a-synth type thing and could actually be super marketable
    - should be good at returning good results even on samples with significant backgrounds. 

    Cons: 

    - more complex conceptually and implementation-wise. more steps for things to go wrong than with a vanilla neural network. should probably be implemented after a straight neural network so we know first whether this is possible at all 
    - autoencoder training will take a long time. Number of total nodes will increase linearly with signal sample size, and training/eval time will (roughly) increase as the product of sample size with hidden layer depth squared. 

