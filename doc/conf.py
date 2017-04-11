#!/usr/bin/env python
"""Sphinx configurations to build package documentation."""

from documenteer.sphinxconfig.stackconf import build_package_configs

import lsst.verify.metrics


_g = globals()
_g.update(build_package_configs(
    project_name='verify_metrics',
    copyright='2017 Association of Universities for '
              'Research in Astronomy, Inc.',
    version=lsst.verify.metrics.__version__,
    doxygen_xml_dirname=None))

intersphinx_mapping['astropy'] = ('http://docs.astropy.org/en/stable', None)

# DEBUG only
automodsumm_writereprocessed = False
