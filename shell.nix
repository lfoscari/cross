with import <nixpkgs> {};

pkgs.mkShell {
    buildInputs = with pkgs; [
        python3Packages.numpy
        python3
    ];
}
