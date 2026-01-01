#pragma once

// Include JUCE GUI library for styling components
#include <juce_gui_basics/juce_gui_basics.h>

// CustomLookAndFeel defines how all UI components look and behave
// Inherits from LookAndFeel_V4 (JUCE's modern default styling system)
class CustomLookAndFeel : public juce::LookAndFeel_V4
{
public:
    // Enum to define available theme modes
    enum class ThemeMode { Dark, Light };

    // Store current theme mode (starts with Dark)
    ThemeMode currentMode = ThemeMode::Dark;

    // Constructor: Initialize the look and feel system
    CustomLookAndFeel()
    {
        setTheme(currentMode);  // Apply the default dark theme

        // Set up modern font (commented out as it needs font file)
        // setDefaultSansSerifTypeface(juce::Typeface::createSystemTypefaceFor(
        //     BinaryData::getNamedResource("font", 0), BinaryData::getNamedResourceSize("font", 0)));
    }

    // Apply color scheme based on selected theme mode
    void setTheme(ThemeMode mode)
    {
        currentMode = mode;     // Store the new theme mode

        // === DARK MODE COLORS ===
        if (mode == ThemeMode::Dark)    // Dark theme colors
        {
            // === COMBO BOX (DROPDOWN) STYLING ===
            
            // Background color for dropdown boxes
            setColour(juce::ComboBox::backgroundColourId, juce::Colour(35, 35, 45));
            
            // Text color inside dropdowns
            setColour(juce::ComboBox::textColourId, juce::Colours::white);  // White text
            
            // Border color around dropdowns
            setColour(juce::ComboBox::outlineColourId, juce::Colour(60, 60, 70));

            // Color of the dropdown arrow
            setColour(juce::ComboBox::arrowColourId, juce::Colour(120, 120, 130));

            // === SLIDER (KNOB) STYLING ===
            
            // Color of the active arc on rotary sliders - Glowing knob arc
            setColour(juce::Slider::rotarySliderFillColourId, juce::Colours::aqua);
            
            // Color of the inactive track on rotary sliders
            setColour(juce::Slider::rotarySliderOutlineColourId, juce::Colour(60, 60, 70));
            
            // Color of the slider thumb/handle
            setColour(juce::Slider::thumbColourId, juce::Colours::white);

            // === BUTTON STYLING ===
            
            // Background color for buttons
            setColour(juce::TextButton::buttonColourId, juce::Colour(45, 45, 55));

            // Text color when button is pressed/on
            setColour(juce::TextButton::textColourOnId, juce::Colours::white);

            // Text color when button is not pressed/off
            setColour(juce::TextButton::textColourOffId, juce::Colour(200, 200, 210));

            // === TOGGLE BUTTON (CHECKBOX) STYLING ===

            // Text color next to checkboxes
            setColour(juce::ToggleButton::textColourId, juce::Colours::white),

            // Color of unchecked checkbox
            setColour(juce::ToggleButton::tickDisabledColourId, juce::Colour(100, 100, 110));

            // Color of checked checkbox
            setColour(juce::ToggleButton::tickColourId, juce::Colours::aqua);
        }
        else    // Light theme colors
        {
            // === LIGHT THEME COLORS ===
            // Light backgrounds and dark text for contrast
            setColour(juce::ComboBox::backgroundColourId, juce::Colour(245, 245, 250));
            setColour(juce::ComboBox::textColourId, juce::Colour(40, 40, 50));
            setColour(juce::ComboBox::outlineColourId, juce::Colour(180, 180, 190));

            // Blue accent colors for sliders in light mode
            setColour(juce::Slider::rotarySliderFillColourId, juce::Colour(0, 150, 200));
            setColour(juce::Slider::thumbColourId, juce::Colour(60, 60, 70));

            // Light button styling
            setColour(juce::TextButton::buttonColourId, juce::Colour(220, 220, 230));
            setColour(juce::TextButton::textColourOnId, juce::Colour(40, 40, 50));
        }
    }

