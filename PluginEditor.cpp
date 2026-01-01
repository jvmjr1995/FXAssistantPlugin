#include "PluginEditor.h"

#include <juce_core/juce_core.h>

// This is the code that paints the UI window and handles any visual updates.

// Constructor - this is where we configure the GUI when the window is created
WorkflowAIAudioProcessorEditor::WorkflowAIAudioProcessorEditor(WorkflowAIAudioProcessor& p)
    : AudioProcessorEditor(&p), // Link this editor to the processor
      audioProcessor(p),              // Store the processor reference for later use
      selectedFXIndex(-1)
{
    // Set the initial size of the plugin window (width, height in pixels)
    setSize(800, 600);

    // setResizable(true, true);

    // Apply custom styling
    setLookAndFeel(&customLookandFeel);     // Apply our custom theme

    // Initialize all UI components in organized sections
    setupTopRowControls();          // Genre/FX type dropdowns
    setupMainContentArea();         // Metallic knob + FX chain display
    setupBottomRowButtons();        // Action buttons
}

// Destructor — clean up when the plugin UI is closed
WorkflowAIAudioProcessorEditor::~WorkflowAIAudioProcessorEditor() 
{
    setLookAndFeel(nullptr);  // Reset look and feel when plugin closes
}

// Setup function: Initialize the top row controls (Genre and FX Type selectors)
void WorkflowAIAudioProcessorEditor::setupTopRowControls()
{

    // === GENRE SELECTOR ===
    // Add genre options for music style selection
    genreSelector.addItem("Hip-Hop", 1);
    genreSelector.addItem("EDM", 2);
    genreSelector.addItem("Lo-Fi", 3);
    genreSelector.addItem("Rock", 4);
    genreSelector.addItem("Pop", 5);
    genreSelector.addItem("R&B", 6);
    genreSelector.addItem("Jazz", 7);
    genreSelector.addItem("Country", 8);
    genreSelector.addItem("Reggae", 9);
    genreSelector.addItem("Ambient", 10);
    genreSelector.addItem("Trap", 11);
    genreSelector.addItem("Drill", 12);
    genreSelector.addItem("Afrobeats", 13);
    addAndMakeVisible(genreSelector);

    // === FX TYPE SELECTOR ===
    // Add FX type options for instrument/source selection
    fxTypeSelector.addItem("Vocals", 1);
    fxTypeSelector.addItem("Guitar", 2);
    fxTypeSelector.addItem("Bass", 3);
    fxTypeSelector.addItem("Drums", 4);
    fxTypeSelector.addItem("Piano", 5);
    fxTypeSelector.addItem("Synth", 6);
    fxTypeSelector.addItem("Keys", 7);
    fxTypeSelector.addItem("Saxophone", 8);
    fxTypeSelector.addItem("Percussion", 9);
    fxTypeSelector.addItem("Pad", 10);
    fxTypeSelector.addItem("Full Mix", 11);
    fxTypeSelector.addItem("Hi-Hats", 12);
    addAndMakeVisible(fxTypeSelector);
}

// Setup function: Initialize the main content area (knob and FX chain)
void WorkflowAIAudioProcessorEditor::setupMainContentArea()
{
    // === PREMIUM METALLIC KNOB ===
    // Set up the large parameter control knob
    metallicKnob.onValueChanged = [this](float value) {
        // Only process value changes if we have a valid FX selected
        if (selectedFXIndex >= 0 && selectedFXIndex < fxBlocks.size())
        {
            // Adjust the selected FX parameter based on knob value (0.0 to 1.0)
            adjustSelectedFXParameter(value);
        }
    };
    addAndMakeVisible(metallicKnob);        // Add knob to interface


    // === FX CHAIN DISPLAY ===
    // Initialize with a demo chain to show the interface
    createFXChain({"EQ", "Compressor", "Reverb", "Delay"});
}

