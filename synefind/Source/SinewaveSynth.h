/*
  ==============================================================================

   This file is part of the JUCE library.
   Copyright (c) 2017 - ROLI Ltd.

   JUCE is an open source library subject to commercial or open-source
   licensing.

   By using JUCE, you agree to the terms of both the JUCE 5 End-User License
   Agreement and JUCE 5 Privacy Policy (both updated and effective as of the
   27th April 2017).

   End User License Agreement: www.juce.com/juce-5-licence
   Privacy Policy: www.juce.com/juce-5-privacy-policy

   Or: You may also use this code under the terms of the GPL v3 (see
   www.gnu.org/licenses).

   JUCE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY, AND ALL WARRANTIES, WHETHER
   EXPRESSED OR IMPLIED, INCLUDING MERCHANTABILITY AND FITNESS FOR PURPOSE, ARE
   DISCLAIMED.

  ==============================================================================
*/
#include "maximilian.h"
/** A demo synth sound that's just a basic sine wave.. */
class SineWaveSound : public SynthesiserSound
{
public:
    SineWaveSound() {}

    bool appliesToNote (int /*midiNoteNumber*/) override    { return true; }
    bool appliesToChannel (int /*midiChannel*/) override    { return true; }
};


//==============================================================================
/** A simple demo synth voice that just plays a sine wave.. */
class SineWaveVoice   : public SynthesiserVoice
{
public:
    SineWaveVoice()
       : currentAngle (0), angleDelta (0), level (0), tailOff (0)
    {
    }

    bool canPlaySound (SynthesiserSound* sound) override
    {
        return dynamic_cast<SineWaveSound*> (sound) != nullptr;
    }

    void startNote (int midiNoteNumber, float velocity,
                    SynthesiserSound* /*sound*/,
                    int /*currentPitchWheelPosition*/) override
    {
        env1.trigger = 1;
        currentAngle = 0.0;
        level = velocity;
        tailOff = 0.0;

        cyclesPerSecond = MidiMessage::getMidiNoteInHertz (midiNoteNumber);
        double cyclesPerSample = cyclesPerSecond / getSampleRate();

        angleDelta = cyclesPerSample * MathConstants<double>::twoPi;
    }

    void stopNote (float velocity, bool allowTailOff) override
    {
        /*env1.trigger = 0;
        allowTailOff = true;

        if (velocity == 0) {
            clearCurrentNote();
        }*/
        if (allowTailOff)
        {
            // start a tail-off by setting this flag. The render callback will pick up on
            // this and do a fade out, calling clearCurrentNote() when it's finished.

            if (tailOff == 0.0) // we only need to begin a tail-off if it's not already doing so - the
                                // stopNote method could be called more than once.
                tailOff = 1.0;
        }
        else
        {
            // we're being told to stop playing immediately, so reset everything..

            clearCurrentNote();
            angleDelta = 0.0;
        }
    }

    void pitchWheelMoved (int /*newValue*/) override
    {
    }

    void controllerMoved (int /*controllerNumber*/, int /*newValue*/) override
    {
    }

    void renderNextBlock (AudioBuffer<float>& outputBuffer, int startSample, int numSamples) override
    {
        /*env1.setAttack(1000);
        env1.setDecay(500);
        env1.setSustain(0.8);
        env1.setRelease(1000);*/
        
        if (angleDelta != 0.0)
        {
            if (tailOff > 0)
            {
                for (int sample = 0; sample < numSamples; ++sample)
                {
                    double theWave = osc1.square(cyclesPerSecond) * level * tailOff;
                    for (int channel = 0; channel < outputBuffer.getNumChannels(); ++channel)
                    {
                        outputBuffer.addSample(channel, startSample, theWave);
                    }
                    ++startSample;
                    tailOff *= 0.99;

                    if (tailOff <= 0.005)
                    {
                        // tells the synth that this voice has stopped
                        clearCurrentNote();

                        //angleDelta = 0.0;
                        break;
                    }
                }
            }
            else
            {
                for (int sample = 0; sample < numSamples; ++sample)
                {
                    double theWave = osc1.square(cyclesPerSecond) * level;
                    //double theSound = env1.adsr(theWave, env1.trigger) * level;
                    for (int channel = 0; channel < outputBuffer.getNumChannels(); ++channel)
                    {
                        outputBuffer.addSample(channel, startSample, theWave);
                    }
                    ++startSample;
                }
            }
        }
    }

private:
    double currentAngle, angleDelta, level, tailOff, cyclesPerSecond;
    maxiOsc osc1;
    maxiEnv env1;
};
