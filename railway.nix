{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312Full
    python312Packages.pip

    # WeasyPrint dependencies
    cairo
    gdk-pixbuf
    pango
    libffi
    glib
    gobject-introspection
    harfbuzz
  ];
}
