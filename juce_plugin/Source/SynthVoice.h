
#pragma once

#include "../JuceLibraryCode/JuceHeader.h"
#include "SynthSound.h"
#include "Maximilian.h"


class SynthVoice : public SynthesiserVoice
{
public:
    bool canPlaySound(SynthesiserSound* sound) override
    {
        return dynamic_cast <SynthSound*>(sound) != nullptr;
    }

    void getParam(float* attack)
    {
        env1.setAttack(double(*attack));
    }
    //=======================================================

    void startNote(int midiNoteNumber, float velocity, SynthesiserSound* sound, int currentPitchWheelPosition) override
    {
        env1.trigger = 1;
        frequency = MidiMessage::getMidiNoteInHertz(midiNoteNumber);
        level = velocity;
    }

    //=======================================================

    void stopNote(float velocity, bool allowTailOff) override
    {
        env1.trigger = 0;
        allowTailOff = true;

        if (velocity == 0)
            clearCurrentNote();
    }

    //=======================================================

    void pitchWheelMoved(int newPitchWheelValue) override
    {

    }

    //=======================================================

    void controllerMoved(int controllerNumber, int newControllerValue) override
    {

    }

    //=======================================================

    void renderNextBlock(AudioBuffer <float> &outputBuffer, int startSample, int numSamples) override
    {
        env1.setAttack(500);
        env1.setDecay(500);
        env1.setSustain(0.8);
        env1.setRelease(500);
        double theWave, envelopedWave, filteredWave;

        for (int sample = 0; sample < numSamples; ++sample)
        {
            theWave = osc1.sinewave(frequency) + osc2.sinewave(frequency * 1.5);
            envelopedWave = env1.adsr(theWave, env1.trigger) * level;
            filteredWave = filter1.lores(envelopedWave, 1000, 0.0);

            for (int channel = 0; channel < outputBuffer.getNumChannels(); ++channel)
            {
                outputBuffer.addSample(channel, startSample, envelopedWave);
            }
            ++startSample;
        }
    }

    //=======================================================
private:
    double level;
    double frequency;

    maxiOsc osc1;
    maxiOsc osc2;
    maxiEnv env1;
    maxiEnv env2;
    maxiFilter filter1;
    maxiFilter filter2;


};