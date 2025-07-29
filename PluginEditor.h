#pragma once

// GUI components
#include <juce_gui_basics/juce_gui_basics.h>
#include <juce_gui_extra/juce_gui_extra.h>
#include <juce_audio_processors/juce_audio_processors.h>

#include "PluginProcessor.h" // Include the main processor class so we can reference it from the editor
#include "CustomLookAndFeel.h"
#include "FXBlockComponent.h"

// This is the header for the GUI editor — it defines the window you see when you open the plugin in a DAW.

//  This class is your plugin's user interface (the window the user interacts with)
class FXAssistantPluginAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    // Constructor: gets called when the editor is created
    FXAssistantPluginAudioProcessorEditor(FXAssistantPluginAudioProcessor&);

    // Destructor: called when the editor is closed
    ~FXAssistantPluginAudioProcessorEditor() override;

    // Draw visuals in the window
    void paint(juce::Graphics&) override; // Called automatically when the window needs to repaint (we do custom drawing here)

    // Called when the window is resized - useful for layout
    void resized() override; // Called when the window is resized (we set component positions here)

    void callDjangoSuggestChainAPI();

private:

    CustomLookAndFeel customLookandFeel; // Our custom style class

    // reference to your main processor (backend logic of the plugin)
    FXAssistantPluginAudioProcessor& audioProcessor;

    juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();

    juce::OwnedArray<FXBlockComponent> fxBlocks;

    juce::TextButton regenerateButton { "Suggest New FX Chain" };

    // === UI Components ===
    juce::ComboBox genreSelector;
    juce::ComboBox fxTypeSelector;
    juce::ToggleButton themeToggle; // Dark/Light mode toggle

    // Reverb Controls
    juce::Label reverbLabel;
    juce::Slider reverbKnob;

    // Compressor Controls
    juce::Label compressorLabel;
    juce::Slider compressorKnob;

    // EQ Sliders
    juce::Label eqLabel;
    juce::Slider eqLowSlider, eqMidSlider, eqHighSlider;

    // Feedback Controls
    juce::Label feedbackLabel;
    juce::Slider feedbackKnob;
    juce::ComboBox syncSelector;

    // Buttons
    juce::TextButton suggestButton { "Suggest Chain" };
    juce::TextButton saveButton { "Save Preset" };

    // Attachment type
    using SliderAttachment = juce::AudioProcessorValueTreeState::SliderAttachment;

    // Attachment instance
    std::unique_ptr<SliderAttachment> reverbAttachment;
    std::unique_ptr<SliderAttachment> compressorAttachment;
    std::unique_ptr<SliderAttachment> eqLowAttachment;
    std::unique_ptr<SliderAttachment> eqMidAttachment;
    std::unique_ptr<SliderAttachment> eqHighAttachment;

    // This macro disables copy/move constructors for safety
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(FXAssistantPluginAudioProcessorEditor) // memory safety macro
};