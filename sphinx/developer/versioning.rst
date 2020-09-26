=================
Versioning Ren'Py
=================

This document explains how Ren'Py is versioned, and what one can
expect when different components of the version change. This manual
documents practices begun with Ren'Py 6.13 - a more ad-hoc versioning
scheme was used for previous releases.

A Ren'Py version, like 6.13.0.1520, consists of four numbers. Each
number has its own meaning. In order, they are:

Major Version
=============

The first component of the version is the major version. There are two
cases where the major version may change:

* At the culmination of a series of major changes and improvements to
  Ren'Py, to the point where the style of programming in Ren'Py is
  expected to have changed.

* After the removal of backwards compatibility between this Ren'Py
  version and previous versions. In this case, it may take several
  minor versions before backwards compatibility is restored.

Minor Version
=============

The second component of the version is the minor version. A full
release of Ren'Py is determined by the combination of the major and
minor version numbers. A full release of Ren'Py adds features or makes
major changes to Ren'Py's internals.

A full release of Ren'Py is given its own name and web page. It's also
given its own version control branch, to allow bugfix releases to be
made.

Full releases of Ren'Py may require changes to game scripts, but should be
capable of running older games that use the ``script_version`` mechanism
to indicate the version of Ren'Py they are written for.

Full releases of Ren'Py may break savegame compatibility, although we have
and will continue to attempt to maintain savegame compatibility when
feasible.

Bugfix Version
==============

The third component of the version is the bugfix version. This number
is zero for a full release of Ren'Py, and is incremented by 1 when a
bugfix release is made.

A bugfix release should be 100% compatible with the corresponding full
release of Ren'Py, except when the full release is clearly broken. It
should avoid adding features or making large changes to the internals
or dependencies of Ren'Py.

Revision
========

The fourth component of the version is the revision. This is the
revision number that a release or prerelease is made from, and hence
can be used to distinguish prereleases.

Ren'Py makes no guarantee about the forward-compatibility of
prereleases - functionality may be removed or changed between a
prerelease and full or bugfix release.

