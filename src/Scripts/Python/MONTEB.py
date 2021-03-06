import numpy as np
import math
from SORT import SORT


def MONTEB(Magboltz):
    
    STO = np.zeros(2000000)
    XST = np.zeros(2000000)
    YST = np.zeros(2000000)
    ZST = np.zeros(2000000)
    DFZZST = np.zeros(10)
    DFXXST = np.zeros(10)
    DFYYST = np.zeros(10)
    DFYZST = np.zeros(10)
    DFLNST = np.zeros(10)
    DFTRST = np.zeros(10)
    WZST = np.zeros(10)
    WYST = np.zeros(10)
    AVEST = np.zeros(10)
    TEMP = np.zeros(4000)
    for J in range(4000):
        TEMP[J] = Magboltz.TCF[J] + Magboltz.TCFN[J]

    Magboltz.WX = 0.0
    Magboltz.DWX = 0.0
    Magboltz.X = 0.0
    Magboltz.Y = 0.0
    Magboltz.Z = 0.0
    Magboltz.DIFXZ = 0.0
    Magboltz.DIFXY = 0.0
    Magboltz.DXZER = 0.0
    Magboltz.DXYER = 0.0
    Magboltz.ST = 0.0
    ST1 = 0.0
    ST2 = 0.0
    SUMXX = 0.0
    SUMYY = 0.0
    SUMZZ = 0.0
    SUMYZ = 0.0
    SUMLS = 0.0
    I=0
    SUMTS = 0.0
    SUMVX = 0.0
    ZOLD = 0.0
    YOLD = 0.0
    STOLD = 0.0
    ST1OLD = 0.0
    ST2OLD = 0.0
    SZZOLD = 0.0
    SXXOLD = 0.0
    SYYOLD = 0.0
    SYZOLD = 0.0
    SVXOLD = 0.0
    SLNOLD = 0.0
    STROLD = 0.0
    EBAROLD = 0.0
    Magboltz.SMALL = 1e-20
    Magboltz.TMAX1 = 0.0
    EF100 = Magboltz.EFIELD * 100
    E1 = Magboltz.ESTART
    INTEM = 8
    Magboltz.ITMAX = 10
    ID = 0
    NCOL = 0
    Magboltz.NNULL = 0
    IEXTRA = 0
    TDASH = 0.0
    CONST9 = Magboltz.CONST3 * 0.01

    ABSFAKEI = Magboltz.FAKEI
    Magboltz.IFAKE = 0

    F4 = 2 * math.acos(-1)
    DCZ1 = math.cos(Magboltz.THETA)
    DCX1 = math.sin(Magboltz.THETA) * math.cos(Magboltz.PHI)
    DCY1 = math.sin(Magboltz.THETA) * math.sin(Magboltz.PHI)

    VTOT = CONST9 * math.sqrt(E1)
    CX1 = DCX1 * VTOT
    CY1 = DCY1 * VTOT
    CZ1 = DCZ1 * VTOT

    J2M = Magboltz.NMAX / Magboltz.ITMAX

    DELTAE = Magboltz.EFINAL / float(INTEM)

    for J1 in range(int(Magboltz.ITMAX)):
        for J2 in range(int(J2M)):
            while True:
                R1 = Magboltz.RAND48.drand()
                I = int(E1 / DELTAE) + 1
                I = min(I, INTEM) - 1
                TLIM = Magboltz.TCFMAX[I]
                T = -1 * np.log(R1) / TLIM + TDASH
                TDASH = T
                WBT = Magboltz.WB * T
                COSWT = math.cos(WBT)
                SINWT = math.sin(WBT)
                DZ = (CZ1 * SINWT + (Magboltz.EOVB - CY1) * (1 - COSWT)) / Magboltz.WB
                E = E1 + DZ * EF100
                IE = int(E / Magboltz.ESTEP)
                IE = min(IE, 3999)
                if TEMP[IE] > TLIM:
                    TDASH += np.log(R1) / TLIM
                    Magboltz.TCFMAX[I] *= 1.05
                    continue

                R5 = Magboltz.RAND48.drand()
                TEST1 = Magboltz.TCF[IE] / TLIM

                if R5 > TEST1:
                    Magboltz.NNULL += 1
                    TEST2 = TEMP[IE] / TLIM
                    if R5 < TEST2:
                        if Magboltz.NPLAST == 0:
                            continue
                        R2 = Magboltz.RAND48.drand()
                        I = 0
                        while Magboltz.CFN[IE][I] < R2:
                            I += 1

                        Magboltz.ICOLNN[I] += 1
                        continue
                    else:
                        TEST3 = (TEMP[IE] + ABSFAKEI) / TLIM
                        if R5 < TEST3:
                            # FAKE IONISATION INCREMENT COUNTER
                            Magboltz.IFAKE += 1
                            continue
                        continue
                else:
                    break
            T2 = T ** 2
            if (T >= Magboltz.TMAX1):
                Magboltz.TMAX1 = T
            TDASH = 0.0
            CX2 = CX1
            CY2 = (CY1 - Magboltz.EOVB) * COSWT + CZ1 * SINWT + Magboltz.EOVB
            CZ2 = CZ1 * COSWT - (CY1 - Magboltz.EOVB) * SINWT
            VTOT = math.sqrt(CX2 ** 2 + CY2 ** 2 + CZ2 ** 2)
            DCX2 = CX2 / VTOT
            DCY2 = CY2 / VTOT
            DCZ2 = CZ2 / VTOT
            NCOL += 1

            Magboltz.X += CX1 * T
            Magboltz.Y += Magboltz.EOVB * T + ((CY1 - Magboltz.EOVB) * SINWT + CZ1 * (1 - COSWT)) / Magboltz.WB
            Magboltz.Z += DZ
            Magboltz.ST += T
            IT = int(T)
            IT = min(IT, 299)
            Magboltz.TIME[IT] += 1
            Magboltz.SPEC[IE] += 1
            Magboltz.WZ = Magboltz.Z / Magboltz.ST
            Magboltz.WY = Magboltz.Y / Magboltz.ST
            SUMVX += (CX1 ** 2) * T2
            if ID != 0:
                KDUM = 0
                for J in range(int(Magboltz.NCORST)):
                    ST2 = ST2 + T
                    NCOLDM = NCOL + KDUM
                    if NCOLDM > Magboltz.NCOLM:
                        NCOLDM = NCOLDM - Magboltz.NCOLM
                    SDIF = Magboltz.ST - STO[NCOLDM]
                    SUMXX += ((Magboltz.X - XST[NCOLDM]) ** 2) * T / SDIF
                    KDUM += Magboltz.NCORLN
                    if J1 >= 2:
                        ST1 += T
                        SUMZZ += ((Magboltz.Z - ZST[NCOLDM] - Magboltz.WZ * SDIF) ** 2) * T / SDIF
                        SUMYY += ((Magboltz.Y - YST[NCOLDM] - Magboltz.WY * SDIF) ** 2) * T / SDIF
                        SUMYZ += (Magboltz.Z - ZST[NCOLDM] - Magboltz.WZ * SDIF) * (
                                Magboltz.Y - YST[NCOLDM] - Magboltz.WY * SDIF) * T / SDIF
                        A2 = (Magboltz.WZ * SDIF) ** 2 + (Magboltz.WY * SDIF) ** 2
                        B2 = (Magboltz.Z - Magboltz.WZ * SDIF - ZST[NCOLDM]) ** 2 + (
                                Magboltz.Y - Magboltz.WY * SDIF - YST[NCOLDM]) ** 2
                        C2 = (Magboltz.Z - ZST[NCOLDM]) ** 2 + (Magboltz.Y - YST[NCOLDM]) ** 2
                        DL2 = (A2 + B2 - C2) ** 2 / (4 * A2)
                        DT2 = B2 - DL2
                        SUMLS += DL2 * T / SDIF
                        SUMTS += DT2 * T / SDIF
            XST[NCOL] = Magboltz.X
            YST[NCOL] = Magboltz.Y
            ZST[NCOL] = Magboltz.Z
            STO[NCOL] = Magboltz.ST
            if NCOL >= Magboltz.NCOLM:
                ID += 1
                Magboltz.XID = float(ID)
                NCOL = 0
            R2 = Magboltz.RAND48.drand()

            I = SORT(I, R2, IE, Magboltz)

            while Magboltz.CF[IE][I] < R2:
                I += 1
            S1 = Magboltz.RGAS[I]
            EI = Magboltz.EIN[I]
            if Magboltz.IPN[I] > 0:
                R9 = Magboltz.RAND48.drand()
                EXTRA = R9 * (E - EI)
                EI = EXTRA + EI
                IEXTRA += Magboltz.NC0[I]
            IPT = Magboltz.IARRY[I]
            Magboltz.ICOLL[int(IPT)] += 1
            Magboltz.ICOLN[I] += 1
            if E < EI:
                EI = E - 0.0001

            if Magboltz.IPEN != 0:
                if Magboltz.PENFRA[0][I] != 0:
                    RAN = Magboltz.RAND48.drand()
                    if RAN <= Magboltz.PENFRA[0][I]:
                        IEXTRA += 1
            S2 = (S1 ** 2) / (S1 - 1.0)

            R3 = Magboltz.RAND48.drand()
            if Magboltz.INDEX[I] == 1:
                R31 = Magboltz.RAND48.drand()
                F3 = 1.0 - R3 * Magboltz.ANGCT[IE][I]
                if R31 > Magboltz.PSCT[IE][I]:
                    F3 = -1 * F3
            elif Magboltz.INDEX[I] == 2:
                EPSI = Magboltz.PSCT[IE][I]
                F3 = 1 - (2 * R3 * (1 - EPSI) / (1 + EPSI * (1 - 2 * R3)))
            else:
                F3 = 1 - 2 * R3
            THETA0 = math.acos(F3)
            R4 = Magboltz.RAND48.drand()
            PHI0 = F4 * R4
            F8 = math.sin(PHI0)
            F9 = math.cos(PHI0)
            ARG1 = 1 - S1 * EI / E
            ARG1 = max(ARG1, Magboltz.SMALL)
            D = 1 - F3 * math.sqrt(ARG1)
            E1 = E * (1 - EI / (S1 * E) - 2 * D / S2)
            E1 = max(E1, Magboltz.SMALL)
            Q = math.sqrt((E / E1) * ARG1) / S1
            Q = min(Q, 1)
            Magboltz.THETA = math.asin(Q * math.sin(THETA0))
            F6 = math.cos(Magboltz.THETA)
            U = (S1 - 1) * (S1 - 1) / ARG1
            CSQD = F3 * F3
            if F3 < 0 and CSQD > U:
                F6 = -1 * F6
            F5 = math.sin(Magboltz.THETA)
            DCZ2 = min(DCZ2, 1)
            ARGZ = math.sqrt(DCX2 * DCX2 + DCY2 * DCY2)
            if ARGZ == 0:
                DCZ1 = F6
                DCX1 = F9 * F5
                DCY1 = F8 * F5
            else:
                DCZ1 = DCZ2 * F6 + ARGZ * F5 * F8
                DCY1 = DCY2 * F6 + (F5 / ARGZ) * (DCX2 * F9 - DCY2 * DCZ2 * F8)
                DCX1 = DCX2 * F6 - (F5 / ARGZ) * (DCY2 * F9 + DCX2 * DCZ2 * F8)
            CX1 = DCX1 * VTOT
            CY1 = DCY1 * VTOT
            CZ1 = DCZ1 * VTOT

        Magboltz.WZ *= 1e9
        Magboltz.WY *= 1e9
        if ST2 != 0.0:
            Magboltz.DIFXX = 5e15 * SUMXX / ST2
        if ST1 != 0.0:
            Magboltz.DIFZZ = 5e15 * SUMZZ / ST1
            Magboltz.DIFYY = 5e15 * SUMYY / ST1
            Magboltz.DIFYZ = -5e15 * SUMYZ / ST1
            Magboltz.DIFLN = 5e15 * SUMLS / ST1
            Magboltz.DIFTR = 5e15 * SUMTS / ST1
        if Magboltz.NISO == 0:
            Magboltz.DIFXX = 5e15 * SUMVX / Magboltz.ST
        EBAR = 0.0
        for IK in range(4000):
            EBAR += Magboltz.ES[IK] * Magboltz.SPEC[IK] / Magboltz.TCF[IK]
        Magboltz.AVE = EBAR / Magboltz.ST
        WZST[J1] = (Magboltz.Z - ZOLD) / (Magboltz.ST - STOLD) * 1e9
        WYST[J1] = (Magboltz.Y - YOLD) / (Magboltz.ST - STOLD) * 1e9
        AVEST[J1] = (EBAR - EBAROLD) / (Magboltz.ST - STOLD)
        EBAROLD = EBAR
        DFZZST[J1] = 0.0
        DFYYST[J1] = 0.0
        DFYZST[J1] = 0.0
        DFLNST[J1] = 0.0
        DFTRST[J1] = 0.0
        if J1 > 1:
            DFZZST[J1] = 5e15 * (SUMZZ - SZZOLD) / (ST1 - ST1OLD)
            DFYYST[J1] = 5e15 * (SUMYY - SYYOLD) / (ST1 - ST1OLD)
            DFYZST[J1] = 5e15 * (SUMYZ - SYZOLD) / (ST1 - ST1OLD)
            DFLNST[J1] = 5e15 * (SUMLS - SLNOLD) / (ST1 - ST1OLD)
            DFTRST[J1] = 5e15 * (SUMTS - STROLD) / (ST1 - ST1OLD)
        DFXXST[J1] = 5e15 * (SUMXX - SXXOLD) / (ST2 - ST2OLD)
        if Magboltz.NISO == 0:
            DFXXST[J1] = 5e15 * (SUMVX - SVXOLD) / (Magboltz.ST - STOLD)
        ZOLD = Magboltz.Z
        YOLD = Magboltz.Y
        STOLD = Magboltz.ST
        ST1OLD = ST1
        ST2OLD = ST2
        SVXOLD = SUMVX
        SZZOLD = SUMZZ
        SXXOLD = SUMXX
        SYYOLD = SUMYY
        SYZOLD = SUMYZ
        SLNOLD = SUMLS
        STROLD = SUMTS
    TWZST = 0.0
    TWYST = 0.0
    TAVE = 0.0
    T2WZST = 0.0
    T2WYST = 0.0
    T2AVE = 0.0
    TZZST = 0.0
    TYYST = 0.0
    TXXST = 0.0
    TYZST = 0.0
    TLNST = 0.0
    TTRST = 0.0
    T2ZZST = 0.0
    T2YYST = 0.0
    T2XXST = 0.0
    T2YZST = 0.0
    T2LNST = 0.0
    T2TRST = 0.0

    for K in range(10):
        TWZST = TWZST + WZST[K]
        TWYST = TWYST + WYST[K]
        TAVE = TAVE + AVEST[K]
        T2WZST = T2WZST + WZST[K] * WZST[K]
        T2WYST = T2WYST + WYST[K] * WYST[K]
        T2AVE = T2AVE + AVEST[K] * AVEST[K]
        TXXST += DFXXST[K]
        T2XXST += DFXXST ** 2
        if K >= 2:
            TZZST = TZZST + DFZZST[K]
            TYYST = TYYST + DFYYST[K]
            TYZST = TYZST + DFYZST[K]
            TLNST = TLNST + DFLNST[K]
            TTRST = TTRST + DFTRST[K]
            T2ZZST += DFZZST[K] ** 2
            T2YYST += DFYYST[K] ** 2
            T2YZST += DFYZST[K] ** 2
            T2LNST += DFLNST[K] ** 2
            T2TRST += DFTRST[K] ** 2
    Magboltz.DWZ = 100 * math.sqrt((T2WZST - TWZST * TWZST / 10.0) / 9.0) / Magboltz.WZ
    Magboltz.DWY = 100 * math.sqrt((T2WYST - TWYST * TWYST / 10.0) / 9.0) / abs(Magboltz.WY)
    Magboltz.DEN = 100 * math.sqrt((T2AVE - TAVE * TAVE / 10.0) / 9.0) / Magboltz.AVE
    Magboltz.DXXER = 100 * math.sqrt((T2XXST - TXXST * TXXST / 10.0) / 9.0) / Magboltz.DIFXX
    Magboltz.DYYER = 100 * math.sqrt((T2YYST - TYYST * TYYST / 10.0) / 9.0) / Magboltz.DIFYY
    Magboltz.DZZER = 100 * math.sqrt((T2ZZST - TZZST * TZZST / 8.0) / 7.0) / Magboltz.DIFZZ
    Magboltz.DYZER = 100 * math.sqrt((T2YZST - TYZST * TYZST / 8.0) / 7.0) / abs(Magboltz.DIFYZ)
    Magboltz.DFLER = 100 * math.sqrt((T2LNST - TLNST * TLNST / 8.0) / 7.0) / Magboltz.DIFLN
    Magboltz.DFTER = 100 * math.sqrt((T2TRST - TTRST * TTRST / 8.0) / 7.0) / Magboltz.DIFTR
    Magboltz.DWZ = Magboltz.DWZ / math.sqrt(10)
    Magboltz.DWY = Magboltz.DWY / math.sqrt(10)
    Magboltz.DEN = Magboltz.DEN / math.sqrt(10)
    Magboltz.DXXER = Magboltz.DXXER / math.sqrt(10)
    Magboltz.DYYER = Magboltz.DYYER / math.sqrt(8)
    Magboltz.DZZER = Magboltz.DZZER / math.sqrt(8)
    Magboltz.DYZER = Magboltz.DYZER / math.sqrt(8)
    Magboltz.DFLER = Magboltz.DFLER / math.sqrt(8)
    Magboltz.DFTER = Magboltz.DFTER / math.sqrt(8)

    # CONVERT CM/SEC

    Magboltz.WZ *= 1e5
    Magboltz.WY *= 1e5

    ANCATT = 0.0
    ANCION = 0.0
    for I in range(Magboltz.NGAS):
        ANCATT += Magboltz.ICOLL[5 * I + 2]
        ANCION += Magboltz.ICOLL[5 * I + 1]
    ANCION += IEXTRA
    Magboltz.ATTER = 0.0
    if ANCATT != 0:
        Magboltz.ATTER = 100 * math.sqrt(ANCATT) / ANCATT
    Magboltz.ATT = ANCATT / (Magboltz.ST * Magboltz.WZ) * 1e12
    Magboltz.ALPER = 0.0
    if ANCION != 0:
        Magboltz.ALPER = 100 * math.sqrt(ANCION) / ANCION
    Magboltz.ALPHA = ANCION / (Magboltz.ST * Magboltz.WZ) * 1e12


