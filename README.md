# synefind

an extremely WIP utility for making it easier to track down synthesizer parameters on rippin' solos.    

Luc Le Pottier (University of Michigan; CERN ATLAS group) <br> 
Aaron Willette (University of Michigan) <br>
Murali Saravanan (Cornell University; CERN CMS group) <br>
Alex Meith (University of Michigan; CERN CMS group) <br> 

## importing

One of the only things that is possible as of now, other than the JUCE related stuff that I don't really understand.


To run and import, run `python setup.py develop`, which will set the module up for importing. Then navigate to your most favoritist python3 environment and smash an `import synefind`.  


You will be greeted by a lovely init message. 


## objects
`fourier_analyzer`, object for (obviously) analyzing waves and applying fourier analysis


`autoencoder`, object for using fourier-analyzed waves and learnin' synth parameters


Note: no objects are implemented. Don't try and run them or you will become ensaddened. 
