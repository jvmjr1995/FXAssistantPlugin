// Include our header file
#include "PluginEditor.h"

// Constructor - sets up the GUI window
WorkflowAIAudioProcessorEditor::WorkflowAIAudioProcessorEditor(WorkflowAIAudioProcessor& p)
    : AudioProcessorEditor(&p),     // Call parent constructor, pass processor address
      audioProcessor(p)             // Store reference to processor
{
    // === SET UP THE ANALYZE BUTTON ===
    
    // Set the text that appears on the button
    analyzeButton.setButtonText("Analyze Tracks");

    // Set up what happens when the button is clicked
    // Lambda function (think of it like a mini-function written inline)
    analyzeButton.onClick = [this]
    {
        analyzeTracksButtonClicked();   // Call our handler function in PluginEditor.h
    };

    // Make the button visible in the window
    addAndMakeVisible(analyzeButton);

    // === SET UP THE RESULTS TITLE ===

    // Set the text for the title
    resultsTitle.setText("Analysis Results:", juce::dontSendNotification);

    // Make the text white so it shows up on our dark background
    resultsTitle.setColour(juce::Label::textColourId, juce::Colours::white);

    // Set font size to 16 pixels
    resultsTitle.setFont(juce::FontOptions(16.0f));

    // Make it visible
    addAndMakeVisible(resultsTitle);

    // === SET UP THE RESULTS DISPLAY ===

    // Allow multiple lines of text
    resultsDisplay.setMultiLine(true);

    // Make it read-only (user can't edit the results)
    resultsDisplay.setReadOnly(true);

    // Set background color (dark grey)
    resultsDisplay.setColour(juce::TextEditor::backgroundColourId, juce::Colour(0xff252530));

    // Set text color (white)
    resultsDisplay.setColour(juce::TextEditor::textColourId, juce::Colours::white);

    // Set outline color (slightly lighter grey for border)
    resultsDisplay.setColour(juce::TextEditor::outlineColourId, juce::Colour(0xff3a3a44));

    // Set font
    resultsDisplay.setFont(juce::FontOptions(14.0f));

    // Initial placeholder text
    resultsDisplay.setText("Click 'Analyze Tracks' to begin...");

    // Make it visible
    addAndMakeVisible(resultsDisplay);

    // === SET WINDOW SIZE ===

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
    // Fill the background with our dark theme color
    g.fillAll(juce::Colour(0xff1a1a24)); // Dark blue-grey background

    // Set the drawing color to white for the text
    g.setColour(juce::Colours::white);

    // Set the font size to 28 pixels
    g.setFont(28.0f);

    // Get a rectangle for the title area (top 60 pixels)
    auto titleBounds = getLocalBounds().removeFromTop(60);

    // Draw "WorkflowAI" text in the center of the window
    // getLocalBounds() = get the full window area
    // Justification::centred = center the text horizontally and vertically
    g.drawText("WorkflowAI", titleBounds, juce::Justification::centred);
}

// Resized method - called when window size changes
void WorkflowAIAudioProcessorEditor::resized()
{
    // Get the area we have to work with (the whole window)
    auto area = getLocalBounds();

    // Add some padding around the edges (20 pixels)
    area.reduce(20, 20);

    // === POSITION THE ANALYZE BUTTON ===
    // Take a slice from the top of our area for the button
    // removeFromTop(height) removes that much space and returns it
    auto buttonArea = area.removeFromTop(40); // 40 pixels tall

    // Use the space we just took for the button
    analyzeButton.setBounds(buttonArea);

    // Add some spacing between button and next element
    area.removeFromTop(20);

    // === POSITION THE RESULTS TITLE ===
    auto titleArea = area.removeFromTop(30);    // 30 pixels for title
    resultsTitle.setBounds(titleArea);

    // Small gap
    area.removeFromTop(10);

    // === POSITION THE RESULTS DISPLAY ===
    // Give the results display all remaining space
    resultsDisplay.setBounds(area);
}

void WorkflowAIAudioProcessorEditor::analyzeTracksButtonClicked()
{
    // This function is called when the user clicks "Analyze Tracks"

    // For now, we'll show fake/demo results
    // Later, we'll replace this with real audio analysis

    // Build a string with fake analysis results
    juce::String results;

    results += "=== Track Analysis ===\n\n";
    
    results += "Track 1: Kick Drum\n";
    results += "  Type: Drums (Kick)\n";
    results += "  Current Level: -12.3 dBFS\n";
    results += "  Target Level: -18.0 dBFS\n";
    results += "  Adjustment: -5.7 dB (too loud!)\n\n";
    
    results += "Track 2: 808 Bass\n";
    results += "  Type: Bass (Sub)\n";
    results += "  Current Level: -22.1 dBFS\n";
    results += "  Target Level: -18.0 dBFS\n";
    results += "  Adjustment: +3.9 dB (too quiet!)\n\n";
    
    results += "Track 3: Lead Vocal\n";
    results += "  Type: Vocals (Lead)\n";
    results += "  Current Level: -19.8 dBFS\n";
    results += "  Target Level: -20.0 dBFS\n";
    results += "  Adjustment: -0.2 dB (perfect!)\n\n";
    
    results += "=== Analysis Complete ===\n";
    results += "3 tracks analyzed in 0.3 seconds";

    // Display the results in our text box
    resultsDisplay.setText(results);
}