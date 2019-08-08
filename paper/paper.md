---
title: 'feign: a Python package to estimate geometric efficiency in passive gamma spectroscopy measurements of nuclear fuel'
tags:
  - Python
  - nuclear safeguards
  - gamma spectroscopy
authors:
 - name: Zsolt Elter
   orcid: 0000-0003-2339-4340
   affiliation: 1
affiliations:
 - name: Uppsala University, Division of Applied Nuclear Physics
   index: 1
date: 10 August 2019
bibliography: paper.bib
---

# Summary

The operator declarations of spent nuclear fuel assemblies have to be verified for safety and nuclear safeguards purposes before being placed in copper canisters which are lowered into the geological storage. Verifying parameters such as burnup (ie. the time the fuel spent in the reactor), cooling time (ie. the time the fuel spent outside the reactor after operation), initial enrichment (ie. the amount of fissile material in the fuel before operation) and integrity (whether pins are missing from the assembly) is an important task of nuclear safeguards since a discrepancy in the declared values may indicate unathorized activities at the facility handling the fuel. Ideally, the verification should be done with non-destructive assay system. Since the characteristics of spent nuclear fuel strongy affect the gamma radiation emitted from the fuel, passive gamma spectroscopy provides a robust and relatively simple method to analyze spent fuel [@Jansson thesis]. Also, lately passive gamma tomography is a widely accepted tool to characterize spent fuel assemblies [@PGET]. In both cases, gamma radiation is measured around the fuel assembly from a distance with a collimated detector which has spectroscopic capabilities. The detector efficiency, the ratio between number of detected particles and number of particles emitted by the source, of such systems is of great interest. This quantity is often estimated with Monte Carlo simulations, for example by using the MCNP code [@mcnp]. Nevertheless, analoge Monte Carlo simulation of spent fuel passive gamma measurements is extremely time consuming, since the source, the fuel assembly is made of high density uranium-dioxide, is located far from the detector (often several meters) and is usually viewed through collimators with narrow slits, thus only a tiny fraction of source particles reach the detector. As a solution, the simulation is often split into two parts: first, a point-detector (F5 in the MCNP jargon) tally is used to estimate the energy resolved gamma photon flux at the location of the detector, and then a subsequent pulse-height (F8 in the MCNP jargon) tally computation is done to estimate the detector response. The F5 tally provides a semi-deterministic solution of the transport problem. The history of the gamma ray is tracked with Monte Carlo, however at each interaction of the particle the contribution to a point-detector is calculated analytically. A great advantage of this method is that both the direct attenuation of gamma radiation and the build-up factor is considered. Nevertheless, the method presents some disadvantages as well [@elteresarda]. One could argue, that computing the uncollided F5 tally is satisfactory in case the detector is collimated, and the background removed peak counts in the gamma spectrum are the main interest of the analysis. However, using a Monte Carlo Code, such as MCNP

# feign

``feign`` is a Python package implements a 2D point-kernel method to estimate the uncollided point-detector gamma flux around a rectangular spent fuel assembly. The user defines the experimental setup: materials, pin types (consisting of nested annular material regions), assembly lattice, detector locations and optionally collimators and additional absorber elements. Then, the program iterates through each lattice position containing source material and calculates the distance travelled in various materials towards the detector point by a gamma-ray emitted from the given position. A travelled distance map can be seen for a 17x17 PWR assembly in \ref{fig:distance}. Based on the travelled distance maps and user provided total attenuation coefficient data, the program evaluates probability

$$frac{1}{4\pi R_{i}^2}\prod\limits_m e^{-\mu_m d_{i,m}}$$

that a gamma-ray emitted from position _i_ to the detector. Where $$R_i$$ is the distance between the position and the detector, $$\mu_m$$ is the total attenuation coefficient of material _m_ and $$d_{i,m}$$ is the distance travelled by a gamma-ray emitted from position _i_ through material _m_.


The program includes several approximations, which limits its area of applications. These approximations and the rationale behind them are the following:

- the program is limited to 2D geometries, which is a fair approximation in case collimators with a horizontal slit are placed in front of the detector points.

- buildup



![An example of distance travelled in uranium-dioxide and water for a 17x17 PWR assembly measured at Clab. Each pixel represents the distance travelled in a certain material by a gamma-ray emitted from that position to the detector.\label{distance:example}](article_distancetravelled.png)


# References
