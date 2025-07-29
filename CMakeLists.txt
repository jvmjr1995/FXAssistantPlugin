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
    PLUGIN_CODE FXAS
    FORMATS AU AUv3 Standalone
    PRODUCT_NAME "FXAssistant"
)

target_sources(FXAssistantPlugin
    PRIVATE
        PluginProcessor.cpp
        PluginProcessor.h
        PluginEditor.cpp
        PluginEditor.h
        CustomLookAndFeel.h
        FXBlockComponent.h
)

target_compile_definitions(FXAssistantPlugin
    PRIVATE
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=1
)

target_link_libraries(FXAssistantPlugin
    PRIVATE
        juce::juce_core
        juce::juce_audio_basics
        juce::juce_audio_utils
        juce::juce_audio_processors
        juce::juce_gui_basics
        juce::juce_graphics
        juce::juce_gui_extra
)