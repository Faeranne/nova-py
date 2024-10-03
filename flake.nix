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
      };
    in pkgs.callPackages ./pkgs {inherit self inputs;});
    devShells = forAllSystems (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      default = pkgs.mkShell {
        shellHook = ''
          zsh
          exit
        '';
        packages = [
          (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
            hidapi
            numpy
            pillow
          ]))
        ];
      };
    });
  };
}
