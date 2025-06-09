#pragma once

// Core JUCE functionality
#include <juce_core/juce_core.h>

// Audio plugin base classes
#include <juce_audio_processors/juce_audio_processors.h>

// This is the header file that defines your audio plugin class — its structure, available functions, and basic properties.

// The main audio processor class - this handles audio input/output and processing.
class FXAssistantAudioProcessor : public juce::AudioProcessor {
public:
    FXAssistantAudioProcessor(); // Constructor
    ~FXAssistantAudioProcessor() override; // Destructor

    // Called before playback starts - used to initialize audio settings
    void prepareToPlay(double sampleRate, int samplesPerBlock) override {}

    // Called after playback ends - used to clean up
    void releaseResources() override {}

    // Called constantly during playback - this is where audio processing happens
    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) override {}

    // GUI (plugin window) functions
    juce::AudioProcessorEditor* createEditor() override; // returns the visual editor
    bool hasEditor() const override { return true; } // this plugin has a GUI

    // Metadata about your plugin
    const juce::String getName() const override { return "FX Assistant"; }

    // MIDI and audio behavior flags
    bool acceptsMidi() const override { return false; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 0.0; }

    // Preset support (optional for now)
    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    void setCurrentProgram(int index) override {}
    const juce::String getProgramName(int index) override { return {}; }
    void changeProgramName(int index, const juce::String& newName) override {}

    // Save and load plugin state (parameters/settings)
    void getStateInformation(juce::MemoryBlock& destData) override {}
    void setStateInformation(const void* data, int sizeInBytes) override {}
};