// Generated by inkscape None + inkscape-paths2openscad 0.27
// Sat Sep 26 10:30:30 2020 from "inkscape.svg"

// Module names are of the form poly_<inkscape-path-id>().  As a result,
// you can associate a polygon in this OpenSCAD program with the corresponding
// SVG element in the Inkscape document by looking for the XML element with
// the attribute id="inkscape-path-id".

// fudge value is used to ensure that subtracted solids are a tad taller
// in the z dimension than the polygon being subtracted from.  This helps
// keep the resulting .stl file manifold.
fudge = 0.1;
user_unit_scale_x = 1.0;
user_unit_scale_y = 1.0;
custom_scale_x = 1;
custom_scale_y = 1;
zsize = 50;
line_fn = 16;
min_line_width = 1.0;
line_width_scale = 1.0;
function min_line_mm(w) = max(min_line_width, w * line_width_scale) * 1;


path955_0_center = [0.068998,0.000000];
path955_0_points = [[-0.284593,3.915664],[-0.459532,3.628714],[-0.459848,3.400684],[-0.460165,3.172644],[-0.286974,3.051344],[-0.268334,3.037116],[-0.247942,3.019406],[-0.202564,2.974524],[-0.152163,2.918668],[-0.098063,2.853809],[-0.041586,2.781916],[0.015945,2.704960],[0.073207,2.624913],[0.128877,2.543744],[0.181631,2.463423],[0.230147,2.385922],[0.273102,2.313211],[0.309173,2.247261],[0.337037,2.190041],[0.355370,2.143523],[0.360549,2.124893],[0.362850,2.109677],[0.362107,2.098122],[0.358154,2.090474],[0.347634,2.085646],[0.324168,2.078895],[0.241138,2.060112],[0.114551,2.035106],[-0.050105,2.004857],[-0.471677,1.932553],[-0.979681,1.851044],[-1.521508,1.765611],[-2.035173,1.682634],[-2.462713,1.611596],[-2.746165,1.561984],[-2.851195,1.543424],[-2.971384,1.523907],[-3.240369,1.484340],[-3.519372,1.447946],[-3.774646,1.419394],[-3.890041,1.406688],[-4.002213,1.392020],[-4.108384,1.375910],[-4.205775,1.358880],[-4.291608,1.341451],[-4.363105,1.324144],[-4.417489,1.307481],[-4.437394,1.299554],[-4.451980,1.291984],[-4.566498,1.220584],[-4.473188,1.070014],[-4.379878,0.919434],[-4.057030,0.877134],[-3.734182,0.834834],[-3.875175,0.718634],[-3.903499,0.693654],[-3.929922,0.667179],[-3.953866,0.640014],[-3.974753,0.612967],[-3.992005,0.586844],[-4.005044,0.562451],[-4.013291,0.540595],[-4.016169,0.522084],[-4.018847,0.503262],[-4.026523,0.480528],[-4.038659,0.454746],[-4.054716,0.426786],[-4.074157,0.397514],[-4.096443,0.367798],[-4.121036,0.338505],[-4.147398,0.310504],[-4.278627,0.179284],[-4.251377,0.041394],[-4.224127,-0.096500],[-3.887312,-0.082230],[-3.819168,-0.078345],[-3.742577,-0.072192],[-3.568501,-0.053789],[-3.373984,-0.028436],[-3.167926,0.002453],[-2.959226,0.037463],[-2.756784,0.075181],[-2.569501,0.114193],[-2.406275,0.153084],[-2.193386,0.208184],[-2.004108,0.484414],[-1.966086,0.543061],[-1.930615,0.603876],[-1.898471,0.665092],[-1.870430,0.724942],[-1.847270,0.781659],[-1.829765,0.833474],[-1.818693,0.878622],[-1.815812,0.898142],[-1.814830,0.915334],[-1.814830,1.070024],[-2.301664,1.016924],[-2.769844,0.963375],[-3.211830,0.909234],[-3.635164,0.854634],[-3.574504,0.919534],[-3.564685,0.926777],[-3.548002,0.935058],[-3.495608,0.954347],[-3.420445,0.976634],[-3.325641,1.001156],[-3.214319,1.027147],[-3.089606,1.053842],[-2.954626,1.080476],[-2.812504,1.106284],[-2.130654,1.227912],[-1.476168,1.349234],[-1.166761,1.406537],[-0.793731,1.473047],[-0.404047,1.540516],[-0.044680,1.600694],[0.751807,1.731074],[0.825767,1.657074],[0.899727,1.583074],[0.756289,0.930294],[0.612851,0.277513],[0.357490,0.027853],[0.285766,-0.037323],[0.179367,-0.127169],[0.043445,-0.237640],[-0.116849,-0.364695],[-0.296362,-0.504290],[-0.489941,-0.652382],[-0.692434,-0.804928],[-0.898689,-0.957886],[-1.899507,-1.693959],[-1.899507,-1.789579],[-1.898151,-1.800609],[-1.894171,-1.813862],[-1.878879,-1.846328],[-1.854702,-1.885565],[-1.822712,-1.930160],[-1.783983,-1.978701],[-1.739586,-2.029776],[-1.690594,-2.081972],[-1.638079,-2.133876],[-1.609734,-2.162133],[-1.578819,-2.195337],[-1.510497,-2.274917],[-1.435539,-2.369285],[-1.356374,-2.475109],[-1.275430,-2.589056],[-1.195133,-2.707795],[-1.117912,-2.827992],[-1.046195,-2.946316],[-0.715738,-3.510082],[-0.397456,-3.759565],[-0.258376,-3.865631],[-0.130805,-3.956695],[-0.071182,-3.996685],[-0.014252,-4.033023],[0.040044,-4.065744],[0.091769,-4.094879],[0.140983,-4.120463],[0.187747,-4.142528],[0.232123,-4.161108],[0.274172,-4.176236],[0.313954,-4.187944],[0.351531,-4.196266],[0.386964,-4.201235],[0.420314,-4.202883],[0.453802,-4.199890],[0.490042,-4.191040],[0.528876,-4.176525],[0.570148,-4.156540],[0.613700,-4.131278],[0.659375,-4.100932],[0.707017,-4.065696],[0.756469,-4.025762],[0.807573,-3.981326],[0.860172,-3.932579],[0.914109,-3.879716],[0.969227,-3.822929],[1.025370,-3.762413],[1.082380,-3.698361],[1.140101,-3.630965],[1.198374,-3.560420],[1.257044,-3.486919],[1.315952,-3.410655],[1.433859,-3.250613],[1.550838,-3.081841],[1.665632,-2.905887],[1.721818,-2.815700],[1.776987,-2.724297],[1.830981,-2.631873],[1.883644,-2.538621],[1.934820,-2.444733],[1.984350,-2.350404],[2.032077,-2.255826],[2.077846,-2.161193],[2.320654,-1.647775],[2.731826,-1.380162],[2.924863,-1.252529],[3.112760,-1.124112],[3.297798,-0.993210],[3.482260,-0.858123],[3.668428,-0.717151],[3.858585,-0.568595],[4.055012,-0.410755],[4.259993,-0.241929],[4.704493,0.128214],[4.703193,0.439164],[4.701893,0.750114],[4.378924,1.342784],[4.055954,1.935454],[3.786148,1.940454],[3.516342,1.945453],[3.136764,2.317973],[2.757186,2.690503],[2.757186,2.875773],[2.757186,3.061043],[2.442255,3.337553],[2.127323,3.614064],[1.584540,3.860174],[1.041757,4.106284],[0.466060,4.154584],[-0.109637,4.202883],[-0.284576,3.915933],[-0.284593,3.915664]];
path955_1_center = [-3.344334,2.063084];
path955_1_points = [[-3.105436,2.521554],[-3.114287,2.516276],[-3.130499,2.510568],[-3.183374,2.498075],[-3.260793,2.484507],[-3.359492,2.470299],[-3.476203,2.455882],[-3.607660,2.441690],[-3.750597,2.428156],[-3.901748,2.415714],[-4.649233,2.358714],[-4.676863,2.214264],[-4.704493,2.069814],[-4.423833,1.814584],[-4.143174,1.559354],[-3.736166,1.556354],[-3.647161,1.557596],[-3.550121,1.561871],[-3.448171,1.568871],[-3.344437,1.578291],[-3.242044,1.589825],[-3.144118,1.603168],[-3.053783,1.618012],[-2.974166,1.634054],[-2.811276,1.669185],[-2.630187,1.705566],[-2.452964,1.738898],[-2.301674,1.764884],[-1.984174,1.815484],[-1.984174,1.922044],[-1.985622,1.934301],[-1.989872,1.948970],[-2.006204,1.984767],[-2.032024,2.027889],[-2.066188,2.076787],[-2.107549,2.129915],[-2.154964,2.185725],[-2.207286,2.242670],[-2.263371,2.299204],[-2.542568,2.569814],[-2.799593,2.569814],[-2.852221,2.568816],[-2.903244,2.565957],[-2.951408,2.561439],[-2.995460,2.555464],[-3.034144,2.548231],[-3.066205,2.539945],[-3.090391,2.530805],[-3.105445,2.521014],[-3.105436,2.521554]];
module poly_path955(h, w, s, res=line_fn)
{
  scale([custom_scale_x, -custom_scale_y, 1]) union()
  {
    translate (path955_0_center) linear_extrude(height=h, convexity=10, scale=0.01*s)
      translate (-path955_0_center) polygon(path955_0_points);
    translate (path955_1_center) linear_extrude(height=h, convexity=10, scale=0.01*s)
      translate (-path955_1_center) polygon(path955_1_points);
  }
}

module immobilize(h)
{
  difference()
  {
    union()
    {
      translate ([0,0,0]) poly_path955(h, min_line_mm(0.999998), 100.0);
    }
    union()
    {
    }
  }
}

immobilize(zsize);