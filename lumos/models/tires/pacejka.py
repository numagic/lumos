import logging
from typing import Any, Dict, Optional, Tuple

import lumos.numpy as lnp
from lumos.models.base import model_io, ModelReturn
from lumos.models.tires.base import BaseTire

logger = logging.getLogger(__name__)


@model_io(
    inputs=(
        "Fz",  # vertical load
        "kappa",  # slip ratio
        "alpha",  # slip angle
        "vx",  # x-velocity in tire coordinate
        "gamma",  # inclination angle
    ),
    outputs=("Fx", "Fy", "Mx", "My", "Mz", "Kxk", "Gxa", "Kya", "Gyk", "GSum"),
)
class MF52(BaseTire):
    def __init__(
        self,
        model_config: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
        opt_mode: bool = True,
    ):
        """MF5.2 Pacjeka magic formula

        Args:
            params (Dict[str, Any], optional): model parameters. Defaults to None.
            opt_mode (bool, optional): use optimization mode if True. Defaults to True.

        currently _opt_mode is used to make an optimization variant of the model, which
        includes the following modifications:
        - no calculation of moments (to speed up compile time for experiment,until
        vehicle model is ready)

        Reference implementation in:
        - doc: https://mfeval.wordpress.com
        - code: https://de.mathworks.com/matlabcentral/fileexchange/63618-mfeval

        The MF5.2 is steady-state model which also doesn't contain effects such as:
        - effects from inflation pressure
        - some secondary effects from camber angle
        - speed effect on grip

        Also the variant implemented here ignores turn slip.

        ISO-W (TYDEX W) Contact-Patch Axis System coordinate system is used in
        all calculations, see page 29 of
        https://functionbay.com/documentation/onlinehelp/Documents/Tire/MFTire-MFSwift_Help.pdf

        params refers to a MF-Tire tire property file (.TIR) containing
        all the Magic Formula coefficients or to a structure with all the parameters.

        All units are SI.
        """

        super().__init__(model_config=model_config, params=params)

        self._opt_mode = opt_mode

    @classmethod
    def get_default_params(cls) -> Dict[str, Any]:
        # default pacejka parameters from data/tires/default.tir
        params = {
            "FILE_VERSION": 3.0,
            "VXLOW": 1.0,
            "LONGVL": 15.0,
            "UNLOADED_RADIUS": 0.4,
            "WIDTH": 0.235,
            "RIM_RADIUS": 0.2032,
            "RIM_WIDTH": 0.1778,
            "VERTICAL_STIFFNESS": 463000.0,
            "VERTICAL_DAMPING": 500.0,
            "BREFF": 8.4,
            "DREFF": 0.27,
            "FREFF": 0.07,
            "FNOMIN": 9416.6,
            "KPUMIN": -1.5,
            "KPUMAX": 1.5,
            "ALPMIN": -1.5,
            "ALPMAX": 1.5,
            "CAMMIN": -0.2634,
            "CAMMAX": 0.26395,
            "FZMIN": 100.0,
            "FZMAX": 20469.8,
            "LFZO": 1.0,
            "LCX": 1.0,
            "LMUX": 1.0,
            "LEX": 1.0,
            "LKX": 1.0,
            "LHX": 1.0,
            "LVX": 1.0,
            "LGAX": 1.0,
            "LCY": 1.0,
            "LMUY": 1.0,
            "LEY": 1.0,
            "LKY": 1.0,
            "LHY": 1.0,
            "LVY": 1.0,
            "LGAY": 1.0,
            "LTR": 1.0,
            "LRES": 1.0,
            "LGAZ": 1.0,
            "LXAL": 1.0,
            "LYKA": 1.0,
            "LVYKA": 1.0,
            "LS": 1.0,
            "LSGKP": 1.0,
            "LSGAL": 1.0,
            "LGYR": 1.0,
            "LMX": 1.0,
            "LVMX": 1.0,
            "LMY": 1.0,
            "PCX1": 1.3605,
            "PDX1": 0.885,
            "PDX2": -0.05653,
            "PDX3": -8.768,
            "PEX1": -0.13155,
            "PEX2": -0.475,
            "PEX3": -1.3126,
            "PEX4": -1.685,
            "PKX1": 16.675,
            "PKX2": -0.04552,
            "PKX3": 0.4205,
            "PHX1": 8.731e-05,
            "PHX2": -0.0011733,
            "PVX1": 0.01913,
            "PVX2": 0.02654,
            "RBX1": 9.509,
            "RBX2": -9.51,
            "RCX1": 1.0061,
            "REX1": -1.9815,
            "REX2": -4.552,
            "RHX1": 0.010039,
            "PTX1": 1.1898,
            "PTX2": -0.0006148,
            "PTX3": -0.3717,
            "QSX1": -0.003093,
            "QSX2": 0.6038,
            "QSX3": 0.025405,
            "PCY1": 1.889,
            "PDY1": 0.8271,
            "PDY2": -0.2306,
            "PDY3": -7.088,
            "PEY1": 0.4585,
            "PEY2": -0.21823,
            "PEY3": -0.3872,
            "PEY4": 3.96,
            "PKY1": -29.1,
            "PKY2": 7.576,
            "PKY3": 0.944,
            "PHY1": 0.004476,
            "PHY2": 0.0025996,
            "PHY3": 0.006973,
            "PVY1": 0.005978,
            "PVY2": 0.008146,
            "PVY3": -0.4066,
            "PVY4": -0.4417,
            "RBY1": 5.042,
            "RBY2": 4.858,
            "RBY3": 0.06116,
            "RCY1": 1.0642,
            "REY1": -0.9207,
            "REY2": -0.4334,
            "RHY1": -0.0009546,
            "RHY2": 3.506e-05,
            "RVY1": -0.02541,
            "RVY2": 0.02259,
            "RVY3": -0.9322,
            "RVY4": 21.16,
            "RVY5": 1.9,
            "RVY6": -15.552,
            "PTY1": 1.6245,
            "PTY2": 2.8506,
            "QSY1": 0.01,
            "QSY2": 0.0,
            "QSY3": 0.0,
            "QSY4": 0.0,
            "QBZ1": 6.035,
            "QBZ2": -0.8902,
            "QBZ3": 1.1858,
            "QBZ4": 0.0887,
            "QBZ5": -0.2598,
            "QBZ9": 7.32,
            "QBZ10": 0.0,
            "QCZ1": 1.6637,
            "QDZ1": 0.07618,
            "QDZ2": -0.02726,
            "QDZ3": 0.5106,
            "QDZ4": 27.5,
            "QDZ6": -0.0012362,
            "QDZ7": -0.003485,
            "QDZ8": -0.10836,
            "QDZ9": -0.03984,
            "QEZ1": -0.04218,
            "QEZ2": 0.002656,
            "QEZ3": 0.0,
            "QEZ4": 1.3648,
            "QEZ5": -99.3,
            "QHZ1": 0.019396,
            "QHZ2": -0.0017907,
            "QHZ3": 0.09319,
            "QHZ4": -0.03752,
            "SSZ1": 0.009003,
            "SSZ2": -0.011339,
            "SSZ3": 0.6903,
            "SSZ4": -0.7046,
            "QTZ1": 0.0,
            "MBELT": 0.0,
            "epsilonv": 1e-06,
            "epsilonx": 0.001,
            "epsilonk": 1e-06,
            "epsilony": 0.001,
        }

        return params

    def forward(self, inputs: Dict[str, float]) -> lnp.ndarray:
        """Pacejka MF5.2 tire model

        There are essentially two sources of equations:
        - from paper, makred with A (eg A56)
        - from the book equations from page 184 onwards (4.3.2 Full Set of Equations).
        marked with E4.xx, eg: E4.43

        Book:
        Title: Tire and Vehicle Dynamics
        Author: Hans Pacejka
        Edition: 3, revised
        https://www.elsevier.com/books/tire-and-vehicle-dynamics/pacejka/978-0-08-097016-5

        Paper:
        Besselink, I. J. M. , Schmeitz, A. J. C. and Pacejka, H. B.(2010)
        ‘An improved Magic Formula/Swift tyre model that can handle inflation pressure changes’
        Vehicle System Dynamics, 48: 1, 337 — 352
        http://dx.doi.org/10.1080/00423111003748088
        """

        # Unpack inputs
        gamma = inputs["gamma"]
        vx = inputs["vx"]
        Fz = inputs["Fz"]
        kappa = inputs["kappa"]
        alpha = inputs["alpha"]

        (Fx, Fy, Mx, My, Mz, Kxk, Gxa, Kya, Gyk) = self._do_force_and_moments(
            kappa=kappa,
            alpha=alpha,
            gamma=gamma,
            vx=vx,
            Fz=Fz,
        )

        outputs = dict(
            Fx=Fx,
            Fy=Fy,
            Mx=Mx,
            My=My,
            Mz=Mz,
            Kxk=Kxk,
            Gxa=Gxa,
            Kya=Kya,
            Gyk=Gyk,
            GSum=lnp.sqrt(Gyk**2 + Gxa**2),
        )

        return ModelReturn(outputs=outputs)

    def _do_force_and_moments(
        self,
        kappa: float,
        alpha: float,
        gamma: float,
        vx: float,
        Fz: float,
    ) -> lnp.ndarray:
        """Top level computation

        See MFeval Solver.doForcesAndMoments
        """

        starVar, primeVar, incrVar = self._calculate_basic(
            kappa=kappa,
            alpha=alpha,
            Vcx=vx,
            gamma=gamma,
            Fz=Fz,
        )

        Fx0, mux, Kxk = self._calculate_Fx0(
            kappa=kappa,
            gamma=gamma,
            Fz=Fz,
            starVar=starVar,
            primeVar=primeVar,
            incrVar=incrVar,
        )

        Fx, Gxa = self._calculate_Fx(
            kappa=kappa,
            starVar=starVar,
            incrVar=incrVar,
            Fx0=Fx0,
        )

        Fy0, muy, Kya, SHy, SVy, By, Cy = self._calculate_Fy0(
            Fz=Fz, starVar=starVar, primeVar=primeVar, incrVar=incrVar
        )

        Fy, Gyk, SVyk = self.calcluate_Fy(
            Fz=Fz,
            kappa=kappa,
            Fy0=Fy0,
            muy=muy,
            starVar=starVar,
            incrVar=incrVar,
        )

        if self._opt_mode:
            # Skip computaion of moments
            Mx = My = Mz = 0.0
        else:
            # TODO: clean this up
            lat_coeff = {
                "Kya": Kya,
                "SHy": SHy,
                "SVy": SVy,
                "SVyk": SVyk,
                "By": By,
                "Cy": Cy,
            }

            Mx = self._calculate_Mx(gamma=gamma, Fz=Fz, Fy=Fy)
            My = self._calculate_My(Fz=Fz, vx=vx, Fx=Fx)

            # NOTE: we combined the calculateMz0 and calculateMz from the origional function
            # as the Mz0 value is not needed in MF5.2. (but a few intermedaite coefficients
            # are needed.)
            Mz = self._calculate_Mz(
                kappa=kappa,
                alpha=alpha,
                gamma=gamma,
                Fz=Fz,
                vx=vx,
                Fx=Fx,
                Kxk=Kxk,
                Fy=Fy,
                lat_coeff=lat_coeff,
                starVar=starVar,
                primeVar=primeVar,
                incrVar=incrVar,
            )

        return (Fx, Fy, Mx, My, Mz, Kxk, Gxa, Kya, Gyk)

    def _calculate_basic(
        self,
        kappa: float,
        alpha: float,
        Vcx: float,
        gamma: float,
        Fz: float,
    ) -> Tuple[Dict[str, float]]:
        """Corresponds to Solver.calculateBasic in mfeval

        Note:
        This implementation ignores the potential use of tan(alpha) at very large slip
        angles and possibly backwards running of the wheel, Eqn (4.E3-4.E4) p.177 of Book
        This is called alpha_star in MFeval
        """

        # TODO: there are things we could simplify here:
        # 1) speed dependent grip: LMUV does not exist in MF5.2, so hard coded to 0,
        # which means we could get rid of related computation
        # 2) pressure effect: does not exist in MF5.2, so we could get rid of dpi.

        # Unpack Parameters
        Fz0 = self._params["FNOMIN"]  # Nominal wheel load
        LFZO = self._params["LFZO"]  # Scale factor of nominal (rated) load
        LMUX = self._params["LMUX"]  # Scale factor of Fx peak friction coefficient
        LMUY = self._params["LMUY"]  # Scale factor of Fy peak friction coefficient

        epsilonv = self._params["epsilonv"]

        # Slip velocities in point S (slip point)
        Vsy = (
            lnp.tan(alpha) * Vcx
        )  # Assumption page 67 of book, paragraph above Eqn (2.11)

        # Velocities in point C (contact)
        Vcy = Vsy
        # TODO: sqrt singularity here
        Vc = lnp.sqrt(Vcx**2 + Vcy**2)  # Velocity of wheel contact centre C,
        # Not described in the book but is the same as [Eqn (3.39) Page 102 - Book]

        # Effect of having a tire with a different nominal load
        Fz0_prime = LFZO * Fz0  # [Eqn (4.E1) Page 177 - Book]

        # Normalized change in vertical load
        dfz = (Fz - Fz0_prime) / Fz0_prime  # [Eqn (4.E2a) Page 177 - Book]

        # NOTE: we do not use alpha_star mode from MFeval
        alpha_star = alpha
        gamma_star = gamma

        # For the aligning torque at high slip angles
        # NOTE: we omit the sign(Vc) part as we assume Vc is always positive.
        Vc_prime = Vc + epsilonv  # [Eqn (4.E6a) Page 178 - Book]

        alpha_prime = lnp.arccos(Vcx / Vc_prime)  # [Eqn (4.E6) Page 177 - Book]

        # NOTE: here we ignore mu scaling with changing slip speed as these are not
        # included in MF5.2 (effect set to )
        LMUX_star = LMUX  # [Eqn (4.E7) Page 179 - Book] without slip speed effect
        LMUY_star = LMUY  # [Eqn (4.E7) Page 179 - Book] without slip speed effect

        # Degressive friction factor
        # On Page 179 of the book is suggested Amu = 10, but after comparing the use of
        # the scaling factors against TNO, Amu = 1 was giving perfect match
        Amu = 1
        # [Eqn (4.E8) Page 179 - Book]
        LMUX_prime = Amu * LMUX_star / (1 + (Amu - 1) * LMUX_star)
        LMUY_prime = Amu * LMUY_star / (1 + (Amu - 1) * LMUY_star)

        # Pack outputs
        starVar = {
            "alpha_star": alpha_star,
            "gamma_star": gamma_star,
            "LMUX_star": LMUX_star,
            "LMUY_star": LMUY_star,
        }

        primeVar = {
            "Fz0_prime": Fz0_prime,
            "alpha_prime": alpha_prime,
            "LMUX_prime": LMUX_prime,
            "LMUY_prime": LMUY_prime,
        }

        incrVar = {"dfz": dfz}

        return starVar, primeVar, incrVar

    def _calculate_Fx0(self, kappa, gamma, Fz, starVar, primeVar, incrVar):
        """Calculate the longitudinal tire force for pure longitudinal slips.

        See MFEval Solver.calculateFx0
        """
        # [SCALING_COEFFICIENTS]
        LCX = self._params["LCX"]  # Scale factor of Fx shape factor
        LEX = self._params["LEX"]  # Scale factor of Fx curvature factor
        LKX = self._params["LKX"]  # Scale factor of Fx slip stiffness
        LHX = self._params["LHX"]  # Scale factor of Fx horizontal shift
        LVX = self._params["LVX"]  # Scale factor of Fx vertical shift

        # [LONGITUDINAL_COEFFICIENTS]
        PCX1 = self._params["PCX1"]  # Shape factor Cfx for longitudinal force
        PDX1 = self._params["PDX1"]  # Longitudinal friction Mux at Fznom
        PDX2 = self._params["PDX2"]  # Variation of friction Mux with load
        PDX3 = self._params["PDX3"]  # Variation of friction Mux with camber squared
        PEX1 = self._params["PEX1"]  # Longitudinal curvature Efx at Fznom
        PEX2 = self._params["PEX2"]  # Variation of curvature Efx with load
        PEX3 = self._params["PEX3"]  # Variation of curvature Efx with load squared
        PEX4 = self._params["PEX4"]  # Factor in curvature Efx while driving
        PKX1 = self._params["PKX1"]  # Longitudinal slip stiffness Kfx/Fz at Fznom
        PKX2 = self._params["PKX2"]  # Variation of slip stiffness Kfx/Fz with load
        PKX3 = self._params["PKX3"]  # Exponent in slip stiffness Kfx/Fz with load
        PHX1 = self._params["PHX1"]  # Horizontal shift Shx at Fznom
        PHX2 = self._params["PHX2"]  # Variation of shift Shx with load
        PVX1 = self._params["PVX1"]  # Vertical shift Svx/Fz at Fznom
        PVX2 = self._params["PVX2"]  # Variation of shift Svx/Fz with load

        epsilonx = self._params["epsilonx"]

        dfz = incrVar["dfz"]

        LMUX_star = starVar["LMUX_star"]
        LMUX_prime = primeVar["LMUX_prime"]

        # NOTE: we ignore turn slip
        zeta1 = 1.0

        # Longitudinal force (pure longitudinal slip, alpha = 0)
        Cx = PCX1 * LCX  # (> 0) (4.E11)
        # NOTE: here for mux and Kxk we ignore inflation pressure effects which are only
        # in MF6.1 (PPX1, 2, 3, 4...)
        mux = (PDX1 + PDX2 * dfz) * (1 - PDX3 * gamma**2) * LMUX_star  # (4.E13)
        # TODO: here we don't ensure Dx is not -ve. But neither does MFeval
        # (-ve Dx should only happen when Fz is -ve or if mux is -ve, as zeta1=1.0)
        Dx = mux * Fz * zeta1  # (> 0) (4.E12)
        Kxk = (
            Fz * (PKX1 + PKX2 * dfz) * lnp.exp(PKX3 * dfz) * LKX
        )  # (= BxCxDx = dFxo./dkx at kappax = 0) (= Cfk) (4.E15)

        # NOTE: here we ignore the sign(Dx) part muliplied on epsilonx.
        Bx = Kxk / (
            Cx * Dx + epsilonx * lnp.sign(Dx)
        )  # (4.E16) [sign(Dx) term explained on page 177]
        SHx = (PHX1 + PHX2 * dfz) * LHX  # (4.E17)
        SVx = Fz * (PVX1 + PVX2 * dfz) * LVX * LMUX_prime * zeta1  # (4.E18)

        # NOTE: here we ignore the low speed model part in MFeval

        kappax = kappa + SHx  # (4.E10)

        # NOTE: here we ignore the linear transient part in MFeval

        # Ex is a function of sign(kappa)
        # TODO: here we have a discontinous function lnp.sign
        # jax: jacobian(jnp.sign)(0.0) -> 0.0, so always 0.0 derivative
        Ex = (
            (PEX1 + PEX2 * dfz + PEX3 * dfz**2) * (1 - PEX4 * lnp.sign(kappax)) * LEX
        )  # (<=1) (4.E14)

        # TODO: here we ignore limit that Ex needs to be <=1 (enforced in MFeval if
        # useLimitsCheck == True
        Ex = lnp.minimum(Ex, 1.0)

        # Pure longitudinal force
        Bx_kappax = Bx * kappax
        Fx0 = (
            Dx
            * lnp.sin(
                Cx * lnp.arctan(Bx_kappax - Ex * (Bx_kappax - lnp.arctan(Bx_kappax)))
            )
            + SVx
        )  # (4.E9)

        return Fx0, mux, Kxk

    def _calculate_Fx(self, kappa, starVar, incrVar, Fx0):
        """Combined slip modifier on top of pure longitudinal slip force.

        See MFeval Solver.calculateFx
        """
        # Longitudinal force (combined slip)

        alpha_star = starVar["alpha_star"]
        gamma_star = starVar["gamma_star"]
        dfz = incrVar["dfz"]

        # [SCALING_COEFFICIENTS]
        LXAL = self._params["LXAL"]  # Scale factor of alpha influence on Fx

        # [LONGITUDINAL_COEFFICIENTS]
        RBX1 = self._params["RBX1"]  # Slope factor for combined slip Fx reduction
        RBX2 = self._params["RBX2"]  # Variation of slope Fx reduction with kappa
        RCX1 = self._params["RCX1"]  # Shape factor for combined slip Fx reduction
        REX1 = self._params["REX1"]  # Curvature factor of combined Fx
        REX2 = self._params["REX2"]  # Curvature factor of combined Fx with load
        RHX1 = self._params["RHX1"]  # Shift factor for combined slip Fx reduction

        Cxa = RCX1  # (4.E55)
        # TODO: here we ignore the limit check on Exa <=1
        # MFeval checks it when useLimitsCheck == True
        Exa = REX1 + REX2 * dfz  # (<= 1) (4.E56)
        Exa = lnp.minimum(Exa, 1.0)

        SHxa = RHX1  # (4.E57)
        # NOTE: here RBX3 effect is ignored as it's only from MF6.1 onwards.
        # TODO: here we ignore the limit check for Bxa > 0 (but MFeval doesn't check it
        # either)
        Bxa = RBX1 * lnp.cos(lnp.arctan(RBX2 * kappa)) * LXAL  # (> 0) (4.E54)

        alphas = alpha_star + SHxa  # (4.E53)

        Bxa_SHxa = Bxa * SHxa
        Gxa0 = lnp.cos(
            Cxa * lnp.arctan(Bxa_SHxa - Exa * (Bxa_SHxa - lnp.arctan(Bxa_SHxa)))
        )  # (4.E52)

        # Gxa is a function of alpha since alphas is a funciton of alpha
        # it's also a function of kappa as Bxa is a function of kappa
        # exa
        # TODO: here we ignore the lmit check on Gxa > 0, which MFeval ignores as well.
        Bxa_alphas = Bxa * alphas
        Gxa = (
            lnp.cos(
                Cxa
                * lnp.arctan(Bxa_alphas - Exa * (Bxa_alphas - lnp.arctan(Bxa_alphas)))
            )
            / Gxa0  # (> 0)(4.E51)
        )

        Fx = Gxa * Fx0  # (4.E50)

        return Fx, Gxa

    def _calculate_Fy0(self, Fz, starVar, primeVar, incrVar):
        """Calculate the lateral tire force for pure lateral slips.

        See MFeval Solver.calculateFy0
        """
        # [SCALING_COEFFICIENTS]
        LCY = self._params["LCY"]  # Scale factor of Fy shape factor
        LEY = self._params["LEY"]  # Scale factor of Fy curvature factor
        LKY = self._params["LKY"]  # Scale factor of Fy cornering stiffness
        LHY = self._params["LHY"]  # Scale factor of Fy horizontal shift
        LVY = self._params["LVY"]  # Scale factor of Fy vertical shift

        # [LATERAL_COEFFICIENTS]
        PCY1 = self._params["PCY1"]  # Shape factor Cfy for lateral forces
        PDY1 = self._params["PDY1"]  # Lateral friction Muy
        PDY2 = self._params["PDY2"]  # Variation of friction Muy with load
        PDY3 = self._params["PDY3"]  # Variation of friction Muy with squared camber
        PEY1 = self._params["PEY1"]  # Lateral curvature Efy at Fznom
        PEY2 = self._params["PEY2"]  # Variation of curvature Efy with load
        PEY3 = self._params["PEY3"]  # Zero order camber dependency of curvature Efy
        PEY4 = self._params["PEY4"]  # Variation of curvature Efy with camber
        PKY1 = self._params["PKY1"]  # Maximum value of stiffness Kfy./Fznom
        PKY2 = self._params["PKY2"]  # Load at which Kfy reaches maximum value
        PKY3 = self._params["PKY3"]  # Variation of Kfy./Fznom with camber
        PHY1 = self._params["PHY1"]  # Horizontal shift Shy at Fznom
        PHY2 = self._params["PHY2"]  # Variation of shift Shy with load
        PHY3 = self._params["PHY3"]  # Variation of shift Shy with camber
        PVY1 = self._params["PVY1"]  # Vertical shift in Svy./Fz at Fznom
        PVY2 = self._params["PVY2"]  # Variation of shift Svy./Fz with load
        PVY3 = self._params["PVY3"]  # Variation of shift Svy./Fz with camber
        PVY4 = self._params["PVY4"]  # Variation of shift Svy./Fz with camber and load

        # NOTE: we only keep the branch for useTurnSlip == False
        # No turn slip and small camber angles
        # First paragraph on page 178 of the book
        zeta0 = 1.0
        zeta2 = 1.0
        zeta3 = 1.0
        zeta4 = 1.0

        epsilony = self._params["epsilony"]

        dfz = incrVar["dfz"]

        LMUY_star = starVar["LMUY_star"]
        alpha_star = starVar["alpha_star"]
        gamma_star = starVar["gamma_star"]

        LMUY_prime = primeVar["LMUY_prime"]
        Fz0_prime = primeVar["Fz0_prime"]

        # TODO: here we need smooth abs
        abs_gamma_star = lnp.abs(gamma_star)

        # NOTE: here we exclude the PPY1 factors (inflation pressure) and PKY4(curvature
        # of stiffness Kya) and PKY5(peak stiffness variation with camber squared)
        # which are only available in MF6.1
        Kya = (
            PKY1
            * Fz0_prime
            * (1 - PKY3 * abs_gamma_star)
            * lnp.sin(2 * lnp.arctan(Fz / Fz0_prime / PKY2))
            * zeta3
            * LKY
        )  # (= ByCyDy = dFyo./dalphay at alphay = 0) (if gamma =0: =Kya0 = CFa)
        # Based on (4.E25), it is equivalent to PKY4

        # NOTE: no LKYC (camber force stiffness scaling factor), MF6.1 only.
        SVyg = Fz * (PVY3 + PVY4 * dfz) * gamma_star * LMUY_prime * zeta2  # (4.E28)

        # NOTE: Ignored Kya0 and Kyg0 computaiton as they are only used for turn slip
        # and MF6.1 related computations

        # MF5.2 branch of MFeval, From the MF-Tyre equation manual
        SHy = (PHY1 + PHY2 * dfz) * LHY + PHY3 * gamma_star

        SVy = Fz * (PVY1 + PVY2 * dfz) * LVY * LMUY_prime * zeta2 + SVyg  # (4.E29)

        alphay = alpha_star + SHy  # (4.E20)
        Cy = PCY1 * LCY  # (> 0) (4.E21)
        # NOTE: ignore PPY4 and PPY4 effect, MF6.1 only
        muy = (PDY1 + PDY2 * dfz) * (1 - PDY3 * gamma_star**2) * LMUY_star  # (4.E23)
        Dy = muy * Fz * zeta2  # (4.E22)

        # TODO: smoothen sign
        sign_alphay = lnp.sign(alphay)

        # NOTE: ignore PEY4 and PEY5 (effects w.r.t. camber), MF6.1 only
        Ey = (
            (PEY1 + PEY2 * dfz) * (1 - (PEY3 + PEY4 * gamma_star) * sign_alphay) * LEY
        )  # (<=1)(4.E24)
        # TODO: smoothen min
        Ey = lnp.minimum(Ey, 1.0)

        signDy = lnp.sign(Dy)
        # NOTE: ignored assigning signDy[signDy==0] = 1
        By = Kya / (
            Cy * Dy + epsilony * signDy
        )  # (4.E26) [sign(Dy) term explained on page 177]

        # Pure lateral force
        Fy0 = (
            Dy
            * lnp.sin(
                Cy
                * lnp.arctan(By * alphay - Ey * (By * alphay - lnp.arctan(By * alphay)))
            )
            + SVy
        )  # (4.E19)

        return Fy0, muy, Kya, SHy, SVy, By, Cy

    def calcluate_Fy(self, Fz, kappa, Fy0, muy, starVar, incrVar):
        """Combined slip force on top of pure lateral slip force

        See MFeval Solver.calculateFy
        """
        # [SCALING_COEFFICIENTS]
        LYKA = self._params["LYKA"]  # Scale factor of alpha influence on Fx
        LVYKA = self._params["LVYKA"]  # Scale factor of kappa induced Fy

        alpha_star = starVar["alpha_star"]
        gamma_star = starVar["gamma_star"]
        dfz = incrVar["dfz"]

        # NOTE: no turn slip
        zeta2 = 1.0

        # [LATERAL_COEFFICIENTS]
        RBY1 = self._params["RBY1"]  # Slope factor for combined Fy reduction
        RBY2 = self._params["RBY2"]  # Variation of slope Fy reduction with alpha
        RBY3 = self._params["RBY3"]  # Shift term for alpha in slope Fy reduction
        RCY1 = self._params["RCY1"]  # Shape factor for combined Fy reduction
        REY1 = self._params["REY1"]  # Curvature factor of combined Fy
        REY2 = self._params["REY2"]  # Curvature factor of combined Fy with load
        RHY1 = self._params["RHY1"]  # Shift factor for combined Fy reduction
        RHY2 = self._params["RHY2"]  # Shift factor for combined Fy reduction with load
        RVY1 = self._params["RVY1"]  # Kappa induced side force Svyk/muy*Fz at Fznom
        RVY2 = self._params["RVY2"]  # Variation of Svyk/muy*Fz with load
        RVY3 = self._params["RVY3"]  # Variation of Svyk/muy*Fz with camber
        RVY4 = self._params["RVY4"]  # Variation of Svyk/muy*Fz with alpha
        RVY5 = self._params["RVY5"]  # Variation of Svyk/muy*Fz with kappa
        RVY6 = self._params["RVY6"]  # Variation of Svyk/muy*Fz with atan(kappa)

        DVyk = (
            muy
            * Fz
            * (RVY1 + RVY2 * dfz + RVY3 * gamma_star)
            * lnp.cos(lnp.arctan(RVY4 * alpha_star))
            * zeta2
        )  # (4.E67)
        SVyk = DVyk * lnp.sin(RVY5 * lnp.arctan(RVY6 * kappa)) * LVYKA  # (4.E66)
        SHyk = RHY1 + RHY2 * dfz  # (4.E65)
        Eyk = REY1 + REY2 * dfz  # (<=1) (4.E64)

        # TODO: smoothen minimum func
        Eyk = lnp.minimum(Eyk, 1.0)

        Cyk = RCY1  # (4.E63)
        Byk = (
            RBY1 * lnp.cos(lnp.arctan(RBY2 * (alpha_star - RBY3))) * LYKA
        )  # (>0) (4.E62)
        # NOTE: Byk should be > 0, but MFeval did not enforce it.

        kappas = kappa + SHyk  # (4.E61)

        Byk_SHyk = Byk * SHyk
        Gyk0 = lnp.cos(
            Cyk * lnp.arctan(Byk_SHyk - Eyk * (Byk_SHyk - lnp.arctan(Byk_SHyk)))
        )  # (4.E60)

        Byk_kappas = Byk * kappas
        Gyk = (
            lnp.cos(
                Cyk
                * lnp.arctan(Byk_kappas - Eyk * (Byk_kappas - lnp.arctan(Byk_kappas)))
            )
            / Gyk0
        )  # (> 0)(4.E59)

        # NOTE: Gyk should be > 0, but MFeval did not enforce it
        Fy = Gyk * Fy0 + SVyk  # (4.E58)

        return Fy, Gyk, SVyk

    def _calculate_Mz(
        self,
        kappa,
        alpha,
        gamma,
        Fz,
        vx,
        Fx,
        Kxk,
        Fy,
        lat_coeff,
        starVar,
        primeVar,
        incrVar,
    ):
        """Calculate the self-aligning torque for combined slips.

        We have combined two funtions from MFeval into one.

        See MFEval Solver.calculateMz0 and Solver.calculateMz
        """

        epsilonk = self._params["epsilonk"]

        Kya = lat_coeff["Kya"]
        SHy = lat_coeff["SHy"]
        SVy = lat_coeff["SVy"]
        SVyk = lat_coeff["SVyk"]
        By = lat_coeff["By"]
        Cy = lat_coeff["Cy"]

        dfz = incrVar["dfz"]

        LMUY_star = starVar["LMUY_star"]

        Fz0_prime = primeVar["Fz0_prime"]
        alpha_prime = primeVar["alpha_prime"]

        # [DIMENSION]
        R0 = self._params["UNLOADED_RADIUS"]  # Free tire radius

        # [VERTICAL]
        Fz0 = self._params["FNOMIN"]  # Nominal wheel load

        # [SCALING_COEFFICIENTS]
        LKY = self._params["LKY"]  # Scale factor of Fy cornering stiffness
        LTR = self._params["LTR"]  # Scale factor of peak of pneumatic trail
        LRES = self._params["LRES"]  # Scale factor for offset of residual torque
        LS = self._params["LS"]  # Scale factor of lever arm of Fx
        LFZO = self._params["LFZO"]  # Scale factor of nominal (rated) load

        # [ALIGNING_COEFFICIENTS]
        QBZ1 = self._params["QBZ1"]  # Trail slope factor for trail Bpt at Fznom
        QBZ2 = self._params["QBZ2"]  # Variation of slope Bpt with load
        QBZ3 = self._params["QBZ3"]  # Variation of slope Bpt with load squared
        QBZ4 = self._params["QBZ4"]  # Variation of slope Bpt with camber
        QBZ5 = self._params["QBZ5"]  # Variation of slope Bpt with absolute camber
        QBZ9 = self._params["QBZ9"]  # Factor for scaling factors of Br of Mzr
        QBZ10 = self._params["QBZ10"]  # Factor for corner. stiff. of Br of Mzr
        QCZ1 = self._params["QCZ1"]  # Shape factor Cpt for pneumatic trail
        QDZ1 = self._params["QDZ1"]  # Peak trail Dpt = Dpt*(Fz/Fznom.*R0)
        QDZ2 = self._params["QDZ2"]  # Variation of peak Dpt" with load
        QDZ3 = self._params["QDZ3"]  # Variation of peak Dpt" with camber
        QDZ4 = self._params["QDZ4"]  # Variation of peak Dpt" with camber squared
        QDZ6 = self._params["QDZ6"]  # Peak residual torque Dmr" = Dmr/(Fz*R0)
        QDZ7 = self._params["QDZ7"]  # Variation of peak factor Dmr" with load
        QDZ8 = self._params["QDZ8"]  # Variation of peak factor Dmr" with camber
        QDZ9 = self._params[
            "QDZ9"
        ]  # Variation of peak factor Dmr" with camber and load
        QEZ1 = self._params["QEZ1"]  # Trail curvature Ept at Fznom
        QEZ2 = self._params["QEZ2"]  # Variation of curvature Ept with load
        QEZ3 = self._params["QEZ3"]  # Variation of curvature Ept with load squared
        QEZ4 = self._params["QEZ4"]  # Variation of curvature Ept with sign of Alpha-t
        QEZ5 = self._params["QEZ5"]  # Variation of Ept with camber and sign Alpha-t
        QHZ1 = self._params["QHZ1"]  # Trail horizontal shift Sht at Fznom
        QHZ2 = self._params["QHZ2"]  # Variation of shift Sht with load
        QHZ3 = self._params["QHZ3"]  # Variation of shift Sht with camber
        QHZ4 = self._params["QHZ4"]  # Variation of shift Sht with camber and load
        SSZ1 = self._params["SSZ1"]  # Nominal value of s/R0: effect of Fx on Mz
        SSZ2 = self._params["SSZ2"]  # Variation of distance s/R0 with Fy/Fznom
        SSZ3 = self._params["SSZ3"]  # Variation of distance s/R0 with camber
        SSZ4 = self._params["SSZ4"]  # Variation of distance s/R0 with load and camber

        SHt = QHZ1 + QHZ2 * dfz + (QHZ3 + QHZ4 * dfz) * gamma  # (4.E35)

        # TODO: need to smoothen sign and avoid divide by zero when kya=0
        sign_Kya = lnp.sign(Kya)
        # sign_Kya = (Kya + eps_Kya) / lnp.sqrt((Kya + eps_Kya) ** 2 + eps_Kya)

        Kya_prime = Kya + epsilonk * sign_Kya  # (4.E39)
        SHf = SHy + SVy / Kya_prime  # (4.E38)
        alphar = alpha + SHf  # = alphaf (4.E37)
        alphat = alpha + SHt  # (4.E34)

        # IMPORTANT NOTE: The above original equation (4.E43) was not matching the
        # TNO solver. The coefficient Dt affects the pneumatic trail (t) and the
        # self aligning torque (Mz).
        # It was observed that when negative inclination angles where used as
        # inputs, there was a discrepancy between the TNO solver and mfeval.
        # This difference comes from the term QDZ3, that in the original equation
        # is multiplied by abs(gamma_star). But in the paper the equation is
        # different and the abs() term is not written. Equation (A60) from the
        # paper resulted into a perfect match with TNO.
        # Keep in mind that the equations from the paper don't include turn slip
        # effects. The term zeta5 has been added although it doesn't appear in the
        # paper.

        # Paper definition:
        Dt = (
            (QDZ1 + QDZ2 * dfz)
            * (1 + QDZ3 * gamma + QDZ4 * gamma**2)
            * Fz
            * (R0 / Fz0_prime)
            * LTR
        )  # (A60)

        # TODO: smoothen abs
        abs_gamma = lnp.abs(gamma)

        # IMPORTANT NOTE: In the original equation (4.E40) it is used the
        # parameter QBZ6, which doesn't exist in the standard TIR files. Also note
        # that on page 190 and 615 of the book a full set of parameters is given
        # and QBZ6 doesn't appear.
        # The equation has been replaced with equation (A58) from the paper.
        # Paper definition
        Bt = (
            (QBZ1 + QBZ2 * dfz + QBZ3 * dfz**2)
            * (1 + QBZ4 * gamma + QBZ5 * abs_gamma)
            * LKY
            / LMUY_star
        )  # (> 0) (A58)

        Ct = QCZ1  # (> 0) (4.E41)
        Et = (QEZ1 + QEZ2 * dfz + QEZ3 * dfz**2) * (
            1 + (QEZ4 + QEZ5 * gamma) * (2.0 / lnp.pi) * lnp.arctan(Bt * Ct * alphat)
        )  # (<=1) (4.E44)

        # NOTE: zeta values from the non-turnslip branch
        zeta0 = 1.0
        zeta2 = 1.0
        zeta6 = 1.0
        zeta7 = 1.0
        zeta8 = 1.0

        # TODO: smoothen this sign
        sign_Vcx = lnp.sign(vx)
        # NOTE: ommit QDZ10, QDZ11, LKZC terms: MF6.1 only
        Dr = (
            (
                Fz
                * R0
                * (
                    (QDZ6 + QDZ7 * dfz) * LRES * zeta2
                    + (QDZ8 + QDZ9 * dfz) * gamma * zeta0
                )
                * LMUY_star
                * sign_Vcx
                * lnp.cos(alpha)
            )
            + zeta8
            - 1.0
        )  # (4.E47)
        Br = (
            QBZ9 * LKY / LMUY_star + QBZ10 * By * Cy
        ) * zeta6  # preferred QBZ9=0 (4.E45)
        Cr = zeta7  # (4.E46)

        # Equations from here onwards are from "calculateMz"

        # IMPORTANT Note: The equations 4.E78 and 4.E77 are not used due to small
        # differences discovered at negative camber angles with the TNO solver.
        # Instead equations A54 and A55 from the paper are used.

        # IMPORTANT Note: The coefficient "s" (Equation 4.E76) determines the
        # effect of Fx into Mz. The book uses "Fz0_prime" in the formulation,
        # but the paper uses "Fz0". The equation (A56) from the paper has a better
        # correlation with TNO.

        # TODO: smooth these sign functions
        sign_alphar = lnp.sign(alphar)
        sign_alphat = lnp.sign(alphat)

        alphar_eq = (
            lnp.arctan(
                lnp.sqrt(lnp.tan(alphar) ** 2 + (Kxk / Kya_prime) ** 2 * kappa**2)
            )
            * sign_alphar
        )  # (A54)

        alphat_eq = (
            lnp.arctan(
                lnp.sqrt(lnp.tan(alphat) ** 2 + (Kxk / Kya_prime) ** 2 * kappa**2)
            )
            * sign_alphat
        )  # (A55)

        # Lever arm of Fx on Mz
        s = R0 * (SSZ1 + SSZ2 * (Fy / Fz0) + (SSZ3 + SSZ4 * dfz) * gamma) * LS  # (A56)
        # Residual torque: aligning torque component from conicity and camber
        Mzr = Dr * lnp.cos(Cr * lnp.arctan(Br * alphar_eq))  # (4.E75)

        # NOTE: here we omit Fy_prime computation which is not reqruied for MF5.2. In
        # MF6.1 and 6.2, the Fy and Fy0 needs to be computed at zero camber in these
        # computatino ommited.

        # Pneumatic trail
        t = (
            Dt
            * lnp.cos(
                Ct
                * lnp.arctan(
                    Bt * alphat_eq - Et * (Bt * alphat_eq - lnp.arctan(Bt * alphat_eq))
                )
            )
            * lnp.cos(alpha_prime)
        )  # (4.E73)

        # IMPORTANT NOTE: the equation below is not written in any source, but "t"
        # is multiplied by LFZO in the TNO dteval function. This has been empirically
        # discovered.
        t = LFZO * t

        # MF5.2 equations
        Mz = -t * (Fy - SVyk) + Mzr + s * Fx  # From the MF-Tire equation manual

        return Mz

    def _calculate_My(self, Fz, vx, Fx):
        """Calculate the rolling reistance moment of the tire.

        In MF5.2, this is a function of vx and Fz only.

        See MFeval Solver.calculateMy
        """
        Vcx = vx

        # [MODEL]
        V0 = self._params["LONGVL"]  # Nominal speed

        # [VERTICAL]
        Fz0 = self._params["FNOMIN"]  # Nominal wheel load

        # [DIMENSION]
        R0 = self._params["UNLOADED_RADIUS"]  # Free tire radius

        # [SCALING_COEFFICIENTS]
        LMY = self._params["LMY"]  #  Scale factor of rolling resistance torque

        # [ROLLING_COEFFICIENTS]
        QSY1 = self._params["QSY1"]  # Rolling resistance torque coefficient
        QSY2 = self._params["QSY2"]  # Rolling resistance torque depending on Fx
        QSY3 = self._params["QSY3"]  # Rolling resistance torque depending on speed
        QSY4 = self._params["QSY4"]  # Rolling resistance torque depending on speed^4

        # NOTE: only MF5.2 part from MFeval implemented here
        # NOTE: abs(Vcx/V0) has its 'abs' removed as we only consider forward running
        My = (
            -R0
            * Fz
            * LMY
            * (QSY1 + QSY2 * (Fx / Fz0) + QSY3 * (Vcx / V0) + QSY4 * (Vcx / V0) ** 4)
        )  # From the MF-Tire equation manual

        return My

    def _calculate_Mx(self, gamma, Fz, Fy):
        """Calculate the overturning moment of the tire.

        See MFeval Solver.calculateMx
        """

        # [VERTICAL]
        Fz0 = self._params["FNOMIN"]  # Nominal wheel load

        # [DIMENSION]
        R0 = self._params["UNLOADED_RADIUS"]  # Free tire radius

        # [SCALING_COEFFICIENTS]
        LVMX = self._params["LVMX"]  #  Scale factor of Mx vertical shift
        LMX = self._params["LMX"]  #  Scale factor of overturning couple

        # [OVERTURNING_COEFFICIENTS]
        QSX1 = self._params["QSX1"]  # Vertical shift of overturning moment
        QSX2 = self._params["QSX2"]  # Camber induced overturning couple
        QSX3 = self._params["QSX3"]  # Fy induced overturning couple

        # NOTE: only the TNO equations in MFeval, but without all effects after QSX3,
        # which are MF6.1 only
        Mx = R0 * Fz * LMX * (QSX1 * LVMX - QSX2 * gamma + QSX3 * (Fy / Fz0))

        return Mx