// Setup function: Initialize the bottom row action buttons
void WorkflowAIAudioProcessorEditor::setupBottomRowButtons()
{
    // === AI SUGGEST BUTTON ===
    // Button to trigger AI FX chain suggestions
    aiSuggestButton.onClick = [this]() {
        callDjangoSuggestChainAPI();        // Call your existing API function
    };
    addAndMakeVisible(aiSuggestButton);

    // === SAVE BUTTON ===
    // Button to save current FX chain configuration
    saveButton.onClick = [this]() {
        saveCurrentChain();                 // Save current settings
    };
    addAndMakeVisible(saveButton);

    // === IMPORT/CONVERT BUTTON ===
    // Button to open import/convert dialog for industry presets
    importConvertButton.onClick = [this]() {
        openImportConvertDialog();          // Open import interface
    };
    addAndMakeVisible(importConvertButton);
}

    // // Theme Toggle
    // themeToggle.setButtonText("Dark Mode");
    // themeToggle.setToggleState(true, juce::dontSendNotification);
    // addAndMakeVisible(themeToggle);

    // // Reverb
    // reverbLabel.setText("Reverb", juce::dontSendNotification);
    // addAndMakeVisible(reverbLabel);
    // reverbKnob.setSliderStyle(juce::Slider::Rotary);
    // reverbKnob.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    // addAndMakeVisible(reverbKnob);

    // // Compressor
    // compressorLabel.setText("Compressor", juce::dontSendNotification);
    // addAndMakeVisible(compressorLabel);
    // compressorKnob.setSliderStyle(juce::Slider::Rotary);
    // compressorKnob.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    // addAndMakeVisible(compressorKnob);

    // // EQ Sliders
    // eqLabel.setText("EQ", juce::dontSendNotification);
    // addAndMakeVisible(eqLabel);
    // eqLowSlider.setSliderStyle(juce::Slider::LinearVertical);
    // eqMidSlider.setSliderStyle(juce::Slider::LinearVertical);
    // eqHighSlider.setSliderStyle(juce::Slider::LinearVertical);
    // addAndMakeVisible(eqLowSlider);
    // addAndMakeVisible(eqMidSlider);
    // addAndMakeVisible(eqHighSlider);

    // // Feedback
    // feedbackLabel.setText("Feedback", juce::dontSendNotification);
    // addAndMakeVisible(feedbackLabel);
    // feedbackKnob.setSliderStyle(juce::Slider::Rotary);
    // feedbackKnob.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    // addAndMakeVisible(feedbackKnob);
    // syncSelector.addItem("1/4", 1);
    // syncSelector.addItem("1/8", 2);
    // syncSelector.addItem("1/16", 3);
    // addAndMakeVisible(syncSelector);

    // themeToggle.onClick = [this]()
    // {
    //     if (themeToggle.getToggleState())
    //     {
    //         themeToggle.setButtonText("Dark Mode");
    //         customLookandFeel.setTheme(CustomLookAndFeel::ThemeMode::Dark);
    //     }
    //     else
    //     {
    //         themeToggle.setButtonText("Light Mode");
    //         customLookandFeel.setTheme(CustomLookAndFeel::ThemeMode::Light);
    //     }

    //     repaint();
    // };

    // reverbAttachment = std::make_unique<SliderAttachment>(
    //     audioProcessor.parameters, "reverb", reverbKnob);

    // compressorAttachment = std::make_unique<SliderAttachment>(
    //     audioProcessor.parameters, "compressor", compressorKnob);

    // eqLowAttachment = std::make_unique<SliderAttachment>(
    //     audioProcessor.parameters, "eqLow", eqLowSlider);

    // eqMidAttachment = std::make_unique<SliderAttachment>(
    //     audioProcessor.parameters, "eqMid", eqMidSlider);

    // eqHighAttachment = std::make_unique<SliderAttachment>(
    //     audioProcessor.parameters, "eqHigh", eqHighSlider);
   
