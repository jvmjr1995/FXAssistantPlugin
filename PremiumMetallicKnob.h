#include <juce_gui_basics/juce_gui_basics.h>
#include <juce_gui_extra/juce_gui_extra.h>
#include <functional>   // For std::function callback support

// Premium Metallic Knob Component with rainbow ring and smooth animations
// This is the main control knob that adjusts parameters of the selected FX
class PremiumMetallicKnob : public juce::Component,     // Base GUI component
                            private juce::Timer         // Timer for animations
{
public:
    // Constructor: Initialize the metallic knob with default values
    PremiumMetallicKnob()
        : currentColor(juce::Colours::lightblue)    // Start with light blue color
        , currentValue(0.5f)                        // Start at middle position (50%)
        , targetValue(0.5f)                         // Target also at middle initially
        , isDragging(false)                         // Not being dragged initially
        , lastMouseY(0)                             // No previous mouse position
        , rainbowPhase(0.0f)                        // Rainbow animation starts at 0
    {
        startTimerHz(60);       // Start 60 FPS timer for smooth animations
        setSize(120, 120);      // Set knob size to 120x120 pixels
    }

    // Destructor: Clean up when the component is destroyed
    ~PremiumMetallicKnob() override
    {
        stopTimer();        // Stop the animation timer to prevent crashes
    }

    // Set the color theme of the knob (usually matches the selected FX color)
    // color: juce::Colour that the knob should use for its accent elements
    void setColor(const juce::Colour& color)
    {
        currentColor = color;       // Store the new color
        repaint();                  // Redraw to show the color change
    }

    // Set the knob value with smooth animation to the target
    // newValue: Float between 0.0 and 1.0 representing knob position
    void setValue(float newValue)
    {
        // Clamp value to valid range (0.0 to 1.0) to prevent invalid positions
        targetValue = juce::jlimit(0.0f, 1.0f, newValue);
    }

    // Get the current knob value
    // Returns: Float between 0.0 and 1.0 representing current position
    float getValue() const { return currentValue; }

    // Callback function pointer for value change notifications
    // Set this to receive notifications when knob value changes
    std::function<void(float)> onValueChanged;

    // Override from Component: Main drawing function for the metallic knob
    // g: Graphics context for all drawing operations
    void paint(juce::Graphics& g) override
    {
        // Create drawing bounds with 10-pixel margin for glow effects and depth
        auto bounds = getLocalBounds().toFloat().reduced(10);
        auto center = bounds.getCentre();       // Get center point for circular elements
        auto radius = juce::jmin(bounds.getWidth(), bounds.getHeight()) / 2.0f;     // Use smaller dimension for radius
    

        // Draw outer metallic ring with animated rainbow effect
        juce::ColourGradient outerRing(
            // Create HSV color based on current rainbow phase (cycles through hue spectrum)
            juce::Colour::fromHSV(std::fmod(rainbowPhase, 1.0f), 0.7f, 0.9f, 1.0f),
            center.translated(-radius * 0.3f, -radius * 0.3f),  // Start position (offset for gradient)
            // Second color offset by 0.3 in hue for smooth gradient transition
            juce::Colour::fromHSV(std::fmod(rainbowPhase + 0.3f, 1.0f), 0.7f, 0.6f, 1.0f),
            center.translated(radius * 0.3f, radius * 0.3f),    // End position (opposite offset)
            true                                                // Radial gradient (circular)
        );
        g.setGradientFill(outerRing);   // Apply the rainbow gradient
        g.fillEllipse(bounds);          // Fill the entire circular area

        // Draw inner metallic surface with realistic metal gradient
        auto innerBounds = bounds.reduced(8);   // Smaller circle inside the rainbow ring
        juce::ColourGradient metallic(
            juce::Colour(80, 80, 90),               // Lighter metallic grey at top
            center.translated(0, -radius * 0.4f),   // Start position (above center)
            juce::Colour(40, 40, 50),               // Darker metallic grey at bottom
            center.translated(0, radius * 0.4f),    // End position (below center)
            false                                   // Linear gradient (vertical)
        );
        g.setGradientFill(metallic);    // Apply metallic gradient
        g.fillEllipse(innerBounds);     // Fill the inner circle

        // Draw current FX color indicator ring
        g.setColour(currentColor.withAlpha(0.8f));          // Use current FX color with transparency
        auto colorRingBounds = innerBounds.reduced(6);      // Slightly smaller ring for color indicator
        g.drawEllipse(colorRingBounds, 3.0f);               // Draw 3-pixel thick colored ring

        // Draw value arc showing current knob position
        auto arcBounds = innerBounds.reduced(12);       // Even smaller bounds for the value arc
        juce::Path valueArc;                            // Create path for the arc

        // Define arc range: starts at 1.2π (about 7 o'clock) and ends at 2.8π (about 5 o'clock)
        float startAngle = juce::MathConstants<float>::pi * 1.2f;
        float endAngle = juce::MathConstants<float>::pi * 2.8f;

        // Calculate current angle based on knob value (0.0 = start, 1.0 = end)
        float currentAngle = startAngle + (endAngle - startAngle) * currentValue;

        // Create arc from start position to current value position
        valueArc.addCentredArc(center.x, center.y,              // Center point
                               arcBounds.getWidth() / 2.0f, arcBounds.getHeight() / 2.0f,   // Arc radius
                               0.0f,                        // No rotation
                               startAngle, currentAngle,    // From start to current position
                               true);                       // Use center point

        // Draw the value arc with current FX color
        g.setColour(currentColor);
        g.strokePath(valueArc, juce::PathStrokeType(4.0f, juce::PathStrokeType::curved));

        // Draw metallic pointer indicating exact current position
        juce::Path pointer;
        float pointerLength = radius * 0.7f;    // Pointer length as percentage of knob radius
        
        // Create rectangular pointer shape (centered at origin)
        pointer.addRectangle(-1.5, -pointerLength, 3.0f, pointerLength * 0.6f);

        // Rotate pointer to current angle and position at knob center
        pointer.applyTransform(juce::AffineTransform::rotation(currentAngle).translated(center));

        // Draw pointer in white for visibility
        g.setColour(juce::Colours::white);
        g.fillPath(pointer);

        // Draw center cap/button for realistic hardware appearance
        g.setColour(juce::Colour(60, 60, 70));          // Dark grey for main cap   
        g.fillEllipse(center.x - 8, center.y - 8, 16, 16);  // 16x16 pixel circle at center

        // Add highlight on center cap for 3D effect
        g.setColour(juce::Colours::white.withAlpha(0.3f));  // Semi-transparent white highlight
        g.fillEllipse(center.x - 6, center.y - 6, 12, 12);  // Slightly smaller highlight circle
    }

    // Override from Component: Called when user starts clicking/dragging the knob
    // e: MouseEvent containing click information
    void mouseDown(const juce::MouseEvent& e) override
    {
        isDragging = true;      // Enable dragging mode
        lastMouseY = e.y;       // Remember starting Y position for drag calculations
    }

    // Override from Component: Called continuously while user drags the knob
    // e: MouseEvent containing current mouse position
    void mouseDrag(const juce::MouseEvent& e) override
    {
        if (isDragging)     // Only process if we're in dragging mode
        {
            // Calculate change in Y position (negative Y = upward = increase value)
            float delta = (lastMouseY - e.y) * 0.01f;  // Scale factor for sensitivity

            // Update current value and clamp to valid range
            setValue(currentValue + delta);
            lastMouseY = e.y;       // Update last position for next drag calculation
            
            // Notify listeners that value changed (if callback is set)
            if (onValueChanged)
                onValueChanged(currentValue);
        }
    }

    // Override from Component: Called when user releases mouse button
    void mouseUp(const juce::MouseEvent&) override
    {
        isDragging = false;     // Exit dragging mode
    }

    // Override from Timer: Called 60 times per second for smooth animations
    void timerCallback() override
    {
        // Smooth value animation: gradually move current value toward target value
        if (std::abs(currentValue - targetValue) > 0.001f)  // Only animate if difference is meaningful
        {
            // Move 10% of the way toward target each frame (creates smooth easing)
            currentValue += (targetValue - currentValue) * 0.1f;
            repaint();      // Redraw to show value change
        }

        // Rainbow ring animation: slowly cycle through color spectrum
        rainbowPhase += 0.002f;         // Small increment for slow, smooth color transition
        if (rainbowPhase > 1.0f)        // Reset when we complete full hue cycle
            rainbowPhase = 0.0f;
        repaint();                      // Redraw to show color change
    }

private:
    // Private member variables for knob state
    juce::Colour currentColor;      // Current theme color (matches selected FX)
    float currentValue;             // Current knob position (0.0 to 1.0)
    float targetValue;              // Target position for smooth animation
    bool isDragging;                // Whether user is currently dragging
    int lastMouseY;                 // Last mouse Y position for drag calculations
    float rainbowPhase;             // Current phase of rainbow animation (0.0 to 1.0)

    // JUCE macro to prevent accidental copying (safety feature)
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PremiumMetallicKnob)
};