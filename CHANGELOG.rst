Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.4
---
2021-02-09

- Allow regex wildcard match.

0.3
---
2021-02-08

- Allow custom identifier of the ``The Great Suspender`` plugin.

0.2
---
2021-02-05

- Split body in functions (preparing for the API).

0.1
---
2021-02-05

- Initial version.
