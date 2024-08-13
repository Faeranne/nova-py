{lib, self, inputs, pkgs}:let
  callPackage = lib.callPackageWith (pkgs // packages // {inherit self inputs;});
  packages = {
    default = pkgs.python3Packages.callPackage ./test.nix {};
  };
in packages
