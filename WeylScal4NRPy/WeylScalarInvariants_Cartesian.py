# Step P1: import all needed modules from NRPy+:
import NRPy_param_funcs as par
import indexedexp as ixp
import grid as gri
import finite_difference as fin
#import reference_metric as rfm
from outputC import *
#import BSSN.BSSNs as bssn
import sympy as sp

# Step P2: Initialize WeylScalar Invariants parameters
# None at this time.

def WeylScalarInvariants_Cartesian():
    # Step 1: Declare Weyl scalar psi's as gridfunctions, as they will be read from memory.
    psi4r,psi4i,psi3r,psi3i,psi2r,psi2i,psi1r,psi1i,psi0r,psi0i = gri.register_gridfunctions("AUX",["psi4r","psi4i",\
                                                                                                    "psi3r","psi3i",\
                                                                                                    "psi2r","psi2i",\
                                                                                                    "psi1r","psi1i",\
                                                                                                    "psi0r","psi0i"])

    psi4 = psi4r + sp.I * psi4i
    psi3 = psi3r + sp.I * psi3i
    psi2 = psi2r + sp.I * psi2i
    psi1 = psi1r + sp.I * psi1i
    psi0 = psi0r + sp.I * psi0i

    global curvIr,curvIi,curvJr,curvJi,curvJ1,curvJ2,curvJ3,curvJ4

    curvIr, curvIi, curvJr, curvJi, curvJ1, curvJ2, curvJ3, curvJ4 = gri.register_gridfunctions("AUX",["curvIr","curvIi",\
                                                                                                       "curvJr","curvJi",\
                                                                                                       "curvJ1","curvJ2",\
                                                                                                       "curvJ3","curvJ4"])

    curvIr = sp.re(3*psi2*psi2 - 4*psi1*psi3 + psi4*psi0)
    curvIi = sp.im(3*psi2*psi2 - 4*psi1*psi3 + psi4*psi0)
    curvJr = sp.re(psi4 * (psi2*psi0 - psi1*psi1) - \
                   psi3 * (psi3*psi0 - psi1*psi2) +\
                   psi2 * (psi3*psi1 - psi2*psi2) )
    curvJi = sp.im(psi4 * (psi2*psi0 - psi1*psi1) - \
                   psi3 * (psi3*psi0 - psi1*psi2) +\
                   psi2 * (psi3*psi1 - psi2*psi2) )

    curvJ1 =-16*(3*psi2i**2-3*psi2r**2-4*psi1i*psi3i+4*psi1r*psi3r+psi0i*psi4i-psi0r*psi4r)

    curvJ2 = 96*(-3*psi2i**2*psi2r+psi2r**3+2*psi1r*psi2i*psi3i+2*psi1i*psi2r*psi3i-psi0r*psi3i**2+\
                2*psi1i*psi2i*psi3r-2*psi1r*psi2r*psi3r-2*psi0i*psi3i*psi3r+psi0r*psi3r**2-\
                2*psi1i*psi1r*psi4i+psi0r*psi2i*psi4i+psi0i*psi2r*psi4i-psi1i**2*psi4r+psi1r**2*psi4r+\
                psi0i*psi2i*psi4r-psi0r*psi2r*psi4r)

    curvJ3 = 64*(9*psi2i**4-54*psi2i**2*psi2r**2+9*psi2r**4-24*psi1i*psi2i**2*psi3i+48*psi1r*psi2i*psi2r*psi3i+\
                24*psi1i*psi2r**2*psi3i+16*psi1i**2*psi3i**2-16*psi1r**2*psi3i**2+\
                24*psi1r*psi2i**2*psi3r+48*psi1i*psi2i*psi2r*psi3r-24*psi1r*psi2r**2*psi3r-64*psi1i*psi1r*psi3i*psi3r-\
                16*psi1i**2*psi3r**2+16*psi1r**2*psi3r**2+6*psi0i*psi2i**2*psi4i-12*psi0r*psi2i*psi2r*psi4i-\
                6*psi0i*psi2r**2*psi4i-8*psi0i*psi1i*psi3i*psi4i+8*psi0r*psi1r*psi3i*psi4i+8*psi0r*psi1i*psi3r*psi4i+\
                8*psi0i*psi1r*psi3r*psi4i+psi0i**2*psi4i**2-psi0r**2*psi4i**2-6*psi0r*psi2i**2*psi4r-\
                12*psi0i*psi2i*psi2r*psi4r+6*psi0r*psi2r**2*psi4r+8*psi0r*psi1i*psi3i*psi4r+8*psi0i*psi1r*psi3i*psi4r+\
                8*psi0i*psi1i*psi3r*psi4r-8*psi0r*psi1r*psi3r*psi4r-4*psi0i*psi0r*psi4i*psi4r-psi0i**2*psi4r**2+\
                psi0r**2*psi4r**2)

    curvJ4 = -640*(-15*psi2i**4*psi2r+30*psi2i**2*psi2r**3-3*psi2r**5+10*psi1r*psi2i**3*psi3i+\
                  30*psi1i*psi2i**2*psi2r*psi3i-30*psi1r*psi2i*psi2r**2*psi3i-10*psi1i*psi2r**3*psi3i-\
                  16*psi1i*psi1r*psi2i*psi3i**2-3*psi0r*psi2i**2*psi3i**2-8*psi1i**2*psi2r*psi3i**2+\
                  8*psi1r**2*psi2r*psi3i**2-6*psi0i*psi2i*psi2r*psi3i**2+3*psi0r*psi2r**2*psi3i**2+\
                  4*psi0r*psi1i*psi3i**3+4*psi0i*psi1r*psi3i**3+10*psi1i*psi2i**3*psi3r-\
                  30*psi1r*psi2i**2*psi2r*psi3r-30*psi1i*psi2i*psi2r**2*psi3r+10*psi1r*psi2r**3*psi3r-\
                  16*psi1i**2*psi2i*psi3i*psi3r+16*psi1r**2*psi2i*psi3i*psi3r-6*psi0i*psi2i**2*psi3i*psi3r+\
                  32*psi1i*psi1r*psi2r*psi3i*psi3r+12*psi0r*psi2i*psi2r*psi3i*psi3r+6*psi0i*psi2r**2*psi3i*psi3r+\
                  12*psi0i*psi1i*psi3i**2*psi3r-12*psi0r*psi1r*psi3i**2*psi3r+16*psi1i*psi1r*psi2i*psi3r**2+\
                  3*psi0r*psi2i**2*psi3r**2+8*psi1i**2*psi2r*psi3r**2-8*psi1r**2*psi2r*psi3r**2+\
                  6*psi0i*psi2i*psi2r*psi3r**2-3*psi0r*psi2r**2*psi3r**2-12*psi0r*psi1i*psi3i*psi3r**2-\
                  12*psi0i*psi1r*psi3i*psi3r**2-4*psi0i*psi1i*psi3r**3+4*psi0r*psi1r*psi3r**3-\
                  6*psi1i*psi1r*psi2i**2*psi4i+2*psi0r*psi2i**3*psi4i-6*psi1i**2*psi2i*psi2r*psi4i+\
                  6*psi1r**2*psi2i*psi2r*psi4i+6*psi0i*psi2i**2*psi2r*psi4i+6*psi1i*psi1r*psi2r**2*psi4i-\
                  6*psi0r*psi2i*psi2r**2*psi4i-2*psi0i*psi2r**3*psi4i+12*psi1i**2*psi1r*psi3i*psi4i-\
                  4*psi1r**3*psi3i*psi4i-2*psi0r*psi1i*psi2i*psi3i*psi4i-2*psi0i*psi1r*psi2i*psi3i*psi4i-\
                  2*psi0i*psi1i*psi2r*psi3i*psi4i+2*psi0r*psi1r*psi2r*psi3i*psi4i-2*psi0i*psi0r*psi3i**2*psi4i+\
                  4*psi1i**3*psi3r*psi4i-12*psi1i*psi1r**2*psi3r*psi4i-2*psi0i*psi1i*psi2i*psi3r*psi4i+\
                  2*psi0r*psi1r*psi2i*psi3r*psi4i+2*psi0r*psi1i*psi2r*psi3r*psi4i+2*psi0i*psi1r*psi2r*psi3r*psi4i-\
                  2*psi0i**2*psi3i*psi3r*psi4i+2*psi0r**2*psi3i*psi3r*psi4i+2*psi0i*psi0r*psi3r**2*psi4i-\
                  psi0r*psi1i**2*psi4i**2-2*psi0i*psi1i*psi1r*psi4i**2+psi0r*psi1r**2*psi4i**2+\
                  2*psi0i*psi0r*psi2i*psi4i**2+psi0i**2*psi2r*psi4i**2-psi0r**2*psi2r*psi4i**2-3*psi1i**2*psi2i**2*psi4r+\
                  3*psi1r**2*psi2i**2*psi4r+2*psi0i*psi2i**3*psi4r+12*psi1i*psi1r*psi2i*psi2r*psi4r-\
                  6*psi0r*psi2i**2*psi2r*psi4r+3*psi1i**2*psi2r**2*psi4r-3*psi1r**2*psi2r**2*psi4r-\
                  6*psi0i*psi2i*psi2r**2*psi4r+2*psi0r*psi2r**3*psi4r+4*psi1i**3*psi3i*psi4r-12*psi1i*psi1r**2*psi3i*psi4r-\
                  2*psi0i*psi1i*psi2i*psi3i*psi4r+2*psi0r*psi1r*psi2i*psi3i*psi4r+2*psi0r*psi1i*psi2r*psi3i*psi4r+\
                  2*psi0i*psi1r*psi2r*psi3i*psi4r-psi0i**2*psi3i**2*psi4r+psi0r**2*psi3i**2*psi4r-\
                  12*psi1i**2*psi1r*psi3r*psi4r+4*psi1r**3*psi3r*psi4r+2*psi0r*psi1i*psi2i*psi3r*psi4r+\
                  2*psi0i*psi1r*psi2i*psi3r*psi4r+2*psi0i*psi1i*psi2r*psi3r*psi4r-2*psi0r*psi1r*psi2r*psi3r*psi4r+\
                  4*psi0i*psi0r*psi3i*psi3r*psi4r+psi0i**2*psi3r**2*psi4r-psi0r**2*psi3r**2*psi4r-\
                  2*psi0i*psi1i**2*psi4i*psi4r+4*psi0r*psi1i*psi1r*psi4i*psi4r+2*psi0i*psi1r**2*psi4i*psi4r+\
                  2*psi0i**2*psi2i*psi4i*psi4r-2*psi0r**2*psi2i*psi4i*psi4r-4*psi0i*psi0r*psi2r*psi4i*psi4r+\
                  psi0r*psi1i**2*psi4r**2+2*psi0i*psi1i*psi1r*psi4r**2-psi0r*psi1r**2*psi4r**2-
                  2*psi0i*psi0r*psi2i*psi4r**2-psi0i**2*psi2r*psi4r**2+psi0r**2*psi2r*psi4r**2)