    // Custom drawing method for ComboBox (dropdown) components
    void drawComboBox(juce::Graphics& g, int width, int height, bool isButtonDown,
                      int buttonX, int buttonY, int buttonW, int buttonH,
                      juce::ComboBox& comboBox) override
    {
        juce::ignoreUnused(isButtonDown);  // Add this line at the start

        // Create rectangle representing the entire dropdown area
        auto bounds = juce::Rectangle<float>(0, 0, width, height);

        // === MODERN GRADIENT BACKGROUND ===
        // Create vertical gradient from slightly lighter top to darker bottom
        juce::ColourGradient gradient(
            comboBox.findColour(juce::ComboBox::backgroundColourId).brighter(0.1f), // Top color (10% brighter)
            bounds.getTopLeft(),                                                    // Start position
            comboBox.findColour(juce::ComboBox::backgroundColourId).darker(0.1f),   // Bottom color (10% darker)
            bounds.getBottomRight(),                                                // End position
            false                                                                   // Linear (not radial)
        );

        // Apply gradient and fill the rounded rectangle
        g.setGradientFill(gradient);
        g.fillRoundedRectangle(bounds, 8.0f);   // 8px corner radius for modern look


        // === MODERN BORDER WITH FOCUS GLOW ===

        // Change border color based on focus state
        auto borderColor = comboBox.hasKeyboardFocus(true) ?        // Is dropdown focused?
                           juce::Colours::aqua :                    // Yes: bright aqua glow
                           comboBox.findColour(juce::ComboBox::outlineColourId);    // No: normal grey
        
        // Draw border with focus-dependent thickness
        g.setColour(borderColor.withAlpha(0.8f));   // Slightly transparent
        g.drawRoundedRectangle(bounds, 8.0f, comboBox.hasKeyboardFocus(true) ? 2.0f : 1.5f);


        // === MODERN DROPDOWN ARROW ===

        // Create area for the dropdown arrow (right side of combobox)
        auto arrowBounds = juce::Rectangle<float>(buttonX, buttonY, buttonW, buttonH).reduced(4);

        // Create triangular arrow path pointing downward
        juce::Path arrow;
        arrow.addTriangle(
            arrowBounds.getTopLeft().translated(arrowBounds.getWidth() * 0.3f, arrowBounds.getHeight() * 0.3f),     // Left point
            arrowBounds.getTopRight().translated(-arrowBounds.getWidth() * 0.3f, arrowBounds.getHeight() * 0.3f),   // Right point
            juce::Point<float>(arrowBounds.getCentreX(), arrowBounds.getBottom() - arrowBounds.getHeight() * 0.2f) // Bottom point
        );

        // Draw the arrow with specified color
        g.setColour(comboBox.findColour(juce::ComboBox::arrowColourId));
        g.fillPath(arrow);
    }

