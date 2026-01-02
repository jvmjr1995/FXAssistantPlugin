#pragma once        // Prevent this file from being included multiple times (C++ safety feature)

// Include JUCE's audio processor framework
// This gives us the AudioProcessor class that all plugins inherit from
#include <juce_audio_processors/juce_audio_processors.h>

// Our main audio processing class
// Think of this as the "brain" of the plugin - it handles all audio processing
// The ": public juce::AudioProcessor" part means we're inheriting from JUCE's base class
class WorkflowAIAudioProcessor : public juce::AudioProcessor
{
public:     // Public methods - these can be called from outside this class

    // Constructor - called when the plugin is first loaded
    // This is where we initialize/set up the plugin
    WorkflowAIAudioProcessor();

    // Destructor - called when the plugin is closed/deleted
    // "override" means we're replacing JUCE's version with our own
    ~WorkflowAIAudioProcessor() override;



    // === AUDIO PROCESSING METHODS ===

    // Called before audio playback starts
    // sampleRate = how many samples per second (e.g., 44100 Hz)
    // samplesPerBlock = how many samples processed at once (e.g., 512)
    void prepareToPlay(double sampleRate, int samplesPerBlock) override {}

    // Called when audio playback stops
    // Use this to free up resources or reset things
    void releaseResources() override {}

    // THE MOST IMPORTANT METHOD!
    // This is called continuously during playback - it's where you process audio
    // buffer = the audio data coming in and going out
    // midiMessages = MIDI notes/events (we don't use these for now)
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override {}



    // === GUI METHODS ===

    // Creates the plugin window (the UI the user sees)
    // Returns a pointer to the editor object
    juce::AudioProcessorEditor* createEditor() override;

    // Does this plugin have a GUI?
    // We return "true" because we want a window
    bool hasEditor() const override { return true; }



    // === PLUGIN METADATA ===
    // These methods tell the DAW information about the plugin

    // What's the plugin called?
    const juce::String getName() const override { return "WorkflowAI"; }

    // Does it accept MIDI input? (No, we're an audio effect)
    bool acceptsMidi() const override { return false; }

    // Does it produce MIDI output? (No)
    bool producesMidi() const override { return false; }

    // How long does the effect "tail" last after audio stops?
    // For reverb/delay this might be several seconds, for us it's 0
    double getTailLengthSeconds() const override { return 0.0; }



    // === PRESET MANAGEMENT ===
    // These handle saving/loading different plugin settings

    // How many presets does this plugin have?
    int getNumPrograms() override { return 1; }

    // Which preset is currently active?
    int getCurrentProgram() override { return 0; }

    // Switch to a different preset
    void setCurrentProgram(int index) override {}

    // Get the name of a preset
    const juce::String getProgramName(int index) override { return {}; }

    // Rename a preset
    void changeProgramName(int index, const juce::String&) override {}



    // === STATE SAVING/LOADING ===
    // These save the plugin's settings when you save your project

    // Save plugin state to a binary blob
    // destData = where to save the data
    void getStateInformation(juce::MemoryBlock&) override {}

    // Load plugin state from a binary blob
    // data = the saved data
    // sizeInBytes = how big the data is
    void setStateInformation(const void*, int) override {}

private:    // Private section - only this class can access these
    // JUCE macro that prevents copying this object
    // This is a safety feature - you shouldn't be able to copy a plugin
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(WorkflowAIAudioProcessor)
};