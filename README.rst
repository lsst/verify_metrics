###################
lsst.verify.metrics
###################

**Centralized metric and specification definitions for the LSST Science Pipeline Verification Framework.**

For background on the ``lsst.verify`` framework, see the SQR-017_ (design) and SQR-019_ (demo) technotes.

Installation
============

This ``verify_metrics`` package is a dependency of the `verify`_ package, and available through the ``lsst_distrib`` top-level package.
See https://pipelines.lsst.io for details on installing ``lsst_distrib``.

Registering metrics
===================

**Metrics** are *measureable things*.
They can be astronomy concepts (an astrometric RMS), or computational (a task's timing or memory usage).

Metrics that are measured by packages are **registered** here in ``verify_metrics`` by adding or extending a metric definition YAML file in the ``metrics/`` directory.
See `metrics/README.rst <./metrics/README.rst>`_ for more information.

Registering specifications
==========================

**Specifications** are tests of metric measurements.
A specification might say that a metric measurement should be less than a certain value if that measurement was made under a certain set of conditions (*provenance*).
Whenever metrics are measured, DM's SQUASH harness tests those measurements against specifications.
Depending on the pass/fail outcome, subscribers can receive notifications (alerts).

New specifications are **registered** here in ``verify_metrics`` by adding or extending a specification definition YAML file in the ``specs/`` directory.
See `specs/README.rst <./specs/README.rst>`_ for more information.

Getting help and reporting bugs
===============================

If you're not part of the LSST Project, please post your question or issue in `our support forum <https://community.lsst.org/c/support>`_.
It's easy to create a Community forum account.

*We don't use GitHub Issues.*

If you're part of the LSST Project, please create a `JIRA ticket <https://jira.lsstcorp.org/>`_.
Use the `Verification component`_ component and `verify_metrics label`_.

Contributions
=============

- This repository should only contain metric and specification YAML files.
  Don't add Python code; instead consider extending the ``lsst.verify`` API in the `verify`_ package.

- Follow `LSST Data Management's workflow <https://developer.lsst.io/processes/workflow.html>`_ for contributions.

License
=======

This product includes software developed by the `LSST Project <http://www.lsst.org/>`_.
See the `COPYRIGHT <./COPYRIGHT>`_ file.

This product's source code is licensed under the terms of GPLv3 (see `LICENSE <./LICENSE>`_), and all documentation content is licensed under the `Creative Commons Attribution 4.0 International (CC BY 4.0) <https://creativecommons.org/licenses/by/4.0/>`_ license.

.. _SQR-017: https://sqr-017.lsst.io
.. _SQR-019: https://sqr-019.lsst.io
.. _verify: https://github.com/lsst/verify
.. _Verification Component: https://jira.lsstcorp.org/browse/DM/component/14170
.. _`verify_metrics label`: https://jira.lsstcorp.org/issues/?jql=labels%20%3D%20verify_metrics
