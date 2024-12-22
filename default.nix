{ pkgs ? import <nixpkgs> {}}: pkgs.stdenv.mkDerivation {
    pname = "quasar";
    version = "1.0.6";

    src = ./.;

    configurePhase = ''
        python build-scripts/configure.py standalone
        mv build.ninja standalone.ninja
        python build-scripts/configure.py lv2
        mv build.ninja lv2.ninja
    '';

    buildPhase = ''
        ninja -f lv2.ninja
        ninja -f standalone.ninja
    '';

    installPhase = ''
        mkdir -p $out/bin
        mkdir -p $out/lib/lv2

        cp out/Quasar $out/bin
        cp out/Quasar.lv2 $out/lib/lv2
    '';

    buildInputs = with pkgs; [
        ninja
        python3
        pkg-config
        freetype
        alsa-lib
        libGL
        xorg.libX11
        xorg.libXinerama
        xorg.libXext
        xorg.libXcursor
        jack1
    ];
}
