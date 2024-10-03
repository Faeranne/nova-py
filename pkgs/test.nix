{python3, writeShellScriptBin, ...}: let
  python = python3.withPackages (ppkgs: with ppkgs; [
    hidapi
    numpy
    pillow
  ]);
in writeShellScriptBin "test" ''
  ${python}/bin/python ${../test.py}
''
