.. _verify-metrics-package:

##############
verify_metrics
##############

``verify_metrics`` provides centralized metric and specification definitions for the LSST Science Pipelines Verification Framework.
The :ref:`lsst.verify <lsst.verify>` module uses these metrics and specifications by default.

For background, see the SQR-017_ (design) and SQR-019_ (demo) technotes.

Project info
============

Repository
   https://github.com/lsst/verify_metrics

JIRA component
   `Verification <https://jira.lsstcorp.org/browse/DM/component/14170>`_.

Contributing
============

Basics
------

- This repository should only contain metric and specification YAML files.
  Don't add Python code; instead consider extending the `lsst.verify` API in the :ref:`verify <verify-package>` package.

- Follow `LSST Data Management's workflow <https://developer.lsst.io/processes/workflow.html>`_ for contributions.

Registering metrics
-------------------

**Metrics** are *measureable things*.
They can be astronomy concepts (an astrometric RMS) or computational (a task's timing or memory usage).

Metrics that are measured by packages are **registered** here in ``verify_metrics`` by adding or extending a metric definition YAML file in the ``metrics/`` directory.
See `metrics/README.rst <https://github.com/lsst/verify_metrics/blob/master/metrics/README.rst>`_ for more information.

Registering specifications
--------------------------

**Specifications** are tests of metric measurements.
A specification might say that a metric measurement should be less than a certain value if that measurement was made under a certain set of conditions (*provenance*).
Whenever metrics are measured, DM's SQUASH harness tests those measurements against specifications.
Depending on the pass/fail outcome, subscribers can receive notifications (alerts).

New specifications are **registered** here in ``verify_metrics`` by adding or extending a specification definition YAML file in the ``specs/`` directory.
See `specs/README.rst <https://github.com/lsst/verify_metrics/blob/master/specs/README.rst>`_ for more information.

.. _SQR-017: https://sqr-017.lsst.io
.. _SQR-019: https://sqr-019.lsst.io
