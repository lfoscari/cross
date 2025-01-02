with import <nixpkgs> {};

pkgs.mkShell {
    buildInputs = with pkgs; [
        python311Packages.numpy
        python311Packages.gensim
        python311
    ];

    shellHook = ''
        export GENSIM_DATA_DIR="$(pwd)/words"
    '';
}
