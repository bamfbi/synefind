/*
==============================================================================

This file was auto-generated!

It contains the basic framework code for a JUCE plugin editor.

==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"


//==============================================================================
synefindAudioProcessorEditor::synefindAudioProcessorEditor(synefindAudioProcessor& p)
    : AudioProcessorEditor(&p), processor(p)
{
    setSize(400, 300);
    attackSlider.setSliderStyle(Slider::SliderStyle::LinearVertical);
    attackSlider.setRange(0.1f, 5000.0f);
    attackSlider.setValue(0.1f);
    //attackSlider.setTextBoxStyle(Slider::TextBoxBelow, true, 20, 10);
    attackSlider.addListener(this);
    addAndMakeVisible(&attackSlider);

    //sliderTree = new AudioProcessorValueTreeState::SliderAttachment(processor.tree, "attack", attackSlider);
}

synefindAudioProcessorEditor::~synefindAudioProcessorEditor()
{
}

//==============================================================================
void synefindAudioProcessorEditor::paint(Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll(getLookAndFeel().findColour(ResizableWindow::backgroundColourId));

}

void synefindAudioProcessorEditor::resized()
{
    attackSlider.setBounds(10, 10, 40, 100);
}

void synefindAudioProcessorEditor::sliderValueChanged(Slider* slider)
{
    if (slider == &attackSlider)
    {
        processor.attackTime = attackSlider.getValue();
    }
}
