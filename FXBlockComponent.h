#pragma once

// Include JUCE GUI libraries for UI components and graphics
#include <juce_gui_basics/juce_gui_basics.h>
#include <juce_gui_extra/juce_gui_extra.h>
#include <functional>

// Enhanced FXBlockComponent with selection states and visual feedback
// This represents a single effect in the FX chain (like "EQ" or "Compressor")
class FXBlockComponent : public juce::Component,        // Base GUI component
                         public juce::TooltipClient,    // Enables hover tooltips
                         private juce::Timer            // Enables animations via timer callbacks
{
public:
    // Enum defining the different visual states an FX block can be in
    // Each state has different colors, glow effects, and behaviors
    enum class BlockState
    {
        Suggested,      // AI suggested this effect (blue glow with gentle pulse)
        Selected,       // Currently selected for knob control (bright glow with FX color)
        Active,         // Enabled but not selected (subtle glow)
        Bypassed        // Disabled/turned off (no glow, dimmed appearance)
    };

    // Constructor: Creates a new FX block with a name and associated color
    // fxName: Display name like "EQ", "Compressor", "Reverb"
    // fxColor: Unique color for this FX type (used for knob and glow effects)
    FXBlockComponent(const juce::String& fxName, const juce::Colour& fxColorIn)
        : name(fxName)                              // Store the effect name for display
        , fxColor(fxColorIn)                          // Store the unique color for this FX
        , currentState(BlockState::Suggested)      // Start in "AI suggested" state
        , isHovered(false)                          // Not hovered initially
        , glowIntensity(0.6f)                       // Start with moderate glow
        , pulsePhase(0.0f)                          // Animation starts at phase 0
        , onSelectionChanged(nullptr)               // No callback set initially
    {
        // Start a 60 FPS timer for smooth animations (calls timerCallback() 60x per second)
        startTimerHz(60);
    }

    // Destructor: Clean up when the component is destroyed
    ~FXBlockComponent() override
    {
        stopTimer();    // Stop the animation timer to prevent crashes
    }

    // Change the visual state of this FX block
    // newState: The new state to transition to (Suggested, Selected, Active, or Bypassed)
    void setState(BlockState newState)
    {
        currentState = newState;    //Update internal state
        repaint();
    }

    // Get the current state of this FX block
    // Returns: Current BlockState enum value
    BlockState getState() const { return currentState; }

    // Get the color associated with this FX type
    // Returns: juce::Colour object representing this FX's theme color
    juce::Colour getFXColor() const { return fxColor; }

    // Get the name of this FX effect
    // Returns: String containing the FX name (like "EQ" or "Compressor")
    juce::String getFXName() const { return name; }

    // Callback function pointer that gets called when this block is selected
    std::function<void(FXBlockComponent*)> onSelectionChanged;

    // Override from TooltipClient: Provides hover tooltip text based on current state
    // Returns: String containing helpful text shown when user hovers over this block
    juce::String getTooltip() override
    {
        // Return different tooltip text based on the current state
        switch (currentState)
        {
            case BlockState::Suggested:
                return name + " - AI Suggested • Click to select";
            case BlockState::Selected:
                return name + " - Selected • Use knob to adjust";
            case BlockState::Active:
                return name + " - Active • Click to select";
            case BlockState::Bypassed:
                return name + " - Bypassed • Click to enable";
        }
        return name;    // Fallback if state is unexpected
    }

    // Override from Component: Main drawing function called whenever component needs to be redrawn
    // g: Graphics context for drawing operations (like a paintbrush)
    void paint(juce::Graphics& g) override
    {
        // Create drawing bounds with 3-pixel margin from edges for glow effects
        auto bounds = getLocalBounds().reduced(3);

        // Declare colors that will be set based on current state
        juce::Colour baseColor, glowColor;
        float currentGlow = glowIntensity;

        // Set colors and glow intensity based on current state
        switch (currentState)
        {
            case BlockState::Suggested:
                baseColor = juce::Colour(45, 45, 55);       // Medium grey background
                glowColor = juce::Colours::lightblue;       // Blue glow for AI suggestions
                // Create gentle pulsing glow using sine wave (0.4 base + 0.2 oscillation)
                currentGlow = 0.4f + 0.2f * std::sin(pulsePhase);
                break;

            case BlockState::Selected:
                baseColor = juce::Colour(60, 50, 40);       // Warmer brown-orange background
                glowColor = fxColor;                        // Use this FX's unique color
                // Create bright pulsing glow with double frequency for attention
                currentGlow = 0.8f + 0.2f * std::sin(pulsePhase * 2.0f);
                break;
            
            case BlockState::Active:
                baseColor = juce::Colour(50, 55, 45);       // Slightly green-tinted background
                glowColor = fxColor.withAlpha(0.6f);        // FX color but more transparent
                currentGlow = 0.3f;                         // Constant subtle glow
                break;

            case BlockState::Bypassed:
                baseColor = juce::Colour(35, 35, 40);       // Dark grey (dimmed appearance)
                glowColor = juce::Colours::grey;            // Neutral grey glow
                currentGlow = 0.1f;                         // Very minimal glow
                break;
        }

        // Draw glow effect with multiple concentric rings for smooth appearance
        if (currentGlow > 0.1f)     // Only draw glow if intensity is meaningful
        {
            // Draw 4 concentric glow rings, each one larger and more transparent
            for (int i = 0; i < 4; i++)
            {
                // Calculate transparency: outer rings are more transparent
                // Formula: (1 - ring_position/total_rings) * base_alpha * current_glow
                float alpha = (1.0f - (i / 4.0f)) * 0.3f * currentGlow;
                
                // Set glow color with calculated transparency
                g.setColour(glowColor.withAlpha(alpha));

                // Draw rounded rectangle ring, each ring 2 pixels larger than the last
                g.drawRoundedRectangle(bounds.expanded(i * 2).toFloat(), 10.0f, 1.5f);
            }
        }

        // Draw main background with gradient for 3D depth effect
        juce::ColourGradient gradient(
            baseColor.brighter(0.1f),               // Slightly brighter color at top
            bounds.getTopLeft().toFloat(),          // Start position (top-left)
            baseColor.darker(0.2f),                 // Darker color at bottom for depth
            bounds.getBottomRight().toFloat(),      // End position (bottom-right)
            false                                   // Linear gradient (not radial)
        );
        g.setGradientFill(gradient);                        // Apply the gradient
        g.fillRoundedRectangle(bounds.toFloat(), 10.0f);    // Fill with 10px rounded corners
        
        // Draw border around the block with state-dependent thickness
        float borderWidth = (currentState == BlockState::Selected) ? 2.5f : 1.5f;
        g.setColour(glowColor.withAlpha(0.8f));     // Use glow color for border
        g.drawRoundedRectangle(bounds.toFloat(), 10.0f, borderWidth);

        // Draw the FX name text in the center
        // Set text color: dimmed for bypassed effects, bright for others
        g.setColour(juce::Colours::white.withAlpha(currentState == BlockState::Bypassed ? 0.6f : 0.95f));
        g.(juce::Font(14.0f, juce::Font::bold));     // 14px bold font
        // Draw text centered within the bounds, reduced by 8px horizontal and 4px vertical padding
        g.drawFittedText(name, bounds.reduced(8, 4), juce::Justification::centred, 1);

        // Draw selection indicator dot for currently selected blocks
        if (currentState == BlockState::Selected)
        {
            g.setColour(fxColor.withAlpha(0.8f));       // Use FX color with transparency
            // Draw small circle in top-right corner as selection indicator
            g.fillEllipse(bounds.getRight() - 12, bounds.getY() + 4, 8, 8);
        }
    }

    // Override from Component: Called when user clicks on this block
    // e: MouseEvent containing click information (position, button, etc.)
    void mouseDown(const juce::MouseEvent&) override
    {
        // If we have a selection callback set, call it with this block as parameter
        if (onSelectionChanged)
            onSelectionChanged(this);
    }

    // Override from Component: Called when mouse cursor enters this component's area
    void mouseEnter(const juce::MouseEvent&) override
    {
        isHovered = true;   // Set hover state to true
        repaint();          // Trigger a redraw to show hover effects
    }

    // Override from Component: Called when mouse cursor leaves this component's area
    void mouseExit(const juce::MouseEvent&) override
    {
        isHovered = false;  // Clear hover state
        repaint();          // Trigger redraw to remove hover effects
    }

    // NO mouseDRAG method = no dragging possible!
    // This prevents blocks from being dragged off-screen

    // Animation timer callback - called 60 times per second for smooth animations
    void timerCallback() override
    {
        // Update pulse phase for border color animation (increments create smooth sine wave)
        pulsePhase += 0.08f;        // Increment animation phase

        // Reset phase to 0 when it completes a full cycle (prevents infinite growth)
        if (pulsePhase > juce::MathConstants<float>::twoPi)      // Reset when we complete a cycle
            pulsePhase = 0.0f;

        // Only trigger redraws for blocks that have animated states (saves CPU)
        if (currentState == BlockState::Suggested || currentState == BlockState::Selected)
            repaint();
    }

private:
    // Private member variables to store component state
    juce::String name;          // Name of the FX (e.g., "EQ", "Compressor")
    juce::Colour fxColor;       // Text shown in tooltip on hover
    BlockState currentState;    // Current visual/functional state
    bool isHovered;             // True when mouse is over the component
    float glowIntensity;        // Current glow strength (0.0 to 1.0)
    float pulsePhase;           // Animation phase for pulsing effects (0.0 to 1.0)

    // JUCE macro to prevent copying this component (safety feature)
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(FXBlockComponent)
};