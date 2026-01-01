#pragma once

// Include necessary JUCE headers for GUI components, graphics, and audio processing
#include <juce_gui_basics/juce_gui_basics.h>    // Basic GUI components (buttons, sliders, etc.)
#include <juce_gui_extra/juce_gui_extra.h>      // Extra GUI utilities and advanced components
#include <juce_audio_processors/juce_audio_processors.h>    // Audio processor base classes

// Include our custom components and processor
#include "PluginProcessor.h"        // Include the main processor class so we can reference it from the editor
#include "CustomLookAndFeel.h"      // Custom styling and theme system
#include "FXBlockComponent.h"       // Enhanced FX block component (what you just updated)
#include "PremiumMetallicKnob.h"    // Premium metallic knob component (new separate file)

// Enhanced Plugin Editor with Hybrid Interface
//  This class is your plugin's user interface (the window the user interacts with)
class FXAssistantPluginAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    // Constructor: gets called when the editor is created
    // p: Reference to the audio processor that handles the actual audio processing
    FXAssistantPluginAudioProcessorEditor(FXAssistantPluginAudioProcessor& p);

    // Destructor: called when the editor is closed
    ~FXAssistantPluginAudioProcessorEditor() override;

    // Draw visuals in the window
    // g: Graphics context for all drawing operations
    void paint(juce::Graphics& g) override; // Called automatically when the window needs to repaint (we do custom drawing here)

    // Called when the window is resized - useful for layout
    void resized() override; // Called when the window is resized (we set component positions here)

    // API call function to get FX chain suggestions from Django backend
    void callDjangoSuggestChainAPI();

    // Layout function to position FX blocks in organized grid
    void layoutFXBlocks();

    // Fallback function when API calls fail
    void showFallbackChain();

private:
    // reference to your main processor (backend logic of the plugin)
    FXAssistantPluginAudioProcessor& audioProcessor;

    // Custom styling system for consistent visual theme
    CustomLookAndFeel customLookandFeel; // Our custom style class


    // === HYBRID INTERFACE COMPONENTS ===

    // === UI Components ===
    juce::ComboBox genreSelector;
    juce::ComboBox fxTypeSelector;

    // Premium metallic knob for parameter control
    PremiumMetallicKnob metallicKnob;

    // FX Chain Management
    juce::OwnedArray<FXBlockComponent> fxBlocks;        // Container for FX block components
    int selectedFXIndex;                                // Index of currently selected FX (-1 = none)


    // === ORIGINAL UI COMPONENTS ===
    // (Keeping these for backward compatibility and additional controls)

    // Action Buttons
    juce::TextButton aiSuggestButton { "AI Suggest" };
    juce::TextButton saveButton { "Save" };
    juce::TextButton importConvertButton { "Import/Convert" };

    // === HELPER FUNCTIONS FOR CLEAN ORGANIZATION ===

    // Setup functions called from constructor
    void setupTopRowControls();         // Initialize genre/FX type dropdowns
    void setupMainContentArea();        // Initialize knob and FX chain area
    void setupBottomRowButtons();       // Initialize action buttons

    // FX chain management functions
    void createFXChain(const juce::StringArray& fxNames);   // Create new FX chain from API response 
    void selectFXBlock(FXBlockComponent* selectedBlock);    // Handle FX block selection
    void adjustSelectedFXParameter(float value);            // Adjust selected FX parameter via knob
    void saveCurrentChain();                                // Save current FX configuration
    void openImportConvertDialog();                         // Open import/convert interface

    // Color mapping for different FX types - each effect gets a unique color theme
    const std::map<juce::String, juce::Colour> fxColors = {
        {"EQ", juce::Colours::cyan},            // Cyan for equalizers
        {"Compressor", juce::Colours::orange},  // Orange for compressors
        {"Reverb", juce::Colours::lightgreen},  // Light green for reverbs
        {"Delay", juce::Colours::yellow},       // Yellow for delays
        {"Chorus", juce::Colours::magenta},     // Magenta for chorus effects
        {"Saturation", juce::Colours::red},     // Red for saturation/distortion
        {"Filter", juce::Colours::blue},        // Blue for filters
        {"Gate", juce::Colours::purple},        // Purple for gates
        {"Limiter", juce::Colours::pink},       // Pink for limiters
        {"DeEsser", juce::Colours::lightcyan},  // Light cyan for de-essers
        {"Auto-Tune", juce::Colours::gold}      // Gold for pitch correction
    };

    // // Reverb Controls
    // juce::Label reverbLabel;
    // juce::Slider reverbKnob;

    // // Compressor Controls
    // juce::Label compressorLabel;
    // juce::Slider compressorKnob;

    // // Feedback Controls
    // juce::Label feedbackLabel;
    // juce::Slider feedbackKnob;

    // // EQ Sliders
    // juce::Label eqLabel;
    // juce::Slider eqLowSlider, eqMidSlider, eqHighSlider;

    // // Sync selector
    // juce::ComboBox syncSelector;

    // // Attachment type
    // using SliderAttachment = juce::AudioProcessorValueTreeState::SliderAttachment;

    // // Attachment instance
    // std::unique_ptr<SliderAttachment> reverbAttachment;
    // std::unique_ptr<SliderAttachment> compressorAttachment;
    // std::unique_ptr<SliderAttachment> eqLowAttachment;
    // std::unique_ptr<SliderAttachment> eqMidAttachment;
    // std::unique_ptr<SliderAttachment> eqHighAttachment;



    // This macro disables copy/move constructors for safety
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(FXAssistantPluginAudioProcessorEditor) // memory safety macro
};