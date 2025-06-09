#pragma once

// GUI components
#include <juce_gui_basics/juce_gui_basics.h>
#include <juce_gui_extra/juce_gui_extra.h>

#include "PluginProcessor.h" // Include the main processor class so we can reference it from the editor

// This is the header for the GUI editor — it defines the window you see when you open the plugin in a DAW.

//  This class is your plugin's user interface (the window the user interacts with)
class FXAssistantAudioProcessorEditor : public juce::AudioProcessorEditor,
                                        private juce::Button::Listener // We want to handle button clicks
{
public:
    // Constructor: gets called when the editor is created
    FXAssistantAudioProcessorEditor(FXAssistantAudioProcessor&);

    // Destructor: called when the editor is closed
    ~FXAssistantAudioProcessorEditor() override;

    // Draw visuals in the window
    void paint(juce::Graphics&) override; // Called automatically when the window needs to repaint (we do custom drawing here)

    // Called when the window is resized - useful for layout
    void resized() override; // Called when the window is resized (we set component positions here)

private:
    // reference to your main processor (backend logic of the plugin)
    FXAssistantAudioProcessor& processor;

    // Declare a button named "Analyze Track"
    juce::TextButton analyzeButton { "Analyze Track" };

    // This function handles clicks on any button we listen to
    void buttonClicked(juce::Button*) override;

    // This macro disables copy/move constructors for safety
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(FXAssistantAudioProcessorEditor) // memory safety macro
};