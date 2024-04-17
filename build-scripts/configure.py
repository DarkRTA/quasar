#!/usr/bin/python3
import sys

sys.dont_write_bytecode = True

import ninja_syntax
import subprocess
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(prog="configure")
parser.add_argument("format")
args = parser.parse_args()

if not args.format in ["lv2", "vst3", "vst2", "standalone"]:
    print("invalid plugin format")
    print('try, "lv2", "vst3", "vst2", or "standalone"')
    exit(1)

ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

files = [
    "src/unity_build/common.cpp",
    "src/unity_build/interface_editor_components.cpp",
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

match args.format:
    case "lv2":
        files.append("src/JuceLibraryCode/include_juce_audio_plugin_client_LV2.cpp")
    case "standalone":
        files.append(
            "src/JuceLibraryCode/include_juce_audio_plugin_client_Standalone.cpp"
        )
    case "vst3":
        files.append("src/JuceLibraryCode/include_juce_audio_plugin_client_VST3.cpp")
    case "vst2":
        files.append("src/JuceLibraryCode/include_juce_audio_plugin_client_VST2.cpp")

includes = [
    "-I/usr/include/freetype2",
    "-I/usr/include/libpng16",
    "-I/usr/include/harfbuzz",
    "-I/usr/include/glib-2.0",
    "-I/usr/lib/glib-2.0/include",
    "-I/usr/include/sysprof-6",
    "-Ithird_party/JUCE/modules/juce_audio_processors/format_types/VST3_SDK",
    "-Ithird_party/VST_SDK/VST2_SDK",
    "-Isrc/JuceLibraryCode",
    "-Ithird_party/JUCE/modules",
    "-Isrc/common",
    "-Isrc/common/wavetable",
    "-Isrc/interface/editor_components",
    "-Isrc/interface/editor_sections",
    "-Isrc/interface/look_and_feel",
    "-Isrc/interface/wavetable",
    "-Isrc/interface/wavetable/editors",
    "-Isrc/interface/wavetable/overlays",
    "-Isrc/plugin",
    "-Isrc/synthesis/synth_engine",
    "-Isrc/synthesis/effects",
    "-Isrc/synthesis/filters",
    "-Isrc/synthesis/framework",
    "-Isrc/synthesis/lookups",
    "-Isrc/synthesis/modulators",
    "-Isrc/synthesis/modules",
    "-Isrc/synthesis/producers",
    "-Isrc/synthesis/utilities",
    "-Ithird_party",
]

cflags = [
    "-pthread",
    "-fPIC",
    "-Ofast",
    "-ffast-math",
    "-ftree-vectorize",
    "-ftree-slp-vectorize",
    "-funroll-loops",
    "-fvisibility=hidden",
    "-fvisibility-inlines-hidden",
    "-g",
    "-fdiagnostics-color=always",
    "-std=c++14",
]

defines = [
    "-DBUILD_DATE=2024-04-12",
    "-D_GLIBCXX_USE_CXX11_ABI=0",
    "-DJUCE_APP_VERSION=1.0.0",
    "-DJUCE_APP_VERSION_HEX=0x10000",
    "-DJUCE_DSP_USE_SHARED_FFTW=1",
    "-DJUCE_OPENGL3=1",
    "-DJucePlugin_Build_AAX=0",
    "-DJucePlugin_Build_AU=0",
    "-DJucePlugin_Build_AUv3=0",
    "-DJucePlugin_Build_RTAS=0",
    '-DJucePlugin_LV2Category=\\"InstrumentPlugin\\"',
    '-DJucePlugin_LV2URI=\\"io:thev0id:quasar\\"',
    "-DJucePlugin_WantsLV2Presets=1",
    "-DJucePlugin_WantsLV2State=1",
    "-DJucePlugin_WantsLV2TimePos=1",
    "-DJUCER_LINUX_MAKE_1D9049C2=1",
    "-DJUCE_SHARED_CODE=1",
    "-DJUCE_USE_XRANDR=0",
    "-DLINUX=1",
    "-DNDEBUG=1",
    "-DNO_AUTH=1",
]

match args.format:
    case "lv2":
        defines.append("-DJucePlugin_Build_LV2=1");
        defines.append("-DJucePlugin_Build_VST3=0");
        defines.append("-DJucePlugin_Build_Standalone=0");
        defines.append("-DJucePlugin_Build_VST=0");
    case "vst3":
        defines.append("-DJucePlugin_Build_LV2=0");
        defines.append("-DJucePlugin_Build_VST3=1");
        defines.append("-DJucePlugin_Build_Standalone=0");
        defines.append("-DJucePlugin_Build_VST=0");
    case "vst2":
        defines.append("-DJucePlugin_Build_LV2=0");
        defines.append("-DJucePlugin_Build_VST3=0");
        defines.append("-DJucePlugin_Build_Standalone=0");
        defines.append("-DJucePlugin_Build_VST=1");
    case "standalone":
        defines.append("-DJucePlugin_Build_LV2=0");
        defines.append("-DJucePlugin_Build_VST3=0");
        defines.append("-DJucePlugin_Build_Standalone=1");
        defines.append("-DJucePlugin_Build_VST=0");

ninja.variable("iflags", " ".join(includes))

ninja.variable("cflags", " ".join(cflags))

ninja.variable("defines", " ".join(defines))

pkgconf_libs = subprocess.check_output(
    ["pkg-config", "--libs", "alsa", "freetype2", "libcurl"]
)

ldflags = [
    "-L/usr/X11R6/lib/",
    "-lrt",
    "-ldl",
    "-lpthread",
    "-lGL",
    "-lsecret-1",
    "-lglib-2.0",
    pkgconf_libs.decode("utf-8").rstrip("\n"),
]

if not args.format == "standalone":
    ldflags.append("-shared")

ninja.variable("ldflags", " ".join(ldflags))

ninja.variable("cc", "gcc")
ninja.variable("cxx", "g++")
ninja.variable("ld", "g++")

ninja.rule("cxx", "$cxx $cflags $defines $iflags -c -MD -MF $out.d -o $out $in", description="CXX $in", depfile="$out.d")
ninja.rule("cc", "$cc $cflags $defines $iflags -c -MD -MF $out.d -o $out $in", description="CC $in", depfile="$out.d")
ninja.rule("ld", "$cxx $cflags $ldflags -o $out $in", description="LD $out")
ninja.rule("mv", "mv $in $out", "MV $in")
ninja.rule("genttl", "out/lv2_ttl_generator $in", "Generating TTL files")

obj_files = []

for i in files:
    path = Path(i)
    output = str(Path("obj", args.format).joinpath(path.with_suffix(".o")))

    match path.suffix:
        case ".cpp":
            ninja.build(output, "cxx", i)
            obj_files.append(output)


match args.format:
    case "lv2":
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
        ninja.build("out/Quasar.lv2/Quasar.so", "ld", obj_files)
        ninja.build(
            "Quasar.ttl",
            "genttl",
            "out/Quasar.lv2/Quasar.so",
            implicit_outputs=["manifest.ttl", "presets.ttl"],
        )
        ninja.build("out/Quasar.lv2/Quasar.ttl", "mv", "Quasar.ttl")
        ninja.build("out/Quasar.lv2/presets.ttl", "mv", "presets.ttl")
        ninja.build("out/Quasar.lv2/manifest.ttl", "mv", "manifest.ttl")
    case "standalone":
        ninja.build("out/Quasar", "ld", obj_files)
    case "vst3":
        ninja.build("out/Quasar.vst3/Contents/x86_64-linux/Quasar.so", "ld", obj_files)
    case "vst2":
        ninja.build("out/Quasar.vst2.so", "ld", obj_files)
