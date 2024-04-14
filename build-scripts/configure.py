#!/usr/bin/python3
import sys

sys.dont_write_bytecode = True

import ninja_syntax
import subprocess
from pathlib import Path

ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

files = [
    "src/unity_build/common.cpp",
    "src/unity_build/interface_editor_components.cpp",
    "third_party/JUCE/modules/juce_audio_plugin_client/LV2/juce_LV2_Wrapper.cpp",
    #"plugin/JuceLibraryCode/include_juce_audio_plugin_client_Standalone.cpp",
    "src/unity_build/interface_editor_sections2.cpp",
    "src/unity_build/interface_editor_sections.cpp",
    "src/unity_build/interface_look_and_feel.cpp",
    "src/unity_build/interface_wavetable.cpp",
    "src/unity_build/plugin.cpp",
    "src/unity_build/synthesis.cpp",
    "src/JuceLibraryCode/BinaryData.cpp",
    "src/JuceLibraryCode/include_juce_audio_basics.cpp",
    "src/JuceLibraryCode/include_juce_audio_devices.cpp",
    "src/JuceLibraryCode/include_juce_audio_formats.cpp",
    "src/JuceLibraryCode/include_juce_audio_plugin_client_utils.cpp",
    "src/JuceLibraryCode/include_juce_audio_processors.cpp",
    "src/JuceLibraryCode/include_juce_audio_utils.cpp",
    "src/JuceLibraryCode/include_juce_core.cpp",
    "src/JuceLibraryCode/include_juce_data_structures.cpp",
    "src/JuceLibraryCode/include_juce_dsp.cpp",
    "src/JuceLibraryCode/include_juce_events.cpp",
    "src/JuceLibraryCode/include_juce_graphics.cpp",
    "src/JuceLibraryCode/include_juce_gui_basics.cpp",
    "src/JuceLibraryCode/include_juce_gui_extra.cpp",
    "src/JuceLibraryCode/include_juce_opengl.cpp",
]

ninja.variable(
    "iflags",
    (
        "-I/usr/include/freetype2 "
        "-I/usr/include/libpng16 "
        "-I/usr/include/harfbuzz "
        "-I/usr/include/glib-2.0 "
        "-I/usr/lib/glib-2.0/include "
        "-I/usr/include/sysprof-6 "
        "-Ithird_party/JUCE/modules/juce_audio_processors/format_types/VST3_SDK "
        "-Ithird_party/VST_SDK/VST2_SDK "
        "-Isrc/JuceLibraryCode "
        "-Ithird_party/JUCE/modules "
        "-Isrc/common "
        "-Isrc/common/wavetable "
        "-Isrc/interface/editor_components "
        "-Isrc/interface/editor_sections "
        "-Isrc/interface/look_and_feel "
        "-Isrc/interface/wavetable "
        "-Isrc/interface/wavetable/editors "
        "-Isrc/interface/wavetable/overlays "
        "-Isrc/plugin "
        "-Isrc/synthesis/synth_engine "
        "-Isrc/synthesis/effects "
        "-Isrc/synthesis/filters "
        "-Isrc/synthesis/framework "
        "-Isrc/synthesis/lookups "
        "-Isrc/synthesis/modulators "
        "-Isrc/synthesis/modules "
        "-Isrc/synthesis/producers "
        "-Isrc/synthesis/utilities "
        "-Ithird_party "
    ),
)

ninja.variable(
    "cflags",
    (
        "-pthread "
        "-fPIC "
        "-Ofast "
        "-ffast-math "
        "-ftree-vectorize "
        "-ftree-slp-vectorize "
        "-funroll-loops "
        "-fvisibility=hidden "
        "-fvisibility-inlines-hidden "
        "-fdiagnostics-color=always "
        "-std=c++14 "
    ),
)

ninja.variable(
    "defines",
    (
        "-DBUILD_DATE=2024-04-12 "
        "-D_GLIBCXX_USE_CXX11_ABI=0 "
        "-DJUCE_APP_VERSION=1.0.0 "
        "-DJUCE_APP_VERSION_HEX=0x10000 "
        "-DJUCE_DSP_USE_SHARED_FFTW=1 "
        "-DJUCE_OPENGL3=1 "
        "-DJucePlugin_Build_AAX=0 "
        "-DJucePlugin_Build_AU=0 "
        "-DJucePlugin_Build_AUv3=0 "
        "-DJucePlugin_Build_LV2=1 "
        "-DJucePlugin_Build_RTAS=0 "
        "-DJucePlugin_Build_Standalone=1 "
        "-DJucePlugin_Build_VST=0 "
        "-DJucePlugin_Build_VST3=0 "
        '-D JucePlugin_LV2Category=\\"InstrumentPlugin\\" '
        '-D JucePlugin_LV2URI=\\"http://git.thev0id.io/dark/Quasar\\" '
        "-D JucePlugin_WantsLV2Presets=1 "
        "-D JucePlugin_WantsLV2State=1 "
        "-D JucePlugin_WantsLV2TimePos=1 "
        "-DJUCER_LINUX_MAKE_1D9049C2=1 "
        "-DJUCE_SHARED_CODE=1 "
        "-DJUCE_USE_XRANDR=0 "
        "-DLINUX=1 "
        "-DNDEBUG=1 "
        "-DNO_AUTH=1 "
    ),
)

pkgconf_libs = subprocess.check_output(
    ["pkg-config", "--libs", "alsa", "freetype2", "libcurl"]
)

ninja.variable(
    "ldflags",
    (
        "-L/usr/X11R6/lib/ "
        "-lrt "
        "-ldl "
        "-lpthread "
        "-lGL "
        "-lsecret-1 "
        "-lglib-2.0 "
        "-shared "
    )
    + pkgconf_libs.decode("utf-8"),
)

ninja.variable("cc", "gcc")
ninja.variable("cxx", "g++")
ninja.variable("ld", "g++")

ninja.rule("cxx", "$cxx $cflags $defines $iflags -c -o $out $in", description="CXX $in")
ninja.rule("cc", "$cc $cflags $defines $iflags -c -o $out $in", description="CC $in")
ninja.rule("ld", "$cxx $cflags $ldflags -o $out $in", description="LD $out")
ninja.rule("mv", "mv $in $out", "MV $in")
ninja.rule("genttl", "out/lv2_ttl_generator $in", "Generating TTL files")

ninja.build(
    "obj/lv2_ttl_generator.o",
    "cc",
    "build-scripts/lv2_ttl_generator.c",
    variables={
        "cflags": "",
        "defines": "",
        "iflags": "",
    },
)

ninja.build(
    "out/lv2_ttl_generator",
    "ld",
    "obj/lv2_ttl_generator.o",
    variables={
        "cflags": "",
        "ldflags": "-ldl",
    },
)


obj_files = []

for i in files:
    path = Path(i)
    output = str(Path("obj", "lv2").joinpath(path.with_suffix(".o")))

    match path.suffix:
        case ".cpp":
            ninja.build(output, "cxx", i)
            obj_files.append(output)


ninja.build("out/Quasar.lv2/Quasar.so", "ld", obj_files)
ninja.build("Quasar.ttl", "genttl", "out/Quasar.lv2/Quasar.so", implicit_outputs=["manifest.ttl", "presets.ttl"])
ninja.build("out/Quasar.lv2/Quasar.ttl", "mv", "Quasar.ttl");
ninja.build("out/Quasar.lv2/presets.ttl", "mv", "presets.ttl");
ninja.build("out/Quasar.lv2/manifest.ttl", "mv", "manifest.ttl");
