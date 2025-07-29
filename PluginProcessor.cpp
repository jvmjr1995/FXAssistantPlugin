#include "PluginProcessor.h"
#include "PluginEditor.h"

// This is the implementation file — it tells the system how the functions declared above actually behave

// Constructor: initializes your processor
FXAssistantPluginAudioProcessor::FXAssistantPluginAudioProcessor()
    : AudioProcessor(BusesProperties()
        .withInput("Input", juce::AudioChannelSet::stereo(), true)    // defines one stereo input
        .withOutput("Output", juce::AudioChannelSet::stereo(), true)), // defines one stereo output
        parameters (*this, nullptr, juce::Identifier("FXParams"), createParameterLayout())
{
    
}

// Destructor
FXAssistantPluginAudioProcessor::~FXAssistantPluginAudioProcessor() {}

// This connects your processor to the GUI/editor window
juce::AudioProcessorEditor* FXAssistantPluginAudioProcessor::createEditor() {
    return new FXAssistantPluginAudioProcessorEditor(*this);
}

juce::AudioProcessorValueTreeState::ParameterLayout FXAssistantPluginAudioProcessor::createParameterLayout()
{
    std::vector<std::unique_ptr<juce::RangedAudioParameter>> params;(std::make_unique<juce::AudioParameterFloat>("reverb", "Reverb", 0.0f, 100.0f, 50.0f));
    
    params.push_back(std::make_unique<juce::AudioParameterFloat>("reverb", "Reverb", 0.0f, 100.0f, 50.0f));
    params.push_back(std::make_unique<juce::AudioParameterFloat>("compressor", "Compressor", 0.0f, 10.0f, 2.0f));
    params.push_back(std::make_unique<juce::AudioParameterFloat>("eqLow", "EQ Low", -12.0f, 12.0f, 0.0f));
    params.push_back(std::make_unique<juce::AudioParameterFloat>("eqMid", "EQ Mid", -12.0f, 12.0f, 0.0f));
    params.push_back(std::make_unique<juce::AudioParameterFloat>("eqHigh", "EQ High", -12.0f, 12.0f, 0.0f));

    return { params.begin(), params.end() };
}