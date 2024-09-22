with import <nixpkgs> {};

pkgs.mkShell {
    buildInputs = with pkgs; [
        python312Packages.numpy
        python312Packages.nltk
        python312
    ];
}
