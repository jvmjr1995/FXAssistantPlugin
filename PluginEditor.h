#pragma once    // Prevent multiple includes

// Include JUCE's GUI framework
// This gives us components like buttons, sliders, text, graphics, etc.
#include <juce_gui_basics/juce_gui_basics.h>

// Include our processor so we can communicate with it
#include "PluginProcessor.h"

// Our GUI class - this is the window the user sees
// Inherits from AudioProcessorEditor which is JUCE's base class for plugin GUIs
class WorkflowAIAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:     // Public methods

    // Constructor - called when the GUI is created
    // Takes a reference to our processor so we can access its data
    WorkflowAIAudioProcessorEditor(WorkflowAIAudioProcessor& processor);

    // Destructor - called when the GUI is closed
    ~WorkflowAIAudioProcessorEditor() override;



    // === DRAWING METHODS ===

    // Paint the window - this is where we draw everything
    // g = Graphics context (like a canvas we can draw on)
    // This method is called automatically whenever the window needs to redraw
    void paint(juce::Graphics& g) override;

    // Resized - called when the window size changes
    // This is where we position/size our buttons, sliders, etc.
    void resized() override;

private:    // Private members

    // Store a reference to the processor
    // We use "&" (reference) instead of "*" (pointer) because it can't be null
    // This lets us access the processor's parameters and call its methods
    WorkflowAIAudioProcessor& audioProcessor;

    // JUCE safety macro - prevents copying this object
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(WorkflowAIAudioProcessorEditor)
};