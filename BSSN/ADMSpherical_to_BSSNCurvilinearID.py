# This module performs the conversion between ADM
# spacetime variables in Spherical coordinates to
# rescaled BSSN-in-curvilinear coordinate quantities,
# as defined in BSSN_RHSs.py

# Author: Zachariah B. Etienne
#         zachetie **at** gmail **dot* com

import sympy as sp
import NRPy_param_funcs as par
from outputC import *
import indexedexp as ixp
import reference_metric as rfm
import BSSN.BSSN_RHSs as bssnrhs # The ConformalFactor parameter is used below

def Convert_Spherical_ADM_to_BSSN_curvilinear(Sph_r_th_ph, gammaSphDD_in, KSphDD_in, alphaSph_in, betaSphU_in, BSphU_in):
    # This routine convert the ADM variables
    # $$\left\{\gamma_{ij}, K_{ij}, \alpha, \beta^i\right\}$$
    # in Spherical coordinates to the BSSN variables
    # $$\left\{\bar{\gamma}_{i j},\bar{A}_{i j},\phi, K, \bar{\Lambda}^{i}, \alpha, \beta^i, B^i\right\},$$
    # to the rescaled variables
    # $$\left\{h_{i j},a_{i j},\phi, K, \lambda^{i}, \alpha, \mathcal{V}^i, \mathcal{B}^i\right\}.$$


    # The ADM & BSSN formalisms only work in 3D; they are 3+1 decompositions of Einstein's equations.
    #    To implement axisymmetry or spherical symmetry, simply set all spatial derivatives in
    #    the relevant angular directions to zero; DO NOT SET DIM TO ANYTHING BUT 3.
    # Step 0: Set spatial dimension (must be 3 for BSSN)
    DIM = 3

    # First copy gammaSphDD_in to gammaSphDD, KSphDD_in to KSphDD, etc.
    #    This ensures that the input arrays are not modified below;
    #    modifying them would result in unexpected effects outside
    #    this function.
    alphaSph = alphaSph_in
    betaSphU   = ixp.zerorank1()
    BSphU      = ixp.zerorank1()
    gammaSphDD = ixp.zerorank2()
    KSphDD     = ixp.zerorank2()
    for i in range(DIM):
        betaSphU[i] = betaSphU_in[i]
        BSphU[i]    = BSphU_in[i]
        for j in range(DIM):
            gammaSphDD[i][j] = gammaSphDD_in[i][j]
            KSphDD[i][j]     = KSphDD_in[i][j]

    # All input quantities are in terms of r,th,ph. We want them in terms of xx0,xx1,xx2:
    # WARNING: Substitution only works when the variable is not an integer. Hence the if not isinstance(...,...) stuff.
    def sympify_integers__replace_rthph(obj, Sph_r_th_ph, r_th_ph_of_xx):
        if isinstance(obj, int):
            return sp.sympify(obj)
        else:
            return obj.subs(Sph_r_th_ph[0], r_th_ph_of_xx[0]).subs(Sph_r_th_ph[1], r_th_ph_of_xx[1]).subs(Sph_r_th_ph[2], r_th_ph_of_xx[2])

    alphaSph = sympify_integers__replace_rthph(alphaSph, Sph_r_th_ph, rfm.xxSph)
    for i in range(DIM):
        betaSphU[i] = sympify_integers__replace_rthph(betaSphU[i], Sph_r_th_ph, rfm.xxSph)
        BSphU[i]    = sympify_integers__replace_rthph(BSphU[i],    Sph_r_th_ph, rfm.xxSph)
        for j in range(DIM):
            gammaSphDD[i][j] = sympify_integers__replace_rthph(gammaSphDD[i][j], Sph_r_th_ph, rfm.xxSph)
            KSphDD[i][j]     = sympify_integers__replace_rthph(KSphDD[i][j],     Sph_r_th_ph, rfm.xxSph)

    # trK and alpha are scalars, so no Jacobian transformations are necessary.
    alpha = alphaSph

    Jac_dUSph_dDrfmUD = ixp.zerorank2()
    for i in range(DIM):
        for j in range(DIM):
            Jac_dUSph_dDrfmUD[i][j] = sp.diff(rfm.xxSph[i],rfm.xx[j])

    Jac_dUrfm_dDSphUD, dummyDET = ixp.generic_matrix_inverter3x3(Jac_dUSph_dDrfmUD)

    betaU   = ixp.zerorank1()
    BU      = ixp.zerorank1()
    gammaDD = ixp.zerorank2()
    KDD     = ixp.zerorank2()
    for i in range(DIM):
        for j in range(DIM):
            betaU[i] += Jac_dUrfm_dDSphUD[i][j] * betaSphU[j]
            BU[i]    += Jac_dUrfm_dDSphUD[i][j] * BSphU[j]
            for k in range(DIM):
                for l in range(DIM):
                    gammaDD[i][j] += Jac_dUSph_dDrfmUD[k][i]*Jac_dUSph_dDrfmUD[l][j] * gammaSphDD[k][l]
                    KDD[i][j]     += Jac_dUSph_dDrfmUD[k][i]*Jac_dUSph_dDrfmUD[l][j] *     KSphDD[k][l]

    # Step 1: Convert ADM $\gamma_{ij}$ to BSSN $\bar{\gamma}_{ij}$
    # We have (Eqs. 2 and 3 of [Ruchlin *et al.*](https://arxiv.org/pdf/1712.07658.pdf)):
    # $$
    # \bar{\gamma}_{i j} = \left(\frac{\bar{\gamma}}{\gamma}\right)^{1/3} \gamma_{ij}.
    # $$
    #
    # We choose $\bar{\gamma}=\hat{\gamma}$, which in spherical coordinates implies $\bar{\gamma}=\hat{\gamma}=r^4 \sin^2\theta$. Instead of manually setting the determinant, we instead call rfm.reference_metric(), which automatically sets up the metric based on the chosen reference_metric::CoordSystem parameter.

    gammaUU, gammaDET = ixp.symm_matrix_inverter3x3(gammaDD)
    gammabarDD = ixp.zerorank2()
    for i in range(DIM):
        for j in range(DIM):
            gammabarDD[i][j] = (rfm.detgammahat/gammaDET)**(sp.Rational(1,3))*gammaDD[i][j]


    # Second, we convert the extrinsic curvature $K_{ij}$ to the trace-free extrinsic curvature $\bar{A}_{ij}$, plus the trace of the extrinsic curvature $K$, where (Eq. 3 of [Baumgarte *et al.*](https://arxiv.org/pdf/1211.6632.pdf)):
    #
    # \begin{align}
    # K &= \gamma^{ij} K_{ij} \\
        # \bar{A}_{ij} &= \left(\frac{\bar{\gamma}}{\gamma}\right)^{1/3} \left(K_{ij} - \frac{1}{3} \gamma_{ij} K \right)
    # \end{align}

    # Step 2: Convert ADM $K_{ij}$ to $\bar{A}_{ij}$ and $K$,
    #          where (Eq. 3 of Baumgarte et al.: https://arxiv.org/pdf/1211.6632.pdf)
    trK = sp.sympify(0)
    for i in range(DIM):
        for j in range(DIM):
            trK += gammaUU[i][j]*KDD[i][j]

    AbarDD = ixp.zerorank2()
    for i in range(DIM):
        for j in range(DIM):
            AbarDD[i][j] = (rfm.detgammahat/gammaDET)**(sp.Rational(1,3))*(KDD[i][j] - sp.Rational(1,3)*gammaDD[i][j]*trK)


    # Third, we define $\bar{\Lambda}^i$ (Eqs. 4 and 5 of [Baumgarte *et al.*](https://arxiv.org/pdf/1211.6632.pdf)):
    #
    # $$
    # \bar{\Lambda}^i = \bar{\gamma}^{jk}\left(\bar{\Gamma}^i_{jk} - \hat{\Gamma}^i_{jk}\right).
    # $$

    # All BSSN tensors and vectors are in Spherical coordinates $x^i_{\rm Sph} = (r,\theta,\phi)$, but we need them in the curvilinear coordinate system $x^i_{\rm rfm}= ({\rm xx0},{\rm xx1},{\rm xx2})$ set by the "reference_metric::CoordSystem" variable. Empirically speaking, it is far easier to write $(x({\rm xx0},{\rm xx1},{\rm xx2}),y({\rm xx0},{\rm xx1},{\rm xx2}),z({\rm xx0},{\rm xx1},{\rm xx2}))$ than the inverse, so we will compute the Jacobian matrix
    #
    # $$
    # {\rm Jac\_dUSph\_dDrfmUD[i][j]} = \frac{\partial x^i_{\rm Sph}}{\partial x^j_{\rm rfm}},
    # $$
    #
    # via exact differentiation (courtesy SymPy), and the inverse Jacobian
    # $$
    # {\rm Jac\_dUrfm\_dDSphUD[i][j]} = \frac{\partial x^i_{\rm rfm}}{\partial x^j_{\rm Sph}},
    # $$
    #
    # using NRPy+'s ${\rm generic\_matrix\_inverter3x3()}$ function. In terms of these, the transformation of BSSN tensors from Spherical to "reference_metric::CoordSystem" coordinates may be written:
    #
    # \begin{align}
    # \bar{\gamma}^{\rm rfm}_{ij} &=
    # \frac{\partial x^\ell_{\rm Sph}}{\partial x^i_{\rm rfm}}
    # \frac{\partial x^m_{\rm Sph}}{\partial x^j_{\rm rfm}} \bar{\gamma}^{\rm Sph}_{\ell m}\\
        # \bar{A}^{\rm rfm}_{ij} &=
    # \frac{\partial x^\ell_{\rm Sph}}{\partial x^i_{\rm rfm}}
    # \frac{\partial x^m_{\rm Sph}}{\partial x^j_{\rm rfm}} \bar{A}^{\rm Sph}_{\ell m}\\
        # \bar{\Lambda}^i_{\rm rfm} &= \frac{\partial x^i_{\rm rfm}}{\partial x^\ell_{\rm Sph}} \bar{\Lambda}^\ell_{\rm Sph} \\
        # \beta^i_{\rm rfm} &= \frac{\partial x^i_{\rm rfm}}{\partial x^\ell_{\rm Sph}} \beta^\ell_{\rm Sph}
    # \end{align}

    # Step 3: Define $\bar{\Lambda}^i$ from Eqs. 4 and 5 of Baumgarte et al.: https://arxiv.org/pdf/1211.6632.pdf
    # Need to compute \bar{\gamma}^{ij} from \bar{\gamma}_{ij}:
    gammabarUU, gammabarDET = ixp.symm_matrix_inverter3x3(gammabarDD)

    GammabarUDD = ixp.zerorank3()
    for i in range(DIM):
        for j in range(DIM):
            for k in range(DIM):
                for l in range(DIM):
                    GammabarUDD[i][j][k] += sp.Rational(1,2)*gammabarUU[i][l]*( sp.diff(gammabarDD[l][j],rfm.xx[k]) +
                                                                                sp.diff(gammabarDD[l][k],rfm.xx[j]) -
                                                                                sp.diff(gammabarDD[j][k],rfm.xx[l]) )
    LambdabarU = ixp.zerorank1()
    for i in range(DIM):
        for j in range(DIM):
            for k in range(DIM):
                LambdabarU[i] += gammabarUU[j][k] * (GammabarUDD[i][j][k] - rfm.GammahatUDD[i][j][k])


    # Step 4: Convert BSSN tensors to destination basis specified by CoordSystem_dest variable above.

    # Step 4.1: First restore reference_metric::CoordSystem to
    #           CoordSystem_dest, and call rfm.reference_metric(),
    #           so that all hatted quantities are updated to
    #           CoordSystem_dest.
