# Minimum version of CMake needed to build this project
cmake_minimum_required(VERSION 3.15)

# Define the project name and version
project(WorkflowAI VERSION 0.1.0)

# Tell the compiler to use C++17 standard
set(CMAKE_CXX_STANDARD 17)

# Point to your JUCE installation
set(JUCE_DIR "/Users/jessiemartin/JUCE")
add_subdirectory(${JUCE_DIR} JUCE)

add_compile_definitions(
    JUCE_VST3_CAN_REPLACE_VST2=0
)

# Create the plugin
juce_add_plugin(WorkflowAI
    COMPANY_NAME "JessieMartinAudio"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    PLUGIN_MANUFACTURER_CODE JMAU
    PLUGIN_CODE WFAI
    FORMATS AU VST3 Standalone
    PRODUCT_NAME "WorkflowAI"
    VST3_CATEGORIES Fx
)

# Add source files
target_sources(WorkflowAI
    PRIVATE
        PluginProcessor.cpp
        PluginProcessor.h
        PluginEditor.cpp
        PluginEditor.h
)

# Link JUCE modules
target_link_libraries(WorkflowAI
    PRIVATE
        juce::juce_core
        juce::juce_audio_basics
        juce::juce_audio_processors
        juce::juce_audio_devices
        juce::juce_audio_utils
        juce::juce_gui_basics
)