#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:24:44 2019

@author: austinmac
"""
import pandas as pd

ceramics = pd.read_csv("file:///Users/austinmac/Downloads/JarSorting/Copy%20of%20tblCeramComb.csv")

#only ceramics with numeric values in "Form"
ceramics = ceramics[ceramics["Form"] != "-"]
ceramics = ceramics[ceramics["Form"] != "nan"]
ceramics["Form"] = pd.to_numeric(ceramics["Form"], errors = "coerce")

#drops entries in ceramics where "SITE" is nan
ceramics = ceramics.dropna(subset = ["SITE"])
ceramics["SITE"] = pd.to_numeric(ceramics["SITE"], errors = "coerce")
ceramics["SITE"] = ceramics["SITE"].astype(int)

#filters by Late Classic Ceramics
ceramics = ceramics[ceramics["Period"] == "LC"]

#Sorts Ceramics into Jars, Bowls, Plates, Vases
ceramics["Vessel"] = str("Other")
ceramics["Vessel"][(ceramics["Group"] == "JG1") | (ceramics["Group"] == "JG2") | (ceramics["Group"] == "JG3") | (ceramics["Group"] == "JG4")] = "Jars"
ceramics["Vessel"][(ceramics["Group"] == "BG1") | (ceramics["Group"] == "BG2") | (ceramics["Group"] == "BG3") | (ceramics["Group"] == "BG4")] = "Bowls"
ceramics["Vessel"][(ceramics["Group"] == "PG1") | (ceramics["Group"] == "PG2") | (ceramics["Group"] == "PG3") | (ceramics["Group"] == "PG4")] = "Plates"
ceramics["Vessel"][(ceramics["Group"] == "VG1") | (ceramics["Group"] == "VG2") | (ceramics["Group"] == "VG3")] = "Vases"

ceramics = ceramics[ceramics["Vessel"] != "Other"]

#Sorts by the selected attributes
ceramics2 = ceramics[["SITE", "Shape", "RimDiameter", "Pocking", "HCL", "WallThick", "Vessel"]]

#in order to get rid of "-" values, replace "-" with "astring" and coerce them to "nan"
ceramics2 = ceramics2.replace("-", "astring")
ceramics2["Pocking"] = pd.to_numeric(ceramics2["Pocking"], errors = "coerce")
ceramics2["HCL"] = pd.to_numeric(ceramics2["HCL"], errors = "coerce")
ceramics2["WallThick"] = pd.to_numeric(ceramics2["WallThick"], errors = "coerce")

#fills "nan" values in the selected attributes with the median of selected attributes
#skips "nan" values in the computation of median
ceramics2["RimDiameter"] = ceramics2["RimDiameter"].fillna(ceramics2["RimDiameter"].median(skipna = True))
ceramics2["Pocking"] = ceramics2["Pocking"].fillna(ceramics2["Pocking"].median(skipna = True))
ceramics2["HCL"] = ceramics2["HCL"].fillna(ceramics2["HCL"].median(skipna = True))
ceramics2["WallThick"] = ceramics2["WallThick"].fillna(ceramics2["WallThick"].median(skipna = True))

#creates a training set and a target set for the random forest
train = ceramics2[["SITE", "Shape", "RimDiameter", "Pocking", "HCL", "WallThick"]]
target = ceramics2["Vessel"]

#Cleaning the Clean Dataframe
clean = pd.read_csv("clean.csv")
original_clean = clean[["SITE", "Shape", "RimDiameter", "Pocking", "HCL", "WallThick", "Vessel"]]
clean = clean[["SITE", "Shape", "RimDiameter", "Pocking", "HCL", "WallThick"]]

#fills "nan" values in the selected attributes with the median of selected attributes
clean["RimDiameter"] = clean["RimDiameter"].fillna(ceramics2["RimDiameter"].median(skipna = True))
clean["Pocking"] = clean["Pocking"].fillna(ceramics2["Pocking"].median(skipna = True))
clean["HCL"] = clean["HCL"].fillna(ceramics2["HCL"].median(skipna = True))
clean["WallThick"] = clean["WallThick"].fillna(ceramics2["WallThick"].median(skipna = True))



