# See COPYRIGHT file at the top of the source tree.

try:
    # verify_metrics does not formally use lsstimport, but we still
    # attempt to import it for compatiblity with the lsst Stack.
    import lsstimport  # noqa: F401
except ImportError:
    pass
import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)
