#include "PluginEditor.h"

#include <juce_core/juce_core.h>

// This is the code that paints the UI window and handles any visual updates.

// Constructor - this is where we configure the GUI when the window is created
FXAssistantPluginAudioProcessorEditor::FXAssistantPluginAudioProcessorEditor(FXAssistantPluginAudioProcessor& p)
    : AudioProcessorEditor(&p), // Link this editor to the processor
      audioProcessor(p)              // Store the processor reference for later use
{
    // Set the initial size of the plugin window (width, height in pixels)
    setSize(700, 480);
    setResizable(true, true);
    setLookAndFeel(&customLookandFeel);     // Apply our custom theme

    // Genre Dropdown
    genreSelector.addItem("Hip-Hop", 1);
    genreSelector.addItem("EDM", 2);
    genreSelector.addItem("Lo-Fi", 3);
    addAndMakeVisible(genreSelector);

    // FX Type Dropdown
    fxTypeSelector.addItem("Reverb", 1);
    fxTypeSelector.addItem("Compressor", 2);
    fxTypeSelector.addItem("EQ", 3);
    addAndMakeVisible(fxTypeSelector);

    // Theme Toggle
    themeToggle.setButtonText("Dark Mode");
    themeToggle.setToggleState(true, juce::dontSendNotification);
    addAndMakeVisible(themeToggle);

    // Reverb
    reverbLabel.setText("Reverb", juce::dontSendNotification);
    addAndMakeVisible(reverbLabel);
    reverbKnob.setSliderStyle(juce::Slider::Rotary);
    reverbKnob.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    addAndMakeVisible(reverbKnob);

    // Compressor
    compressorLabel.setText("Compressor", juce::dontSendNotification);
    addAndMakeVisible(compressorLabel);
    compressorKnob.setSliderStyle(juce::Slider::Rotary);
    compressorKnob.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    addAndMakeVisible(compressorKnob);

    // EQ Sliders
    eqLabel.setText("EQ", juce::dontSendNotification);
    addAndMakeVisible(eqLabel);
    eqLowSlider.setSliderStyle(juce::Slider::LinearVertical);
    eqMidSlider.setSliderStyle(juce::Slider::LinearVertical);
    eqHighSlider.setSliderStyle(juce::Slider::LinearVertical);
    addAndMakeVisible(eqLowSlider);
    addAndMakeVisible(eqMidSlider);
    addAndMakeVisible(eqHighSlider);

    // Feedback
    feedbackLabel.setText("Feedback", juce::dontSendNotification);
    addAndMakeVisible(feedbackLabel);
    feedbackKnob.setSliderStyle(juce::Slider::Rotary);
    feedbackKnob.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    addAndMakeVisible(feedbackKnob);
    syncSelector.addItem("1/4", 1);
    syncSelector.addItem("1/8", 2);
    syncSelector.addItem("1/16", 3);
    addAndMakeVisible(syncSelector);

    // Buttons
    addAndMakeVisible(regenerateButton);
    addAndMakeVisible(suggestButton);
    addAndMakeVisible(saveButton);

    regenerateButton.onClick = [this]()
    {
        DBG("Regenerate button clicked");
        callDjangoSuggestChainAPI();
    };

    suggestButton.onClick = [this]()
    {
        DBG("Suggest Chain button clicked");
        callDjangoSuggestChainAPI();
        // Placeholder: this will trigger a Django API call in the future
    };

    saveButton.onClick = [this]()
    {
        DBG("Save Preset button clicked");
        // Placehodler: this will save the user's selected FX setup
    };

    themeToggle.onClick = [this]()
    {
        if (themeToggle.getToggleState())
        {
            themeToggle.setButtonText("Dark Mode");
            customLookandFeel.setTheme(CustomLookAndFeel::ThemeMode::Dark);
        }
        else
        {
            themeToggle.setButtonText("Light Mode");
            customLookandFeel.setTheme(CustomLookAndFeel::ThemeMode::Light);
        }

        repaint();
    };

    reverbAttachment = std::make_unique<SliderAttachment>(
        audioProcessor.parameters, "reverb", reverbKnob);

    compressorAttachment = std::make_unique<SliderAttachment>(
        audioProcessor.parameters, "compressor", compressorKnob);

    eqLowAttachment = std::make_unique<SliderAttachment>(
        audioProcessor.parameters, "eqLow", eqLowSlider);

    eqMidAttachment = std::make_unique<SliderAttachment>(
        audioProcessor.parameters, "eqMid", eqMidSlider);

    eqHighAttachment = std::make_unique<SliderAttachment>(
        audioProcessor.parameters, "eqHigh", eqHighSlider);
    
}