// Resized function — called when the window size changes or on startup
void WorkflowAIAudioProcessorEditor::resized() 
{
    auto bounds = getLocalBounds();

    // === TOP ROW: Genre and FX Type Selectors ===
    auto topRow = bounds.removeFromTop(60);     // Take top 60 pixels
    topRow.removeFromTop(15);                   // Add 15px top margin
    topRow.removeFromLeft(20);                  // Add 20px left margin

    genreSelector.setBounds(topRow.removeFromLeft(150));        // Genre dropdown: 150px wide
    topRow.removeFromLeft(20);                                  // 20px spacing
    fxTypeSelector.setBounds(topRow.removeFromLeft(150));       // FX type dropdown: 150px wide


    // === MAIN CONTENT AREA ===
    auto mainArea = bounds.removeFromBottom(80);        // Leave 80px for bottom buttons
    mainArea = bounds;                                  // Use remaining space

    // Left side: Huge metallic knob
    auto leftSide = mainArea.removeFromLeft(300);       // Take left 300px for knob area
    leftSide.removeFromTop(50);                         // Top margin
    leftSide.removeFromLeft(90);                        // Center the knob horizontally
    metallicKnob.setBounds(leftSide.removeFromTop(120).removeFromLeft(120));    // 120x120 knob

    // Right side: FX chain display
    auto rightSide = mainArea;                  // Use remaining space for FX blocks
    rightSide.removeFromTop(50);                // Top margin
    rightSide.removeFromLeft(20);               // Left margin
    layoutFXBlocks();                           // Position FX blocks in grid

    // === BOTTOM ROW: Action Buttons ===
    auto bottomRow = getLocalBounds().removeFromBottom(60);     // Take bottom 60 pixels
    bottomRow.removeFromBottom(15);                             // Add 15px bottom margin
    bottomRow.removeFromLeft(50);                               // Add 50px left margin

    aiSuggestButton.setBounds(bottomRow.removeFromLeft(120));       // AI Suggest: 120px wide
    bottomRow.removeFromLeft(20);                                   // 20px spacing
    saveButton.setBounds(bottomRow.removeFromLeft(80));             // Save: 80px wide  
    bottomRow.removeFromLeft(20);                                   // 20px spacing
    importConvertButton.setBounds(bottomRow.removeFromLeft(140));   // Import/Convert: 140px wide


    // // Knobs
    // reverbKnob.setBounds(20, 150, 80, 80);
    // compressorKnob.setBounds(120, 150, 80, 80);
    // feedbackKnob.setBounds(220, 150, 80, 80);

    // // EQ
    // eqLowSlider.setBounds(320, 150, 20, 80);
    // eqMidSlider.setBounds(350, 150, 20, 80);
    // eqHighSlider.setBounds(380, 150, 20, 80);

    // // Labels
    // reverbLabel.setBounds(20, 135, 80, 15);
    // compressorLabel.setBounds(120, 135, 80, 15);
    // feedbackLabel.setBounds(220, 135, 80, 15);
    // eqLabel.setBounds(340, 135, 60, 15);

    // // Sync Dropdown
    // genreSelector.setBounds(20, 20, 150, 30);   // x, y, width, height
    // fxTypeSelector.setBounds(20, 60, 250, 30);
    // syncSelector.setBounds(480, 150, 100, 25);
    
    // // Dark/Light Theme Toggle
    // themeToggle.setBounds(20, 100, 150, 30);

    // Note: FX blocks are positioned dynamically in callDjangoSuggestChainAPI()
}

