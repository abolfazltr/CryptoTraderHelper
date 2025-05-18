{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
    pkgs.python310Packages.pandas
    pkgs.python310Packages.setuptools
  ];
}