void FXAssistantPluginAudioProcessorEditor::callDjangoSuggestChainAPI()
{
    // Get selected values
    juce::String genre = genreSelector.getText();
    juce::String fxType = fxTypeSelector.getText();

    // Build JSON request
    juce::DynamicObject::Ptr jsonObj = new juce::DynamicObject();
    jsonObj->setProperty("genre", genre);
    jsonObj->setProperty("fx_type", fxType);
    juce::String jsonString = juce::JSON::toString(juce::var(jsonObj));

    // Set up request
    juce::URL url("http://127.0.0.1:8000/api/suggest-fx-chain/");
    juce::URL postUrl = url.withPOSTData(jsonString);

    // juce::URL::InputStreamOptions options(postUrl);
    // options.withExtraHeaders("Content-Type: applications/json\r\n")
    //         .withConnectionTimeoutMs(3000);
    
    std::unique_ptr<juce::InputStream> stream = postUrl
        .createInputStream(true,                                // usePostCommand
                           nullptr,                             // progressCallback
                           nullptr,                             // progressCallbackContext
                           "Content-Type: applications/json\r\n",   // extra headers
                           3000,                                // timeout ms
                           nullptr,                             // responseHeaders (optional)
                           nullptr);                            // statusCode(optional)

    // Read and parse response
    if (stream != nullptr)
    {
        juce::String responseText = stream->readEntireStreamAsString();
        juce::var response = juce::JSON::parse(responseText);

        if (response.isArray())
        {
            DBG("FX Chain Suggestion:");
            fxBlocks.clear(); // Remove previous blocks

            int startX = 20;

            for (const auto& item : *response.getArray())
            {
                juce::String fxName = item.toString();
                DBG(" - " + fxName);

                // Create and position a new FX block
                auto* block = new FXBlockComponent(fxName);
                block->setBounds(startX, 200, 120, 40); // position and size
                addAndMakeVisible(block);
                fxBlocks.add(block);

                startX += 140;
            }
            repaint();
        }
        else
        {
            DBG("Unexpected response: " + responseText);
        }
    }
    else
    {
        DBG("Error: Could not reach Django server");
    }
}

// Destructor — clean up when the plugin UI is closed
FXAssistantPluginAudioProcessorEditor::~FXAssistantPluginAudioProcessorEditor() 
{
    setLookAndFeel(nullptr);  // Reset look and feel when plugin closes
}

// Paint function — this draws the visuals in the plugin window
void FXAssistantPluginAudioProcessorEditor::paint(juce::Graphics& g)
{
    // Fill the background with black
    g.fillAll(juce::Colours::black);

    // Set text color to white
    g.setColour(juce::Colours::white);

    // Set font size to 20 points
    g.setFont(20.0f);

    // Draw the plugin title in the top center of the window
    g.drawFittedText("FX Assistant Plugin", getLocalBounds(), juce::Justification::centredTop, 1);
}

// Resized function — called when the window size changes or on startup
void FXAssistantPluginAudioProcessorEditor::resized() 
{
    // Buttons
    regenerateButton.setBounds(180, 20, 200, 30);  // x, y, width, height
    suggestButton.setBounds(400, 20, 120, 30);
    saveButton.setBounds(540, 20, 120, 30);

    // Knobs
    reverbKnob.setBounds(20, 150, 80, 80);
    compressorKnob.setBounds(120, 150, 80, 80);
    feedbackKnob.setBounds(220, 150, 80, 80);

    // EQ
    eqLowSlider.setBounds(320, 150, 20, 80);
    eqMidSlider.setBounds(350, 150, 20, 80);
    eqHighSlider.setBounds(380, 150, 20, 80);

    // Labels
    reverbLabel.setBounds(20, 135, 80, 15);
    compressorLabel.setBounds(120, 135, 80, 15);
    feedbackLabel.setBounds(220, 135, 80, 15);
    eqLabel.setBounds(340, 135, 60, 15);

    // Sync Dropdown
    genreSelector.setBounds(20, 20, 150, 30);   // x, y, width, height
    fxTypeSelector.setBounds(20, 60, 250, 30);
    syncSelector.setBounds(480, 150, 100, 25);
    
    // Dark/Light Theme Toggle
    themeToggle.setBounds(20, 100, 150, 30);

}

// This function is required by JUCE to instantiate the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new FXAssistantPluginAudioProcessor();
}
