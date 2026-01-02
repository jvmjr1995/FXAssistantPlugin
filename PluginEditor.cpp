// Include our header file
#include "PluginEditor.h"

// Constructor - sets up the GUI window
WorkflowAIAudioProcessorEditor::WorkflowAIAudioProcessorEditor(WorkflowAIAudioProcessor& p)
    : AudioProcessorEditor(&p),     // Call parent constructor, pass processor address
      audioProcessor(p)             // Store reference to processor
{
    // Set the initial window size (width, height in pixels)
    setSize(400, 300);  // 400 pixels wide, 300 pixels tall
}

// Destructor - clean up when GUI closes
WorkflowAIAudioProcessorEditor::~WorkflowAIAudioProcessorEditor()
{
    // Empty for now - nothing to clean up
}

// Paint method - draws everything in the window
void WorkflowAIAudioProcessorEditor::paint(juce::Graphics& g)
{
    // Fill the entire window with dark grey/black
    // Colour(20, 20, 25) = RGB color (red=20, green=20, blue=25)
    g.fillAll(juce::Colour(20, 20, 25));

    // Set the drawing color to white for the text
    g.setColour(juce::Colours::white);

    // Set the font size to 28 pixels
    g.setFont(28.0f);

    // Draw "WorkflowAI" text in the center of the window
    // getLocalBounds() = get the full window area
    // Justification::centred = center the text horizontally and vertically
    g.drawText("WorkflowAI", getLocalBounds(), juce::Justification::centred);
}

// Resized method - called when window size changes
void WorkflowAIAudioProcessorEditor::resized()
{
    // Empty for now - we don't have any controls to position yet
    // Later, when we add buttons/sliders, we'll position them here like:
    // myButton.setBounds(10, 10, 100, 30);  // x, y, width, height
}