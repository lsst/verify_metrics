#!/usr/bin/env python
"""Sphinx configurations to build package documentation."""

from documenteer.sphinxconfig.stackconf import build_package_configs

import lsst.validate.metrics


_g = globals()
_g.update(build_package_configs(
    project_name='validate_metrics',
    copyright='2017 Association of Universities for '
              'Research in Astronomy, Inc.',
    version=lsst.validate.metrics.__version__,
    doxygen_xml_dirname=None))

intersphinx_mapping['astropy'] = ('http://docs.astropy.org/en/stable', None)
intersphinx_mapping['validate_base'] = ('https://validate-base.lsst.io', None)

# DEBUG only
automodsumm_writereprocessed = False
