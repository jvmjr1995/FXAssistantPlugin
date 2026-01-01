#pragma once

// Core JUCE functionality
#include <juce_core/juce_core.h>

// Audio plugin base classes
#include <juce_audio_processors/juce_audio_processors.h>

// This is the header file that defines your audio plugin class — its structure, available functions, and basic properties.

// The main audio processor class - this handles audio input/output and processing.
class WorkflowAIAudioProcessor : public juce::AudioProcessor {
public:
    WorkflowAIAudioProcessor(); // Constructor
    ~WorkflowAIAudioProcessor() override; // Destructor

    // Called before playback starts - used to initialize audio settings
    void prepareToPlay(double sampleRate, int samplesPerBlock) override
    {
        juce::ignoreUnused(sampleRate, samplesPerBlock);    // Silence warnings
        // In the future, you'd initialize your audio processing here:
        // processingChain.prepare({sampleRate, (uint32) samplesPerBlock, 2});
    }

    // Called after playback ends - used to clean up
    void releaseResources() override 
    {
        // Future: clean up any audio processing resources
    }

    // Called constantly during playback - this is where audio processing happens
    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) override
    {
        juce::ignoreUnused(buffer, midiMessages);  // Still don't use MIDI
        // In the future, you'd process audio here:
        // applyReverbEffect(buffer);
        // applyCompression(buffer);
        // etc.
    }

    // GUI (plugin window) functions
    juce::AudioProcessorEditor* createEditor() override; // returns the visual editor
    bool hasEditor() const override { return true; } // this plugin has a GUI

    // Metadata about your plugin
    const juce::String getName() const override { return "Workflow AI"; }

    // MIDI and audio behavior flags
    bool acceptsMidi() const override { return false; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 0.0; }

    // Preset support (optional for now)
    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    
    void setCurrentProgram(int index) override 
    { 
        juce::ignoreUnused(index); 
    }
    
    const juce::String getProgramName(int index) override 
    { 
        juce::ignoreUnused(index);
        return {}; 
    }
   
    void changeProgramName(int index, const juce::String& newName) override 
    {
        juce::ignoreUnused(index, newName);
    }

    // Save and load plugin state (parameters/settings)
    void getStateInformation(juce::MemoryBlock& destData) override 
    {
        juce::ignoreUnused(destData);
        // Future: save plugin state to destData
    }

    void setStateInformation(const void* data, int sizeInBytes) override 
    {
        juce::ignoreUnused(data, sizeInBytes);
        // Future: restore plugin state from data
    }

    juce::AudioProcessorValueTreeState parameters;

    // Attachments for sliders
    using SliderAttachment = juce::AudioProcessorValueTreeState::SliderAttachment;

private:
    juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();

    std::unique_ptr<SliderAttachment> reverbAttachment;
    std::unique_ptr<SliderAttachment> compressorAttachment;
    std::unique_ptr<SliderAttachment> eqLowAttachment;
    std::unique_ptr<SliderAttachment> eqMidAttachment;
    std::unique_ptr<SliderAttachment> eqHighAttachment;
};