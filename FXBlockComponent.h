#pragma once

#include <juce_gui_basics/juce_gui_basics.h>
#include <juce_gui_extra/juce_gui_extra.h>

// A visual block representing one FX module (e.g., Reverb, Compressor)
class FXBlockComponent : public juce::Component,
                         public juce::TooltipClient
{
public:
    FXBlockComponent(const juce::String& fxName)
        : name(fxName), tooltipText("Drag to rearrange FX")
    {
        // Set tooltip + styling
        setName(name);
    }

    juce::String getTooltip() override
    {
        return tooltipText;
    }

    void paint(juce::Graphics& g) override
    {
        auto bounds = getLocalBounds().reduced(5);

        // Draw background with glow effect
        g.setColour(juce::Colours::darkgrey.withAlpha(0.9f));
        g.fillRoundedRectangle(bounds.toFloat(),10.0f);

        // Draw outline
        g.setColour(juce::Colours::aqua);
        g.drawRoundedRectangle(bounds.toFloat(), 10.0f, 2.0f);

        // Draw label text
        g.setColour(juce::Colours::white);
        juce::FontOptions fontOptions;
        juce::Font font(juce::FontOptions().withHeight(15.0f).withStyle("Bold"));
        g.setFont(font);
        g.drawFittedText(name, bounds, juce::Justification::centred, 1);
    }

    void mouseDown(const juce::MouseEvent& e) override
    {
        // For dragging support
        dragOffset = e.getPosition();
    }

    void mouseDrag(const juce::MouseEvent& e) override
    {
        // Allow block to be dragged horizontally
        auto newX = getX() + e.getDistanceFromDragStartX();
        setTopLeftPosition(newX, getY());
    }

private:
    juce::String name;
    juce::String tooltipText;
    juce::Point<int> dragOffset;
};