    // Custom drawing method for button backgrounds
    void drawButtonBackground(juce::Graphics& g, juce::Button& button, const juce::Colour& backgroundColour,
                              bool shouldDrawButtonAsHighlighted, bool shouldDrawButtonAsDown) override
    {
        // Create button area with small margin
        auto bounds = button.getLocalBounds().toFloat().reduced(1);

        // === STATE-BASED GRADIENT COLORS ===
        juce::Colour topColor, bottomColor;

        if (shouldDrawButtonAsDown) // Button is being pressed
        {
            topColor = backgroundColour.darker(0.3f);       // Much darker top
            bottomColor = backgroundColour.darker(0.1f);    // Slightly darker bottom
        }
        else if (shouldDrawButtonAsHighlighted) // Button is hovered
        {
            topColor = backgroundColour.brighter(0.2f);     // Brighter top
            bottomColor = backgroundColour.darker(0.1f);    // Darker bottom
        }
        else    // Normal button state
        {
            topColor = backgroundColour.brighter(0.1f);     // Slightly brighter top
            bottomColor = backgroundColour.darker(0.2f);    // Darker bottom for depth
        }

        // Create and apply gradient
        juce::ColourGradient gradient(topColor, bounds.getTopLeft(), bottomColor, bounds.getBottomRight(), false);
        g.setGradientFill(gradient);
        g.fillRoundedRectangle(bounds,8.0f);    // Fill with rounded corners


        // === MODERN BORDER WITH HOVER GLOW ===
        
        // Choose border color: glow when highlighted, subtle when normal
        auto borderColor = shouldDrawButtonAsHighlighted ? juce::Colours::aqua : juce::Colour(80, 80, 90);
        g.setColour(borderColor.withAlpha(0.6f));

        // Draw border with hover-dependent thickness
        g.drawRoundedRectangle(bounds, 8.0f, shouldDrawButtonAsHighlighted ? 2.0f : 1.0f);

        // === SUBTLE INNER HIGHLIGHT ===
        // Add inner glow when highlighted for premium feel
        if (shouldDrawButtonAsHighlighted)
        {
            g.setColour(juce::Colours::white.withAlpha(0.1f));  // Very subtle white
            g.fillRoundedRectangle(bounds.reduced(2), 6.0f);    // Smaller inner rectangle
        }
    }

