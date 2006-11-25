from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext
setup(
  name = "solidfuel",
  description = "Multimedia framework for Python",
  author = "Nat Budin",
  author_email = "natbudin@gmail.com",
  packages = ['Graphics', 'Logic'],
  ext_modules=[
    Extension("Graphics.Node", ["Graphics/Node.pyx"], libraries = [])
    ],
  cmdclass = {'build_ext': build_ext}
)