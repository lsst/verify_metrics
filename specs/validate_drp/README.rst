###################
specs/validate_drp/
###################

Specifications for `validate_drp`_ metrics are defined in this directory as YAML documents.

Specification files prefixed with ``LPM-17-`` reflect **official** requirements, baselined in `LPM-17`_, the *Science Requirements Document*.
One ``LPM-17-`` file is provided per metric family.
Developers should not modify these files, except to support `LPM-17`_.

Developers can add ad-hoc `validate_drp`_ specifications by committing additional YAML files to this directory, or by adding to these:

- ``cfht_gri.yaml``: specifications against the https://github.com/lsst/validation_data_cfht.git dataset in g, r, and i bands.

.. _validate_drp: https://github.com/lsst/validate_drp
.. _LPM-17: http://ls.st/lpm-17