// Paint function: Draw the clean background and layout indicators
void WorkflowAIAudioProcessorEditor::paint(juce::Graphics& g)
{
    // === MODERN GRADIENT BACKGROUND ===

    // Get the entire plugin window area
    auto bounds = getLocalBounds();
    // Create diagonal gradient from dark blue-black to deep black
    juce::ColourGradient backgroundGradient(
        juce::Colour(25, 25, 35),           // Dark blue-grey color at top-left
        bounds.getTopLeft().toFloat(),      // Start position (top-left corner)
        juce::Colour(15, 15, 25),           // Even darker at bottom-right
        bounds.getBottomRight().toFloat(),  // End position (bottom-right corner)
        false                               // Linear gradient (not radial)
    );

    // Apply the gradient to fill the entire plugin background
    g.setGradientFill(backgroundGradient);
    g.fillAll();    // Fill the entire component area


    // === MAIN TITLE ===
    g.setColour(juce::Colours::white.withAlpha(0.9f));
    g.setFont(juce::Font(28.0f, juce::Font::bold));
    g.drawText("FX ASSISTANT", 20, 15, 300, 30, juce::Justification::centredLeft);

    // === FX CHAIN LABEL ===
    if (!fxBlocks.isEmpty())
    {
        g.setColour(juce::Colours::white.withAlpha(0.7f));
        g.setFont(juce::Font(16.0f, juce::Font::bold));
        g.drawText("FX CHAIN", 320, 80, 150, 25, juce::Justification::centredLeft);
    }

    // === SELECTED FX INDICATOR ===
    if (selectedFXIndex >= 0 && selectedFXIndex < fxBlocks.size())
    {
        auto selectedFX = fxBlocks[selectedFXIndex];
        g.setColour(selectedFX->getFXColor());
        g.setFont(juce::Font(14.0f, juce::Font::bold));
        g.drawText("Controlling: " + selectedFX->getFXName(),
                    50, 300, 200, 25, juce::Justification::centred);
    }

    // // === SUBTLE NOISE TEXTURE OVERLAY ===

    // // Add subtle noise texture for premium feel (like expensive hardware)
    // g.setColour(juce::Colours::white.withAlpha(0.02f));     // Very faint white dots

    // // Loop through plugin area in 3-pixel steps
    // for (int i = 0; i < bounds.getWidth(); i += 3)   // Every 3 pixels horizontally
    // {
    //     for (int j = 0; j < bounds.getHeight(); j += 3)    // Every 3 pixels vertically 
    //     {
    //         // Randomly place noise pixels (50% chance for each position)
    //         if (juce::Random::getSystemRandom().nextFloat() > 0.5f)
    //             g.fillRect(i, j, 1, 1);     // Draw 1x1 pixel noise dot
    //     }
    // }


    // // === MODERN HEADER AREA ===

    // // Create header section at top of plugin (55 pixels tall)
    // auto headerBounds = bounds.removeFromTop(55);   // Take top 55px, remove from main bounds

    // // Create subtle gradient for header background
    // juce::ColourGradient headerGradient(
    //     juce::Colour(30, 30, 40).withAlpha(0.3f),   // Semi-transparent lighter grey at top
    //     headerBounds.getTopLeft().toFloat(),        // Start at top of header
    //     juce::Colour(20, 20, 30).withAlpha(0.1f),   // More transparent darker grey at bottom
    //     headerBounds.getBottomLeft().toFloat(),     // End at bottom of header
    //     false                                       // Linear gradient (vertical)
    // );

    // // Apply header gradient and fill the header area
    // g.setGradientFill(headerGradient);
    // g.fillRect(headerBounds);   // Fill the header rectangle


    // // === MODERN TITLE WITH GLOW EFFECT ===

    // // First draw title shadow/glow effect (offset by 1 pixel)
    // g.setColour(juce::Colours::white.withAlpha(0.1f));  // Very faint white for glow
    // auto titleBounds = headerBounds.reduced(20, 10);    // Add 20px horizontal, 10px vertical padding
    // juce::Font titleFont(24.0f, juce::Font::bold);      // 24px bold font for title
    // g.setFont(titleFont);

    // // Draw shadow/glow offset by 1 pixel down and right
    // g.drawText("FX ASSISTANT", titleBounds.translated(1, 1), juce::Justification::centred);

    // // Now draw main title text in bright white
    // g.setColour(juce::Colours::white.withAlpha(0.9f));  // Bright white with slight transparency
    // g.drawText("FX ASSISTANT", titleBounds, juce::Justification::centred);


    // // === SUBTLE SEPARATOR LINE ===

    // // Draw thin line separating header from content area
    // g.setColour(juce::Colour(60, 60, 70).withAlpha(0.5f));  // Semi-transparent grey line
    // g.fillRect(20,                              // Start 20px from left edge
    //            headerBounds.getBottom() - 1,    // Position at bottom of header minus 1px
    //            bounds.getWidth() - 40,          // Width: full width minus 40px (20px each side)
    //            1);                              // Height: 1 pixel thin line
    

    // // === MODERN SECTION DIVIDERS ===
    
    // // Create subtle background for the controls area
    // auto controlArea = juce::Rectangle<int>(0, 55, bounds.getWidth(), 220); // From y=55, height=220
    // g.setColour(juce::Colour(25, 25, 35).withAlpha(0.3f));                  // Semi-transparent dark grey
    // g.fillRoundedRectangle(controlArea.reduced(15).toFloat(), 12.0f);       // Rounded rectangle with 15px margin


    // // === FX BLOCKS AREA BACKGROUND ===

    // // Create area for FX blocks display
    // auto fxArea = juce::Rectangle<int>(0, 275, bounds.getWidth(), bounds.getHeight() - 275);    // Below controls
    
    // // Only draw FX area background if there are actually FX blocks to show
    // if (!fxBlocks.isEmpty())    // Check if any FX blocks exist
    // {
    //     // Draw subtle background for FX blocks area
    //     g.setColour(juce::Colour(20, 20, 30).withAlpha(0.4f));  // Semi-transparent darker background
    //     g.fillRoundedRectangle(fxArea.reduced(15).toFloat(), 12.0f);    // Rounded with 15px margin

    //     // === "AI SUGGESTED CHAIN" LABEL ===

    //     // Add label above the FX blocks
    //     g.setColour(juce::Colours::white.withAlpha(0.6f));  // Semi-transparent white text
    //     juce::Font labelFont(13.0f, juce::Font::bold);      // 13px bold font for label
    //     g.setFont(labelFont);

    //     // Draw label text in top-left of FX area
    //     g.drawText("AI SUGGESTED CHAIN",                    // Label text
    //                fxArea.removeFromTop(25).reduced(25, 5), // Take top 25px, add padding
    //                juce::Justification::centredLeft);       // Left-aligned text
    // }


    // // === ADDITIONAL VISUAL ENHANCEMENTS ===

    // // Draw subtle corner highlights for premium feel
    // g.setColour(juce::Colours::white.withAlpha(0.05f));     // Very faint white

    // // Top-left corner highlight
    // g.fillRect(0, 0, 30, 1);    // Horizontal line at top-left
    // g.fillRect(0, 0, 1, 30);    // Vertical line at top-left

    // // Top-right corner highlight
    // g.fillRect(bounds.getWidth() - 30, 0, 30, 1);   // Horizontal line at top-right
    // g.fillRect(bounds.getWidth() - 1, 0, 1, 30);    // Vertical line at top-right


    // // === SUBTLE VIGNETTE EFFECT ===

    // // Create darker edges for focus on center content
    // auto centreX = bounds.getCentreX();
    // auto centreY = bounds.getCentreY();
    // auto topLeftX = bounds.getX();
    // auto topLeftY = bounds.getY();

    // juce::ColourGradient vignette(
    //     juce::Colours::black.withAlpha(0.0f),   // Transparent center
    //     centreX,                                // Center X
    //     centreY,                                // Center Y
    //     juce::Colours::black.withAlpha(0.1f),   // Semi-transparent black at edges
    //     topLeftX,                               // Edge X
    //     topLeftY,                               // Edge Y
    //     true                                    // Radial gradient (circular)
    // );

    // // Apply vignette effect
    // g.setGradientFill(vignette);
    // g.fillAll();    // Fill entire area with vignette
}

