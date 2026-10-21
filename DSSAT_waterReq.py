#!/usr/bin/env python

# Day after sewing 'DAS'
DAS = int(input("Enter DAS: "))

# ==============================================================
# DSSAT IRRIGATION DECISION SUPPORT
# CERES-Wheat
#
# DSSAT run:
# C:\DSSAT48\temp_runs\temp_runs_GA_3\run_04
#
# INPUTS:
#   EOAA, ETAA  -> ET.OUT
#   SWXD        -> PlantGrf.OUT
#   LL, DUL, SAT, BD, SW -> SoilWater.OUT
#
# SOIL LAYERS:
#   Layer 1 = 0-5 cm
#   Layer 2 = 5-15 cm
#   Layer 3 = 15-30 cm
#   Layer 4 = 30-40 cm
#   Layer 5 = 40-50 cm
# ==============================================================

import os
import re
import pandas as pd
import numpy as np


# ==============================================================
# 1. DSSAT RUN DIRECTORY
# ==============================================================

RUN_DIR = r"C:\DSSAT48\temp_runs\temp_runs_GA_3\run_04"

ET_FILE = os.path.join(RUN_DIR, "ET.OUT")
PLANT_FILE = os.path.join(RUN_DIR, "PlantGrf.OUT")
SOIL_FILE = os.path.join(RUN_DIR, "SoilWater.OUT")


# ==============================================================
# 2. FILE HEADER INFORMATION
# ==============================================================

ET_SKIP = 10
PLANT_SKIP = 11
SOIL_SKIP = 24


# ==============================================================
# 3. SOIL LAYERS
# ==============================================================

DLAYR = {
    "1": 5.0,    # 0-5 cm
    "2": 10.0,   # 5-15 cm
    "3": 15.0,   # 15-30 cm
    "4": 10.0,   # 30-40 cm
    "5": 10.0    # 40-50 cm
}

# ==============================================================
# 4. IRRIGATION MANAGEMENT
# ==============================================================

#  50% depletion is the best irrigation scenario.
DEPLETION_THRESHOLD = 0.50

# Irrigation application efficiency
IRRIGATION_EFFICIENCY = 0.80

# ==============================================================
# 5. FUNCTION TO READ DSSAT OUTPUT FILE
# ==============================================================

