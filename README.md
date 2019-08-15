# FEIGN: a package to estimate the geometric efficiency of  gamma spectroscopy setups in spent nuclear fuel measurements

``feign`` is a python package for estimating the geometric efficiency in passive gamma spectroscopy measurments of spent nuclear fuel assemblies. It implements a 2D point-kernel method without build-up factors (ie. an "uncollided F5 tally" for MCNP users). The name feign implies that the program pretends to be a transport code, however it is rather a ray-tracing code. 

It is intended for nuclear safeguards specialists and nuclear engineers who want to get a quick estimate on the geometric efficiency in their passive gamma setup. It might be also useful to people working with passive gamma emission tomography of spent fuel.

The ``feign`` API allows the user to define the geometry of a rectangular fuel assembly, which is built of pins (nested annular material regions). The user also defines the composition of materials present in the simulation, the detector points where the efficiency needs to be evaluated, and optionally collimators and absorber elements. 

As a package, ``feign`` provides

- basic 2D geometry classes (Point, Segment, Circle, Rectangle)
- classes to describe materials, fuel pins, rectangular fuel assemblies, detectors and absorbers
- methods to perform the ray-tracing and estimating the geometric efficiency.

Installation
------------

``feign`` can be installed by downloading the zipball from github.

```bash
   pip install https://github.com/ezsolti/feign/zipball/master
```

Installation was successfully tested on Linux and Windows.

Uninstall it with the command

```bash
   pip uninstall feign
```

Dependencies

- NumPy
- Matplotlib

Data 

Besides the installation you will need mass attenuation coefficients. You can download some files for testing from the [data folder](https://github.com/ezsolti/feign/tree/master/data). Further information on how to obtain your own data is an the [documentation site](https://ezsolti.github.io/feign/installation.html). When you have gathered your own datafiles, you can link them to Material() objects with the following method:

```python
   uo2=Material('1')
   uo2.set_path(('/yourpath/UO2.dat',1))
```

`set_path` expects a tuple, the first element is the path to the data file, and the second element clarifies which column should be used from the file (since you might have several columns, for example attenuaton with or without coherent scattering).

Getting started
---------------

The basic functionality and the theoretical background is summarized at the [documentation site](https://ezsolti.github.io/feign/quickstart.html)

Examples
--------

Several examples can be found in the [examples folder](https://github.com/ezsolti/feign/tree/master/examples) or at the [documentation site](https://ezsolti.github.io/feign/examples.html)

Docs
----

API documentation, examples and theoretical background is covered at [ezsolti.github.io/feign](https://ezsolti.github.io/feign/examples.html)

Contributing, bugs, suggestions
-------------------------------

Any reported bug or suggestion is appreciated, please [open a new issue](https://github.com/ezsolti/feign/issues/new). If you would like to contribute, do not hesitate to do so, just include tests.

Tests
-----

Several tests can be found in the [tests folder](https://github.com/ezsolti/feign/tree/master/tests), run them with

```bash
python3 -m unittest discover tests/
```

Licence
-------

This work is licensed under the MIT License (see [LICENSE](https://github.com/ezsolti/feign/blob/master/LICENSE))

