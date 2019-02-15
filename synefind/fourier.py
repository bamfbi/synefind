



class fourier_analyzer:
    """
    Fourier analysis object class.
    Will support:
        - loading signal from audio files (types?) to numpy array for fourier transform
        - using FFT to analyze the signal and dumb it down into whatever the hell comes
          out of a fourier transform (Alex help pls) 
        - saving the signal to a data file for subsequent analysis and machine learning

    This class is strictly for analysis of wave patterns and should not have anything
    to do with paring down the resultant fourier data into a machine-learnable format. 
    
    """    
    def __init__(
            self,
            ):
        pass 

    def load_signal(
            self,
            filename=None
            ):
        
        # load filename
        self.filename=filename
        assert(self.filename is not None)
        
        # some analysis of filename into signal
        signal = None
        
        return signal

    def analyze_signal(
            self,
            signal
            ):

        # some analysis of signal 
        analyzed_signal = signal

        return analyzed_signal

    def save_signal(
            self, 
            signal,
            signal_filename
            ):

        # some save function
        # save(blabla) 
        
        # worked
        return 0
