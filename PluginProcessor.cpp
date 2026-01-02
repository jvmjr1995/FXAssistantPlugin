// Include our header file (the interface/blueprint)
#include "PluginProcessor.h"

// Include the editor (GUI) so we can create it
#include "PluginEditor.h"

// Constructor - called when Logic Pro loads the plugin
WorkflowAIAudioProcessor::WorkflowAIAudioProcessor()
    : AudioProcessor(BusesProperties()    // Call parent class constructor  
        .withInput("Input", juce::AudioChannelSet::stereo(), true)      // Create stereo input (left + right)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true))   // Create stereo output (left + right)
{
    // Constructor body is empty for now
    // Later we'll add code here to initialize parameters, load settings, etc.
}

// Destructor - called when Logic Pro closes the plugin
WorkflowAIAudioProcessor::~WorkflowAIAudioProcessor()
{
    // Empty for now - we don't have anything to clean up yet
}

// Create the GUI window
juce::AudioProcessorEditor* WorkflowAIAudioProcessor::createEditor()
{
    // Create a new editor object and return it
    // The "new" keyword allocates memory for the editor
    // "*this" passes a reference to THIS processor to the editor
    // so the editor can access our parameters and call our methods
    return new WorkflowAIAudioProcessorEditor(*this);
}

// This special function is required by JUCE
// The DAW calls this to create an instance of our plugin
// Think of it as a "factory function" that builds plugins
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    // Create and return a new instance of our processor
    return new WorkflowAIAudioProcessor();
}
