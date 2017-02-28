#####################
lsst.validate.metrics
#####################

**Centralized metric and specification definitions for the lsst.validate framework.**

For background on the ``lsst.validate`` framework, see SQR-017_.

Registering metrics
===================

**Metrics** are *measureable things*.
They can be astronomy concepts (an astrometric RMS), or computational (a task's timing or memory usage).

Metrics that are measured by packages are **registered** here in ``validate_metrics`` by adding or extending a metric definition YAML file in the ``metrics/`` directory.
See `metrics/README.rst <./metrics/README.rst>`_ for more information.

Registering specifications
==========================

**Specifications** are tests of metric measurements.
A specification might say that a metric measurement should be less than a certain value if that measurement was made under a certain set of conditions (*provenance*).
Whenever metrics are measured, DM's SQUASH harness tests those measurements against specifications.
Depending on the pass/fail outcome, subscribers can receive notifications (alerts).

New specifications are **registered** here in ``validate_metrics`` by adding or extending a specification definition YAML file in the ``specs/`` directory.
See `specs/README.rst <./specs/README.rst>`_ for more information.

Getting help and reporting bugs
===============================

If you're not part of the LSST Project, please post your question or issue in `our support forum <https://community.lsst.org/c/support>`_.
It's easy to create a Community forum account.

*We don't use GitHub Issues.*

If you're part of the LSST Project, please create a `JIRA ticket <https://jira.lsstcorp.org/>`_.
Use the `Validation <https://jira.lsstcorp.org/browse/DM/component/13205>`_ component.

Contributing code
=================

Follow `LSST Data Management's workflow <https://developer.lsst.io/processes/workflow.html>`_ for code contributions.

License
=======

This product includes software developed by the `LSST Project <http://www.lsst.org/>`_.
See the `COPYRIGHT <./COPYRIGHT>`_ file.

This product's source code is licensed under the terms of GPLv3 (see `LICENSE <./LICENSE>`_), and all documentation content is licensed under the `Creative Commons Attribution 4.0 International (CC BY 4.0) <https://creativecommons.org/licenses/by/4.0/>`_ license.

.. _SQR-017: https://sqr-017.lsst.io
