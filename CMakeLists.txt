cmake_minimum_required(VERSION 3.15)

project(FXAssistantPlugin VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)

# Make JUCE available via CMake’s FetchContent or external path
set(JUCE_DIR "/Users/jessiemartin/JUCE")  # Replace this if you relocate JUCE

add_subdirectory(${JUCE_DIR} JUCE)

juce_add_plugin(FXAssistantPlugin
    COMPANY_NAME "JessieMartinAudio"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    PLUGIN_MANUFACTURER_CODE JMAU
    PLUGIN_CODE WFAI
    FORMATS AU AUv3 Standalone
    PRODUCT_NAME "WorkflowAI"
)

target_sources(FXAssistantPlugin
    PRIVATE
        PluginProcessor.cpp
        PluginProcessor.h
        PluginEditor.cpp
        PluginEditor.h
        CustomLookAndFeel.h
        FXBlockComponent.h
        PremiumMetallicKnob.h
)

target_compile_definitions(FXAssistantPlugin
    PRIVATE
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=1
        JUCE_DISPLAY_SPLASH_SCREEN=0
)

target_link_libraries(FXAssistantPlugin
    PRIVATE
        # Core JUCE modules
        juce::juce_core
        juce::juce_data_structures
        juce::juce_events
        juce::juce_graphics
        juce::juce_gui_basics
        juce::juce_gui_extra
        
        # Audio modules
        juce::juce_audio_basics
        juce::juce_audio_devices
        juce::juce_audio_formats
        juce::juce_audio_processors
        juce::juce_audio_utils
        
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
)