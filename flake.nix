{
  inputs = {
    nixpkgs.url = "nixpkgs";
  };

  outputs = {self, nixpkgs}@inputs :let
    forAllSystems = nixpkgs.lib.genAttrs [
      "x86_64-linux"
      "aarch64-linux"
    ];
  in {
    packages = forAllSystems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
        ];
      };
    in pkgs.callPackages ./pkgs {inherit self inputs;});
    devShells = forAllSystems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
        ];
      };
    in {
      default = pkgs.mkShell {
        shellHook = ''
          zsh
          exit
        '';
        packages = (with pkgs; [
          python3
        ]) ++ (with pkgs.python3Packages; [
          hidapi
          numpy
          pillow
        ]);
      };
    });
  };
}