def read_dssat_file(filename, skiprows):
    """
    Read a DSSAT output file.
    skiprows = number of lines before the variable header.
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"\nFile not found:\n{filename}"
        )

    df = pd.read_csv(filename,sep=r"\s+",skiprows=skiprows,engine="python")
    return df

# ==============================================================
# 6. READ DSSAT FILES
# ==============================================================
print("\nReading DSSAT files...")

ET = read_dssat_file(ET_FILE,ET_SKIP)
PLANT = read_dssat_file(PLANT_FILE,PLANT_SKIP)
SOIL = read_dssat_file(SOIL_FILE,SOIL_SKIP)

print("\nFiles successfully read.")
# ==============================================================
# 7. CHECK REQUIRED VARIABLES
# ==============================================================

required_ET = ["EOAA","ETAA"]
required_PLANT = ["SWXD"]
required_SOIL = ["LL1D","LL2D","LL3D","LL4D","LL5D",
                "DUL1D","DUL2D","DUL3D","DUL4D","DUL5D",
                "SAT1D","SAT2D","SAT3D","SAT4D","SAT5D",
                "BD1D","BD2D","BD3D","BD4D","BD5D",
                "SW1D","SW2D","SW3D","SW4D","SW5D"]

#==============================================================

def check_columns(df, required, filename):

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"\nMissing variables in {filename}:\n"
            + ", ".join(missing)
        )


check_columns(ET,required_ET,"ET.OUT")
check_columns(PLANT,required_PLANT,"PlantGrf.OUT")
check_columns(SOIL,required_SOIL,"SoilWater.OUT")

# ==============================================================
# 8. TAKE SIMULATED DAY (DAS)
# ==============================================================

EOAA = float(ET["EOAA"].iloc[DAS])
ETAA = float(ET["ETAA"].iloc[DAS])
SWXD = float(PLANT["SWXD"].iloc[DAS])

# --------------------------------------------------------------
# Soil hydraulic properties
# --------------------------------------------------------------

LL = {
    "1": float(SOIL["LL1D"].iloc[DAS]),
    "2": float(SOIL["LL2D"].iloc[DAS]),
    "3": float(SOIL["LL3D"].iloc[DAS]),
    "4": float(SOIL["LL4D"].iloc[DAS]),
    "5": float(SOIL["LL5D"].iloc[DAS])
}

DUL = {
    "1": float(SOIL["DUL1D"].iloc[DAS]),
    "2": float(SOIL["DUL2D"].iloc[DAS]),
    "3": float(SOIL["DUL3D"].iloc[DAS]),
    "4": float(SOIL["DUL4D"].iloc[DAS]),
    "5": float(SOIL["DUL5D"].iloc[DAS])
}

SAT = {
    "1": float(SOIL["SAT1D"].iloc[DAS]),
    "2": float(SOIL["SAT2D"].iloc[DAS]),
    "3": float(SOIL["SAT3D"].iloc[DAS]),
    "4": float(SOIL["SAT4D"].iloc[DAS]),
    "5": float(SOIL["SAT5D"].iloc[DAS])
}

BD = {
    "1": float(SOIL["BD1D"].iloc[DAS]),
    "2": float(SOIL["BD2D"].iloc[DAS]),
    "3": float(SOIL["BD3D"].iloc[DAS]),
    "4": float(SOIL["BD4D"].iloc[DAS]),
    "5": float(SOIL["BD5D"].iloc[DAS])
}

SW = {
    "1": float(SOIL["SW1D"].iloc[DAS]),
    "2": float(SOIL["SW2D"].iloc[DAS]),
    "3": float(SOIL["SW3D"].iloc[DAS]),
    "4": float(SOIL["SW4D"].iloc[DAS]),
    "5": float(SOIL["SW5D"].iloc[DAS])
}

# ==============================================================
# 9. PRINT DSSAT VALUES
# ==============================================================

print("\n==============================================")
print("DSSAT OUTPUT")
print("==============================================")

print(f"EOAA = {EOAA:.3f} mm/day")
print(f"ETAA = {ETAA:.3f} mm/day")
print(f"SWXD = {SWXD:.3f} mm")

print("\nSOIL WATER PROPERTIES")
print("----------------------------------------------")

for layer in ["1", "2", "3", "4", "5"]:

    print(
        f"Layer {layer}: "
        f"LL={LL[layer]:.4f}, "
        f"DUL={DUL[layer]:.4f}, "
        f"SAT={SAT[layer]:.4f}, "
        f"BD={BD[layer]:.3f}, "
        f"SW={SW[layer]:.4f}"
    )


# ==============================================================
# 10. CALCULATE ROOT-ZONE WATER
# ==============================================================

ROOT_ZONE_WATER = 0.0

for layer in ["1", "2", "3", "4", "5"]:
    depth = DLAYR[layer]
    ROOT_ZONE_WATER += (SW[layer] * depth * 10.0)

# ==============================================================
# 11. CALCULATE ROOT-ZONE DUL AND LL
# ==============================================================

ROOT_ZONE_DUL = 0.0
ROOT_ZONE_LL = 0.0

for layer in ["1", "2", "3", "4", "5"]:

    depth = DLAYR[layer]
    ROOT_ZONE_DUL += (DUL[layer] * depth * 10.0)
    ROOT_ZONE_LL += (LL[layer] * depth * 10.0)

# ==============================================================
# 12. TOTAL AVAILABLE WATER
# ==============================================================
TAW = ROOT_ZONE_DUL - ROOT_ZONE_LL

# ==============================================================
# 13. CURRENT DEPLETION
# ==============================================================
DEPLETION = max(0.0,ROOT_ZONE_DUL - ROOT_ZONE_WATER)

# ==============================================================
# 14. DEPLETION PERCENTAGE
# ==============================================================
if TAW > 0:
    DEPLETION_PERCENT = (DEPLETION / TAW) * 100.0
else:
    DEPLETION_PERCENT = np.nan

# ==============================================================
# 15. ET RATIO
# ==============================================================
if EOAA > 0:
    ET_RATIO = ETAA / EOAA
else:
    ET_RATIO = np.nan

# ==============================================================
# 16. WATER DEFICIT TO DUL
# ==============================================================
WATER_DEFICIT = max(0.0,ROOT_ZONE_DUL - ROOT_ZONE_WATER)

# ==============================================================
# 17. 50% DEPLETION TRIGGER
# ==============================================================
IRRIGATION_TRIGGER = (DEPLETION >=DEPLETION_THRESHOLD * TAW)

# ==============================================================
# 18. IRRIGATION AMOUNT
# ==============================================================
if IRRIGATION_TRIGGER:

    # Net irrigation required to restore
    # the root zone toward DUL
    NET_IRRIGATION = WATER_DEFICIT

    # Gross irrigation considering efficiency
    GROSS_IRRIGATION = (NET_IRRIGATION /IRRIGATION_EFFICIENCY)
else:
    NET_IRRIGATION = 0.0
    GROSS_IRRIGATION = 0.0

# ==============================================================
# 19. DISPLAY ROOT-ZONE WATER BALANCE
# ==============================================================

print("\n==============================================")
print("ROOT-ZONE WATER BALANCE")
print("==============================================")

print(
    f"Root-zone water       = "
    f"{ROOT_ZONE_WATER:.2f} mm"
)

print(
    f"Root-zone DUL         = "
    f"{ROOT_ZONE_DUL:.2f} mm"
)

print(
    f"Root-zone LL          = "
    f"{ROOT_ZONE_LL:.2f} mm"
)

print(
    f"Total available water = "
    f"{TAW:.2f} mm"
)

print(
    f"Water deficit         = "
    f"{WATER_DEFICIT:.2f} mm"
)

print(
    f"Depletion             = "
    f"{DEPLETION:.2f} mm"
)

print(
    f"Depletion             = "
    f"{DEPLETION_PERCENT:.1f} %"
)

# ==============================================================
# 20. EVAPOTRANSPIRATION
# ==============================================================

print("\n==============================================")
print("EVAPOTRANSPIRATION")
print("==============================================")

print(
    f"EOAA                   = "
    f"{EOAA:.2f} mm/day"
)

print(
    f"ETAA                   = "
    f"{ETAA:.2f} mm/day"
)

print(
    f"ETAA / EOAA            = "
    f"{ET_RATIO:.2f}"
)


# ==============================================================
# 21. FINAL IRRIGATION DECISION
# ==============================================================

print("\n==============================================")
print("IRRIGATION DECISION")
print("==============================================")


if IRRIGATION_TRIGGER:

    print(">>> IRRIGATION REQUIRED")

    print(
        f"Current depletion = "
        f"{DEPLETION_PERCENT:.1f}%"
    )

    print(
        f"Trigger           = "
        f"{DEPLETION_THRESHOLD * 100:.0f}%"
    )

    print(
        f"Net irrigation requirement = "
        f"{NET_IRRIGATION:.2f} mm"
    )

    print(
        f"Gross irrigation to apply  = "
        f"{GROSS_IRRIGATION:.2f} mm"
    )

else:

    print(">>> NO IRRIGATION REQUIRED TODAY")

    print(
        f"Current depletion = "
        f"{DEPLETION_PERCENT:.1f}%"
    )

    print(
        f"Irrigation trigger = "
        f"{DEPLETION_THRESHOLD * 100:.0f}%"
    )


# ==============================================================
# 22. WATER-STRESS WARNING
# ==============================================================

print("\n==============================================")
print("WATER STRESS INDICATOR")
print("==============================================")


if ET_RATIO < 0.80:

    print(
        "WARNING: ETAA is substantially below EOAA."
    )

    print(
        "Possible water limitation."
    )

elif ET_RATIO < 0.90:

    print(
        "CAUTION: ETAA is below EOAA."
    )

else:

    print(
        "ETAA is close to EOAA."
    )


# ==============================================================
# 23. DONE
# ==============================================================

print("\nDone.")