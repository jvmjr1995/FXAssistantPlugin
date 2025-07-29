#pragma once

// Include GUI and Graphics modules from JUCE
#include <juce_gui_basics/juce_gui_basics.h>

// Define a custom LookAndFeel class that inherits from JUCE's LookAndFeel_V4
class CustomLookAndFeel : public juce::LookAndFeel_V4
{
public:
    // Define light and dark mode themes as an enum
    enum class ThemeMode { Dark, Light };

    // Track the current theme mode (default: Dark)
    ThemeMode currentMode = ThemeMode::Dark;

    // Constructor - sets the default theme when the class is created
    CustomLookAndFeel()
    {
        setTheme(currentMode);
    }

    // This function applies color schemes depending on the selected theme
    void setTheme(ThemeMode mode)
    {
        currentMode = mode;

        // === DARK MODE COLORS ===
        if (mode == ThemeMode::Dark)
        {
            setColour(juce::ComboBox::backgroundColourId, juce::Colour(30, 30, 30));    // Dark grey background
            setColour(juce::ComboBox::textColourId, juce::Colours::white);             // White text
            setColour(juce::Slider::rotarySliderFillColourId, juce::Colours::aqua);     // Glowing knob arc
            setColour(juce::Slider::thumbColourId, juce::Colours::orange);              // Knob thumb
            setColour(juce::TextButton::buttonColourId, juce::Colours::darkgrey);        // Button fill
        }
        
        // === LIGHT MODE COLORS ===
        else
        {
            setColour(juce::ComboBox::backgroundColourId, juce::Colours::white);        // White background
            setColour(juce::ComboBox::textColourId, juce::Colours::black);              // Black text
            setColour(juce::Slider::rotarySliderFillColourId, juce::Colours::darkblue); // Blue knob arc
            setColour(juce::Slider::thumbColourId, juce::Colours::black);               // Black knob thumb
            setColour(juce::TextButton::buttonColourId, juce::Colours::lightgrey);       // Light grey button
        }
    }

    // Custom draw function for rotary sliders (circular knobs)
    void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                            float sliderPosProportional, float rotaryStartAngle,
                            float rotaryEndAngle, juce::Slider& slider) override
    {
        // Define knob bounds with padding
        auto bounds = juce::Rectangle<float>(x, y, width, height). reduced(10);

        // Radius of the knob
        auto radius = juce::jmin(bounds.getWidth(), bounds.getHeight()) / 2.0f;

        // Center point of the knob
        auto centre = bounds.getCentre();

        // Current angle based on slider value
        auto angle = rotaryStartAngle + sliderPosProportional * (rotaryEndAngle - rotaryStartAngle);

        // Fill the knob background
        g.setColour(juce::Colours::darkgrey);
        g.fillEllipse(bounds);

        // Draw the glowing arc on top of the knob
        g.setColour(slider.findColour(juce::Slider::rotarySliderFillColourId));
        juce::Path glowPath;
        glowPath.addCentredArc(centre.x, centre.y, radius, 0.0f, rotaryStartAngle, angle, true);
        g.strokePath(glowPath, juce::PathStrokeType(4.0f));
    }
};