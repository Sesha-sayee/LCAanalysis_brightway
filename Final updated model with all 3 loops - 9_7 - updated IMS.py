 # -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 16:20:31 2020

@author: Seshasayee
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import brightway2 as bw
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group
bw.databases
#importing FORWAST database

import requests
from zipfile import ZipFile
from eight import *
import os
import brightway2 as bw2
from pathlib import Path

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:37:00 2020

@author: Seshasayee
"""
global solid_handling_choice 
solid_handling_choice = 1 #1 - yes, 0 - no
global BPA_purification_choice
BPA_purification_choice = 0 #1 - yes, 0 - no
global carbon_sequestration_choice
carbon_sequestration_choice = 1 #1 - yes, 0 - no

from bw2data.ia_data_store import ImpactAssessmentDataStore
from brightway2 import methods, Method, Database

class QuickMethod (ImpactAssessmentDataStore):
    
    _metadata = methods

    def __init__(self, name):
        self.name = name

    def _write(self, data, process=True):
        """Serialize intermediate data to disk. Sets the metadata key ``num_cfs`` automatically.From bw2; """
        self.metadata[u"num_cfs"] = len(data)
        self._metadata.flush()
        super(Method, self).write(data)
        
    def characterization_factor(self):
        """A method to find characterization factors of a lcia method"""
        CFs=[]
        for key, cf in super(QuickMethod, self).load():
            try:
                activity= Database(key[0]).get(key[1])
            except TypeError as err:
                print (err)
            CFs.append((activity, cf))
        return CFs
    
    @property       
    def description(self):
        """Get brieft description of the impact assessment method"""
        return self.metadata.get('description')
    
    @property    
    def unit(self):
        """Get unit of the impact assessment score"""
        return self.metadata.get('unit')
        
    def __str__(self):
        return "%s: %s used in Seshasayee's HTL project" % (self.__class__.__name__, self.name)             

if 'forwast' in bw.databases:
    print("Database has already been imported.")
else:
    url="http://lca-net.com/wp-content/uploads/forwast.bw2package.zip"
    c_path = os.path.abspath(os.path.dirname(__file__))
    dirpath = os.path.join(c_path,'database')
    assert isinstance(dirpath, str), "`directory` must be a string"
    
    if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
    config = Path('forwast.package.zip')
    
    if config.is_file():
        filename='forwast.package.zip'
        filepath=os.path.join(dirpath,filename)
    else: # download database from forwast website
        fp = dirpath
        if not os.path.isdir(fp):
            os.makedirs(fp)
        filename = "forwast.bw2package.zip"
        filepath = os.path.join(fp, filename)
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise ("URL {} returns status code {}.".format(url), r.status_code)
        try:
            with open(filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128): #chunk = 128 * 1024
                    fd.write(chunk)
        except FileNotFoundError as err_mms:
            print (err_mms)
        filepath=os.path.realpath(filename) 
    
    sp=ZipFile(filepath).extractall(dirpath)
    bw2.BW2Package.import_file(os.path.join(dirpath, "forwast.bw2package"))

import zipfile
from bw2data.utils import download_file

bw.projects.dir
bw.bw2setup()
    
#ecoinvent
if 'ecoinvent 3.5_cutoff_ecoSpold02' in bw.databases:
    print("Database has already been imported.")
else:
    # mind that the ecoinvent file must be unzipped; then: path to the datasets subfolder
    fpei35cut = r"C:\Users\Seshasayee\Anaconda3\datasets"
    # the "r" makes sure that the path is read as a string - especially useful when you have spaces in your string
    ei35cut = bw.SingleOutputEcospold2Importer(fpei35cut, 'ecoinvent 3.5_cutoff_ecoSpold02')
    ei35cut
    ei35cut.apply_strategies()
    ei35cut.statistics()
    ei35cut.write_database()

import zipfile
from bw2data.utils import download_file

bw.projects.dir
bw.bw2setup()
    
fw = bw.Database('forwast')
bw3 = bw.Database('biosphere3')
eidb = bw.Database('ecoinvent 3.5_cutoff_ecoSpold02')
print("The imported forwast database is of type {} and has a length of {}.".format(type(fw), len(fw)))

Electricity = [act for act in eidb if 'electricity, low voltage' in act['name'] and 'US-NPCC' in act['location']][0]
Natural_gas = eidb.search('Natural gas')[5]
Hexane = eidb.search('hexane')[0]
DMSO = eidb.search('dimethyl sulfoxide')[1]
NaOH = eidb.search('sodium hydroxide')[0]
H2SO4 = eidb.search('sulfuric acid')[1]
Ethanol = eidb.search('ethanol')[12]

#Landfilling
Landfilling_glass = fw.search('landfill')[5]
Landfilling_plastic = fw.search('landfill')[7]
Landfilling_wood = fw.search('landfill')[8]
Landfilling_food = fw.search('landfill')[10]
Landfilling_copper = fw.search('landfill')[13]
Landfilling_aluminum = fw.search('landfill')[14]
Landfilling_iron = fw.search('landfill')[16]
Landfilling_textiles = fw.search('landfill')[18]
Landfilling_paper = fw.search('landfill')[19]
Landfilling_land = bw3.search('landfill')[0]

#Incineration
Incineration_glass = fw.search('Incineration')[2]
Incineration_plastic = fw.search('Incineration')[6]
Incineration_wood = fw.search('Incineration')[11]
Incineration_food = fw.search('Incineration')[14]
Incineration_metal = fw.search('Incineration')[13]
Incineration_textiles = fw.search('Incineration')[12]
Incineration_paper = fw.search('Incineration')[4]

Composting = fw.search('compost')[0]

Water = bw3.search('water')[1]
water_fresh = eidb.search('market for water, decarbonised')[10]
water_treatment = eidb.search('tap water production, conventional treatment')[2]

TPA_basic = eidb.search("terephthalic")[0]
BPA_basic = eidb.search("bisphenol")[1]

print(bw.databases)

#biochemical composition
#input
# 1) mass processed/mass flow rate
# 2) biochemical composition
# 3) cost of heating (W/$)

# cellulose (%), protein (%), lipid (%), lignin (%), starch (%), massflowrate (kg/hr), costofheating ($/KJ)

import math
from thermo.chemical import Chemical
water = Chemical('water')
#PP = Chemical('polypropylene')
#PS = Chemical('9003-53-6')
#PC = Chemical('80-05-7')
#PET = Chemical('25038-59-9')

class class_process_model(object):
    def __init__(self, cellulose, protein, lipid, lignin, starch, PP, PS, PC, PET, massflowrate, costofheating, desired_end_size, temperature, null):
        self.cellulose = cellulose; #(%)
        self.protein = protein; #(%)
        self.lipid = lipid; #(%)
        self.lignin = lignin; #(%)
        self.starch = starch; #(%)
        self.PP = PP; #(%)
        self.PS = PS; #(%)
        self.PC = PC; #(%)
        self.PET = PET; #(%)
        self.massflowrate = massflowrate; #(kg/hr)
        self.costofheating = costofheating; #($/KJ)
        self.desired_end_size = desired_end_size; #(cm)
        self.temperature = temperature;
        self.oil_yield = null;
        self.solid_yield = null;
        self.C_mixture = null; 
        self.H_mixture = null;
        self.O_mixture = null;
        self.N_mixture = null;
        self.S_mixture = null;
        self.TPA_yield = null;
        self.solid_handling_cost = null;
        self.Unreacted_plastic = null;
        self.BPA_yield = null
        self.Total_BPA_purification_cost = null
        self.feedstock_loading = null
        
        print ("The feedstock has: Cellulose - " + str(round(cellulose,2)) + " %, Starch - " +  str(round(starch,2)) + " %, Protein - " + str(round(protein,2)) + " %, Lignin - " + str(round(lignin,2)) + " %, Lipid - " + str(round(lipid,2))+ " %, PP - " + str(round(PP,2)) + " %, PS - " + str(round(PS,2)) + " %, PC - " + str(round(PC,2)) + " %, PET - " + str(round(PET,2)) +" % \n")
        print ("************************************************************************\n")

    def HTL_process_model(self):
        print ("HTL Process Model: \n")
        
        #reaction information
        Reactorheatingeffeciency = 0.8 #assumption (fraction)
        timeofprocessing = 30; #mins
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        temperature = self.temperature;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #Carbon in plastic
        Carbon_in_plastic_feedstock = PP * 0.8571 + PS * 0.9230 + PET * 0.625 + PC * 0.6593;
        
        #oil yields for individual model compounds
        carbohydrateyield_300 = 9.15;
        carbohydrateyield_350 = 8.95;
        carbohydrateyield_425 = 3.27;
        ligninyield_300 = 5.24;
        ligninyield_350 = 5.24;
        ligninyield_425 = 1.30;
        starchyield_300 = 11.71;
        starchyield_350 = 14.83;
        starchyield_425 = 4.26;
        proteinyield_300 = 24.66;
        proteinyield_350 = 27.80;
        proteinyield_425 = 86.32;
        lipidyield_300 = 86.84;
        lipidyield_350 = 86.32;
        lipidyield_425 = 11.85;
        PPyield_300 = 0.9;
        PSyield_300 = 38.3;
        PCyield_300 = 64.9;
        PETyield_300 = 2.4;
        PPyield_350 = 0.8;
        PSyield_350 = 86.2;
        PCyield_350 = 49.7;
        PETyield_350 = 4.2;
        PPyield_425 = 32.4;
        PSyield_425 = 48.4;
        PCyield_425 = 59.5;
        PETyield_425 = 14.2;
        
        #calculating oil yield to identify temperature
        Yieldat300=(9.15*carbohydrate+5.24*lignin+11.71*starch+24.66*protein+86.84*lipid+0.9*PP+38.3*PS+64.9*PC+2.4*PET)/100+0.00306*carbohydrate*protein+0.00331*starch*protein+0.00459*carbohydrate*lignin+0.00071*starch*lignin+0.0023*lipid*lignin+0.0086*PS*PP+0.0116*PS*PET+0.0064*PS*PC-0.0004*PP*PET-0.0006*PC*PP-0.0013*PC*PET+0.0011*carbohydrate*PP+0.0004*starch*PP-0.0005*lignin*PP+0.0001*carbohydrate*PET+0.0031*starch*PET+0.0073*carbohydrate*PS+0.0069*starch*PS+0.0023*lignin*PS+0.0014*starch*PC-0.0062*lignin*PC;
        Yieldat350=(8.95*carbohydrate+5.24*lignin+14.83*starch+27.80*protein+86.32*lipid+0.8*PP+86.2*PS+49.7*PC+4.2*PET)/100+0.00533*carbohydrate*protein+0.00218*starch*protein+0.00834*carbohydrate*lignin+0.00028*starch*lignin-0.00267*lipid*lignin-0.0037*PS*PP+0.0003*PS*PET-0.0026*PS*PC-0.0005*PP*PET-0.0049*PC*PP+0.0005*PC*PET+0.0021*carbohydrate*PP+0.0032*starch*PP+0.0007*lignin*PP+0.0024*carbohydrate*PET+0.0034*starch*PET+0.0004*lignin*PET-0.0004*carbohydrate*PS-0.0003*starch*PS-0.0061*lignin*PS+0.0080*starch*PC+0.0075*carbohydrate*PC+0.0034*lignin*PC;
        Yieldat425=(3.27*carbohydrate+1.30*lignin+4.26*starch+33.27*protein+11.85*lipid+32.4*PP+48.4*PS+59.5*PC+14.2*PET)/100+0.00128*carbohydrate*protein+0.00085*starch*protein+0.00591*carbohydrate*lignin+0.00161*starch*lignin+0.00153*lipid*lignin-0.0064*PS*PP-0.0028*PS*PET+0.0059*PS*PC-0.0027*PP*PET+0.0057*PC*PP+0.0002*PC*PET+0.0013*carbohydrate*PP+0.0018*starch*PP+0.0016*lignin*PP+0.0002*carbohydrate*PET+0.0017*starch*PET-0.0003*lignin*PET-0.0077*carbohydrate*PS-0.0081*starch*PS-0.0068*lignin*PS-0.0096*starch*PC-0.0091*carbohydrate*PC-0.0082*lignin*PC;

        #identifying optimal temperature:
        #if max(Yieldat300,Yieldat350,Yieldat425)==Yieldat300:
        #    settemperature = 300;
        #    Yield = Yieldat300;
        #elif max(Yieldat300,Yieldat350,Yieldat425)==Yieldat350:
        #    settemperature = 350;
        #    Yield = Yieldat350;
        #elif max(Yieldat300,Yieldat350,Yieldat425)==Yieldat425:
        #    settemperature = 425;
        #    Yield = Yieldat425;
        
        if temperature >= 250 and temperature < 325:
            Yield = Yieldat300;
            settemperature = 300;
            feedstock_loading=6;
            reactor_pressure = 8.588 #MPa   
        elif temperature >= 325 and temperature < 375:
            Yield = Yieldat350;
            settemperature = 350;
            feedstock_loading=7.4;
            reactor_pressure = 16.53 #MPa
        elif temperature >= 375 and temperature < 450:
            Yield = Yieldat425;
            settemperature = 425;
            feedstock_loading=33.7;
            reactor_pressure = 25 #MPa
        elif temperature < 250:
            print ("Temperature is too low")
            return
        else:
            print ("Temperature is too high")
            return
        
        print ("Simulated temperature is "+str(round(settemperature,2))+" degC")
        print ("Feedstock loading is "+str(round(feedstock_loading,2))+" % weight loading of feedstock/weight of water.")
        print ("Yield at simulated temperature is "+str(round(Yield,2))+" %\n")
        
        #dummy values
        TPA_yield_300 = 50;
        TPA_yield_350 = 90;
        TPA_yield_425 = 60;
        
        BPA_yield_250 = 98;

        self.oil_yield = Yield;
        self.feedstock_loading = feedstock_loading;

        #Solid yield
        Solid_Yieldat300=(39.30*carbohydrate+39.92*lignin+31.98*starch+2.86*protein+2.71*lipid+98.42*PP+60.26*PS+0.44*PC+93.20*PET)/100;
        Solid_Yieldat350=(14.03*carbohydrate+43.78*lignin+22.17*starch+1.09*protein+1*lipid+92.15*PP+3.06*PS+3.13*PC+81.78*PET)/100;
        Solid_Yieldat425=(52.70*carbohydrate+56.89*lignin+25.69*starch+3.90*protein+0.29*lipid+2.38*PP+1.73*PS+4.07*PC+79.74*PET)/100;

        Biochar_Yieldat300=(39.30*carbohydrate+39.92*lignin+31.98*starch+2.86*protein+2.71*lipid)/100;
        Biochar_Yieldat350=(14.03*carbohydrate+43.78*lignin+22.17*starch+1.09*protein+1*lipid)/100;
        Biochar_Yieldat425=(52.70*carbohydrate+56.89*lignin+25.69*starch+3.90*protein+0.29*lipid)/100;

        Unreacted_plasticat300 = (98.42*PP+60.26*PS+0.44*PC)/100
        Unreacted_PPat300 = 98.42*PP/100
        Unreacted_PSat300 = 60.26*PS/100
        Unreacted_PCat300 = 0.44*PC/100
        Unreacted_plasticat350 = (92.15*PP+3.06*PS+3.13*PC)/100
        Unreacted_PPat350 = 92.15*PP/100
        Unreacted_PSat350 = 3.06*PS/100
        Unreacted_PCat350 = 3.13*PC/100
        Unreacted_plasticat425 = 0
        Unreacted_PPat425 = 0
        Unreacted_PSat425 = 0
        Unreacted_PCat425 = 0
        
        if settemperature == 300:
            solid_yield = Solid_Yieldat300;
            biochar_yield = Biochar_Yieldat300
            Unreacted_plastic = Unreacted_plasticat300
            Unreacted_PP = Unreacted_PPat300
            Unreacted_PS = Unreacted_PSat300
            Unreacted_PC = Unreacted_PCat300
            Oil_yield_from_unreacted_plastic = (32.4*Unreacted_PPat300+48.4*Unreacted_PSat300+59.5*Unreacted_PCat300)/100-0.0064*Unreacted_PSat300*Unreacted_PPat300+0.0059*Unreacted_PSat300*Unreacted_PCat300+0.0057*Unreacted_PCat300*Unreacted_PPat300;
        elif settemperature == 350:
            solid_yield = Solid_Yieldat350;
            biochar_yield = Biochar_Yieldat350
            Unreacted_plastic = Unreacted_plasticat350
            Unreacted_PP = Unreacted_PPat350
            Unreacted_PS = Unreacted_PSat350
            Unreacted_PC = Unreacted_PCat350
            Oil_yield_from_unreacted_plastic = (32.4*Unreacted_PPat350+48.4*Unreacted_PSat350+59.5*Unreacted_PCat350)/100-0.0064*Unreacted_PSat350*Unreacted_PPat350+0.0059*Unreacted_PSat350*Unreacted_PCat350+0.0057*Unreacted_PCat350*Unreacted_PPat350;
        elif settemperature == 425:
            solid_yield = Solid_Yieldat425;
            biochar_yield = Biochar_Yieldat425
            Unreacted_plastic = Unreacted_plasticat425
            Unreacted_PP = Unreacted_PPat425
            Unreacted_PS = Unreacted_PSat425
            Unreacted_PC = Unreacted_PCat425
            Oil_yield_from_unreacted_plastic = 0
        
        print ("Oil recovered from reacting plastics at 425 C "+str(round(Oil_yield_from_unreacted_plastic,2))+" %\n")
        
        #Gas yield
        Gas_Yieldat300=(41.26*carbohydrate+2.52*lignin+45.44*starch+32.95*protein+9.62*lipid+0*PP+0*PS+33.22*PC+0*PET)/100;
        Gas_Yieldat350=(73.78*carbohydrate+20.35*lignin+59.27*starch+56.55*protein+12.31*lipid+3.95*PP+3*PS+19.13*PC+7.87*PET)/100;
        Gas_Yieldat425=(43.42*carbohydrate+28.79*lignin+68.04*starch+57.95*protein+87.62*lipid+34*PP+1.24*PS+46.76*PC+5.36*PET)/100;

        if settemperature == 300:
            Gas_yield = Gas_Yieldat300;
        elif settemperature == 350:
            Gas_yield = Gas_Yieldat350;
        elif settemperature == 425:
            Gas_yield = Gas_Yieldat425;

        #Gas yield from plastics
        Gas_Yieldfromplastic_at300=(0*PP+0*PS+33.22*PC+0*PET)/100;
        Gas_Yieldfromplastic_at350=(3.95*PP+3*PS+19.13*PC+7.87*PET)/100;
        Gas_Yieldfromplastic_at425=(34*PP+1.24*PS+46.76*PC+5.36*PET)/100;

        if settemperature == 300:
            Gas_yield_fromplastic = Gas_Yieldfromplastic_at300;
        elif settemperature == 350:
            Gas_yield_fromplastic = Gas_Yieldfromplastic_at350;
        elif settemperature == 425:
            Gas_yield_fromplastic = Gas_Yieldfromplastic_at425;
                
        #product properties
        #heating value (HHV)

        if settemperature == 300:
            HHV_carbohydrate = 25.99;
            HHV_lignin = 25.53;
            HHV_starch = 27.07;
            HHV_protein = 29.10;
            HHV_lipid = 31.68;
            HHV_PP = 34.22;
            HHV_PS = 39.13;
            HHV_PC = 26.35;
            HHV_PET = 32.90;
            carbohydrateinoil = carbohydrate*carbohydrateyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            starchinoil = starch*starchyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            lignininoil = lignin*ligninyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            proteininoil = protein*proteinyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            lipidinoil = lipid*lipidyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            PPinoil = PP*PPyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            PSinoil = PS*PSyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            PCinoil = PC*PCyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            PETinoil = PET*PETyield_300*100/(carbohydrate*carbohydrateyield_300+lignin*ligninyield_300+starch*starchyield_300+protein*proteinyield_300+lipid*lipidyield_300+PP*PPyield_300+PC*PCyield_300+PS*PSyield_300+PET*PETyield_300);
            TPA_yield = TPA_yield_300*PET/100;
            BPA_yield = BPA_yield_250*PC/100;
            
        elif settemperature == 350:
            HHV_carbohydrate = 29.02;
            HHV_lignin = 26.52;
            HHV_starch = 27.97;
            HHV_protein = 28.44;
            HHV_lipid = 34.63;
            HHV_PP = 45.62;
            HHV_PS = 42.61;
            HHV_PC = 30.88;
            HHV_PET = 33.55;
            carbohydrateinoil = carbohydrate*carbohydrateyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            starchinoil = starch*starchyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            lignininoil = lignin*ligninyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            proteininoil = protein*proteinyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            lipidinoil = lipid*lipidyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            PPinoil = PP*PPyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            PCinoil = PC*PCyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            PSinoil = PS*PSyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            PETinoil = PET*PETyield_350*100/(carbohydrate*carbohydrateyield_350+lignin*ligninyield_350+starch*starchyield_350+protein*proteinyield_350+lipid*lipidyield_350+PP*PPyield_350+PC*PCyield_350+PS*PSyield_350+PET*PETyield_350);
            TPA_yield = TPA_yield_350*PET/100;
            BPA_yield = BPA_yield_250*PC/100;
            
        elif settemperature == 425:
            HHV_carbohydrate = 27.87;
            HHV_lignin = 25.60;
            HHV_starch = 31.85;
            HHV_protein = 28.87;
            HHV_lipid = 32.40;
            HHV_PP = 42.20;
            HHV_PS = 39.76;
            HHV_PC = 30.14;
            HHV_PET = 33.90;
            carbohydrateinoil = carbohydrate*carbohydrateyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            starchinoil = starch*starchyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            lignininoil = lignin*ligninyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            proteininoil = protein*proteinyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            lipidinoil = lipid*lipidyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            PPinoil = PP*PPyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            PCinoil = PC*PCyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            PSinoil = PS*PSyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            PETinoil = PET*PETyield_425*100/(carbohydrate*carbohydrateyield_425+lignin*ligninyield_425+starch*starchyield_425+protein*proteinyield_425+lipid*lipidyield_425+PP*PPyield_425+PC*PCyield_425+PS*PSyield_425+PET*PETyield_425);
            TPA_yield = TPA_yield_425*PET/100;
            BPA_yield = BPA_yield_250*PC/100;

        HHV_mixture = (HHV_carbohydrate*carbohydrateinoil + HHV_lignin*lignininoil + HHV_starch*starchinoil + HHV_protein*proteininoil + HHV_lipid*lipidinoil + HHV_PP*PPinoil + HHV_PS*PSinoil + HHV_PC*PCinoil + HHV_PET*PETinoil)/100;
        
        Total_oil_yield = Yield+Oil_yield_from_unreacted_plastic-BPA_purification_choice*BPA_yield
        
        self.oil_yield = Total_oil_yield;
        self.solid_yield = solid_yield
        self.biochar_yield = biochar_yield
        self.Unreacted_plastic = Unreacted_plastic
        self.TPA_yield = TPA_yield;
        self.BPA_yield = BPA_yield;
        print ("TPA yield is: ", round(TPA_yield,2))
        print ("BPA yield is: ", round(BPA_yield,2))
        print ("Heating value of oil produced is "+str(round(HHV_mixture,2))+" MJ/Kg\n")

        #elemental analysis

        if settemperature == 300:
            #carbon
            C_carbohydrate = 65.27;
            C_lignin = 65.13;
            C_starch = 65.71; 
            C_protein = 67.58;
            C_lipid = 68.55; 
            C_PP = 73.21;
            C_PS = 87.46;
            C_PC = 68.63;
            C_PET = 74.34;
            #hydrogen
            H_carbohydrate = 6.01;
            H_lignin = 5.65;
            H_starch = 6.56;
            H_protein = 7.16;
            H_lipid = 8.60;
            H_PP = 8.78;
            H_PS = 7.46;
            H_PC = 5.20;
            H_PET = 7.59;
            #oxygen
            O_carbohydrate = 28.59;
            O_lignin = 27.88;
            O_starch = 27.66;
            O_protein = 17.31;
            O_lipid = 22.80;
            O_PP = 18.02;
            O_PS = 5.08;
            O_PC = 26.17;
            O_PET = 18.07;
            #nitrogen
            N_protein = 7.28;
            #sulpher
            S_lignin = 1.19;
            S_protein = 0.66;

        elif settemperature == 350:
            #carbon
            C_carbohydrate = 71.55;
            C_lignin = 69.96;
            C_starch = 69.94; 
            C_protein = 67.48;
            C_lipid = 74.63; 
            C_PP = 83.22;
            C_PS = 90.80;
            C_PC = 68.96;
            C_PET = 59.67;
            #hydrogen
            H_carbohydrate = 6.11;
            H_lignin = 5.94;
            H_starch = 5.82;
            H_protein = 6.78;
            H_lipid = 8.59;
            H_PP = 9.56;
            H_PS = 8.63;
            H_PC = 6.78;
            H_PET = 7.59;
            #oxygen
            O_carbohydrate = 22.23;
            O_lignin = 21.15;
            O_starch = 24.16;
            O_protein = 18.64;
            O_lipid = 16.69;
            O_PP = 5.76;
            O_PS = 0.41;
            O_PC = 23.76;
            O_PET = 29.35;
            #nitrogen
            N_protein = 6.46;
            #sulpher
            S_lignin = 2.20;
            S_protein = 0.64;

        elif settemperature == 425:
            #carbon
            C_carbohydrate = 64.46;
            C_lignin = 65.55;
            C_starch = 74.69; 
            C_protein = 70.26;
            C_lipid = 65.52; 
            C_PP = 84.40;
            C_PS = 89.85;
            C_PC = 76.36;
            C_PET = 65.42;
            #hydrogen
            H_carbohydrate = 7.45;
            H_lignin = 5.68;
            H_starch = 6.80;
            H_protein = 6.18;
            H_lipid = 10.00;
            H_PP = 11.86;
            H_PS = 6.69;
            H_PC = 7.46;
            H_PET = 10.52;
            #oxygen
            O_carbohydrate = 27.93;
            O_lignin = 28.72;
            O_starch = 18.30;
            O_protein = 15.07;
            O_lipid = 24.36;
            O_PP = 3.51;
            O_PS = 3.22;
            O_PC = 15.93;
            O_PET = 23.80;
            #nitrogen
            N_protein = 7.88;
            #sulpher
            S_lignin = 0;
            S_protein = 0.60;

        global C_mixture
        global H_mixture
        global O_mixture
        global N_mixture
        global S_mixture
        C_mixture = (C_carbohydrate*carbohydrateinoil + C_lignin*lignininoil + C_starch*starchinoil + C_protein*proteininoil + C_lipid*lipidinoil + C_PP*PPinoil + C_PC*PCinoil + C_PS*PSinoil + C_PET*PETinoil)/100;
        H_mixture = (H_carbohydrate*carbohydrateinoil + H_lignin*lignininoil + H_starch*starchinoil + H_protein*proteininoil + H_lipid*lipidinoil + H_PP*PPinoil + H_PC*PCinoil + H_PS*PSinoil + H_PET*PETinoil)/100;
        O_mixture = (O_carbohydrate*carbohydrateinoil + O_lignin*lignininoil + O_starch*starchinoil + O_protein*proteininoil + O_lipid*lipidinoil + O_PP*PPinoil + O_PC*PCinoil + O_PS*PSinoil + O_PET*PETinoil)/100;
        N_mixture = (N_protein*proteininoil)/100;
        S_mixture = (S_lignin*lignininoil + S_protein*proteininoil)/100;
        Total_is = C_mixture + H_mixture + O_mixture + N_mixture + S_mixture;

        print ("Carbon in oil is "+str(round(C_mixture,2))+" wt.%")
        print ("Hydrogen in oil is "+str(round(H_mixture,2))+" wt.%")
        print ("Oxygen in oil is "+str(round(O_mixture,2))+" wt.%")
        print ("Nitrogen in oil is "+str(round(N_mixture,2))+" wt.%")
        print ("Sulpher in oil is "+str(round(S_mixture,2))+" wt.%\n")
        #print ("Total is "+ str(round(Total_is,2))+" wt.%\n")
        
        #storing to class
        self.C_mixture = C_mixture;
        self.H_mixture = H_mixture;
        self.O_mixture = O_mixture;
        self.N_mixture = N_mixture;
        self.S_mixture = S_mixture;

        #light and heavy fraction produced

        if settemperature == 300:
            HF_carbohydrate = 85.45;
            HF_lignin = 88.04;
            HF_starch = 82.41;
            HF_protein = 83.71;
            HF_lipid = 49.24;
            #dummyvalues
            HF_PP = 34.22;
            HF_PS = 39.13;
            HF_PC = 26.35;
            HF_PET = 32.90;
        elif settemperature == 350:
            HF_carbohydrate = 92.86;
            HF_lignin = 62.50;
            HF_starch = 82.64;
            HF_protein = 76.92;
            HF_lipid = 31.20;
            #dummyvalues
            HF_PP = 45.62;
            HF_PS = 42.61;
            HF_PC = 30.88;
            HF_PET = 33.55;
        elif settemperature == 425:
            HF_carbohydrate = 55.42;
            HF_lignin = 26.56;
            HF_starch = 81.41;
            HF_protein = 54.02;
            HF_lipid = 0.30;
            #dummyvalues
            HF_PP = 42.20;
            HF_PS = 39.76;
            HF_PC = 30.14;
            HF_PET = 33.90;

        Lightfraction_in_mixture = 100 - (HF_carbohydrate*carbohydrateinoil + HF_lignin*lignininoil + HF_starch*starchinoil + HF_protein*proteininoil + HF_lipid*lipidinoil + HF_PP*PPinoil + HF_PC*PCinoil + HF_PS*PSinoil + HF_PET*PETinoil)/100;

        print ("Percentage of light fraction in oil is "+str(round(Lightfraction_in_mixture,2))+" %")
        print ("Percentage of heavy fraction in oil is "+str(round(100-Lightfraction_in_mixture,2))+" %\n")

        #heat capacity of carbohydrates
        exact_heatcapacity_carbohydrate = 0;
        for temp in range (25,settemperature):
            exact_heatcapacity_carbohydrate += 1.31 + 4.27*0.001*(temp-25); #KJ/KgK #or glucose at 25 C 
        heatcapacity_carbohydrate = exact_heatcapacity_carbohydrate/(settemperature-25)
        
        #heat capacity of starch
        exact_heatcapacity_starch = 0;
        for temp in range (25,settemperature):
            exact_heatcapacity_starch += 1.26 + 5.24*0.001*(temp); #KJ/KgK #or glucose at 25 C 
        heatcapacity_starch = exact_heatcapacity_starch/(settemperature-25)
        #print ("Heating capacity of starch is "+str(round(heatcapacity_starch,2))+" KJ/KgK. \n")
        
        print ("Energy consumed calculations:\n")
        print ("The effeciency of heating equipment is assumed to be "+str(round(Reactorheatingeffeciency*100,2))+" %.\n")
        #print ("Heating capacity of carbohydrate is "+str(round(heatcapacity_carbohydrate,2))+" KJ/KgK.")

        #heat capacity of protein
        heatcapacity_protein_ala_init = 27.13;  #cal/Kmol
        mol_mass_ala = 89.09; #mol/g
        heatcapacity_protein_ala = heatcapacity_protein_ala_init * 4.18/mol_mass_ala;

        heatcapacity_protein_arg_init = 55.8;  #cal/Kmol
        mol_mass_arg = 174.2; #mol/g
        heatcapacity_protein_arg = heatcapacity_protein_arg_init * 4.18/mol_mass_arg;

        heatcapacity_protein_asn_init = 38.3;  #cal/Kmol
        mol_mass_asn = 132.1; #mol/g
        heatcapacity_protein_asn = heatcapacity_protein_asn_init * 4.18/mol_mass_asn;

        heatcapacity_protein_asp_init = 37.09;  #cal/Kmol
        mol_mass_asp = 133.1; #mol/g
        heatcapacity_protein_asp = heatcapacity_protein_asp_init * 4.18/mol_mass_asp;

        heatcapacity_protein_cys_init = 38.8;  #cal/Kmol
        mol_mass_cys = 121.2; #mol/g
        heatcapacity_protein_cys = heatcapacity_protein_cys_init * 4.18/mol_mass_cys;

        heatcapacity_protein_gln_init = 44.02;  #cal/Kmol
        mol_mass_gln = 147.1; #mol/g
        heatcapacity_protein_gln = heatcapacity_protein_gln_init * 4.18/mol_mass_gln;

        heatcapacity_protein_glu_init = 41.84;  #cal/Kmol
        mol_mass_glu = 146.2; #mol/g
        heatcapacity_protein_glu = heatcapacity_protein_glu_init * 4.18/mol_mass_glu;

        heatcapacity_protein_gly_init = 23.71;  #cal/Kmol
        mol_mass_gly = 75.1; #mol/g
        heatcapacity_protein_gly = heatcapacity_protein_gly_init * 4.18/mol_mass_gly;

        heatcapacity_protein_his_init = 51.48;  #cal/Kmol
        mol_mass_his = 155.2; #mol/g
        heatcapacity_protein_his = heatcapacity_protein_his_init * 4.18/mol_mass_his;

        heatcapacity_protein_ile_init = 45;  #cal/Kmol
        mol_mass_ile = 131.2; #mol/g
        heatcapacity_protein_ile = heatcapacity_protein_ile_init * 4.18/mol_mass_ile;

        heatcapacity_protein_leu_init = 48.03;  #cal/Kmol
        mol_mass_leu = 131.2; #mol/g
        heatcapacity_protein_leu = heatcapacity_protein_leu_init * 4.18/mol_mass_leu;

        heatcapacity_protein_lys_init = 48.94;  #cal/Kmol
        mol_mass_lys = 146.2; #mol/g
        heatcapacity_protein_lys = heatcapacity_protein_lys_init * 4.18/mol_mass_lys;

        heatcapacity_protein_met_init = 69.32;  #cal/Kmol
        mol_mass_met = 149.2; #mol/g
        heatcapacity_protein_met = heatcapacity_protein_met_init * 4.18/mol_mass_met;

        heatcapacity_protein_phe_init = 48.52;  #cal/Kmol
        mol_mass_phe = 165.2; #mol/g
        heatcapacity_protein_phe = heatcapacity_protein_phe_init * 4.18/mol_mass_phe;

        heatcapacity_protein_pro_init = 36.13;  #cal/Kmol
        mol_mass_pro = 115.1; #mol/g
        heatcapacity_protein_pro = heatcapacity_protein_pro_init * 4.18/mol_mass_pro;

        heatcapacity_protein_ser_init = 32.4;  #cal/Kmol
        mol_mass_ser = 105.1; #mol/g
        heatcapacity_protein_ser = heatcapacity_protein_ser_init * 4.18/mol_mass_ser;

        heatcapacity_protein_thr_init = 35.2;  #cal/Kmol
        mol_mass_thr = 119.1; #mol/g
        heatcapacity_protein_thr = heatcapacity_protein_thr_init * 4.18/mol_mass_thr;

        heatcapacity_protein_trp_init = 56.92;  #cal/Kmol
        mol_mass_trp = 204.2; #mol/g
        heatcapacity_protein_trp = heatcapacity_protein_trp_init * 4.18/mol_mass_trp;

        heatcapacity_protein_tyr_init = 51.73;  #cal/Kmol
        mol_mass_tyr = 181.2; #mol/g
        heatcapacity_protein_tyr = heatcapacity_protein_tyr_init * 4.18/mol_mass_tyr;

        heatcapacity_protein_val_init = 40.35;  #cal/Kmol
        mol_mass_val = 117.1; #mol/g
        heatcapacity_protein_val = heatcapacity_protein_val_init * 4.18/mol_mass_val;

        Average_heating_capacity_of_soy_protein = (4.3*heatcapacity_protein_ala+7.6*heatcapacity_protein_arg+11.5*heatcapacity_protein_asp+1.2*heatcapacity_protein_cys+19*heatcapacity_protein_glu+4.2*heatcapacity_protein_gly+2.6*heatcapacity_protein_his+4.8*heatcapacity_protein_ile+8.1*heatcapacity_protein_leu+6.2*heatcapacity_protein_lys+1.4*heatcapacity_protein_met+5.2*heatcapacity_protein_phe+5.1*heatcapacity_protein_pro+5.2*heatcapacity_protein_ser+3.7*heatcapacity_protein_thr+1.4*heatcapacity_protein_trp+3.7*heatcapacity_protein_tyr+5*heatcapacity_protein_val)/100;
        #print ("Heating capacity of protein is "+str(round(Average_heating_capacity_of_soy_protein,2))+" KJ/KgK.")

        #heat capacity of lipid
        heatcapacity_lipid_grapeseed_oil = 2.081;  #KJ/KgK
        heatcapacity_lipid_almond_oil = 2.103;  #KJ/KgK
        heatcapacity_lipid_vegetable_oil = 2.081;  #KJ/KgK
        heatcapacity_lipid_olive_oil = 2.116;  #KJ/KgK
        heatcapacity_lipid_cocoa_butter = 2.143;  #KJ/KgK
        heatcapacity_lipid_coconut_oil = 2.111;  #KJ/KgK

        Average_heating_capacity_lipid = 2.106; #KJ/KgK
        #print ("Heating capacity of lipid is "+str(round(Average_heating_capacity_lipid,2))+" KJ/KgK.")

        #heat capacity of lignin
        heatcapacity_lignin = 2.2; #KJ/KgK
        #print ("Heating capacity of lignin is "+str(round(heatcapacity_lignin,2))+" KJ/KgK.")

        #heat capacity of polypropylene
        heatcapacity_PP = 1.92; #KJ/KgK
        #print ("Heating capacity of PP is "+str(round(heatcapacity_PP,2))+" KJ/KgK. \n")
        
        #heat capacity of polystyrene
        heatcapacity_PS = 1.50; #KJ/KgK
        #print ("Heating capacity of PS is "+str(round(heatcapacity_PS,2))+" KJ/KgK. \n")
        
        #heat capacity of polycarbonate
        heatcapacity_PC = 1.25; #KJ/KgK
        #print ("Heating capacity of PC is "+str(round(heatcapacity_PC,2))+" KJ/KgK. \n")     

        #heat capacity of polyethylene terepthalate
        heatcapacity_PET = 1.25; #KJ/KgK	
        #print ("Heating capacity of PET is "+str(round(heatcapacity_PET,2))+" KJ/KgK. \n")
        
        #print ("Heating capacity of water is "+str(round(heatingcapacity_water,2))+" KJ/KgK.\n")

        Heating_capacity_feedstock = (lipid*Average_heating_capacity_lipid+Average_heating_capacity_of_soy_protein*protein+heatcapacity_carbohydrate*carbohydrate+lignin*heatcapacity_lignin+starch*heatcapacity_starch+heatcapacity_PP*PP+heatcapacity_PS*PS+heatcapacity_PC*PC+heatcapacity_PET*PET)/100;
        print ("Heating capacity of feedstock without water is "+str(round(Heating_capacity_feedstock,2))+" KJ/KgK.")

        fractionoffeedstock = feedstock_loading/(feedstock_loading+100/feedstock_loading)
        
        count = 0;
        totalCp = 0;
        for temp in range(298,settemperature+273,10):
            water.calculate(T=temp, P=reactor_pressure*1E6)
            #water.calculate(T=temp, P=(np.exp(34.494 - 4924.99/(temp+237.1))/(temp+105)**1.57)) #https://journals.ametsoc.org/view/journals/apme/57/6/jamc-d-17-0334.1.xml?tab_body=pdf
            count +=1;
            totalCp += water.Cp;
        averageheatingcapacity_water = totalCp/(count*1000); 
        #averageheatingcapacity_water = 3.6175; 

        print ("Heating capacity of water is "+str(round(averageheatingcapacity_water,2))+" KJ/KgK.")
        
        heatingcapacityoffeed=averageheatingcapacity_water*(1-fractionoffeedstock)+Heating_capacity_feedstock*fractionoffeedstock; #J/hr
        print ("Heating capacity of feedstock with water is "+str(round(heatingcapacityoffeed,2))+" KJ/KgK.\n")
        
        self.heatingcapacityoffeed = heatingcapacityoffeed;
        
        #heats of fusion
        Heat_fusion_PP = 165; #KJ/kg https://www.researchgate.net/post/What_is_the_latent_heat_of_polypropylene#:~:text=Latent%20heat%20is%20energy%20released,peak%20temperature%20is%20459%20K.
        Heat_fusion_PS = 105.26; #KJ/kg https://onlinelibrary.wiley.com/doi/epdf/10.1002/pol.1961.1205516208
        Heat_fusion_PC = 134; #KJ/kg https://www.m-ep.co.jp/en/pdf/product/iupi_nova/physicality_04.pdf
        Heat_fusion_PET = 66.94; #KJ/kg https://journals.sagepub.com/doi/pdf/10.1177/004051756903901002

        Heat_integration_factor = 0.9        
        Energy_consumed_by_heating_capacity = heatingcapacityoffeed*(1-Heat_integration_factor)*((settemperature-25)+BPA_purification_choice*(250-25))*massflowrate*((100+feedstock_loading)/feedstock_loading)/Reactorheatingeffeciency; #kJ/hr
        Energy_consumed_by_heating_fusion = massflowrate * (PP*Heat_fusion_PP + PC*Heat_fusion_PC + PS*Heat_fusion_PS + PET*Heat_fusion_PET)/(100*Reactorheatingeffeciency) #kJ/hr
        
        Energy_consumed_for_unreacted_plastic_at_425 = heatingcapacityoffeed*(1-Heat_integration_factor)*(425-25)*(Unreacted_plastic/100)*massflowrate*((100+feedstock_loading)/feedstock_loading)/Reactorheatingeffeciency  + massflowrate * (Unreacted_PP*Heat_fusion_PP + Unreacted_PC*Heat_fusion_PC + Unreacted_PS*Heat_fusion_PS)/(100*Reactorheatingeffeciency); #kJ/hr
        
        #print(Energy_consumed_by_heating_capacity/(massflowrate*1000),Energy_consumed_by_heating_fusion/(massflowrate*1000))
        
        Total_Energy_per_hour = Energy_consumed_by_heating_capacity+Energy_consumed_by_heating_fusion+Energy_consumed_for_unreacted_plastic_at_425 #kJ/hr
        
        #print (Energy_consumed_by_heating_capacity,Energy_consumed_by_heating_fusion)
        print ("Total energy consumed per hour is " + str(round((Total_Energy_per_hour)/1000,2)) + " MJ/hr or " + str(round(Total_Energy_per_hour/(massflowrate*1000),2)) + " MJ/kg.")

        #costofheating = Energy_consumed_by_heating_capacity*costofheating;
        #costpermass = costofheating/massflowrate;
        #print ("Cost of heating reactors is " + str(round(costofheating,3)) + " $/hr or " + str(round(costpermass,3)) + " $/kg.\n")
        
        #energy recovery calculation:
        
        Cellulose_feedstock = 18.60;
        Lignin_feedstock = 23.26;
        Starch_feedstock = 14.96;
        Soy_protein_feedstock = 19.63;
        Stearic_acid_feedstock = 40.99;
        PP_feedstock = 49.03;
        PS_feedstock = 41.88;
        PC_feedstock = 30.25;
        PET_feedstock = 21.73;
        
        HHV_feedstock = (carbohydrate*Cellulose_feedstock+lignin*Lignin_feedstock+starch*Starch_feedstock+protein*Soy_protein_feedstock+lipid*Stearic_acid_feedstock+PP*PP_feedstock+PC*PC_feedstock+PS*PS_feedstock+PET*PET_feedstock)/100;
        
        print ("The HHV of feedstock is: " + str(round(HHV_feedstock,2)) + " MJ/kg \n")
        
        energyconsumedperkg_HTL = Total_Energy_per_hour/(massflowrate*1000); #MJ/kg
        self.energyconsumedperkg_HTL = energyconsumedperkg_HTL
                
        Energy_recovery = (Total_oil_yield*HHV_mixture-energyconsumedperkg_HTL)/(HHV_feedstock);
        
        print ("Energy recovery at this stage is : " + str(round(Energy_recovery,3)) + " % \n")
        print ("************************************************************************\n")
        
        office_space = 1000 #sq. ft
        Energy_needed_for_offices = 112.5 #kg natural gas equivalent/sq. ft
        kg_natural_gas_for_office = Energy_needed_for_offices * office_space;
        
        #electrity for HTL (pump)
                
        differential_head = reactor_pressure*145.03*2.31 #https://www.watertechonline.com/home/article/15530072/head-and-pressure-in-pumps#:~:text=In%20simple%20terms%2C%20the%20mathematical,2.31%20equals%20head%20in%20feet. reason for the 2.31 - pressure to head conversion
        pump_effeciency = 0.6
        Pump_work = (100+feedstock_loading)/(feedstock_loading)/massflowrate* differential_head * 9.81 * 1000 / (pump_effeciency*3.6 * 10**6) #kW
        #Pump_energy = 6.54; #kWh for 100 m3/h
        #Pump_energy_needed_forHTL = 2*Pump_energy * 3600 * (100+feedstock_loading)/(feedstock_loading*100); #kJ/kg, 2 pumps needed (one for recycle)
        Pump_energy_needed_forHTL = 2.4*Pump_work * 3600; #kJ/kg, 4 pumps needed (2 for process and 2 for recycle. Recycle requieres 20 % of the power for the other)
        
        self.Pump_energy_needed_forHTL = Pump_energy_needed_forHTL
        
        recycle_effeciency = 24; #once a day
        fresh_water_needed = 100/(feedstock_loading*recycle_effeciency); #perkg basis
        
        #TransporttoHTL
        #waste source: MSW
        #cite https://www.tandfonline.com/doi/pdf/10.1080/10962247.2014.990587?needAccess=true
        
        Mileage_MSWtrucks = 2.5; #miles/gallon Gordon, Deborah, Juliet Burdelski, and James S. Cannon.  Greening Garbage Trucks: New Technologies for Cleaner Air.  Inform, Inc. 2003.  ISBN #0-918780-80-2.
        truck_capacity = 12000; #kgs
        Truck_distance = 50; #miles
        Gasoline_consumption_to_HTL = Truck_distance / (truck_capacity*Mileage_MSWtrucks); #L_gasoline/kg waste
        
        return Total_oil_yield,Lightfraction_in_mixture,costofheating,C_mixture,H_mixture,N_mixture,S_mixture,O_mixture,Total_Energy_per_hour,TPA_yield, BPA_purification_choice*BPA_yield, Carbon_in_plastic_feedstock, fresh_water_needed, kg_natural_gas_for_office, Pump_energy_needed_forHTL, Gasoline_consumption_to_HTL, biochar_yield, Gas_yield,Gas_yield_fromplastic, Energy_consumed_for_unreacted_plastic_at_425

    def HTL_upgrading(self):
        #HTL upgrading (adapted from 4 PNNL studies)
        print ("Upgrading oil from HTL process:\n")
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        energyconsumedperkg_HTL = self.energyconsumedperkg_HTL
        Yield = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        heatingcapacityoffeed = self.heatingcapacityoffeed;
        
        #multiplicative method
        #effectofupgrading
        change_in_C = 1.087; #increase in C in oil phase due to upgradation
        change_in_H = 1.403; #increase in H in oil phase due to upgradation
        change_in_O = 0.200; #increase in O in oil phase due to upgradation
        change_in_N = 0.072; #increase in N in oil phase due to upgradation
        change_in_S = 0.25; #increase in S in oil phase due to upgradation
        oil_yield_from_upgrading = 82.11;
        Hydrogen_consumption = 0.04842; #g/g of biooil
        #sensitivityofupgrading
        stddev_in_C = 0.017; #standard deviation of increase in C in oil phase due to upgradation
        stddev_in_H = 0.070; #standard deviation of increase in H in oil phase due to upgradation
        stddev_in_O = 0.090; #standard deviation of increase in O in oil phase due to upgradation
        stddev_in_N = 0.086; #standard deviation of increase in N in oil phase due to upgradation
        stddev_in_S = 0.061; #standard deviation of increase in S in oil phase due to upgradation
        stddev_oil_yield_from_upgrading = 5.44;
        stddev_Hydrogen_consumption = 0.008585;
        Hydrogen_consumption_per_kg_feedstock = Yield*Hydrogen_consumption/100;
        
        #calculations
        upgraded_oil_yield = oil_yield_from_upgrading*Yield/100;
        upgraded_oil_C = self.C_mixture * change_in_C;
        upgraded_oil_H = self.H_mixture * change_in_H;
        upgraded_oil_O = self.O_mixture * change_in_O;
        upgraded_oil_N = self.N_mixture * change_in_N;
        upgraded_oil_S = self.S_mixture * change_in_S;
        HHV_upgraded_oil = 0.3383*upgraded_oil_C+1.445*upgraded_oil_H-0.1805*upgraded_oil_O+0.0938*upgraded_oil_S+0.023*upgraded_oil_N;

        Hydrogen_requirement = massflowrate * upgraded_oil_yield * Hydrogen_consumption/1000; #kgH2/hr
        
        Percentage_naptha = 100 - 0.9826*self.C_mixture - 0.1401*self.O_mixture

        print ("The oil blendstock is: " + str(round(Percentage_naptha,2)) + " % naptha (gasoline) and " + str(round(100-Percentage_naptha,2)) + " % diesel ")

        print ("Multiplicative method\nUpgraded oil: \nC content: " + str(round(upgraded_oil_C,2)) + " wt.% ")
        print ("H content: " + str(round(upgraded_oil_H,2)) + " wt.%")
        print ("O content: " + str(round(upgraded_oil_O,2)) + " wt.%")
        print ("N content: " + str(round(upgraded_oil_N,2)) + " wt.%")
        print ("S content: " + str(round(upgraded_oil_S,2)) + " wt.%\n")
        print ("Heating value is: " + str(round(HHV_upgraded_oil,2)) + " MJ/kg\n")
        
        temperatureforupgrading = 400; #(C)
        heatcapacityoil = 1.67; #KJ/kgK
        exact_heatcapacity_oil = 0;
        for temp in range (26,temperatureforupgrading):
            exact_heatcapacity_oil += 2.2233 + 0.4144*0.001*(temp); #KJ/KgK 
        heatcapacityoil = exact_heatcapacity_oil/(temperatureforupgrading-25) #KJ/KgK   
        
        heatcapacity_catalyst = 0.911; #https://www.sciencedirect.com/science/article/pii/S129325580001102X?via%3Dihub
        WHSV_catalyst = 0.37 #kg. feedstock/ kg catalyst
        heat_catalyst = heatcapacity_catalyst/(WHSV_catalyst*20) #catalyst bed heated once a day
        
        exact_heatcapacity_hydrogen = 0; #NIST database
        for temp in range (26,temperatureforupgrading):
            exact_heatcapacity_hydrogen += 20.79 + 0.48506*0.0000000001*(temp+273); #KJ/KgK 
        heatcapacityhydrogen = exact_heatcapacity_hydrogen/(temperatureforupgrading-25)
        
        Heat_for_Highpressureseperator = 0.121*massflowrate/1000; #MJ/h https://pacs.ou.edu/media/filer_public/c9/4a/c94a97ac-9609-4262-ab06-b7b2dda1c4fa/3_oil_and_gas_separation_design_manual_by_c_richard_sivalls.pdf
        Heat_for_Lowpressureseperator = 5.400; #MJ/h http://folk.ntnu.no/tomgra/Diplomer/Kylling.pdf
        
        Reactorheatingeffeciency = 0.8
        Energy_required_for_heating = ((massflowrate * upgraded_oil_yield * (heatcapacityoil + Hydrogen_consumption*heatcapacityhydrogen+heat_catalyst) * (temperatureforupgrading-25))/100000 +Heat_for_Highpressureseperator + Heat_for_Lowpressureseperator)/Reactorheatingeffeciency; #MJ/h
        Energy_needed_perkg_basis = Energy_required_for_heating/massflowrate; #MJ/kg
        
        print("The Total energy per kg for upgrading is " + str(round(Energy_needed_perkg_basis,3)) + " MJ/kg \n")
        
        Energy_for_heating = (upgraded_oil_yield * (heatcapacityoil + Hydrogen_consumption*heatcapacityhydrogen+heat_catalyst) * (temperatureforupgrading-25))/100000;
        print("The heating energy per kg for upgrading is " + str(round(Energy_for_heating,3)) + " MJ/kg \n")
        
        #energy recovery calculation:
        
        Cellulose_feedstock = 18.60;
        Lignin_feedstock = 23.26;
        Starch_feedstock = 14.96;
        Soy_protein_feedstock = 19.63;
        Stearic_acid_feedstock = 40.99;
        PP_feedstock = 49.03;
        PS_feedstock = 41.88;
        PC_feedstock = 30.25;
        PET_feedstock = 21.73;
        
        HHV_feedstock = (carbohydrate*Cellulose_feedstock+lignin*Lignin_feedstock+starch*Starch_feedstock+protein*Soy_protein_feedstock+lipid*Stearic_acid_feedstock+PP*PP_feedstock+PC*PC_feedstock+PS*PS_feedstock+PET*PET_feedstock)/100;
        
        Energy_recovery = ((upgraded_oil_yield*HHV_upgraded_oil)-(0.1*energyconsumedperkg_HTL+Energy_needed_perkg_basis*Yield/1000))/(HHV_feedstock+Hydrogen_consumption*141.7);
        
        print ("Energy recovery at this stage is : " + str(round(Energy_recovery,3)) + " % \n")
        print ("************************************************************************\n")

        #pump energy
        #pump_head = 75; #m
        #Energyofpump = massflowrate * (upgraded_oil_yield/100) * pump_head * 9.8/1000; #MJ/h
        #electrity for HTL (pump)
        differential_head = 500; #m
        pump_effeciency = 0.6
        oil_density = 800; #kg/m3
        Pump_work = (Yield/100) * differential_head * 9.81 * oil_density / (pump_effeciency*3.6 * 10**6) #kW
        #pump_power = 0.654; #kW
        Energyofpump = 2 * Pump_work * 3600/ massflowrate; #kJ/kg (2 pumps in total - one for upgrading and cracking)
        
        office_space = 1000 #sq. ft
        Energy_needed_for_offices = 112.5 #kg natural gas equivalent/sq. ft
        kg_natural_gas_for_office = Energy_needed_for_offices * office_space;
        
        #hydrogenforupgrading
        EmmisionperkgH2 = 11.23; #kg CO2/ kg H2 produced cite: https://www.iea.org/fuels-and-technologies/hydrogen
        Emmision_from_H2 = EmmisionperkgH2 * Hydrogen_requirement/massflowrate; #kg CO2/ kg feedstock
        
        #HTL_oil_to_upgrading facility
        Mileage_tankers = 6; #milespergallon https://www.truckloadindexes.com/data-commentary/how-many-gallons-does-it-take-to-fill-up-a-big-rig#:~:text=How%20far%20can%20a%20big,consumption%20rate%20of%206%20mpg.
        truck_capacity = 3500*3.78*0.87; #kg https://en.wikipedia.org/wiki/Tank_truck
        Truck_distance = 70; #miles cite http://www.columbia.edu/~sc32/documents/ALEP%20Waste%20Managent%20FINAL.pdf
        
        Gasoline_consumption_HTL_oil_to_upgrading = Yield/100 * Truck_distance / (truck_capacity*Mileage_tankers); #L_gasoline/kg waste
        Gasoline_consumption_HTL_upgraded_oil_to_consumer = upgraded_oil_yield * Yield/10000 * Truck_distance / (truck_capacity*Mileage_tankers); #L_gasoline/kg waste
        
        Energy_from_oil = upgraded_oil_yield*HHV_upgraded_oil/100 #MJ/kg
        
        return HHV_upgraded_oil,upgraded_oil_yield,upgraded_oil_C,upgraded_oil_H,upgraded_oil_O,upgraded_oil_N,upgraded_oil_S,Hydrogen_requirement,Energy_required_for_heating,Energyofpump, kg_natural_gas_for_office, Emmision_from_H2, Gasoline_consumption_HTL_oil_to_upgrading, Gasoline_consumption_HTL_upgraded_oil_to_consumer, office_space, Hydrogen_consumption_per_kg_feedstock, Percentage_naptha, Energy_from_oil
    
    def solid_handling(self):
        print ("Solid handling: \n")        
        solid_handling_opt = 2; #0 - DMSO dissolution method, 1 - Density method 2 - Supercritical water method
        PET = self.PET
        massflowrate = self.massflowrate;
        solid_yield = self.solid_yield;
        IMS_value = 702.3; #2019
        CMS_value = 567;
        Solvent_recovery = 0.982; #https://www.sciencedirect.com/science/article/pii/S0959652620327918
        recycle_effeciency = massflowrate * 20;
                
        if solid_handling_opt == 0:
            DMSO_solubility = 0.20 #g TPA/g DMSO
            DMSO_needed = self.TPA_yield/(DMSO_solubility*100); #per kg feedstock
            Evaporator_energy_effeciency = 0.6;
            Specific_heat_DMSO = 149.39/78.13; #KJ/Kg*K https://webbook.nist.gov/cgi/cbook.cgi?ID=C67685&Mask=2
            latent_heat_for_vaporisation = 12.56*4.18*1000/78.13; #KJ/Kg
            Heat_needed_for_evaporation = DMSO_needed*(latent_heat_for_vaporisation+Specific_heat_DMSO*(190-25))/Evaporator_energy_effeciency
            TPA_process_yield = self.TPA_yield
            Biochar_yield = self.biochar_yield
            DMSO_consumed = DMSO_needed*(1-Solvent_recovery)/20
            Hexane_consumed = 0
            Water_needed = 0
            
            Crystallization_NaOH_needed = 0.4113; #g NaOH/ g TPA
            NaOH_recycle_ratio = 10;
            Crystallization_H2SO4_needed = 0.4935; #g H2SO4/ g TPA
            H2SO4_recycle_ratio = 10;
            
            NaOH_needed = self.TPA_yield/(Crystallization_NaOH_needed*100*NaOH_recycle_ratio);
            H2SO4_needed = self.TPA_yield/(Crystallization_H2SO4_needed*100*H2SO4_recycle_ratio);
            Water_crystallization_needed = self.TPA_yield/(0.011*100)
            
            Heat_needed_crystallization = (60-25)*4.18*Water_crystallization_needed;
            
            Water_needed_1 = Water_crystallization_needed + Water_needed
            Water_needed = Water_needed_1
            
            Heat_needed = Heat_needed_for_evaporation + Heat_needed_crystallization
            
            #equipement used is a mixer followed by simple distillation column + dryer
            #pump
            differential_head = 500; #m
            pump_effeciency = 0.6
            DMSO_density = 1100; #kg/m3
            Pump_work = (DMSO_needed)*massflowrate * differential_head * 9.81 / (pump_effeciency*3.6 * 10**6) #kW
            
            Pump_energy_needed_for_solid_handling = Pump_work * 3600/ massflowrate; #kJ/kg 
            Pc_pump = Pump_energy_needed_for_solid_handling*massflowrate*0.0003725; #hp
            
            if Pc_pump<1:
                Pc_pump = 1
                
            #Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump)) #Seidar book
            Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump) - 0.110056*(np.log(Pc_pump))**2 + 0.071413*(np.log(Pc_pump))**3 - 0.0063788*(np.log(Pc_pump))**4) 
            
            Total_electricity = Pump_energy_needed_for_solid_handling
            
            volume_for_mixer = DMSO_needed*massflowrate/(3.79*1.1) #gallons
            mixer_cost = 265*volume_for_mixer**0.513; #Cone roof
            distillation_column_base_cost = 462800; #1000 lb/hr
            scaling_factor = 0.8;
            distillation_column_cost = distillation_column_base_cost*((DMSO_needed*massflowrate)/(453.592*60.66))**scaling_factor
            drying_unit = 2*math.exp(8.5133 + 0.9847*(math.log(DMSO_needed*massflowrate*2.2/100))-0.0561*(math.log(DMSO_needed*massflowrate*2.2/100))**2) #spray dryer
            Cp_pelletizer = 7938*(Biochar_yield*massflowrate*2.2/100)**0.11 #pellet mills
            
            Overall_HTC = 200*0.176; #BTu/hr-ft2 - degF https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.381.6320&rep=rep1&type=pdf
            Heat_transfer_area_crystallizer = 4*3.28; #ft2/ft lenght
            Lenght_crystallizer = (Water_crystallization_needed*4.18*massflowrate*0.94)/(Heat_transfer_area_crystallizer*(5/9)*Overall_HTC)
            Cp_crystallizer = 16440*Lenght_crystallizer**0.67;
            
            #sifter
            area_sifter = massflowrate*solid_yield/20000 #ft2
            if area_sifter < 40:
                Cp_sifter = 6575*area_sifter**0.34
                print ("Sifter type:\t\t\t Vibrating grizzlies")
            elif area_sifter < 60:
                Cp_sifter = 1588*area_sifter**0.71
                print ("Sifter type:\t\t\t Vibrating screens 1 deck")
            else:
                Cp_sifter = 1010*area_sifter**0.91
                print ("Sifter type:\t\t\t Vibrating screens 3 deck")
                        
            Total_cost = (mixer_cost+distillation_column_cost+drying_unit+Cp_pump+Cp_pelletizer+Cp_crystallizer + Cp_sifter)*IMS_value/CMS_value

            print ("Cp Solid handling mixer:\t\t $", round(mixer_cost*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(mixer_cost*IMS_value/CMS_value))
            print ("Cp Solid handling distillation:\t\t $", round(distillation_column_cost*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(distillation_column_cost*IMS_value/CMS_value))
            print ("Cp Solid handling drying unit:\t\t $", round(drying_unit*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(drying_unit*IMS_value/CMS_value))
            print ("Cp Solid handling pump:\t\t $", round(Cp_pump*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_pump*IMS_value/CMS_value))
            print ("Cp Solid handling crystallizer:\t\t $", round(Cp_crystallizer*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_crystallizer*IMS_value/CMS_value))
            
            Water_to_evaporate = 0
            
            self.SHCp_Heat_exchanger = 0*IMS_value/CMS_value                        
            self.SHCp_filter = 0*IMS_value/CMS_value
            self.SHCp_oil_tank = 0*IMS_value/CMS_value                        
            self.SHCp_sifter = 0*IMS_value/CMS_value
            self.SHCp_reactor = 0*IMS_value/CMS_value                        
            self.SHCp_pump = 0*IMS_value/CMS_value
            self.SHCp_pelletizer = 0*IMS_value/CMS_value
            self.SHCp_crystallizer = Cp_crystallizer*IMS_value/CMS_value  
            self.SHCp_feed_tank = 0*IMS_value/CMS_value
            self.SHCp_open_tank = 0*IMS_value/CMS_value
            
        elif solid_handling_opt == 1:
            TPA_water_solubility = 0.0015; #kg TPA/L water
            Water_needed = 100*solid_yield/(20*100); #solid content is typically less than 1 % L/kg feedstock
            TPA_process_yield = self.TPA_yield * (1-Water_needed*TPA_water_solubility/massflowrate)
            Biochar_yield = self.biochar_yield
            Hexane_needed = 100*Biochar_yield/100
            Hexane_consumed = Hexane_needed*(1-Solvent_recovery)/20
            DMSO_consumed = 0
           
            Water_fraction_to_evaporate = 1000; #10 wt. % of TPA mass is water
            Water_to_evaporate = Water_needed/Water_fraction_to_evaporate
            Latent_heat_of_vaporisation_water = 2260 #kJ/kg
            Latent_heat_of_vaporisation_hexane = 365 #kJ/kg
            Specific_heat_Hexane = 2.26; #KJ/Kg*K https://www.engineeringtoolbox.com/specific-heat-fluids-d_151.html
            Specific_heat_Water = 4.18; #KJ/Kg*K https://www.engineeringtoolbox.com/specific-heat-fluids-d_151.html            
            Heat_needed_for_evaporation = Water_to_evaporate*((100-25)*Specific_heat_Water+Latent_heat_of_vaporisation_water)+Hexane_consumed*((69-25)*Specific_heat_Hexane+Latent_heat_of_vaporisation_hexane)
            
            Crystallization_NaOH_needed = 0.4113; #g NaOH/ g TPA
            NaOH_recycle_ratio = 10;
            Crystallization_H2SO4_needed = 0.4935; #g H2SO4/ g TPA
            H2SO4_recycle_ratio = 10;
            
            NaOH_needed = self.TPA_yield/(Crystallization_NaOH_needed*100*NaOH_recycle_ratio);
            H2SO4_needed = self.TPA_yield/(Crystallization_H2SO4_needed*100*H2SO4_recycle_ratio);
            Water_crystallization_needed = self.TPA_yield/(0.011*100)
            
            Heat_needed_crystallization = (60-25)*4.18*Water_crystallization_needed;
            
            Water_needed_1 = Water_crystallization_needed + Water_needed
            Water_needed = Water_needed_1
            
            Heat_needed = Heat_needed_for_evaporation + Heat_needed_crystallization
            
            #Electricity
            volumeflowrate = massflowrate*Water_to_evaporate/1000;
            Energyforcentrifugation_perunitvolume = (21.22151 + 4.068515*math.exp(0.01441221*volumeflowrate))*3.6; #https://onlinelibrary.wiley.com/doi/10.1002/ceat.201800292#:~:text=Currently%2C%20centrifugal%20separators%20operate%20approximately,3%20for%20some%20cases%20with
            print ("Volumetric flow rate of TPA + plastics in water is " + str(round(volumeflowrate,2)) + " m3/hr ")   
            Energyneededforcentrifugation = Energyforcentrifugation_perunitvolume*volumeflowrate/1000;
            print ("Energy for centrifugation in solid handling is " + str(round(Energyneededforcentrifugation,2)) + " MJ/hr or " + str(round(Energyneededforcentrifugation/(massflowrate),5)) + " MJ/kg \n")
            
            #equipement used is a gravity seperator (clarifier) followed by a centrifuge + dryer
            Settling_area_gravity_sep_water = 0.5*Water_needed*massflowrate/(60*3.79) 
            Settling_area_gravity_sep_hexane = 0.5*Hexane_needed*massflowrate/(60*3.79) 
            Cp_clarifier = 3460*Settling_area_gravity_sep_water**0.58 + 3460*Settling_area_gravity_sep_hexane**0.58 #2 items
            Cp_centrifuge = 2440*40**1.11;
            Cp_drying_unit_water = math.exp(8.5133 + 0.9847*(math.log(Water_to_evaporate*massflowrate*2.204))-0.0561*(math.log(Water_to_evaporate*massflowrate*2.204))**2) #1 items
            Cp_drying_unit_hexane = 2*math.exp(8.5133 + 0.9847*(math.log(Hexane_consumed*massflowrate*2.204))-0.0561*(math.log(Hexane_consumed*massflowrate*2.204))**2) #2 items
            Cp_drying_unit = Cp_drying_unit_water + Cp_drying_unit_hexane
    
            #sifter
            area_sifter = massflowrate*solid_yield/20000 #ft2
            if area_sifter < 40:
                Cp_sifter = 6575*area_sifter**0.34
                print ("Sifter type:\t\t\t Vibrating grizzlies")
            elif area_sifter < 60:
                Cp_sifter = 1588*area_sifter**0.71
                print ("Sifter type:\t\t\t Vibrating screens 1 deck")
            else:
                Cp_sifter = 1010*area_sifter**0.91
                print ("Sifter type:\t\t\t Vibrating screens 3 deck")
            
            #pump
            differential_head = 500; #m
            pump_effeciency = 0.6
            Pump_work = (Water_needed+Hexane_needed)*massflowrate/(1000) * differential_head * 9.81 * 1000 / (pump_effeciency*3.6 * 10**6) #kW
            
            Pump_energy_needed_for_solid_handling = Pump_work * 3600/ massflowrate; #kJ/kg 
            Pc_pump = Pump_energy_needed_for_solid_handling*massflowrate*0.0003725;
            #Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump))*IMS_value/CMS_value  #Seidar book
            Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump) - 0.110056*(np.log(Pc_pump))**2 + 0.071413*(np.log(Pc_pump))**3 - 0.0063788*(np.log(Pc_pump))**4) 
            
            #pelletizer
            Cp_pelletizer = 7938*(Biochar_yield*massflowrate*2.2/100)**0.11
            
            #crystallizer
            Overall_HTC = 200*0.176; #BTu/hr-ft2 - degF
            Heat_transfer_area_crystallizer = 4*3.28; #ft2/ft lenght
            Lenght_crystallizer = (Water_crystallization_needed*4.18*massflowrate*0.94)/(Heat_transfer_area_crystallizer*(5/9)*Overall_HTC)
            Cp_crystallizer = 16440*Lenght_crystallizer**0.67;
            
            Total_cost = (Cp_centrifuge+Cp_clarifier+Cp_drying_unit+Cp_sifter+Cp_pump+Cp_pelletizer+Cp_crystallizer)*IMS_value/CMS_value

            print ("Cp Solid handling centrifuge:\t\t $", round(Cp_centrifuge*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_centrifuge*IMS_value/CMS_value))
            print ("Cp Solid handling clarifier:\t\t $", round(Cp_clarifier*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_clarifier*IMS_value/CMS_value))
            print ("Cp Solid handling drying unit:\t\t $", round(Cp_drying_unit*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_drying_unit*IMS_value/CMS_value))
            print ("Cp Solid handling sifter:\t\t $", round(Cp_sifter*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_sifter*IMS_value/CMS_value))
            print ("Cp Solid handling pump:\t\t $", round(Cp_pump*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_pump*IMS_value/CMS_value))
            print ("Cp Solid handling crystallizer:\t\t $", round(Cp_crystallizer*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_crystallizer*IMS_value/CMS_value))
            
            self.SHCp_Heat_exchanger = 0*IMS_value/CMS_value                        
            self.SHCp_filter = 0*IMS_value/CMS_value
            self.SHCp_oil_tank = 0*IMS_value/CMS_value                        
            self.SHCp_sifter = 0*IMS_value/CMS_value
            self.SHCp_reactor = 0*IMS_value/CMS_value                        
            self.SHCp_pump = 0*IMS_value/CMS_value
            self.SHCp_pelletizer = 0*IMS_value/CMS_value
            self.SHCp_crystallizer = Cp_crystallizer*IMS_value/CMS_value
            self.SHCp_feed_tank = 0*IMS_value/CMS_value
            self.SHCp_open_tank = 0*IMS_value/CMS_value
            
            Total_electricity = (Pump_energy_needed_for_solid_handling + Energyneededforcentrifugation)/massflowrate
            
        elif solid_handling_opt == 2: # reactor, solid removal chamber, Heat exchanger, sifter
            TPA_solubility = 29.9/1000*166.13/18; #250 C average  https://pubs.acs.org/doi/abs/10.1021/je300263z
            Water_needed = self.TPA_yield/(TPA_solubility*100)
            #Process heated at 250 C
            TPA_step_yield = 100;
            Specific_heat_Water = 4.18; #KJ/Kg*K https://www.engineeringtoolbox.com/specific-heat-fluids-d_151.html            
            Latent_heat_of_vaporisation_water = 2260 #kJ/kg
            TPA_process_yield = self.TPA_yield *TPA_step_yield/100
            Biochar_yield = self.biochar_yield
            Hexane_consumed = 0
            Water_wasted_ratio = 100
            Water_to_evaporate = Water_needed/Water_wasted_ratio
            Heat_needed_for_evaporation = Water_needed*(250-25)*Specific_heat_Water+Water_to_evaporate*Latent_heat_of_vaporisation_water   #kJ/kg feed
            DMSO_consumed = 0;
            
            Crystallization_NaOH_needed = 0.4113; #g NaOH/ g TPA https://patentimages.storage.googleapis.com/05/20/75/6070b531fdbc62/US3505398.pdf
            NaOH_recycle_ratio = 10;
            Crystallization_H2SO4_needed = 0.4935; #g H2SO4/ g TPA
            H2SO4_recycle_ratio = 10;
            
            NaOH_needed = self.TPA_yield/(Crystallization_NaOH_needed*100*NaOH_recycle_ratio);
            H2SO4_needed = self.TPA_yield/(Crystallization_H2SO4_needed*100*H2SO4_recycle_ratio);
            Water_crystallization_needed = self.TPA_yield/(0.011*100)
            
            Heat_needed_crystallization = (60-25)*4.18*Water_crystallization_needed;
            
            Water_needed_1 = Water_crystallization_needed + Water_needed
            Water_needed = Water_needed_1
            
            #https://patentimages.storage.googleapis.com/ae/53/4b/47ee578cf312f9/US3477829.pdf
            
            
            Heat_needed = Heat_needed_for_evaporation + Heat_needed_crystallization
            
            #Cost
            #reactor
            print ("Reactor Material: \t\t Stainless Steel")
            print ("Reactor Pressure: \t\t 25 MPa")
            print ("Reactor Diameter: \t\t 10 ft")
    
            Fm_reactor = 1.0 #CI solid
            Fp_reactor = 2.50 #10 MPa 
            Fc_reactor = Fm_reactor * Fp_reactor
            
            D_reactor = 10 #ft
            Reactor_allowance = 2
            V_reactor = Reactor_allowance*Water_needed*massflowrate
            H_reactor = V_reactor/(3.14*D_reactor**2*60)
            
            Cp_reactor = 101.9*(2.18+Fc_reactor)*IMS_value*(D_reactor**1.066)*(H_reactor**0.802)/CMS_value
            
            heating_oil_needed = massflowrate/10
            Oil_tank_allowance = 2
            Oil_density = 0.264172/0.95; #gal/kg
            Cp_oil_tank = 265*(heating_oil_needed*Oil_tank_allowance*Oil_density)**0.513*IMS_value/(CMS_value)
            
            #filters
            print ("Solid filter type:\t\t Rotary drum filter") #solid removal is solid filter
            area_filter = massflowrate*solid_yield/(113.25*100); #ft2
            Cp_filter = 28010*area_filter**0.48*IMS_value/CMS_value;
            
            #heat exchanger
            Area_Heat_exchanger = 5138.18*(massflowrate*solid_yield/(23000*100)) #put in actual value later
            print ("Heat exchanger: \t\t Shell and tube: Floating head")
            Cp_Heat_exchanger = np.exp(12.0310-0.8709*np.log(Area_Heat_exchanger)+0.09*np.log(Area_Heat_exchanger)**2)*IMS_value/CMS_value #Spiral plate
            
            #sifter
            area_sifter = solid_yield*massflowrate/(200*100) #ft2
            if area_sifter < 40:
                Cp_sifter = 6575*area_sifter**0.34*IMS_value/CMS_value
                print ("Sifter type:\t\t\t Vibrating grizzlies")
            elif area_sifter < 60:
                Cp_sifter = 1588*area_sifter**0.71*IMS_value/CMS_value
                print ("Sifter type:\t\t\t Vibrating screens 1 deck")
            else:
                Cp_sifter = 1010*area_sifter**0.91*IMS_value/CMS_value
                print ("Sifter type:\t\t\t Vibrating screens 3 deck")
            
            #pump
            differential_head = 1330.0; #m 3.97 MPa pressure
            pump_effeciency = 0.6
            Pump_work = (Water_needed)*massflowrate * (differential_head * 9.81)/ (pump_effeciency*3.6 * 10**6) #kW
            #+ (massflowrate/1000)*3.97*10**6
            Pump_energy_needed_for_solid_handling = Pump_work * 3600/ massflowrate; #kJ/kg 
            Pc_pump = Pump_energy_needed_for_solid_handling*massflowrate*0.0003725;
            print ("Pump energy: ", Pc_pump)
            #Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump))*IMS_value/CMS_value  #Seidar book
            Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump) - 0.110056*(np.log(Pc_pump))**2 + 0.071413*(np.log(Pc_pump))**3 - 0.0063788*(np.log(Pc_pump))**4) 
            
            Total_electricity = (Pump_energy_needed_for_solid_handling)/(1000*massflowrate) #MJ/kg
            
            Cp_pelletizer = 7938*(Biochar_yield*massflowrate*2.2/100)**0.11
            
            Overall_HTC = 200*0.176; #BTu/hr-ft2 - degF
            Heat_transfer_area_crystallizer = 4*3.28; #ft2/ft lenght
            Lenght_crystallizer_1 = ((Water_crystallization_needed)*4.18*massflowrate*0.94)/(Heat_transfer_area_crystallizer*(5/9)*Overall_HTC)
            Lenght_crystallizer_2 = ((NaOH_needed+H2SO4_needed)*4.18*massflowrate*0.94)/(Heat_transfer_area_crystallizer*(5/9)*Overall_HTC) 
            Cp_crystallizer = 16440*Lenght_crystallizer_1**0.67 + 16440*Lenght_crystallizer_2**0.67;

            print ("Cp Solid handling crystallizer:\t\t $", round(Cp_crystallizer*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(Cp_crystallizer*IMS_value/CMS_value))
            
            #piston feed tank
            volume_feed_tank = massflowrate*Water_needed*35.3147*2/1000 #ft3 #feed tank allowance = 2
            if volume_feed_tank < 94.63:
                Cp_feed_tank = 1700*volume_feed_tank**0.60*IMS_value/CMS_value
                print ("Feed tank type:\t\t\t Tumblers - twin shell")
            else:
                Cp_feed_tank = 3856*volume_feed_tank**0.42*IMS_value/CMS_value
                print ("Feed tank type:\t\t\t Tumblers - double cone")           
            
            Tank_allowance = 4
            Cp_open_tank = 18*((Biochar_yield*massflowrate*Tank_allowance/(3.79*100*0.3)))**0.73
            
            self.SHCp_Heat_exchanger = Cp_Heat_exchanger*IMS_value/CMS_value                        
            self.SHCp_filter = Cp_filter*IMS_value/CMS_value
            self.SHCp_oil_tank = Cp_oil_tank*IMS_value/CMS_value                        
            self.SHCp_sifter = Cp_sifter*IMS_value/CMS_value
            self.SHCp_reactor = Cp_reactor*IMS_value/CMS_value                        
            self.SHCp_pump = Cp_pump*IMS_value/CMS_value
            self.SHCp_pelletizer = Cp_pelletizer*IMS_value/CMS_value
            self.SHCp_crystallizer = Cp_crystallizer*IMS_value/CMS_value
            self.SHCp_feed_tank = Cp_feed_tank*IMS_value/CMS_value
            self.SHCp_open_tank = Cp_open_tank*IMS_value/CMS_value
            
            Total_cost = (Cp_pelletizer+Cp_sifter+Cp_Heat_exchanger+Cp_filter+Cp_oil_tank+Cp_reactor + Cp_feed_tank+ Cp_pump*IMS_value/CMS_value + Cp_crystallizer*IMS_value/CMS_value + Cp_open_tank*IMS_value/CMS_value)
                
        print("Total cost price of the solid handling system is: ", round(Total_cost,2), " $")
        print("Total heat needed for the process is: ", round(Heat_needed_for_evaporation,2), " kJ/kg feed")
        print("The TPA yield from process is ", round(TPA_process_yield,2), " % in terms of feedstock mass")
        print("The Biochar yield is: ", round(Biochar_yield,2), " % in terms of feedstock mass")

        print ("\n************************************************************************\n")

        self.solid_handling_cost = Total_cost
        
        return Total_cost, TPA_process_yield, Biochar_yield, Hexane_consumed,Heat_needed, Total_electricity, Water_to_evaporate, DMSO_consumed, NaOH_needed, H2SO4_needed

    def BPA_purification(self):
        
        Oil_250C_yield = self.BPA_yield
        massflowrate = self.massflowrate
        BPA_process_yield = 0.9;
        flowrate = Oil_250C_yield*massflowrate/100
        eluent_flowrate = 10*flowrate
        IMS_value = 702.3; #2019
        CMS_value = 567;
        Chromotograph_capitol_cost = 187867.60 #$ for 476 L/hr system https://pubs.rsc.org/en/content/articlelanding/2013/GC/C2GC36239B#cit42
        scaling_factor = 0.80
        Cp_chromatograph = 2*Chromotograph_capitol_cost*(flowrate/(476))**scaling_factor
        distillation_column_cost = 462800; #1000 lbmol/hr with avg mol mass 60.66
        Cp_distillation_column = 2*distillation_column_cost*(eluent_flowrate/(1000*60.66*0.453592))**scaling_factor
        
        #add heat/ electricity
        Heat_needed_for_distillation_column = 0.121*flowrate/1000; #MJ/h https://pacs.ou.edu/media/filer_public/c9/4a/c94a97ac-9609-4262-ab06-b7b2dda1c4fa/3_oil_and_gas_separation_design_manual_by_c_richard_sivalls.pdf

        #pump
        differential_head = 500; #m
        pump_effeciency = 0.6
        Pump_work = flowrate * differential_head * 9.81 * 800 / (pump_effeciency*3.6 * 10**6) #kW
            
        Pump_energy_needed_for_BPA_purif = Pump_work * 3600/ massflowrate; #kJ/kg 
        Pc_pump = Pump_energy_needed_for_BPA_purif*massflowrate*0.0003725061;
        #Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump))*IMS_value/CMS_value  #Seidar book
        Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump) - 0.110056*(np.log(Pc_pump))**2 + 0.071413*(np.log(Pc_pump))**3 - 0.0063788*(np.log(Pc_pump))**4) 
        
        Ethanol_needed = BPA_process_yield*Oil_250C_yield/(100*1.288) #calculated by measuring solubility https://pubs.acs.org/doi/pdf/10.1021/acs.jced.0c00166
        Heat_for_crystallization = Ethanol_needed*4.18*(40-25)*massflowrate/1000
        
        Heat_needed = Heat_for_crystallization + Heat_needed_for_distillation_column; #MJ/h
        
        Overall_HTC = 200*0.176; #BTu/hr-ft2 - degF
        Heat_transfer_area_crystallizer = 4*3.28; #ft2/ft lenght
        Lenght_crystallizer = (Ethanol_needed*4.18*massflowrate*0.94)/(100*Heat_transfer_area_crystallizer*(5/9)*Overall_HTC)
        #Lenght_crystallizer = ((5/9)*Overall_HTC*100)/(BPA_process_yield*Oil_250C_yield*4.18*massflowrate*0.94*Heat_transfer_area_crystallizer)
        Cp_crystallizer = 16440*Lenght_crystallizer**0.67;
            
        Total_electricity = (Pump_energy_needed_for_BPA_purif)/massflowrate #MJ/kg
                
        Total_BPA_purification_cost = (Cp_distillation_column + Cp_chromatograph + Cp_pump + Cp_crystallizer)*IMS_value/CMS_value

        self.Total_BPA_purification_cost = Total_BPA_purification_cost
        self.BPA_purification_distillation_column = Cp_distillation_column*IMS_value/CMS_value
        self.BPA_purification_chromotograph = Cp_chromatograph*IMS_value/CMS_value
        self.BPA_purification_pump = Cp_pump*IMS_value/CMS_value
        self.BPA_purification_crystallizer = Cp_crystallizer*IMS_value/CMS_value
        
        Ethanol_recycle_ratio = 10
        Ethanol_consumed = Ethanol_needed/Ethanol_recycle_ratio
                
        return BPA_process_yield*Oil_250C_yield, Heat_needed, Total_electricity, Ethanol_consumed

    def shredding_process_model(self): #feedstock flow rate (kg/hr), endsize (cm)
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        Yield = self.oil_yield;
        endsize = self.desired_end_size;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #shredding process model:
        print ("Shredding Process Model: \n")
        if endsize>5:
            costpertonne = 12; #$/ton
            processrate = 12; #ton/hr
            energyneeded = 0.2756; #MJ/kg
            shredder_needed = round(massflowrate/(processrate*1000))
        elif endsize>1.25:
            costpertonne = 31; #$/ton
            processrate = 7; #ton/hr
            energyneeded = 1.7641; #MJ/kg
            shredder_needed = round(massflowrate/(processrate*1000))
        else:
            costpertonne = 49; #$/ton
            processrate = 3; #ton/hr
            energyneeded = 4.9614; #MJ/kg
            shredder_needed = round(massflowrate/(processrate*1000))
            
        if shredder_needed ==0:
            shredder_needed = 1
            
        costofprocessing = shredder_needed*costpertonne*massflowrate/1000;
        energyofprocessing = massflowrate*energyneeded;

        print ("Cost of shredding " + str(round(costofprocessing,2)) + " $/hr ")
        print ("The shredding equipement can process " + str(round(processrate*1000,2)) + " kg/hr while the selected mass flow rate is " + str(round(massflowrate,2)) + " kg/hr, "),
        if massflowrate<(processrate*1000):
            print ("i.e., Mass flow rate acceptable\n")
        else:
            print ("i.e. Mass flow rate not acceptable\n")
        print ("Energy for shredding is " + str(round(energyofprocessing,2)) + " MJ/hr \n")
        print ("************************************************************************\n")
        
        self.shredder_needed = shredder_needed
        
        return energyofprocessing

    def centrifugation_process_model(self):  #oil yield (%), feedstock flow rate (kg/hr)
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        yield_oil = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #centrifugation model:
        print ("Centrifugation Process Model: \n")
        densityof_Lightoil = 870; #kg/m3
        densityof_Heavyoil = 920; #kg/m3
        densityof_water = 1000; #kg/m3
        feedstock_loading = 5;

        fractionoffeedstock = 1/(1+100/feedstock_loading)
        density_absolute = ((50*densityof_Lightoil+50*densityof_Heavyoil)*massflowrate*yield_oil/100+massflowrate*densityof_water/fractionoffeedstock)/(massflowrate+massflowrate/fractionoffeedstock);
        volumeflowrate = massflowrate*yield_oil/(density_absolute*100);
        #10 centrifuges used;
        Centrifuges_used = 1
        Volume_of_1_centrifuge = volumeflowrate/Centrifuges_used
        Energyforcentrifugation_perunitvolume = (21.22151 + 4.068515*math.exp(0.01441221*Volume_of_1_centrifuge))*3.6; #https://onlinelibrary.wiley.com/doi/10.1002/ceat.201800292#:~:text=Currently%2C%20centrifugal%20separators%20operate%20approximately,3%20for%20some%20cases%20with
        print ("Volumetric flow rate of oil + water is " + str(round(volumeflowrate,2)) + " m3/hr ")

        self.Centrifuges_used = Centrifuges_used;

        Energyneededforcentrifugation = Centrifuges_used*Energyforcentrifugation_perunitvolume*1000/(density_absolute*fractionoffeedstock);
        print ("Energy for centrifugation is " + str(round(Energyneededforcentrifugation,2)) + " MJ/hr or " + str(round(Energyneededforcentrifugation/(volumeflowrate*density_absolute),5)) + " MJ/kg \n")
        print ("************************************************************************\n")
    
        return Energyneededforcentrifugation
    
    def Landfilling_process_model(self):
        print ("Landfilling Process Model: \n")
        
        #cite https://www.epa.gov/sites/production/files/2016-03/documents/warm_v14_containers_packaging_non-durable_goods_materials.pdf
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        yield_oil = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #base emmision information
        plastic_emmision_basis = 0.02 * 1.102; #kg CO2/kg feedstock
        paper_emmision_basis = 0.07 * 1.102; #kg CO2/kg feedstock
        food_waste_emmision_basis = 0.50 * 1.102; #kg CO2/kg feedstock
        yard_trimming_emmision_basis = -0.20 * 1.102; #kg CO2/kg feedstock
        wood_emmision_basis = -0.20 * 1.102; #kg CO2/kg feedstock
        
        cellulose_emmision = (0.13*0.8*yard_trimming_emmision_basis+0.07*0.7*wood_emmision_basis+0.15*0.30*food_waste_emmision_basis+0.26*1*paper_emmision_basis)/0.458;
        starch_emmision = (0.13*0.07*yard_trimming_emmision_basis+0.15*0.30*food_waste_emmision_basis)/0.0541;
        lignin_emmision = (0.30*0.07*wood_emmision_basis+0.13*0.13*yard_trimming_emmision_basis)/0.0379;
        protein_emmision = food_waste_emmision_basis
        lipid_emmision = food_waste_emmision_basis
        
        biomass_emmision = (cellulose_emmision*carbohydrate+protein_emmision*protein+lipid_emmision*lipid+starch_emmision*starch+lignin_emmision*lignin)/100
        plastic_emmision = (PP+PET+PS+PC+PET)*plastic_emmision_basis/100;        
        
        Total_emmisions = biomass_emmision + plastic_emmision
        
        print ("Emission from plastic is: "+str(round(plastic_emmision,2))+" % kg_CO2/kg_feedstock.")
        print ("Emission from biomass is: "+str(round(biomass_emmision,2))+" % kg_CO2/kg_feedstock.")
        print ("Net Emission is: "+str(round(Total_emmisions,2))+" % kg_CO2/kg_feedstock.")
        
        return Total_emmisions, biomass_emmision, plastic_emmision
        
    def Combustion_process_model(self):
        print ("Combustion Process Model: \n")

        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        yield_oil = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #base emmision information
        HDPE_emmision_basis = 1.23 * 1.102; #kg CO2/kg plastic
        LDPE_emmision_basis = 1.24 * 1.102; #kg CO2/kg plastic
        PET_emmision_basis = 1.21 * 1.102; #kg CO2/kg plastic
        LLDPE_emmision_basis = 1.23 * 1.102; #kg CO2/kg plastic
        PS_emmision_basis = 1.77 * 1.102; #kg CO2/kg plastic
        PP_emmision_basis =  1.42 * 1.102; #kg CO2/kg plastic
        PC_emmision_basis = 1.36 * 1.102; #kg CO2/kg plastic
        
        paper_emmision_basis = -0.44 * 1.102; #kg CO2/kg feedstock
        food_waste_emmision_basis = -0.12 * 1.102; #kg CO2/kg feedstock
        yard_trimming_emmision_basis = -0.17 * 1.102; #kg CO2/kg feedstock
        wood_emmision_basis = -0.17 * 1.102; #kg CO2/kg feedstock
        
        cellulose_emmision = (0.13*0.8*yard_trimming_emmision_basis+0.07*0.7*wood_emmision_basis+0.15*0.30*food_waste_emmision_basis+0.26*1*paper_emmision_basis)/0.458;
        starch_emmision = (0.13*0.07*yard_trimming_emmision_basis+0.15*0.30*food_waste_emmision_basis)/0.0541;
        lignin_emmision = (0.30*0.07*wood_emmision_basis+0.13*0.13*yard_trimming_emmision_basis)/0.0379;
        protein_emmision = food_waste_emmision_basis
        lipid_emmision = food_waste_emmision_basis
        
        biomass_emmision = (cellulose_emmision*carbohydrate+protein_emmision*protein+lipid_emmision*lipid+starch_emmision*starch+lignin_emmision*lignin)/100
        plastic_emmision = (PP*PP_emmision_basis+PET*PET_emmision_basis+PS*PS_emmision_basis+PC*PC_emmision_basis)/100;        
        
        Total_emmisions = biomass_emmision + plastic_emmision;
        
        print ("Emission from plastic is: "+str(round(plastic_emmision,2))+" % kg_CO2/kg_feedstock.")
        print ("Emission from biomass is: "+str(round(biomass_emmision,2))+" % kg_CO2/kg_feedstock.")
        print ("Net Emission is: "+str(round(Total_emmisions,2))+" % kg_CO2/kg_feedstock.")
        
        return Total_emmisions, biomass_emmision, plastic_emmision
        
    def Recycling_process_model(self):
        print ("Recycling Process Model: \n")
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        yield_oil = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #base emmision information
        PP_emmision_basis = -0.79 * 1.102; #kg CO2/kg plastic
        PET_emmision_basis = -1.04 * 1.102; #kg CO2/kg plastic
        
        paper_emmision_basis = -3.55 * 1.102; #kg CO2/kg paper    
        cellulose_emmision = (0.26*1*paper_emmision_basis)/0.458;
        
        biomass_emmision = (cellulose_emmision*carbohydrate)/100
        plastic_emmision = (PP*PP_emmision_basis+PET*PET_emmision_basis)/100;        
        
        Total_emmisions = biomass_emmision + plastic_emmision;
        
        print ("Emission from plastic is: "+str(round(plastic_emmision,2))+" % kg_CO2/kg_feedstock.")
        print ("Emission from biomass is: "+str(round(biomass_emmision,2))+" % kg_CO2/kg_feedstock.")    
        print ("Net Emission is: "+str(round(Total_emmisions,2))+" % kg_CO2/kg_feedstock.")
        
        return Total_emmisions, biomass_emmision, plastic_emmision
 
    def Composting_process_model(self):
        print ("Composting Process Model: \n")
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        yield_oil = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #base emmision information
        food_waste_emmision_basis = -0.12 * 1.102; #kg CO2/kg plastic
        yard_trimming_emmision_basis = -0.05 * 1.102; #kg CO2/kg paper
        
        cellulose_emmision = (0.13*0.8*yard_trimming_emmision_basis+0.15*0.30*food_waste_emmision_basis)/0.458;
        starch_emmision = (0.13*0.07*yard_trimming_emmision_basis+0.15*0.30*food_waste_emmision_basis)/0.0541;
        lignin_emmision = (0.13*0.13*yard_trimming_emmision_basis)/0.0379;
        protein_emmision = food_waste_emmision_basis
        lipid_emmision = food_waste_emmision_basis
        
        biomass_emmision = (cellulose_emmision*carbohydrate+protein_emmision*protein+lipid_emmision*lipid+starch_emmision*starch+lignin_emmision*lignin)/100
        
        Total_emmisions = biomass_emmision;
        
        print ("Net Emission/ Emission from biomass is: "+str(round(Total_emmisions,2))+" % kg_CO2/kg_feedstock.")
        
        return Total_emmisions
       
    def Virgin_plastic_process_model(self):
        print ("Recycling Process Model: \n")
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        yield_oil = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        
        #base emmision information
        HDPE_emmision_basis = 1.47 * 1.102; #kg CO2/kg plastic
        LDPE_emmision_basis = 1.80 * 1.102; #kg CO2/kg plastic
        PET_emmision_basis = 2.20 * 1.102; #kg CO2/kg plastic
        LLDPE_emmision_basis = 1.58 * 1.102; #kg CO2/kg plastic
        PS_emmision_basis = 2.50 * 1.102; #kg CO2/kg plastic
        PP_emmision_basis =  1.55 * 1.102; #kg CO2/kg plastic
        PVC_emmision_basis = 1.95 * 1.102; #kg CO2/kg plastic
                
        plastic_emmision = (PP*HDPE_emmision_basis+PET*PET_emmision_basis+PS*HDPE_emmision_basis)/100;        
        
        print ("Net Emission is: "+str(round(plastic_emmision,2))+" % kg_CO2/kg_feedstock.")
        
        return plastic_emmision

    def HTL_capital_cost(self):
        #HTL upgrading (adapted from 4 PNNL studies)
        print ("Calculating capitol cost for HTL:\n")
        print ("The basic equipments are: ")
        
        #initializing class variables
        carbohydrate = self.cellulose;
        protein = self.protein;
        lipid = self.lipid;
        lignin = self.lignin;
        starch = self.starch;
        massflowrate = self.massflowrate;
        costofheating = self.costofheating;
        energyconsumedperkg_HTL = self.energyconsumedperkg_HTL
        Yield = self.oil_yield;
        PP = self.PP; #(%)
        PS = self.PS; #(%)
        PC = self.PC; #(%)
        PET = self.PET; #(%)
        endsize = self.desired_end_size;
        temperature = self.temperature;
        heatingcapacityoffeed = self.heatingcapacityoffeed
        Total_BPA_purification_cost = self.Total_BPA_purification_cost
        
        #reaction information
        feedstock_loading=self.feedstock_loading;
        Reactorheatingeffeciency = 0.8 #assumption (fraction)
        timeofprocessing = 30; #mins
        IMS_value = 702.3; #2019

        #All information obtained from the Seider text book unless said otherwise
        
        CMS_value = 567;
        
        #shredder
        W_shredder = massflowrate/(1000*self.shredder_needed) #ton/hr
        if W_shredder<4.65:
            Cp_shredder = 2041*W_shredder**1.05*IMS_value/CMS_value
            print ("Shredder type:\t\t\t Cone crusher")
        elif W_shredder<187.65:
            Cp_shredder = 2610*W_shredder**0.89*IMS_value/CMS_value
            print ("Shredder type:\t\t\t Jaw crusher")
        else:
            Cp_shredder = 11910*W_shredder**0.60*IMS_value/CMS_value
            print ("Shredder type:\t\t\t Gyratory crusher")
        
        #sifter
        area_sifter = massflowrate/200 #ft2
        if area_sifter < 40:
            Cp_sifter = 6575*area_sifter**0.34*IMS_value/CMS_value
            print ("Sifter type:\t\t\t Vibrating grizzlies")
        elif area_sifter < 60:
            Cp_sifter = 1588*area_sifter**0.71*IMS_value/CMS_value
            print ("Sifter type:\t\t\t Vibrating screens 1 deck")
        else:
            Cp_sifter = 1010*area_sifter**0.91*IMS_value/CMS_value
            print ("Sifter type:\t\t\t Vibrating screens 3 deck")

        #piston feed tank
        volume_feed_tank = massflowrate*(100+feedstock_loading)*35.3147/(feedstock_loading*1000) #ft3
        if volume_feed_tank < 94.63:
            Cp_feed_tank = 1700*volume_feed_tank**0.60*IMS_value/CMS_value
            print ("Feed tank type:\t\t\t Tumblers - twin shell")
        else:
            Cp_feed_tank = 3856*volume_feed_tank**0.42*IMS_value/CMS_value
            print ("Feed tank type:\t\t\t Tumblers - double cone")           
        
        #conveyer belt
        conveyer_width = 30; #in
        conveyer_lenght = 100; #ft
        Cp_conveyer = 24.4*conveyer_lenght*conveyer_width*IMS_value/CMS_value;
        
        #filters
        print ("Solid filter type:\t\t Rotary drum filter")
        area_filter = massflowrate/113.25; #ft2
        Cp_filter = 28010*area_filter**0.48*IMS_value/CMS_value;
        
        #waste water treatment
        print ("Waste water treatment plant: \t Primary")
        volume_water_to_treatment  = massflowrate*264.172/(feedstock_loading*1000*60)
        Cp_water_treatment = 16785*volume_water_to_treatment**0.64*IMS_value/CMS_value;
        
        #heat exchanger
        #Area_Heat_exchanger = 513.818*(massflowrate/23000)*(5/feedstock_loading) #ft2
        Area_Heat_exchanger = 24198.3*(massflowrate/23000)*(5/feedstock_loading) #ft2
        print ("Heat exchanger: \t\t Shell and tube: Floating head")
        Cp_Heat_exchanger = 4*np.exp(12.0310-0.8709*np.log(Area_Heat_exchanger)+0.09*np.log(Area_Heat_exchanger)**2)*IMS_value/CMS_value #Spiral plate 4 heat exchangers in total

        #pump
        print ("Pump: \t\t\t\t Centrifugal")
        Pump_energy_needed_forHTL = self.Pump_energy_needed_forHTL
        Pc_pump = Pump_energy_needed_forHTL*massflowrate/2684; #hp
        Cp_pump = np.exp(5.9332 + 0.16829*np.log(Pc_pump) - 0.110056*(np.log(Pc_pump))**2 + 0.071413*(np.log(Pc_pump))**3 - 0.0063788*(np.log(Pc_pump))**4) 
        #Cp_pump = 4*np.exp(5.9332 + 0.16829*np.log(Pc_pump))*IMS_value/CMS_value  #Seidar book
       
        #centrifuge
        print ("Centrifuge: \t\t\t Horizontal auto-batch system \n\t\t\t\t (2 min cycle)")
        Cp_centrifuge = 2*self.Centrifuges_used*2440*40**1.11*IMS_value/CMS_value;
        
        #heater
        print ("Fired heater: \t\t\t Silicon oil design")

        #heat_preheater = massflowrate*(100+feedstock_loading)/feedstock_loading*heatingcapacityoffeed*(temperature-250)*0.977;
        
        print ("energyconsumedperkg_HTL is ", round(energyconsumedperkg_HTL,2))
        
        heat_preheater = massflowrate*(energyconsumedperkg_HTL/2)*947.817 #Btu/hr
        Cp_heat_preheater = 2*13.97* (heat_preheater)** 0.64 *IMS_value/CMS_value
        #Cp_heat_preheater = np.exp(9.7188 - 0.3769*(np.log(heat_preheater))+0.03434*(np.log(heat_preheater))**2)
               
        #reactor
        print ("Reactor Material: \t\t Stainless Steel")
        print ("Reactor Pressure: \t\t 25 MPa")
        print ("Reactor Diameter: \t\t 10 ft")

        Fm_reactor = 2.25 #SS solid
        Fp_reactor = 2.50 #10 MPa 
        Fc_reactor = Fm_reactor * Fp_reactor
        
        D_reactor = 10 #ft
        V_reactor = (100+feedstock_loading)*massflowrate/(feedstock_loading*1000)
        H_reactor = timeofprocessing*V_reactor*35.3147/(3.14*D_reactor**2*60)
        
        Cp_reactor = 2*101.9*(2.18+Fc_reactor)*IMS_value*(D_reactor**1.066)*(H_reactor**0.802)/CMS_value
        
        heating_oil_needed = massflowrate*100/feedstock_loading
        Oil_tank_allowance = 2
        Oil_density = 0.264172/0.95; #gal/kg
        Cp_oil_tank = 2*265*(heating_oil_needed*Oil_tank_allowance*Oil_density)**0.513*IMS_value/(CMS_value)
        Cp_cooling_tower = 2*50000*((100*3.79*60*feedstock_loading)/massflowrate)**0.778 #https://www.coolingtowerproducts.com/cooling-tower-cost/#:~:text=On%20average%2C%20cooling%20towers%20cost,manufacturers%20of%20commercial%20cooling%20towers.
        
        Purchase_cost = self.shredder_needed*Cp_shredder + Cp_sifter + Cp_feed_tank + Cp_conveyer + Cp_filter + Cp_water_treatment + Cp_Heat_exchanger + Cp_centrifuge  + Cp_heat_preheater + Cp_pump * 2 + Cp_reactor+Cp_oil_tank+Cp_cooling_tower + solid_handling_choice*self.solid_handling_cost + BPA_purification_choice*Total_BPA_purification_cost;
        
        print ("\nCp Shredder:\t\t\t\t\t\t $", round(self.shredder_needed*Cp_shredder/10**6,2), "millions or ", "{:e}".format(Cp_shredder))
        print ("Cp Sifter:\t\t\t\t\t\t\t $", round(Cp_sifter/10**6,2), "millions or ", "{:e}".format(Cp_sifter))
        print ("Cp Feed Tank:\t\t\t\t\t\t $", round(Cp_feed_tank/10**6,2), "millions or ", "{:e}".format(Cp_feed_tank))
        print ("Cp Conveyer:\t\t\t\t\t\t $", round(Cp_conveyer/10**6,2), "millions or ", "{:e}".format(Cp_conveyer))
        print ("Cp Filter:\t\t\t\t\t\t\t $", round(Cp_filter/10**6,2), "millions or ", "{:e}".format(Cp_filter))
        print ("Cp Water Treatment:\t\t\t\t\t $", round(Cp_water_treatment/10**6,2), "millions or ", "{:e}".format(Cp_water_treatment))
        print ("Cp Heat Exchanger:\t\t\t\t\t $", round(Cp_Heat_exchanger/10**6,2), "millions or ", "{:e}".format(Cp_Heat_exchanger))
        print ("Cp Centrifuge:\t\t\t\t\t\t $", round(Cp_centrifuge/10**6,2), "millions or ", "{:e}".format(Cp_centrifuge))
        print ("Cp Preheater:\t\t\t\t\t\t $", round(Cp_heat_preheater/10**6,2), "millions or ", "{:e}".format(Cp_heat_preheater))
        print ("Cp Pump:\t\t\t\t\t\t\t $", round(Cp_pump*2/10**6,2), "millions or ", "{:e}".format(Cp_pump*2))
        print ("Cp reactor:\t\t\t\t\t\t\t $", round(Cp_reactor/10**6,2), "millions or ", "{:e}".format(Cp_reactor))
        print ("Cp Oil tank:\t\t\t\t\t\t $", round(Cp_oil_tank/10**6,2), "millions or ", "{:e}".format(Cp_oil_tank))
        print ("Cp Cooling tower:\t\t\t\t\t $", round(Cp_cooling_tower/10**6,2), "millions or ", "{:e}".format(Cp_cooling_tower))
        print ("Cp BPA purification system:\t\t\t $", round(BPA_purification_choice*Total_BPA_purification_cost/10**6,2), "millions or ", "{:e}".format(BPA_purification_choice*Total_BPA_purification_cost))
        print ("Cp BPA pur. distillation column:\t $", round(BPA_purification_choice*self.BPA_purification_distillation_column/10**6,2), "millions or ", "{:e}".format(BPA_purification_choice*self.BPA_purification_distillation_column))
        print ("Cp BPA pur. flash chromotograph:\t $", round(BPA_purification_choice*self.BPA_purification_chromotograph/10**6,2), "millions or ", "{:e}".format(BPA_purification_choice*self.BPA_purification_chromotograph))
        print ("Cp BPA pur. pumping system:\t\t\t $", round(BPA_purification_choice*self.BPA_purification_pump/10**6,2), "millions or ", "{:e}".format(BPA_purification_choice*self.BPA_purification_pump))
        print ("Cp BPA pur. crystallizer:\t\t $", round(BPA_purification_choice*self.BPA_purification_crystallizer/10**6,2), "millions or ", "{:e}".format(BPA_purification_choice*self.BPA_purification_crystallizer))
        print ("Cp Solid handling:\t\t\t\t\t $", round(solid_handling_choice*self.solid_handling_cost/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.solid_handling_cost))
        print ("Cp Solid handling heat exchanger:\t $", round(solid_handling_choice*self.SHCp_Heat_exchanger/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_Heat_exchanger))
        print ("Cp Solid handling filter:\t\t\t $", round(solid_handling_choice*self.SHCp_filter/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_filter))
        print ("Cp Solid handling oil tank:\t\t\t $", round(solid_handling_choice*self.SHCp_oil_tank/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_oil_tank))
        print ("Cp Solid handling sifter:\t\t\t $", round(solid_handling_choice*self.SHCp_sifter/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_sifter))
        print ("Cp Solid handling reactor:\t\t\t $", round(solid_handling_choice*self.SHCp_reactor/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_reactor))
        print ("Cp Solid handling pump:\t\t\t\t $", round(solid_handling_choice*self.SHCp_pump/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_pump))         
        print ("Cp Solid handling pelletizer:\t\t $", round(solid_handling_choice*self.SHCp_pelletizer/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_pelletizer))
        print ("Cp Solid handling crystallizer:\t\t $", round(solid_handling_choice*self.SHCp_crystallizer*IMS_value/CMS_value/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_crystallizer*IMS_value/CMS_value))
        print ("Cp Solid handling feed tank:\t\t $", round(solid_handling_choice*self.SHCp_feed_tank/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_feed_tank))
        print ("Cp Solid handling open tank:\t\t $", round(solid_handling_choice*self.SHCp_open_tank/10**6,2), "millions or ", "{:e}".format(solid_handling_choice*self.SHCp_open_tank))
       
        print ("\nTotal purchase cost for 2019 is: $", round(Purchase_cost/10**6,2), "millions or ", "{:e}".format(Purchase_cost))
                
        cbm_heater = 1.86;
        cbm_heat_exchanger = 1.80
        cbm_pressure_vessel = 3.05
        cbm_pumps = 3.30
        cbm_centrifuge = 2.03
        cbm_conveyor = 1.61
        cbm_crusher = 1.39
        cbm_filter = 2.32
        cbm_screens = 1.73
        
        Bare_module_cost = cbm_crusher*self.shredder_needed*Cp_shredder + cbm_screens*Cp_sifter + cbm_pressure_vessel*Cp_feed_tank + cbm_conveyor*Cp_conveyer + cbm_filter*Cp_filter + Cp_water_treatment + cbm_heat_exchanger*Cp_Heat_exchanger + cbm_centrifuge*Cp_centrifuge  + cbm_heater*Cp_heat_preheater + cbm_pumps*Cp_pump * 2 + cbm_pressure_vessel*Cp_reactor + cbm_pressure_vessel*Cp_oil_tank + cbm_heat_exchanger*Cp_cooling_tower + solid_handling_choice*cbm_heater*self.solid_handling_cost + BPA_purification_choice*cbm_heater*Total_BPA_purification_cost;
        print ("\nTotal net cost is: $", round(Bare_module_cost/10**6,2), "millions or ", "{:e}".format(Bare_module_cost))

        F1_Order_of_Magnitude_method = 0.80 #indoor construction
        F2_Order_of_Magnitude_method = 0.80 #grass roots plant
        C_DPI_Order_of_Magnitude_method = (1+F1_Order_of_Magnitude_method+F2_Order_of_Magnitude_method)*Bare_module_cost
        TCI_Order_of_Magnitude_method = 1.15*1.50*C_DPI_Order_of_Magnitude_method
        print ("\nThe total capitol investment by order of magnitude method for HTL is: $", round(TCI_Order_of_Magnitude_method/10**6,2), "millions or ", "{:e}".format(TCI_Order_of_Magnitude_method))
        
        Lang_factor = 5.93;
        TCI_lang_method = 1.05*Lang_factor*Bare_module_cost
        
        print ("\nThe total capitol investment by lang method for HTL is: $", round(TCI_lang_method/10**6,2), "millions or ", "{:e}".format(TCI_lang_method))
        
        #Guthrie method
        C_site_factor = 0.05;
        C_building_factor = 0.05;
        C_offsite_building_factor = 0.05;
        C_offsite_building_constant = 1500000;
        C_grass_root_factor = 0.25;
        Working_capitol = 3.7*10**6

        TCI_Guthrie_method = Bare_module_cost*(1+C_site_factor+C_building_factor+C_offsite_building_factor+C_grass_root_factor)+C_offsite_building_constant+Working_capitol; 
        
        print ("\nThe total capitol investment by guthrie method for HTL is: $", round(TCI_Guthrie_method/10**6,2), "millions or ", "{:e}".format(TCI_Guthrie_method))

        print ("\n************************************************************************\n")
                
        return Purchase_cost,Bare_module_cost, TCI_Order_of_Magnitude_method, TCI_lang_method,TCI_Guthrie_method

    def Upgrading_capital_cost(self):
        scaling_factor = 0.8
        massflowrate = 9*self.massflowrate; #9 - HTL plants pool together
        HTL_oilyield = self.oil_yield;
        #2016 PNNL article (scaled with lang factor)
        base_capitol_cost = 16.237*10**6
        base_flow_rate = 15313.13; #kg HTL oil/hr
        oilflowrate = massflowrate*HTL_oilyield/100
        IMS_value = 702.3; #https://www.toweringskills.com/financial-analysis/cost-indices/
        CMS_value = 541.7; #https://www.toweringskills.com/financial-analysis/cost-indices/
        
        print("the oil flow rate is", oilflowrate, " kg/hr")
        
        Upgrading_instrument_cost = base_capitol_cost*(oilflowrate/base_flow_rate)**scaling_factor*IMS_value/CMS_value
        #Upgrading_instrument_cost = 32.28*10**5 #2016 PNNL w/o hydrogen plant
        
        print("Capitol cost for upgrading: \n")
        
        print ("\nThe purchase cost for upgrading is: $", round(Upgrading_instrument_cost/(9*10**6),2), "millions or ", "{:e}".format(Upgrading_instrument_cost/9))
        
        F1_Order_of_Magnitude_method = 0.80 #indoor construction
        F2_Order_of_Magnitude_method = 0.80 #grass roots plant
        C_DPI_Order_of_Magnitude_method = (1+F1_Order_of_Magnitude_method+F2_Order_of_Magnitude_method)*Upgrading_instrument_cost
        TCI_Order_of_Magnitude_method = 1.15*1.50*C_DPI_Order_of_Magnitude_method
        
        print ("\nThe total capitol investment by order of magnitude method for upgrading is: $", round(TCI_Order_of_Magnitude_method/(9*10**6),2), "millions or ", "{:e}".format(TCI_Order_of_Magnitude_method/9))
        
        Lang_factor = 5.93;
        TCI_lang_method = 1.05*Lang_factor*Upgrading_instrument_cost
        
        print ("\nThe total capitol investment by lang method for upgrading is: $", round(TCI_lang_method/(9*10**6),2), "millions or ", "{:e}".format(TCI_lang_method/9))
        
        #Guthrie method
        C_site_factor = 0.05;
        C_building_factor = 0.05;
        C_offsite_building_factor = 0.05;
        C_offsite_building_constant = 1500000;
        C_grass_root_factor = 0.25;
        Working_capitol = 3.7*10**6

        TCI_Guthrie_method = Upgrading_instrument_cost*(1+C_site_factor+C_building_factor+C_offsite_building_factor+C_grass_root_factor)+C_offsite_building_constant+Working_capitol; 
        
        print ("\nThe total capitol investment by guthrie method for upgrading is: $", round(TCI_Guthrie_method/(9*10**6),2), "millions or ", "{:e}".format(TCI_Guthrie_method/9))

        print ("\n************************************************************************\n")
                
        return TCI_Order_of_Magnitude_method,TCI_lang_method, TCI_Guthrie_method
        
max_iter = 1;

#data
Kg_CO2_per_kg_TPA = 3.1; #cite https://pubs.acs.org/doi/pdfplus/10.1021/acssuschemeng.7b00105?src=recsys#:~:text=Generally%2C%20the%20cradle%2Dto%2D,kg%20of%20purified%20terephthalic%20acid.
Kg_CO2_per_kg_BPA = 2.4; 
Kg_CO2_per_kg_gasoline = 3.30 + 0.70 + 0.21; #data from greet model for US refinaries - refining and production 
Kg_CO2_per_kg_diesel = 3.15 + 0.53 + 0.21;

#initiating variables

HeatfromHTL = [0]*max_iter;
TPA_yield = [0]*max_iter;
BPA_yield = [0]*max_iter;
Carbon_in_plastic_feedstock = [0]*max_iter;
fresh_water_needed = [0]*max_iter;
kg_natural_gas_for_office = [0]*max_iter;
Pump_energy_needed_forHTL =[0]*max_iter;
Gasoline_consumption_to_HTL = [0]*max_iter;
Hydrogenforupgrading = [0]*max_iter;
Heatforupgrading = [0]*max_iter;
Pump_energy_needed_forUpgrading = [0]*max_iter;
Gasolineproduced = [0]*max_iter;
kg_natural_gas_for_office_upgrading = [0]*max_iter;
Emmision_from_H2 = [0]*max_iter;
Gasoline_consumption_HTL_oil_to_upgrading = [0]*max_iter;
Gasoline_consumption_HTL_upgraded_oil_to_consumer = [0]*max_iter;
office_space = [0]*max_iter;
Totalheatneeded = [0]*max_iter;
Electricityneeded_HTL = [0]*max_iter;
Electricityneeded_upgrading = [0]*max_iter;
Electricityneeded = [0]*max_iter;
totallca = [0]*max_iter;
HTLlca = [0]*max_iter;
Upgradinglca = [0]*max_iter;
Officespacelca = [0]*max_iter;
Transport_emmision_fromHTL = [0]*max_iter;
HTL_emmisions = [0]*max_iter;
Upgrading_emmisions = [0]*max_iter;
Substitution_lca = [0]*max_iter;
Total_emmisions = [0]*max_iter;
Kg_CO2_in_feedstock = [0]*max_iter;
CO2_substitution_from_gasoline = [0]*max_iter;
CO2_substitution_from_TPA = [0]*max_iter;
CO2_substitution_from_BPA = [0]*max_iter;
HTL_emmision_per_kg = [0]*max_iter;
Transport_emmision_fromUpgrading = [0]*max_iter;
HTL_capital_cost_purchase = [0]*max_iter;
HTL_capital_cost_net = [0]*max_iter;
Hydrogen_consumption_per_kg_feedstock = [0]*max_iter;
HTL_capital_lang_method = [0]*max_iter;
Upgrading_capital_lang_method = [0]*max_iter;
HTL_capital_order_of_magnitude = [0]*max_iter;
Upgrading_capital_order_of_magnitude = [0]*max_iter;
Upgrading_lang_method = [0]*max_iter;
Total_cost_order_of_magnitude = [0]*max_iter;
Total_cost_lang_method = [0]*max_iter;
Biochar_yield = [0]*max_iter;
Gas_yield = [0]*max_iter;
Gas_yield_fromplastic = [0]*max_iter;

first_object = []    

for i in range(max_iter):
    #feedstock composition MSW basis 

    cellulose = 51; #(%)
    protein = 6; #(%)
    lipid = 4; #(%)
    lignin = 10; #(%)
    starch = 9; #(%)
    PP = 50.17*0.20; #(%)
    PC = 3.36*0.20; #(%)
    PS = 13.91*0.20; #(%)
    PET = 32.56*0.20; #(%)
    massflowrate = 25209; #(kg/hr) 500 tons/day 9 plants needed to process 10 % of total MSW produced 18,351,295 people producing 816 kg per day
    costofheating = 0.00001; #($/KJ)
    desired_end_size = 10; #(cm)
    temperature = 300;
    null = 0;
    print("running iter number ",i+1, "\n")
    
    '''#feedstock composition Plastic mixture basis
    cellulose = 0; #(%)
    protein = 0; #(%)
    lipid = 0; #(%)
    lignin = 0; #(%)
    starch = 0; #(%)
    PP = 0; #(%)
    PC = 0; #(%)
    PS = 0; #(%)
    PET = 100; #(%)
    massflowrate = 25209; #(kg/hr) 500 tons/day
    costofheating = 0.00001; #($/KJ)
    desired_end_size = 10; #(cm)
    temperature = 300;
    null = 0;'''
    
    #mock object created and functions called
    tempObj = None
    tempObj = class_process_model(cellulose, protein, lipid, lignin, starch, PP, PS, PC, PET, massflowrate, costofheating, desired_end_size, temperature, null)
    first_object.append(tempObj) #cellulose (%), protein (%), lipid (%), lignin (%), starch (%), massflowrate (kg/hr), costofheating ($/KJ)
    Electricityfromshredding = first_object[i].shredding_process_model()
    process_model = first_object[i].HTL_process_model() 
    Electricityfromcentrifuge = first_object[i].centrifugation_process_model()
    solid_handling = first_object[i].solid_handling()
    BPA_purification = first_object[i].BPA_purification()
    upgrading = first_object[i].HTL_upgrading()
    HTL_capital_cost = first_object[i].HTL_capital_cost()
    Upgrading_capital_cost = first_object[i].Upgrading_capital_cost()
    
    #storing required return values
    HeatfromHTL[i] = process_model[8]
    TPA_yield[i] = solid_handling_choice*solid_handling[1]
    BPA_yield[i] = BPA_purification_choice*BPA_purification[0]
    Heat_for_BPA_purification = BPA_purification_choice*BPA_purification[1]
    Electricity_for_BPA_purification = BPA_purification_choice*BPA_purification[2]
    Ethanol_needed = BPA_purification_choice*BPA_purification[3]
    Carbon_in_plastic_feedstock[i] = process_model[11]
    fresh_water_needed[i] = process_model[12] + solid_handling_choice*solid_handling[6]
    kg_natural_gas_for_office[i] = process_model[13]
    Pump_energy_needed_forHTL[i] = process_model[14]
    Gasoline_consumption_to_HTL[i] = process_model[15]
    Biochar_yield[i] = solid_handling_choice*solid_handling[2]
    Gas_yield[i] = process_model[17]
    Gas_yield_fromplastic[i] = process_model[18]
    Energy_consumed_for_unreacted_plastic_at_425 = process_model[19]
    Hexane_consumed = solid_handling_choice*solid_handling[3]
    Solid_handling_heat = solid_handling_choice*solid_handling[4]
    Solid_handling_electricity = solid_handling_choice*solid_handling[5]
    Solid_handling_Water_needed = solid_handling_choice*solid_handling[6]
    Solid_handling_DMSO_needed = solid_handling_choice*solid_handling[7]
    Solid_handling_NaOH_needed = solid_handling_choice*solid_handling[8]
    Solid_handling_H2SO4_needed = solid_handling_choice*solid_handling[9]
    
    Hydrogenforupgrading[i] = upgrading[7]
    Heatforupgrading[i] = upgrading[8]
    Pump_energy_needed_forUpgrading[i] = upgrading[9]
    Gasolineproduced[i] = upgrading[1]
    kg_natural_gas_for_office_upgrading[i] = upgrading[10]
    Emmision_from_H2[i] = upgrading[11]
    Gasoline_consumption_HTL_oil_to_upgrading[i] = upgrading[12]
    Gasoline_consumption_HTL_upgraded_oil_to_consumer[i] = upgrading[13]
    office_space[i] = upgrading[14]
    Hydrogen_consumption_per_kg_feedstock[i] = upgrading[15]
    Percentage_naptha = upgrading[16]
    Energy_from_oil = upgrading[17]
    
    HTL_capital_cost_purchase[i] = HTL_capital_cost[0]
    HTL_capital_cost_net[i] = HTL_capital_cost[1]
    HTL_capital_order_of_magnitude[i] = HTL_capital_cost[2]
    HTL_capital_lang_method[i] = HTL_capital_cost[3]
    HTL_capital_guthrie_method = HTL_capital_cost[4]
    Upgrading_capital_order_of_magnitude[i] = Upgrading_capital_cost[0]/9
    Upgrading_capital_lang_method[i] = Upgrading_capital_cost[1]/9
    Upgrading_capital_guthrie_method = Upgrading_capital_cost[2]/9
    
    Natural_gas_energy = 37000; #kJ/m3
    
    #calculating total heat needed
    Totalheatneeded[i] = Heatforupgrading[i] + HeatfromHTL[i]/1000+solid_handling_choice*Solid_handling_heat*massflowrate/1000 + BPA_purification_choice*Heat_for_BPA_purification; #MJ/hr
    
    #calculating total electricity needed
    Energy_HTL_Sifter = 19.8*2; #MJ/hr  https://www.gerickegroup.com/en/products/sifting/centrifugal-sifter/ 84000 kg/hr capacity
    Energy_feed_tank = 18*massflowrate/1000; #MJ/hr https://core.ac.uk/download/pdf/29030339.pdf
    Electricityneeded_HTL[i] = Electricityfromshredding + Electricityfromcentrifuge + Pump_energy_needed_forHTL[i]*massflowrate/1000+Energy_HTL_Sifter+Energy_feed_tank; #MJ/hr
    Electricityneeded_upgrading[i] = Pump_energy_needed_forUpgrading[i]*massflowrate/1000; #MJ/hr
    Electricityneeded[i] = Electricityneeded_upgrading[i] + Electricityneeded_HTL[i] + solid_handling_choice*Solid_handling_electricity*massflowrate + BPA_purification_choice*Electricity_for_BPA_purification*massflowrate; #MJ/hr
    
    CO2_emmision_for_burning_natural_gas = 1.876; #kg CO2/m3 natural gas
    HTL_Emmision_from_burning_natural_gas = (HeatfromHTL[i]+solid_handling_choice*Solid_handling_heat*massflowrate)/(massflowrate*Natural_gas_energy)*CO2_emmision_for_burning_natural_gas;
    Upgrading_Emmision_from_burning_natural_gas = (Heatforupgrading[i]*1000/(massflowrate*Natural_gas_energy))*CO2_emmision_for_burning_natural_gas;
    
    print ("\nEquipement: \t\t\t\t\t Energy in MJ/kg feedstock")
    print ("HTL heating \t\t\t\t\t", round((HeatfromHTL[i]-Energy_consumed_for_unreacted_plastic_at_425)/(massflowrate*1000),4))
    print ("Upgrading heating \t\t\t\t", round(Heatforupgrading[i]/(massflowrate),4))
    print ("Solid handling heating \t\t\t", round(solid_handling_choice*Solid_handling_heat/1000,4))
    print ("HTL unreacted plastic heating \t", round(Energy_consumed_for_unreacted_plastic_at_425/(massflowrate*1000),4))
    print ("HTL Electricity for shredding \t", round(Electricityfromshredding/(massflowrate),4))
    print ("HTL Electricity for centrifuge \t", round(Electricityfromcentrifuge/(massflowrate),4))
    print ("HTL electrictiy for pump \t\t", round(Pump_energy_needed_forHTL[i]/1000,4))
    print ("HTL electricity for sifter \t\t", round(Energy_HTL_Sifter/(massflowrate),4))
    print ("HTL electricity for feed tank \t", round(Energy_feed_tank/(massflowrate),4))
    print ("Upgrading electricity for pump \t", round(Pump_energy_needed_forUpgrading[i]/(massflowrate*1000),4))
    print ("Solid handling electricity \t\t", round(solid_handling_choice*Solid_handling_electricity,4), "\n")
    
    print ("Heat energy consumed ",round(Totalheatneeded[i],2), " MJ/hr or ",round(Totalheatneeded[i]/(massflowrate),4)," MJ/kg") 
    print ("Electricity consumed ",round(Electricityneeded[i],2), " MJ/hr or ",round(Electricityneeded[i]/(massflowrate),4)," MJ/kg\n")
    #the object can be looped to test sensitivity due to change of MSW composition and MSW availability (mass flow rate)
    
    Process_energy = (Totalheatneeded[i]/(massflowrate))
    EROI = Energy_from_oil/Process_energy
    print ("The EROI is ", round(EROI,2))
    
    #basis is one kg of feedstock
        
    HTLDemand_array = {Electricity : Electricityneeded_HTL[i]*0.28/massflowrate+solid_handling_choice*Solid_handling_electricity*0.28, Natural_gas : (HeatfromHTL[i]+solid_handling_choice*Solid_handling_heat*massflowrate)/(massflowrate*Natural_gas_energy), water_fresh : fresh_water_needed[i], water_treatment : fresh_water_needed[i], Hexane: Hexane_consumed, DMSO: solid_handling_choice*Solid_handling_DMSO_needed, NaOH: solid_handling_choice*Solid_handling_NaOH_needed, H2SO4: solid_handling_choice*Solid_handling_H2SO4_needed, Ethanol: Ethanol_needed}
    Method = ('TRACI (obsolete)', 'environmental impact', 'global warming')
    HTLlca[i] = bw.LCA(HTLDemand_array, Method)
    HTLlca[i].lci()
    HTLlca[i].lcia()

    UpgradingDemand_array = {Electricity : Electricityneeded_upgrading[i]*0.28/massflowrate, Natural_gas : Heatforupgrading[i]*1000/(massflowrate*Natural_gas_energy)}
    Method = ('TRACI (obsolete)', 'environmental impact', 'global warming')
    Upgradinglca[i] = bw.LCA(UpgradingDemand_array, Method)
    Upgradinglca[i].lci()
    Upgradinglca[i].lcia()
    
    method = QuickMethod (('TRACI (obsolete)', 'environmental impact', 'global warming'))
    LCA_score_unit = method.unit
    
    Transport_emmision_fromHTL[i] = Kg_CO2_per_kg_gasoline * Gasoline_consumption_to_HTL[i];
    Transport_emmision_fromUpgrading[i] = Kg_CO2_per_kg_gasoline * (Gasoline_consumption_HTL_oil_to_upgrading[i]+Gasoline_consumption_HTL_upgraded_oil_to_consumer[i]);
    
    HTL_emmisions[i] = HTLlca[i].score + Transport_emmision_fromHTL[i] + HTL_Emmision_from_burning_natural_gas;
    Upgrading_emmisions[i] = Upgradinglca[i].score + Transport_emmision_fromUpgrading[i] + Emmision_from_H2[i]+Upgrading_Emmision_from_burning_natural_gas;
    Total_emmisions[i] = HTL_emmisions[i] + Upgrading_emmisions[i];
    
    HTLlcaelectricity = bw.LCA({Electricity : Electricityneeded_HTL[i]*0.28/massflowrate}, Method)
    HTLlcaelectricity.lci()
    HTLlcaelectricity.lcia()
    
    HTL_heat_lca = bw.LCA({Natural_gas : (HeatfromHTL[i])/(massflowrate*Natural_gas_energy)}, Method)
    HTL_heat_lca.lci()
    HTL_heat_lca.lcia()
    
    Solidhandling_heat = bw.LCA({Natural_gas : (solid_handling_choice*Solid_handling_heat)/(Natural_gas_energy)}, Method)
    Solidhandling_heat.lci()
    Solidhandling_heat.lcia()
    
    Total_Water_needed = bw.LCA({water_fresh : fresh_water_needed[i]}, Method)
    Total_Water_needed.lci()
    Total_Water_needed.lcia()

    Total_Water_treatment = bw.LCA({water_treatment : fresh_water_needed[i]}, Method)
    Total_Water_treatment.lci()
    Total_Water_treatment.lcia()

    Total_hexane_needed = bw.LCA({Hexane: Hexane_consumed}, Method)
    Total_hexane_needed.lci()
    Total_hexane_needed.lcia()

    Total_DMSO_needed = bw.LCA({DMSO: solid_handling_choice*Solid_handling_DMSO_needed}, Method)
    Total_DMSO_needed.lci()
    Total_DMSO_needed.lcia()
    
    Total_NaOH_needed = bw.LCA({NaOH: solid_handling_choice*Solid_handling_NaOH_needed}, Method)
    Total_NaOH_needed.lci()
    Total_NaOH_needed.lcia()
    
    Total_H2SO4_needed = bw.LCA({H2SO4: solid_handling_choice*Solid_handling_H2SO4_needed}, Method)
    Total_H2SO4_needed.lci()
    Total_H2SO4_needed.lcia()
    
    Upgrading_electricity_lca = bw.LCA({Electricity : Electricityneeded_upgrading[i]*0.28/massflowrate}, Method)
    Upgrading_electricity_lca.lci()
    Upgrading_electricity_lca.lcia()

    Upgrading_heat_lca = bw.LCA({Natural_gas : Heatforupgrading[i]*1000/(massflowrate*Natural_gas_energy)}, Method)
    Upgrading_heat_lca.lci()
    Upgrading_heat_lca.lcia()    
    
    BPA_ethanol = bw.LCA({Ethanol: Ethanol_needed}, Method)
    BPA_ethanol.lci()
    BPA_ethanol.lcia() 

    CO2_emmision_from_HTL_electricty = HTLlcaelectricity.score
    CO2_emmision_from_HTL_heat = HTL_heat_lca.score
    CO2_emmision_from_solidhandling_heat = Solidhandling_heat.score
    CO2_emmision_from_total_water_needed = Total_Water_needed.score
    CO2_emmision_from_total_water_treatment = Total_Water_treatment.score
    CO2_emmision_from_total_hexane_needed = Total_hexane_needed.score
    CO2_emmision_from_total_DMSO_needed = Total_DMSO_needed.score
    CO2_emmision_from_total_NaOH_needed = Total_NaOH_needed.score
    CO2_emmision_from_total_H2SO4_needed = Total_H2SO4_needed.score
    CO2_emmision_from_upgrading_electricity = Upgrading_electricity_lca.score
    CO2_emmision_from_upgrading_heat = Upgrading_heat_lca.score
    CO2_emmision_from_ethanol = BPA_ethanol.score
    
    print ("\nFactor: \t\t\t\t kg CO2 emmisions per ton of feedstock") 
    print ("HTL electricty: \t\t\t", round(CO2_emmision_from_HTL_electricty*1000,2))
    print ("HTL heat: \t\t\t\t\t", round((CO2_emmision_from_HTL_heat+HTL_Emmision_from_burning_natural_gas)*1000,2))
    print ("HTL transport: \t\t\t\t", round(Transport_emmision_fromHTL[i]*1000,2))
    print ("Solid handling heat: \t", round(CO2_emmision_from_solidhandling_heat*1000,2))
    print ("Total water needed: \t\t", round(CO2_emmision_from_total_water_needed*1000,2))
    print ("Total water treatment: \t\t", round(CO2_emmision_from_total_water_treatment*1000,2))
    print ("Total hexane needed: \t\t", round(CO2_emmision_from_total_hexane_needed*1000,2))
    print ("Total DMSO needed: \t\t\t", round(CO2_emmision_from_total_DMSO_needed*1000,2))
    print ("Total NaOH needed: \t\t\t", round(CO2_emmision_from_total_NaOH_needed*1000,2))
    print ("Total H2SO4 needed: \t\t", round(CO2_emmision_from_total_H2SO4_needed*1000,2))
    print ("Total Ethanol needed: \t\t", round(CO2_emmision_from_ethanol*1000,2))
    print ("Upgrading electricty: \t\t", round(CO2_emmision_from_upgrading_electricity*1000,2))
    print ("Upgrading heat: \t\t\t", round((Upgrading_Emmision_from_burning_natural_gas+CO2_emmision_from_upgrading_heat)*1000,2))
    print ("Upgrading transport: \t\t", round(Transport_emmision_fromUpgrading[i]*1000,2))
    print ("Upgrading hydrogen: \t\t", round(Emmision_from_H2[i]*1000,2),"\n")
    
    print("The LCA outputs are : ")
    print("Total LCA emmisions per ton of waste processed:", round(Total_emmisions[i]*1000,2), " ", LCA_score_unit)
    print("HTL alone emits ", round((HTL_emmisions[i])*1000,2), " ", LCA_score_unit)
    print("Upgrading alone emits ", round(Upgrading_emmisions[i]*1000,2), " ", LCA_score_unit,"\n")
    
    
    Kg_CO2_in_feedstock[i] = Carbon_in_plastic_feedstock[i]*44/12;
    CO2_substitution_from_gasoline_diesel_blend_per_kg = (Kg_CO2_per_kg_gasoline*Percentage_naptha + Kg_CO2_per_kg_diesel*(100-Percentage_naptha))/100
    CO2_substitution_from_gasoline[i] =  Gasolineproduced[i]*CO2_substitution_from_gasoline_diesel_blend_per_kg/100;
    
    Negation_due_to_plastic_in_feedstock = Kg_CO2_in_feedstock[i]/100

    SubstitutionDemand_array = {BPA_basic : 0, TPA_basic: TPA_yield[i]/100}
    Substitution_lca[i] = bw.LCA(SubstitutionDemand_array, Method)
    Substitution_lca[i].lci()
    Substitution_lca[i].lcia()
    
    CO2_substitution_from_TPA[i] =  Substitution_lca[i].score
    
    SubstitutionDemand_array = {BPA_basic : BPA_purification_choice*BPA_yield[i]/100, TPA_basic: 0}
    Substitution_lca[i] = bw.LCA(SubstitutionDemand_array, Method)
    Substitution_lca[i].lci()
    Substitution_lca[i].lcia()
    
    CO2_substitution_from_BPA[i] =  Substitution_lca[i].score
    
    Biochar_CO2_avoided = 0.98  ; #kg CO2/kg biochar #Life Cycle Assessment and Environmental Valuation of Biochar Production: Two Case Studies in Belgium
    CO2_substitution_from_biochar = Biochar_CO2_avoided*Biochar_yield[i]/100
    
    gas_factor = 0.8*1+0.2*44/28; #80% CO2 and 20% CO (assumption)
    CO2_substitution_from_gas_phase = carbon_sequestration_choice*Gas_yield[i] * gas_factor/100
                
    print("Substitutions:")
    print("Gasoline - Diesel blend: \t", round(-CO2_substitution_from_gasoline[i]*1000,2), " ", LCA_score_unit)
    print("Plastic combustion from feed: \t", round(Negation_due_to_plastic_in_feedstock*1000,2), " ", LCA_score_unit)
    print("TPA: \t\t", round(-CO2_substitution_from_TPA[i]*1000,2), " ", LCA_score_unit)
    print("BPA: \t\t", round(-CO2_substitution_from_BPA[i]*1000,2), " ", LCA_score_unit)
    print("Biochar: \t", round(-CO2_substitution_from_biochar*1000,2), " ", LCA_score_unit)
    print("Gas phase sequestration: \t", round(-CO2_substitution_from_gas_phase*1000,2), " ", LCA_score_unit)
    HTL_emmision_per_kg[i] = (Total_emmisions[i]-CO2_substitution_from_gasoline[i]-CO2_substitution_from_TPA[i]-CO2_substitution_from_BPA[i]-CO2_substitution_from_gas_phase-CO2_substitution_from_biochar+Negation_due_to_plastic_in_feedstock);
    
    print("Total LCA emmisions per ton of waste processed with substitution:", round((HTL_emmision_per_kg[i])*1000,2), " ", LCA_score_unit)
    
    #Landfilling,recycling,combustion model
    print ("\n************************************************************************\n")
    landfilling = first_object[i].Landfilling_process_model()
    print ("\n************************************************************************\n")
    recycling = first_object[i].Recycling_process_model()
    print ("\n************************************************************************\n")
    combustion = first_object[i].Combustion_process_model()
    print ("\n************************************************************************\n")
    composting = first_object[i].Composting_process_model()
    print ("\n************************************************************************\n")
    print("Comparing the same feedstock with contemporary techniques (per ton of waste processed)")
    print("LCA emmisions from:")
    
    landfilling_average_percentage = 52;
    recycling_average_percentage = 25;
    combustion_average_percentage = 13;
    composting_average_percentage = 10;
    
    print("Recycling: \t\t\t\t\t\t", round(recycling_average_percentage*recycling[0]/100*1000,2), " ", LCA_score_unit)
    print("Landfilling: \t\t\t\t\t", round(landfilling_average_percentage*landfilling[0]*1000/100,2), " ", LCA_score_unit)
    print("Combustion: \t\t\t\t\t", round(combustion_average_percentage*combustion[0]*1000/100,2), " ", LCA_score_unit)
    print("Composting: \t\t\t\t\t", round(composting_average_percentage*composting*1000/100,2), " ", LCA_score_unit)
    
    print("Net conventional emmision: \t\t", round((recycling_average_percentage*recycling[0]+landfilling_average_percentage*landfilling[0]+combustion_average_percentage*combustion[0]+composting_average_percentage*composting)/100*1000,2), " ", LCA_score_unit, "\n")
    print("HTL: \t\t\t\t\t\t\t", round(HTL_emmision_per_kg[i]*1000,2), " ", LCA_score_unit)

    Conventional_emmision = (recycling_average_percentage*recycling[0]+landfilling_average_percentage*landfilling[0]+combustion_average_percentage*combustion[0]+composting_average_percentage*composting)/100

    Carbon_saved_by_HTL = Conventional_emmision - HTL_emmision_per_kg[i]
    print("Carbon saved by HTL: \t\t\t", round(Carbon_saved_by_HTL*1000,2), " ", LCA_score_unit, "\n")

    #Analyzing the economics 
    #capital cost
    Upgrading_instrument_cost = 32.28*10**6 #2016 PNNL w/o hydrogen plant
    HTL_capitol_cost = HTL_capital_cost_net[i]
    Building_cost = 5.2*10**6
    Working_capitol = 3.7*10**6
    Total_cost_order_of_magnitude[i] = Upgrading_capital_order_of_magnitude[i] + HTL_capital_order_of_magnitude[i]
    Total_cost_lang_method[i] = HTL_capital_lang_method[i] + Upgrading_capital_lang_method[i]
    Total_cost_guthrie_method = HTL_capital_guthrie_method + Upgrading_capital_guthrie_method
    
    print ("Total cost by lang method is: $", round(Total_cost_lang_method[i],2), "or ", "{:e}".format(Total_cost_lang_method[i]))
    print ("Total cost by order of magnitude method is: $", round(Total_cost_order_of_magnitude[i],2), "or ", "{:e}".format(Total_cost_order_of_magnitude[i]))
    
    #operating cost
    Natural_gas_per_kg = 4.30/(3.63*1000); #$
    Electricity_per_kWh = 6.56/100; #$
    Water_per_kg = 3.35/3790; #$ https://www.energy.gov/sites/prod/files/2017/10/f38/water_wastewater_escalation_rate_study.pdf
    Hydrogen_per_kg = 1.20; #$
    Catalyst_per_kg = 15.5/0.453; #$
    Catalyst_needed_per_kg_feedstock = 3.4383*10**-5
    Gasoline_per_kg = 2.88; #$/kg check?????
    CO2_sequestration = 74.95/1000; #$/kg-CO2 for cement https://www.researchgate.net/publication/331042323_Comparison_of_Technologies_for_CO2_Capture_from_Cement_Production-Part_2_Cost_Analysis
    Hexane_cost = 60/78;
    DMSO_cost = 70/78
    Cost_Natural_gas_per_mJ = 0.00372236288;
    NaOH_cost = 125/1000; #$/kg https://yosemite.epa.gov/sab/sabproduct.nsf/953CCBEB820F0470852577920076316D/$File/NaOH+Practicality+Study.pdf
    H2SO4_cost = 49/1000; #$/kg https://www.echemi.com/productsInformation/pid_Rock19440-sulfuric-acid.html#:~:text=Sulfuric%20Acid%20Price%20Analysis&text=Reference%20price%20of%20Sulfuric%20Acid,on%202021%2D01%2D15.&text=Reference%20price%20of%20Sulfuric%20Acid%20is%2049.065USD%2FMT%2C%20down,on%202021%2D01%2D14.
    Ethanol_cost = 1.49/2.96; #$/kg https://markets.businessinsider.com/commodities/ethanol-price
    
    Cost_Natural_gas = Totalheatneeded[i] *Cost_Natural_gas_per_mJ /(massflowrate) #cost per kg feedstock
    Cost_Electricity = Electricityneeded[i] * 0.28 * Electricity_per_kWh/massflowrate #cost per kg feedstock
    Cost_water = (fresh_water_needed[i]) * Water_per_kg #cost per kg feedstock
    Cost_Hydrogen = Hydrogen_consumption_per_kg_feedstock[i] * Hydrogen_per_kg #cost per kg feedstock
    Cost_catalyst = Catalyst_needed_per_kg_feedstock * Catalyst_per_kg #cost per kg feedstock
    Cost_transport = (Gasoline_consumption_to_HTL[i] + Gasoline_consumption_HTL_oil_to_upgrading[i]+Gasoline_consumption_HTL_upgraded_oil_to_consumer[i])*Gasoline_per_kg;
    Cost_CO2_sequestration = carbon_sequestration_choice*CO2_sequestration*Gas_yield[i]*gas_factor/100
    Cost_hexane = Hexane_cost*Hexane_consumed;
    Cost_DMSO =  DMSO_cost*solid_handling_choice*Solid_handling_DMSO_needed
    Cost_NaOH = NaOH_cost*Solid_handling_NaOH_needed*solid_handling_choice
    Cost_H2SO4 = H2SO4_cost*Solid_handling_H2SO4_needed*solid_handling_choice
    Cost_ethanol = Ethanol_cost*Ethanol_needed*BPA_purification_choice
    
    print ("Factor: \t\t\t", "Cost in $/kg feedstock processed")
    print ("Natural gas: \t\t", round(Cost_Natural_gas,4))
    print ("Electricity: \t\t", round(Cost_Electricity,4))
    print ("Water: \t\t\t\t", round(Cost_water,4))
    print ("Hydrogen: \t\t\t", round(Cost_Hydrogen,4))
    print ("Catalyst: \t\t\t", round(Cost_catalyst,4))
    print ("Transport: \t\t\t", round(Cost_transport,4))
    print ("CO2 sequestration: \t", round(Cost_CO2_sequestration,4))
    print ("Hexane: \t\t\t", round(Cost_hexane,4))
    print ("DMSO: \t\t\t\t", round(Cost_DMSO,4))
    print ("NaOH: \t\t\t\t", round(Cost_NaOH,4))
    print ("Ethanol: \t\t\t\t", round(Cost_NaOH,4))
    print ("H2SO4: \t\t\t\t", round(Cost_H2SO4,4),"\n")
    
    operating_hours_per_day = 20
    operating_days = 275
    Net_operating_cost_per_kg = Cost_Natural_gas + Cost_Electricity + Cost_water + Cost_Hydrogen + Cost_catalyst+Cost_transport + carbon_sequestration_choice*Cost_CO2_sequestration + Cost_hexane + Cost_DMSO + Cost_NaOH + Cost_H2SO4 + Cost_ethanol;
    Net_operating_cost_per_year = Net_operating_cost_per_kg*massflowrate*operating_hours_per_day*operating_days
    
    print ("Operating cost per year: ", round(Net_operating_cost_per_year,2), "$ or ", "{:e}".format(Net_operating_cost_per_year),"$")
    print ("Operating cost per kg feedstock: ", round(Net_operating_cost_per_kg,4),"$/kg")
    
    #Assuming 10 year for profit, 275 working days, 20 hour working days. 
    Time_plant_for_profit = 10; #years
    Feedstock_processed_in_10_years = massflowrate*Time_plant_for_profit*operating_days*operating_hours_per_day;
    
    Annual_interest_rate = 8
    Compounded = 12; #monthly
 
    selling_price_BPA = 1.725 #$/kg
    selling_price_TPA = 0.95 #$/kg
    Biochar_selling_price = 485/1000 #$/kg

    credit_per_kg_feedstock = (selling_price_TPA*TPA_yield[i] + BPA_purification_choice*selling_price_BPA*BPA_yield[i] + Biochar_selling_price*Biochar_yield[i])/100;

    print ("\nLang Method:\n")
    
    capitol_cost_method = 0 #0 - lang, 1 - order of magnitude, 2 - guthrie
    
    if capitol_cost_method == 0:
        Net_expense_for_10_years = Total_cost_lang_method[i]*(1+Annual_interest_rate/(100*Compounded))**(Compounded*Time_plant_for_profit)
    elif capitol_cost_method == 1:
        Net_expense_for_10_years = Total_cost_order_of_magnitude[i]*(1+Annual_interest_rate/(100*Compounded))**(Compounded*Time_plant_for_profit)
    elif capitol_cost_method == 2:
        Net_expense_for_10_years = Total_cost_guthrie_method*(1+Annual_interest_rate/(100*Compounded))**(Compounded*Time_plant_for_profit)
    
    Capitol_cost_per_kg = Net_expense_for_10_years/Feedstock_processed_in_10_years;
    print ("The capitol cost per kg feedstock is : \t\t\t",round(Capitol_cost_per_kg,2), " $/kg")
    
    Net_cost_per_kg_feedstock = Capitol_cost_per_kg + Net_operating_cost_per_kg;
    print ("The total cost per kg feedstock is : \t\t\t",round(Net_cost_per_kg_feedstock,2), " $/kg")
    Net_cost_per_kg_gasoline_produced = 100*Net_cost_per_kg_feedstock/Gasolineproduced[i]
    print ("The total cost per kg gasoline produced is : \t",round(Net_cost_per_kg_gasoline_produced,2), " $/kg or ",round(Net_cost_per_kg_gasoline_produced*3.79,2), " $/gallon")

    Net_cost_per_kg_gasoline_produced_with_credits = 100*(Net_cost_per_kg_feedstock-credit_per_kg_feedstock)/Gasolineproduced[i]
    
    print("\nCredits per gallon gasoline produced:")
    print("Baseline Gasoline cost: \t\t\t\t\t", round(Net_cost_per_kg_gasoline_produced*3.79,2), " $/gallon")
    print("TPA credit: \t\t\t\t\t\t\t\t", round(-selling_price_TPA*TPA_yield[i]*3.79/Gasolineproduced[i],2), " $/gallon")
    print("BPA credit: \t\t\t\t\t\t\t\t", round(-BPA_purification_choice*selling_price_BPA*BPA_yield[i]*3.79/Gasolineproduced[i],2), " $/gallon")
    print("Biochar credit: \t\t\t\t\t\t\t", round(-Biochar_selling_price*Biochar_yield[i]*3.79/Gasolineproduced[i],2), " $/gallon")
    print ("Net cost per gallon gasoline with credits: \t",round(Net_cost_per_kg_gasoline_produced_with_credits,2), " $/kg or ",round(Net_cost_per_kg_gasoline_produced_with_credits*3.79,2), " $/gallon")

    print ("The EROI is ", round(EROI,2))
    print("HTL: \t\t\t\t\t\t\t", round(HTL_emmision_per_kg[i]*1000,2), " ", LCA_score_unit)

    print("Substitutions:")
    print("Total LCA emmisions per ton of waste processed:", round(Total_emmisions[i]*1000,2), " ", LCA_score_unit)
    print("Gasoline - Diesel blend: \t", round(-CO2_substitution_from_gasoline[i]*1000,2), " ", LCA_score_unit)
    print("Plastic combustion from feed: \t", round(Negation_due_to_plastic_in_feedstock*1000,2), " ", LCA_score_unit)
    print("TPA: \t\t", round(-CO2_substitution_from_TPA[i]*1000,2), " ", LCA_score_unit)
    print("BPA: \t\t", round(-CO2_substitution_from_BPA[i]*1000,2), " ", LCA_score_unit)
    print("Biochar: \t", round(-CO2_substitution_from_biochar*1000,2), " ", LCA_score_unit)
    print("Gas phase sequestration: \t", round(-CO2_substitution_from_gas_phase*1000,2), " ", LCA_score_unit)
    
    print("Total LCA emmisions per ton of waste processed with substitution:", round((HTL_emmision_per_kg[i])*1000,2), " ", LCA_score_unit)
  
    
    print("\nCredits per ton feedstock produced:")
    print("Baseline Gasoline cost: \t\t\t\t\t", round(Net_cost_per_kg_gasoline_produced*Gasolineproduced[i]*10,2), " $/ton")
    print("TPA credit: \t\t\t\t\t\t\t\t", round(-selling_price_TPA*TPA_yield[i]*10,2), " $/ton")
    print("BPA credit: \t\t\t\t\t\t\t\t", round(-BPA_purification_choice*selling_price_BPA*BPA_yield[i]*10,2), " $/ton")
    print("Biochar credit: \t\t\t\t\t\t\t", round(-Biochar_selling_price*Biochar_yield[i]*10,2), " $/ton")
    print ("Net cost per gallon gasoline with credits: \t",round(Net_cost_per_kg_gasoline_produced_with_credits*Gasolineproduced[i]*10,2), " $/ton")

    print("Substitutions:")
    print("Total LCA emmisions per ton of waste processed:", round(Total_emmisions[i]*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    print("Gasoline - Diesel blend: \t", round(-CO2_substitution_from_gasoline[i]*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    print("Plastic combustion from feed: \t", round(Negation_due_to_plastic_in_feedstock*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    print("TPA: \t\t", round(-CO2_substitution_from_TPA[i]*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    print("BPA: \t\t", round(-CO2_substitution_from_BPA[i]*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    print("Biochar: \t", round(-CO2_substitution_from_biochar*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    print("Gas phase sequestration: \t", round(-CO2_substitution_from_gas_phase*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    
    print("Total LCA emmisions per gallon of gasoline processed with substitution:", round((HTL_emmision_per_kg[i])*379/Gasolineproduced[i],2), " ", LCA_score_unit)
    
    print("\nValues to note down: \nPer ton feedstock: ", round((HTL_emmision_per_kg[i])*1000,2), " ", LCA_score_unit, " ", round(Gasoline_per_kg*Gasolineproduced[i]*10-Net_cost_per_kg_gasoline_produced_with_credits*Gasolineproduced[i]*10,2), " $/ton")
    print("Per gallon of gasoline: ", round((HTL_emmision_per_kg[i]+CO2_substitution_from_gasoline[i])*379/Gasolineproduced[i],2), " ", LCA_score_unit, " ", round(Net_cost_per_kg_gasoline_produced_with_credits*3.79,2), " $/gallon ")
      