// Create FX chain from array of effect names (called from API response)
void WorkflowAIAudioProcessorEditor::createFXChain(const juce::StringArray& fxNames)
{
    // Clear any existing FX blocks
    fxBlocks.clear();

    // Create new FX blocks for each effect in the chain
    for (int i = 0; i < fxNames.size(); ++i)
    {
        auto fxName = fxNames[i];

        // Get color for this FX type (default to white if not found)
        auto color = fxColors.count(fxName) ? fxColors.at(fxName) : juce::Colours::white;

        // Create new FX block component
        auto* block = new FXBlockComponent(fxName, color);

        // Set up selection callback
        block->onSelectionChanged = [this](FXBlockComponent* selectedBlock) {
            selectFXBlock(selectedBlock);
        };

        // Add to interface and container
        addAndMakeVisible(block);
        fxBlocks.add(block);
    }

    // Auto-select first block if any exist
    if (!fxBlocks.isEmpty())
    {
        selectFXBlock(fxBlocks[0]);
    }

    // Position blocks and refresh display
    layoutFXBlocks();
    repaint();
}

// Handle FX block selection (updates knob color and states)
void WorkflowAIAudioProcessorEditor::selectFXBlock(FXBlockComponent* selectedBlock)
{
    // Update all block states based on selection
    for(int i = 0; i < fxBlocks.size(); ++i)
    {
        auto* block = fxBlocks[i];
        if (block == selectedBlock)
        {
            // Set this block as selected
            block->setState(FXBlockComponent::BlockState::Selected);
            selectedFXIndex = i;

            // Update metallic knob color to match selected FX
            metallicKnob.setColor(block->getFXColor());
        }
        else
        {
            // Set other blocks to active state (if they were previously selected)
            if (block->getState() == FXBlockComponent::BlockState::Selected)
                block->setState(FXBlockComponent::BlockState::Active);
        }
    }

    repaint();      // Refresh display
}