#     par.set_parval_from_str("reference_metric::CoordSystem",CoordSystem_dest)
#     rfm.reference_metric()

    # Next we set the conformal factor variable $\texttt{cf}$, which is set by the "BSSN_RHSs::ConformalFactor" parameter. For example if "ConformalFactor" is set to "phi", we can use Eq. 3 of [Ruchlin *et al.*](https://arxiv.org/pdf/1712.07658.pdf), which in arbitrary coordinates is written:
    #
    # $$
    # \phi = \frac{1}{12} \log\left(\frac{\gamma}{\bar{\gamma}}\right).
    # $$
    #
    # Alternatively if "BSSN_RHSs::ConformalFactor" is set to "chi", then
    # $$
    # \chi = e^{-4 \phi} = \exp\left(-4 \frac{1}{12} \left(\frac{\gamma}{\bar{\gamma}}\right)\right)
    # = \exp\left(-\frac{1}{3} \log\left(\frac{\gamma}{\bar{\gamma}}\right)\right) = \left(\frac{\gamma}{\bar{\gamma}}\right)^{-1/3}.
    # $$
    #
    # Finally if "BSSN_RHSs::ConformalFactor" is set to "W", then
    # $$
    # W = e^{-2 \phi} = \exp\left(-2 \frac{1}{12} \log\left(\frac{\gamma}{\bar{\gamma}}\right)\right) =
    # \exp\left(-\frac{1}{6} \log\left(\frac{\gamma}{\bar{\gamma}}\right)\right) =
    # \left(\frac{\gamma}{\bar{\gamma}}\right)^{-1/6}.
    # $$

    # Step 5: Set the conformal factor variable according to the parameter BSSN_RHSs::ConformalFactor
    cf = sp.sympify(0)

    if par.parval_from_str("ConformalFactor") == "phi":
        cf = sp.Rational(1,12)*sp.log(gammaDET/gammabarDET)
    elif par.parval_from_str("ConformalFactor") == "chi":
        cf = (gammaDET/gammabarDET)**(-sp.Rational(1,3))
    elif par.parval_from_str("ConformalFactor") == "W":
        cf = (gammaDET/gammabarDET)**(-sp.Rational(1,6))
    else:
        print("Error ConformalFactor type = \""+par.parval_from_str("ConformalFactor")+"\" unknown.")
        exit(1)


    # Finally, we rescale tensorial quantities according to the prescription described in the [BSSN in curvilinear coordinates tutorial module](Tutorial-BSSNCurvilinear.ipynb) (also [Ruchlin *et al.*](https://arxiv.org/pdf/1712.07658.pdf)):
    #
    # h_{ij} &= (\bar{\gamma}_{ij} - \hat{\gamma}_{ij})/\text{ReDD[i][j]}\\
    # a_{ij} &= \bar{A}_{ij}/\text{ReDD[i][j]}\\
    # \lambda^i &= \bar{\Lambda}^i/\text{ReU[i]}\\
    # \mathcal{V}^i &= \beta^i/\text{ReU[i]}\\
    # \mathcal{B}^i &= B^i/\text{ReU[i]}\\

    # Step 6: Rescale all tensorial quantities.

    if rfm.have_already_called_reference_metric_function == False:
        print("Error. Called Convert_Spherical_ADM_to_BSSN_curvilinear() without")
        print("       first setting up reference metric, by calling rfm.reference_metric().")
        exit(1)

    hDD     = ixp.zerorank2()
    aDD     = ixp.zerorank2()
    lambdaU = ixp.zerorank1()
    vetU    = ixp.zerorank1()
    betU    = ixp.zerorank1()
    for i in range(DIM):
        lambdaU[i] = LambdabarU[i] / rfm.ReU[i]
        vetU[i]    =      betaU[i] / rfm.ReU[i]
        betU[i]    =         BU[i] / rfm.ReU[i]
        for j in range(DIM):
            hDD[i][j] = (gammabarDD[i][j] - rfm.ghatDD[i][j]) / rfm.ReDD[i][j]
            aDD[i][j] =                          AbarDD[i][j] / rfm.ReDD[i][j]
    #print(sp.mathematica_code(hDD[0][0]))

    return cf, hDD, lambdaU, aDD, trK, alpha, vetU, betU