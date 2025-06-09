#include "PluginProcessor.h"
#include "PluginEditor.h"

// This is the implementation file — it tells the system how the functions declared above actually behave

// Constructor: initializes your processor
FXAssistantAudioProcessor::FXAssistantAudioProcessor()
    : AudioProcessor(BusesProperties()
        .withInput("Input", juce::AudioChannelSet::stereo(), true)    // defines one stereo input
        .withOutput("Output", juce::AudioChannelSet::stereo(), true)) // defines one stereo output
{}

// Destructor
FXAssistantAudioProcessor::~FXAssistantAudioProcessor() {}

// This connects your processor to the GUI/editor window
juce::AudioProcessorEditor* FXAssistantAudioProcessor::createEditor() {
    return new FXAssistantAudioProcessorEditor(*this);
}