// Position FX blocks in organized display (right side of interface)
void WorkflowAIAudioProcessorEditor::layoutFXBlocks()
{
    if (fxBlocks.isEmpty())
        return;

    // Calculate layout parameters for right side of interface
    int startX = 320;          // Start position (right of knob area)  
    int startY = 110;          // Start position (below header) 
    int blockWidth = 120;      // Individual block width 
    int blockHeight = 40;      // Individual block height 
    int spacing = 15;          // Spacing between blocks 
    int maxBlocksPerRow = 3;   // Maximum blocks per row

    // Position blocks in organized rows
    for (int i = 0; i < fxBlocks.size(); ++i)
    {
        int row = i / maxBlocksPerRow;      // Calculate row number
        int col = i % maxBlocksPerRow;      // Calculate column number

        int x = startX + (col * (blockWidth + spacing));    // X position
        int y = startY + (row * (blockHeight + spacing));   // Y position

        // Set block position
        fxBlocks[i]->setBounds(x, y, blockWidth, blockHeight);
    }

    // DBG("Laying out " + juce::String(fxBlocks.size()) + " FX blocks");
    
    // // Get available area for FX blocks
    // auto totalArea = getLocalBounds();
    // auto fxArea = totalArea.removeFromBottom(totalArea.getHeight() - 280); // Start below controls
    // fxArea = fxArea.reduced(20, 10); // Add padding
    
    // // Calculate layout
    // int blockWidth = 140;
    // int blockHeight = 50;
    // int spacing = 15;
    // int blocksPerRow = juce::jmax(1, (fxArea.getWidth() + spacing) / (blockWidth + spacing));
    
    // DBG("FX Area: " + fxArea.toString());
    // DBG("Blocks per row: " + juce::String(blocksPerRow));
    
    // // Position blocks in rows
    // int currentX = fxArea.getX();
    // int currentY = fxArea.getY();
    // int blocksInCurrentRow = 0;
    
    // for (int i = 0; i < fxBlocks.size(); ++i)
    // {
    //     auto* block = fxBlocks[i];
        
    //     // Move to next row if needed
    //     if (blocksInCurrentRow >= blocksPerRow)
    //     {
    //         currentX = fxArea.getX();
    //         currentY += blockHeight + 10;
    //         blocksInCurrentRow = 0;
    //     }
        
    //     // Set position immediately (no animation for now to debug)
    //     block->setBounds(currentX, currentY, blockWidth, blockHeight);
        
    //     DBG("Block " + juce::String(i) + " (" + block->getName() + ") positioned at: " + 
    //         juce::String(currentX) + ", " + juce::String(currentY));
        
    //     currentX += blockWidth + spacing;
    //     blocksInCurrentRow++;
}