    // Custom drawing method for rotary sliders (circular knobs)
    void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                            float sliderPosProportional, float rotaryStartAngle,
                            float rotaryEndAngle, juce::Slider& slider) override
    {
        // Define knob bounds with padding
        auto bounds = juce::Rectangle<float>(x, y, width, height). reduced(12);

        // Radius of the knob
        auto radius = juce::jmin(bounds.getWidth(), bounds.getHeight()) / 2.0f; // Half of smaller dimension

        // Center point of the knob
        auto centre = bounds.getCentre();

        // Calculate current angle based on slider value (0.0 to 1.0)
        auto angle = rotaryStartAngle + sliderPosProportional * (rotaryEndAngle - rotaryStartAngle);

        // === MODERN KNOB BACKGROUND WITH GRADIENT ===

        // Create vertical gradient for 3D effect
        juce::ColourGradient knobGradient(
            juce::Colour(60, 60, 70),               // Lighter grey at top
            centre.translated(0, -radius * 0.5f),   // Top position
            juce::Colour(30, 30, 40),               // Darker grey at bottom
            centre.translated(0, radius * 0.5f),    // Bottom position
            false                                   // Linear gradient
        );

        // Apply gradient and fill circular knob
        g.setGradientFill(knobGradient);
        g.fillEllipse(bounds);

        // === OUTER RING ===

        // Draw subtle outer ring for definition
        g.setColour(juce::Colour(80, 80, 90));
        g.drawEllipse(bounds, 2.0f);    // 2px thick ring

        // === MODERN ARC WITH GLOW EFFECT ===

        // Create arc path showing current value
        juce::Path arc;
        arc.addCentredArc(
            centre.x, centre.y,         // Center point
            radius - 4, radius - 4,     // Width and height (slightly smaller than knob)
            0.0f,                       // Rotation
            rotaryStartAngle,           // Start angle
            angle,                      // End angle (current value)
            true                        // Use clockwise direction
        );

        // Draw the glowing arc on top of the knob/Draw main arc with accent color
        g.setColour(slider.findColour(juce::Slider::rotarySliderFillColourId));
        g.strokePath(arc, juce::PathStrokeType(4.0f, juce::PathStrokeType::curved, juce::PathStrokeType::rounded));

        // === GLOW EFFECT FOR THE ARC ===

        // Draw wider, more transparent arc behind for glow effect
        g.setColour(slider.findColour(juce::Slider::rotarySliderFillColourId).withAlpha(0.3f));
        g.strokePath(arc, juce::PathStrokeType(8.0f, juce::PathStrokeType::curved, juce::PathStrokeType::rounded));

        // === MODERN POINTER ===

        // Create pointer indicating current value
        juce::Path pointer;
        auto pointerLength = radius * 0.6f;     // 60% of knob radius
        auto pointerThickness = 3.0f;           // 3px thick pointer

        // Create rectangular pointer
        pointer.addRectangle(-pointerThickness * 0.5f, -pointerLength, pointerThickness, pointerLength * 0.7f);

        // Rotate pointer to current angle and position at center
        pointer.applyTransform(juce::AffineTransform::rotation(angle).translated(centre));

        // Draw white pointer
        g.setColour(juce::Colours::white);
        g.fillPath(pointer);
    }

    // Custom drawing method for linear sliders (vertical faders)
    void drawLinearSlider(juce::Graphics& g, int x, int y, int width, int height,
                          float sliderPos, float minSliderPos, float maxSliderPos,
                          const juce::Slider::SliderStyle style, juce::Slider& slider) override
    {
        juce::ignoreUnused(minSliderPos, maxSliderPos, slider);  // Add this line
        
        // Only handle vertical linear sliders (like EQ faders)
        if (style == juce::Slider::LinearVertical)
        {
            // Create slider area with padding
            auto bounds = juce::Rectangle<float>(x, y, width, height).reduced(8, 4);

            // Create narrow track in center of slider area
            auto trackBounds = bounds.withWidth(4).withX(bounds.getCentreX() - 2.0f);   // 4px wide, centered

            // === MODERN TRACK BACKGROUND ===

            // Draw inactive track background
            g.setColour(juce::Colour(50, 50, 60));
            g.fillRoundedRectangle(trackBounds, 2.0f);  // Rounded track

            // === MODERN TRACK FILL ===

            // Calculate fill height based on current slider position
            auto fillHeight = sliderPos - bounds.getY();
            auto fillBounds = trackBounds.withHeight(fillHeight).withBottomY(sliderPos);

            // Create gradient for active portion of track
            auto topX = fillBounds.getCentreX();
            auto topY = fillBounds.getY();
            auto bottomX = fillBounds.getCentreX();
            auto bottomY = fillBounds.getBottom();

            juce::ColourGradient fillGradient(
                juce::Colours::aqua,                // Bright aqua at top
                topX,                               // Start X (center horizontally, top vertically)
                topY,                               // Start Y
                juce::Colours::aqua.darker(0.3f),   // Darker aqua at bottom
                bottomX,                            // End X (center horizontally, bottom vertically)
                bottomY,                            // End Y
                false                               // Linear gradient
            );

            // Apply gradient and fill active track
            g.setGradientFill(fillGradient);
            g.fillRoundedRectangle(fillBounds, 2.0f);

            // === MODERN THUMB (SLIDER HANDLE) ===

            // Create rectangular thumb centered on current position
            auto thumbBounds = juce::Rectangle<float>(12, 8).withCentre(juce::Point<float>(bounds.getCentreX(), sliderPos));

            // Create gradient for thumb
            auto thumbTopX = thumbBounds.getCentreX();
            auto thumbTopY = thumbBounds.getY();
            auto thumbBottomX = thumbBounds.getCentreX();
            auto thumbBottomY = thumbBounds.getBottom();

            juce::ColourGradient thumbGradient(
                juce::Colours::white,           // White at top
                thumbTopX,                      // Start X
                thumbTopY,                      // Start Y
                juce::Colour(200, 200, 210),    // Light grey at bottom
                thumbBottomX,                   // End X
                thumbBottomY,                   // End Y
                false                           // Linear gradient
            );

            // Apply gradient and fill thumb
            g.setGradientFill(thumbGradient);
            g.fillRoundedRectangle(thumbBounds, 4.0f);  // Rounded thumb

            // Draw subtle border around thumb
            g.setColour(juce::Colour(120, 120, 130));
            g.drawRoundedRectangle(thumbBounds, 4.0f, 1.0f);    // 1px border

        }
    }
};