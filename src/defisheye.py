import cv2
from numpy import arange, sqrt, arctan, sin, tan, meshgrid, pi
from numpy import ndarray, hypot

class Defisheye:
    """
    Defisheye

    fov: fisheye field of view (aperture) in degrees
    pfov: perspective field of view (aperture) in degrees
    xcenter: x center of fisheye area
    ycenter: y center of fisheye area
    radius: radius of fisheye area
    angle: image rotation in degrees clockwise
    dtype: linear, equalarea, orthographic, stereographic
    format: circular, fullframe
    """

    def __init__(self, infile, **kwargs):
        vkwargs = {"fov": 180,
                   "pfov": 120,
                   "xcenter": None,
                   "ycenter": None,
                   "radius": None,
                   "angle": 0,
                   "dtype": "equalarea",
                   "format": "fullframe"
                   }
        self._start_att(vkwargs, kwargs)

        if type(infile) == str:
            _image = cv2.imread(infile)
        elif type(infile) == ndarray:
            _image = infile
        else:
            raise Exception("Image format not recognized")

        width = _image.shape[1]
        height = _image.shape[0]
        xcenter = width // 2
        ycenter = height // 2

        dim = min(width, height)
        x0 = xcenter - dim // 2
        xf = xcenter + dim // 2
        y0 = ycenter - dim // 2
        yf = ycenter + dim // 2

        self._image = _image[y0:yf, x0:xf, :]

        self._width = self._image.shape[1]
        self._height = self._image.shape[0]

        if self._xcenter is None:
            self._xcenter = (self._width - 1) // 2

        if self._ycenter is None:
            self._ycenter = (self._height - 1) // 2

    def _map(self, i, j, ofocinv, dim):

        xd = i - self._xcenter
        yd = j - self._ycenter

        rd = hypot(xd, yd)
        phiang = arctan(ofocinv * rd)

        if self._dtype == "linear":
            ifoc = dim * 180 / (self._fov * pi)
            rr = ifoc * phiang
            # rr = "rr={}*phiang;".format(ifoc)

        elif self._dtype == "equalarea":
            ifoc = dim / (2.0 * sin(self._fov * pi / 720))
            rr = ifoc * sin(phiang / 2)
            # rr = "rr={}*sin(phiang/2);".format(ifoc)

        elif self._dtype == "orthographic":
            ifoc = dim / (2.0 * sin(self._fov * pi / 360))
            rr = ifoc * sin(phiang)
            # rr="rr={}*sin(phiang);".format(ifoc)

        elif self._dtype == "stereographic":
            ifoc = dim / (2.0 * tan(self._fov * pi / 720))
            rr = ifoc * tan(phiang / 2)

        rdmask = rd != 0
        xs = xd.copy()
        ys = yd.copy()

        xs[rdmask] = (rr[rdmask] / rd[rdmask]) * xd[rdmask] + self._xcenter
        ys[rdmask] = (rr[rdmask] / rd[rdmask]) * yd[rdmask] + self._ycenter

        xs[~rdmask] = 0
        ys[~rdmask] = 0

        xs = xs.astype(int)
        ys = ys.astype(int)
        return xs, ys

    def convert(self, outfile=None):
        if self._format == "circular":
            dim = min(self._width, self._height)
        elif self._format == "fullframe":
            dim = sqrt(self._width ** 2.0 + self._height ** 2.0)

        if self._radius is not None:
            dim = 2 * self._radius

        # compute output (perspective) focal length and its inverse from ofov
        # phi=fov/2; r=N/2
        # r/f=tan(phi);
        # f=r/tan(phi);
        # f= (N/2)/tan((fov/2)*(pi/180)) = N/(2*tan(fov*pi/360))

        ofoc = dim / (2 * tan(self._pfov * pi / 360))
        ofocinv = 1.0 / ofoc

        i = arange(self._width)
        j = arange(self._height)
        i, j = meshgrid(i, j)

        xs, ys, = self._map(i, j, ofocinv, dim)
        img = self._image.copy()

        img[i, j, :] = self._image[xs, ys, :]
        if outfile is not None:
            cv2.imwrite(outfile, img)
        return img

    def _start_att(self, vkwargs, kwargs):
        """
        Starting atributes
        """
        pin = []

        for key, value in kwargs.items():
            if key not in vkwargs:
                raise NameError("Invalid key {}".format(key))
            else:
                pin.append(key)
                setattr(self, "_{}".format(key), value)

        pin = set(pin)
        rkeys = set(vkwargs.keys()) - pin
        for key in rkeys:
            setattr(self, "_{}".format(key), vkwargs[key])

dtype = 'linear'
format = 'fullframe'
fov = 
pfov = 120
x_center = -1
y_center = -1
radius = None
angle = 0


img = "/mlcv1/WorkingSpace/Personal/tuongbck/AIC2024/CoDETR/data/splited/train/images/camera10_A_98.png"
img_out = "test.png"

obj = Defisheye(img, dtype=dtype, format=format, fov=fov, pfov=pfov, radius=radius)

# To save image locally 
obj.convert(outfile=img_out)