void WorkflowAIAudioProcessorEditor::callDjangoSuggestChainAPI()
{
    // Get selected values
    juce::String genre = genreSelector.getText();
    juce::String fxType = fxTypeSelector.getText();

    DBG("=== FX ASSISTANT API CALL ===");
    DBG("Making API call with genre: " + genre + ", fx_type: " + fxType);

    // Convert to API-friendly format
    juce::String apiGenre = genre.toLowerCase().replace(" ", "-").replace("&", "");
    juce::String apiFxType = fxType.toLowerCase().replace(" ", "_");
    
    // Handle special cases
    if (apiGenre == "r-b") apiGenre = "rnb";
    if (apiGenre == "lo-fi") apiGenre = "lofi";
    
    DBG("Converted genre: " + apiGenre);
    DBG("Converted fx_type: " + apiFxType);

    // Build JSON request string manually (simpler than using DynamicObject)
    juce::String jsonString = "{\"genre\":\"" + apiGenre + "\",\"fx_type\":\"" + apiFxType + "\"}";
    DBG("Request JSON: " + jsonString);

    // Set up request
    juce::URL url("http://127.0.0.1:8000/api/suggest-fx-chain/");
    
    std::unique_ptr<juce::InputStream> stream = url.createInputStream(
        true,                                   // usePostCommand
        nullptr,                                // progressCallback
        nullptr,                                // progressCallbackContext
        "Content-Type: application/json\r\n",   // extra headers
        3000,                                   // timeoutMs
        nullptr,                                // responseHeaders
        nullptr,                                // statusCode
        5000,                                   // numRedirects
        jsonString                              // postData
    );

    // Clear any existing FX blocks before adding new ones
    fxBlocks.clear();

    // Read and parse response
    if (stream != nullptr)
    {
        juce::String responseText = stream->readEntireStreamAsString();
        DBG("Raw API Response: " + responseText);

        // Parse JSON response
        juce::var response = juce::JSON::parse(responseText);

        if (response.isArray())
        {
            DBG("✅ Successfully parsed JSON array with " + juce::String(response.getArray()->size()) + " effects");
            
            // Create FX blocks from the response array
            for (const auto& item : *response.getArray())
            {
                juce::String fxName = item.toString();
                DBG("Creating FX block: " + fxName);

                // Create new FX block component
                auto color = fxColors.count(fxName) ? fxColors.at(fxName) : juce::Colours::white;
                auto* block = new FXBlockComponent(fxName, color);
                
                // Start with default position (will be repositioned by layoutFXBlocks)
                block->setBounds(0, 0, 140, 50);
                
                addAndMakeVisible(block);
                fxBlocks.add(block);
            }
            
            // NOW USE THE LAYOUT METHOD!
            layoutFXBlocks();
        }
        else if (response.isObject())
        {
            // Handle error response from server
            juce::var errorMsg = response.getProperty("error", "Unknown error");
            DBG("❌ API Error: " + errorMsg.toString());
            showFallbackChain();
        }
        else
        {
            DBG("❌ Unexpected response format: " + responseText);
            showFallbackChain();
        }
    }
    else
    {
        DBG("❌ Failed to connect to Django server at http://127.0.0.1:8000");
        DBG("Make sure Django server is running: python manage.py runserver");
        showFallbackChain();
    }
    
    // Refresh the display
    repaint();
    DBG("=== API CALL COMPLETE ===");
}

