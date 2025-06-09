#include "PluginEditor.h"

#include <juce_core/juce_core.h>

// This is the code that paints the UI window and handles any visual updates.

// Constructor - this is where we configure the GUI when the window is created
FXAssistantAudioProcessorEditor::FXAssistantAudioProcessorEditor(FXAssistantAudioProcessor& p)
    : AudioProcessorEditor(&p), // Link this editor to the processor
      processor(p)              // Store the processor reference for later use
{
    // Set the initial size of the plugin window (width, height in pixels)
    setSize(400, 200);

    // Add the analyze button to the plugin window so it becomes visible
    addAndMakeVisible(analyzeButton);

    // Register this editor as a listener for the button's click events
    analyzeButton.addListener(this);
}

// Destructor — clean up when the plugin UI is closed
FXAssistantAudioProcessorEditor::~FXAssistantAudioProcessorEditor() 
{
    // Stop listening for button events (good practice for memory safety)
    analyzeButton.removeListener(this);
}

// Paint function — this draws the visuals in the plugin window
void FXAssistantAudioProcessorEditor::paint(juce::Graphics& g)
{
    // Fill the background with black
    g.fillAll(juce::Colours::black);

    // Set text color to white
    g.setColour(juce::Colours::white);

    // Set font size to 20 points
    g.setFont(20.0f);

    // Draw the plugin title in the top center of the window
    g.drawFittedText("FX Assistant Plugin", getLocalBounds(), juce::Justification::centred, 1);
}

// Resized function — called when the window size changes or on startup
void FXAssistantAudioProcessorEditor::resized() 
{
    // Set the button's position and size: x, y, width, height
    analyzeButton.setBounds(125, 120, 150, 40);
}

// Button click handler — this function runs when any button is clicked
void FXAssistantAudioProcessorEditor::buttonClicked(juce::Button* button)
{
    // Check if the clicked button is our analyze button
    if (button == &analyzeButton)
    {
        // This prints a message to the JUCE debug console
        DBG("Analyze Track button clicked");

        // (In Step 3, we’ll add code here to call a Django API)
    }
}

// This function is required by JUCE to instantiate the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new FXAssistantAudioProcessor();
}
