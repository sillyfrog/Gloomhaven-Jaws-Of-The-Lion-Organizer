# Condition Token Images

These images and OpenSCAD templates were made as follows.

- The tokens were initially scanned in on a flatbed scanner, then opened in [GIMP](https://www.gimp.org/).
- I then cut out each token, and cleaned it up:
  - Select the white portion(s) of the token
  - Grow the selection by 1 or 2 pixels to smooth out the edges and any "flecks" that were missed
  - I then fill the selection with Black
  - Next invert the selection, and delete everything else
- I then export the image as a PNG
- In [Inkscape](https://inkscape.org/) I then import the PNG and ensure it's at the right scale (for my GIMP exported it as 72 DPI, but the scan was 300DPI). If it's not right, scale the image - for me, that was scaling each image to 24% (72/300).
- Next select _Path_ > _Trace Bitmap..._
- Here I used _Brightness cutoff_ with the following settings:
  - Brightness threshold: 0.45
  - Speckles: 0
  - Smooth corners: 0.2 - 0.6 (depending on the image and how it looked)
  - Optimize: 2.0
- The click _OK_ to create a path object for each of the PNG's.
- Once there is a path for each of the PNGs, I then ran my fork of [Paths to OpenSCAD](https://github.com/sillyfrog/inkscape-paths2openscad) (you will need to ensure this is installed, my fork addresses a number of issues, and has been updated for v1)
- You can then generate each of the OpesSCAD files as per what I have included in this directory.