void WorkflowAIAudioProcessorEditor::showFallbackChain()
{
    DBG("Showing fallback FX chain");
    
    // Default chain when API fails
    juce::StringArray fallback = {"EQ", "Compressor", "Reverb"};
    
    int startX = 20;
    int blockWidth = 120;
    int blockHeight = 40;
    int spacing = 10;
    int yPosition = 250;
    
    for (const auto& fxName : fallback)
    {
        auto color = fxColors.count(fxName) ? fxColors.at(fxName) : juce::Colours::white;
        auto* block = new FXBlockComponent(fxName, color);
        block->setBounds(startX, yPosition, blockWidth, blockHeight);
        addAndMakeVisible(block);
        fxBlocks.add(block);
        startX += blockWidth + spacing;
    }
}

void WorkflowAIAudioProcessorEditor::saveCurrentChain()
{
    DBG("Save Current Chain Clicked");

    // Collect currently active FX blocks
    juce::StringArray activeFX;
    for (auto* block : fxBlocks)
    {
        if (block->getState() != FXBlockComponent::BlockState::Bypassed)
        {
            activeFX.add(block->getFXName());
        }
    }

    if (activeFX.isEmpty())
    {
        DBG("No active FX to save");
        return;
    }

    DBG("Saving FX chain: " + activeFX.joinIntoString(" -> "));

    // TODO: In future versions, save to Django backend
    // For now, just show success message
    juce::AlertWindow::showMessageBoxAsync(
        juce::AlertWindow::InfoIcon,
        "Chain Saved",
        "FX Chain saved: " + activeFX.joinIntoString(" -> ") +
        "\n\nNote: Backend integration coming soon!",
        "OK"
    );
}

void WorkflowAIAudioProcessorEditor::openImportConvertDialog()
{
    DBG("Import/Convert button clicked");

    // Show preview of import feature
    juce::AlertWindow::showMessageBoxAsync(
        juce::AlertWindow::InfoIcon,
        "Import Feature Preview",
        "Import/Convert Feature Coming Soon!\n\n"
        "This will allow you to:\n"
        "• Import industry presets safely\n"
        "• Convert preset files to FX chains\n"
        "• Extract FX structure (legally compliant)\n"
        "• Supports .fxp, .xml, .json formats\n\n"
        "Backend integration in development!",
        "OK"
    );
}

void WorkflowAIAudioProcessorEditor::adjustSelectedFXParameter(float value)
{
    (void)value;
    
    if (selectedFXIndex < 0 || selectedFXIndex >= fxBlocks.size())
    {
        DBG("No FX selected for parameter adjustment");
        return;
    }
    
    auto* selectedBlock = fxBlocks[selectedFXIndex];
    juce::String fxName = selectedBlock->getFXName();
    
    DBG("Adjusting " + fxName + " parameter to " + juce::String(value, 2));
    
    // TODO: Route parameter changes to actual audio processing
    // For now, just provide visual feedback
    
    // Example mappings (these would connect to real audio parameters):
    if (fxName == "Reverb")
    {
        // Could map to reverb size, wetness, etc.
        DBG("Adjusting reverb wetness to " + juce::String(value * 100.0f, 1) + "%");
    }
    else if (fxName == "Compressor") 
    {
        // Could map to compression ratio, threshold, etc.
        DBG("Adjusting compression ratio to " + juce::String(1.0f + value * 9.0f, 1) + ":1");
    }
    else if (fxName == "EQ")
    {
        // Could map to frequency boost/cut
        DBG("Adjusting EQ gain to " + juce::String(value * 24.0f - 12.0f, 1) + " dB");
    }
    
    // Use the audioProcessor to actually set parameters (this removes the unused warning)
    // audioProcessor.setFXParameter(fxName, "intensity", value);
    (void)audioProcessor; // Suppress unused warning until we implement real parameter control

    // In a full implementation, this would call:
    // audioProcessor.setFXParameter(fxName, "intensity", value);
}

// This function is required by JUCE to instantiate the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new WorkflowAIAudioProcessor();
}
