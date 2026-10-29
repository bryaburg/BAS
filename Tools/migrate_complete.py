#!/usr/bin/env python3
"""
Complete migration: route every tracked file (195 non-zip + 7 zips = 202)
from the original BAS library layout into Equipment/<Type>/<Instance>/,
Shared/, Common/, Libraries/, Data/, Tools/.

Uses explicit path->target mapping (no guessing). git mv preserves history.

run:  python3 Tools/migrate_complete.py
"""

import os
import subprocess
import shutil

BASE = "/workspace/BAS"

def ensure(*parts):
    p = os.path.join(BASE, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p

def git_mv(src_rel, dst_rel):
    s = os.path.join(BASE, src_rel)
    d = os.path.join(BASE, dst_rel)
    if not os.path.exists(s):
        print("  SKIP (no src): %s" % src_rel)
        return False
    ensure(*dst_rel.split(os.sep))
    try:
        subprocess.run(["git", "-C", BASE, "mv", "-k", src_rel, dst_rel],
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print("  FAIL: %s -> %s (%s)" % (src_rel, dst_rel, e))
        return False

def zip_snapshot(zname):
    s = os.path.join(BASE, zname)
    d = os.path.join(BASE, "Libraries", zname)
    ensure("Libraries")
    try:
        subprocess.run(["git", "-C", BASE, "rm", "-f", "--quiet", zname],
                       check=True, capture_output=True)
        shutil.copy2(s, d)
        os.remove(s)
        print("  zip -> Libraries/%s" % zname)
        return True
    except Exception as e:
        print("  FAIL zip %s: %s" % (zname, e))
        return False

# ---- target shortcuts (each returns a full relative path string) ------------
def A(*p):  return os.path.join("Equipment","AHU","AHU01",*p)
def V(*p):  return os.path.join("Equipment","VAV","VAV-102",*p)
def C(*p):  return os.path.join("Equipment","Chiller","Chiller01",*p)
def CH(*p): return os.path.join("Equipment","ChilledWater","GlobalSystem",*p)
def P(*p):  return os.path.join("Equipment","Pump",*p)
def B(*p):  return os.path.join("Equipment","Boiler","Boiler01",*p)
def R(*p):  return os.path.join("Equipment","RTU","RTU01",*p)
def U(*p):  return os.path.join("Equipment","UnitVentilator","UV01",*p)
def S(*p):  return os.path.join("Equipment","SmartX",*p)
def T(*p):  return os.path.join("Shared",*p)          # Shared only
def K(*p):  return os.path.join("Common",*p)          # Common only
def D(*p):  return os.path.join("Data",*p)
def LI(*p): return os.path.join("Libraries",*p)

M = []  # (src_rel, dst_rel)

# ============================== AHU =========================================
M += [
    ("AHU/H/Calcs.txt", A("Calculations","Calcs.txt")),
    ("AHU/H/HtgVlvCmd.txt", A("Programs","HtgVlvCmd.txt")),
    ("AHU/H/MaDmpr.txt", A("Programs","MaDmpr.txt")),
    ("AHU/H/MaDprMaxSpt.txt", A("Programs","MaDprMaxSpt.txt")),
    ("AHU/H/MaStpt.txt", A("Programs","MaStpt.txt")),
    ("AHU/H/Mode.txt", A("Programs","Mode.txt")),
    ("AHU/H/PID.txt", A("Programs","PID.txt")),
    ("AHU/H/RaDmpr.txt", A("Programs","RaDmpr.txt")),
    ("AHU/H/ReliefFan.txt", A("Programs","ReliefFan.txt")),
    ("AHU/H/ResetFun.txt", A("Programs","ResetFun.txt")),
    ("AHU/H/SaFanControl.txt", A("Programs","SaFanControl.txt")),
    ("AHU/H/SaFanSts.txt", A("Programs","SaFanSts.txt")),
    ("AHU/H/VRF.txt", A("Programs","VRF.txt")),
    ("SaTmpSpt Ctrl/SaTmpSptCtrl.txt", A("Programs","SaTmpSptCtrl.txt")),
    ("SaTmpSpt Ctrl/SaTmpSptCtrl - For FCU with HW fed from AHU.txt",
        A("Programs","SaTmpSptCtrl - FCU from AHU.txt")),
    ("SaTmpSpt Ctrl/Crusher~AHU12~Programs~SaTmpSptCtrl.txt",
        A("Programs","SaTmpSptCtrl - AHU12.txt")),
    ("Fan Control/FanFailFanHandPrg.txt", A("Programs","FanFailFanHandPrg.txt")),
    ("Fan Control/SaFanCmdCtrl.txt", A("Programs","SaFanCmdCtrl.txt")),
    ("Fan Control/SaFanSpdCtrl Duct Static.txt",
        A("Programs","SaFanSpdCtrl - Duct Static.txt")),
    ("Fan Control/SaFanSpdCtrl Duct Static RampUp RampDn.txt",
        A("Programs","SaFanSpdCtrl - Duct Static RampUp RampDn.txt")),
    ("SaFanSpdCtrl.txt", A("Programs","SaFanSpdCtrl.txt")),
    ("MaDpr Ctrl/Mixed Air Temp Control EconMd.txt",
        A("Programs","Mixed Air Temp Control - MaDpr.txt")),
    ("MEC Program Text Dumps/Programs/Damper Control Programs/Mixed Air Temp Control EconMd.txt",
        A("Programs","Mixed Air Temp Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Damper Control Programs/Mixed Air Temp Control.txt",
        A("Programs","Mixed Air Temp Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Fan Programs/SaFanSpdCtrl.txt",
        A("Programs","SaFanSpdCtrl - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Fan Programs/SaStPrSptCtrl.txt",
        A("Programs","SaStPrSptCtrl - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Airflow Normalization.txt",
        V("Calcs","Airflow Normalization - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Box Size Calcs.txt",
        V("Calcs","Box Size Calcs - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Damper Control.txt",
        V("Programs","Damper Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Reheat Control.txt",
        V("Programs","Reheat Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/TAB Calcs.txt",
        V("Calcs","TAB Calcs - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Valve Control Programs/HwVlvCtrl.txt",
        ("Shared","Controller","HwVlvCtrl.txt")),
    ("MaDpr Ctrl/Mixed Air Temp Control EconMd.txt", A("Programs","Mixed Air Temp Control - MaDpr.txt")),
    ("MEC Program Text Dumps/Programs/Supply Temp Setpoint/SaTmpSptCtrl.txt",
        ("Shared","Controller","SaTmpSptCtrl - Supply Temp.txt")),
]

# ============================== VAV ===========================================
M += [
    ("Basepoint MP VAV/CfmSptCalcs.txt", V("Calcs","CfmSptCalcs.txt")),
    ("Custom VAV Control/CfmCalcs.txt", V("Calcs","CfmCalcs.txt")),
    ("Custom VAV Control/CfmSptCalcs.txt", V("Calcs","CfmSptCalcs.txt")),
    ("Custom VAV Control/DprCtrl.txt", V("Programs","DprCtrl.txt")),
    ("Custom VAV Control/SaTmpSptCtrl with HC Dmd.txt",
        V("Programs","SaTmpSptCtrl - HC Dmd.txt")),
    ("VAV Ctrl/DualDuctDprCtrl.txt", V("Programs","DualDuctDprCtrl.txt")),
    ("MP-VAV RmTmpSpt Ctrl/Calcs.txt", V("Calcs","RmTmpSptCtrl Calcs.txt")),
    ("MP-VAV RmTmpSpt Ctrl/RmTmpSptCtrl.txt", V("Programs","RmTmpSptCtrl.txt")),
    ("MP-VAV RmTmpSpt Ctrl/MP-VAV RmTmpSpt Control Programs.xml",
        V("Config","MP-VAV RmTmpSpt Control Programs.xml")),
    ("MP-VAV RmTmpSpt Ctrl/RmTmpSptCtrl Parameter Point.xml",
        V("Config","RmTmpSptCtrl Parameter Point.xml")),
    ("MP-VAV RmTmpSpt Ctrl/Sample VAV.tgml", D("Graphics","Sample VAV.tgml")),
    ("VAV AHU SaTmpSpt Ctrl.txt", V("Programs","SaTmpSptCtrl - VAV AHU.txt")),
]
b3files = [
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~Airflow Normalization.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~Box Size Calcs.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~Damper Control.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~FlashBack Ctrl.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~Night Cycle Control.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~Override Control.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~Reheat Control.txt",
    "BACnet Interface~MSTP Network 2727 ComA~A3_TAB03~Application~TABCalcs.txt",
]
for f in b3files:
    M.append((os.path.join("B3 VAV Programs", f), V("Programs", os.path.basename(f))))
for f in ["Airflow Normalization.txt","Box Size Calcs.txt"]:
    M.append((os.path.join("Old B3 VAV Programs", f), V("Calcs", f)))
for f in os.listdir(os.path.join(BASE,"Old B3 VAV Programs")):
    if f.endswith(".txt") and f not in ("Airflow Normalization.txt","Box Size Calcs.txt"):
        M.append((os.path.join("Old B3 VAV Programs", f), V("Programs", f)))

# ============================== CHILLER =======================================
M += [
    ("Chiller Alarm Programs/Main~Equipment~Chilled Water System~3 - Chiller01~Chiller~ChillerAlarmControl~Programs~AlarmCtrl.txt",
        C("Alarms","AlarmCtrl.txt")),
    ("Chiller Alarm Programs/Main~Equipment~Chilled Water System~3 - Chiller01~Chiller~ChillerAlarmControl~Programs~AlarmDisplayCtrl.txt",
        C("Alarms","AlarmDisplayCtrl.txt")),
    ("Chiller Fail Alarm Program.txt", C("Alarms","Chiller Fail Alarm Program.txt")),
    ("Chiller Staging 2 Chillers/Ch01CmdPrg.txt", C("Programs","Ch01CmdPrg.txt")),
    ("Chiller Staging 2 Chillers/Ch02CmdPrg.txt", C("Programs","Ch02CmdPrg.txt")),
    ("Chiller Staging 2 Chillers/ChangeLeads.txt", C("Programs","ChangeLeads.txt")),
    ("Chiller Staging 2 Chillers/ChlrAltLdLgPrg.txt", C("LeadLag","ChlrAltLdLgPrg.txt")),
    ("Chiller Staging 2 Chillers/ChlrFailTestPrg.txt", C("LeadLag","ChlrFailTestPrg.txt")),
    ("Chiller Staging 2 Chillers/ChlrLdLgPrg.txt", C("LeadLag","ChlrLdLgPrg.txt")),
    ("Chiller Staging 2 Chillers/ChlrStgPrg.txt", C("LeadLag","ChlrStgPrg.txt")),
    ("Two Chiller Lead Lag Programs/ChangeLeads.txt", C("LeadLag","ChangeLeads.txt")),
    ("Two Chiller Lead Lag Programs/Chlr01CmdPrg.txt", C("LeadLag","Chlr01CmdPrg.txt")),
    ("Two Chiller Lead Lag Programs/Chlr01FailCtrlPrg.txt", C("LeadLag","Chlr01FailCtrlPrg.txt")),
    ("Two Chiller Lead Lag Programs/Chlr02CmdPrg.txt", C("LeadLag","Chlr02CmdPrg.txt")),
    ("Chiller Staging 2 Chillers.zip", LI("Chiller Staging 2 Chillers.zip")),
]

# ============================== CHILLED WATER =================================
M += [
    ("ChwVlv Ctrl/ChwVlvCtrl.txt", CH("Programs","ChwVlvCtrl.txt")),
    ("Chw Controlled as DX Control.txt", T("Staging","Chw Controlled as DX Control.txt")),
    ("Chilled Water Parsing out Sequence and Assigning Pump GPM.txt",
        CH("Programs","Chilled Water Parsing out Sequence and Assigning Pump GPM.txt")),
]
for f in os.listdir(os.path.join(BASE,"Port Louisa ChwSys")):
    s = os.path.join(BASE,"Port Louisa ChwSys",f)
    if not os.path.isfile(s): continue
    b = os.path.basename(f)
    if "ChWtrEnable" in f or "ChWtrVlvPosCtrl" in f or "StartPrg" in f or "ChDivVlvCntrlPrg" in f:
        dst = CH("Programs", b.replace("Main~Equipment~Ahu101 Ahu102~Programs Only Ahu101~","Ahu101 ").replace("Main~Equipment~Ahu101 Ahu102~Programs Only Ahu102~","Ahu102 "))
    elif "Pumps" in f or "New ChwPmpPrg" in f or "New ChwVlvPrg" in f:
        dst = CH("Pumps", b)
    else:
        dst = CH("Programs", b)
    M.append((os.path.relpath(s,BASE), dst))
for grp in ["Secondary Chilled Water Pumping LdLg 2 stages",
            "Secondary Chilled Water Pumping LdLg 3 stages"]:
    for f in os.listdir(os.path.join(BASE,grp)):
        s = os.path.join(BASE,grp,f)
        if os.path.isfile(s):
            M.append((os.path.relpath(s,BASE), CH("Pumps",f)))
M += [
    ("Secondary Chilled Water Pumping LdLg 2 stages.zip", LI("Secondary Chilled Water Pumping LdLg 2 stages.zip")),
    ("Secondary Chilled Water Pumping LdLg 2 stages (2).zip", LI("Secondary Chilled Water Pumping LdLg 2 stages (2).zip")),
    ("Secondary Chilled Water Pumping LdLg 2 stages (3).zip", LI("Secondary Chilled Water Pumping LdLg 3 stages.zip")),
]

# ============================== PUMP ==========================================
M += [
    ("Boiler/Pump_Control/Rotation.txt", P("Primary","Programs","Rotation.txt")),
    ("Boiler/Pump_Control/Speed.txt", P("Primary","Programs","Speed.txt")),
    ("Boiler/Pump_Control/Start_Stop.txt", P("Primary","Programs","Start_Stop.txt")),
    ("Boiler/Pump_Control/Space Logic.xml", P("Primary","Config","SpaceLogic.xml")),
    ("Pump Controls/Secondary Pump Speed Signal Program.txt",
        P("Secondary","Programs","Secondary Pump Speed Signal Program.txt")),
    ("Pump Controls/SmPmpSpdSignalCtrl.txt", P("Secondary","Programs","SmPmpSpdSignalCtrl.txt")),
]

# ============================== BOILER ========================================
M += [
    ("Boiler/Boiler Control/Rotation.txt", B("Programs","Rotation.txt")),
    ("Boiler/Boiler Control/Setpoint.txt", B("Programs","Setpoint.txt")),
    ("Boiler/Boiler Control/Start_Stop.txt", B("Programs","Start_Stop.txt")),
    ("Boiler/Boiler Control/SpaceLogic.xml", B("Config","SpaceLogic.xml")),
]

# ============================== RTU ===========================================
M += [
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~DiagnosticAlertCtrl.txt",
        R("Programs","DiagnosticAlertCtrl.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~EconoCtrl.txt",
        R("Programs","EconoCtrl.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~MirrorPull.txt",
        R("Programs","MirrorPull.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~MirrorPush.txt",
        R("Programs","MirrorPush.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~OccCtrl.txt",
        R("Programs","OccCtrl.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~ResetDiag.txt",
        R("Programs","ResetDiag.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~SaFanCmdCtrl.txt",
        R("Programs","SaFanCmdCtrl.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~SaFanFalmCalcs.txt",
        R("Calcs","SaFanFalmCalcs.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~SaStPrSptCtrl.txt",
        R("Programs","SaStPrSptCtrl.txt")),
    ("TraneRTU/BACnet Interface~Application~Trane RTU01~Programs~SaTmpSptCtrl.txt",
        R("Programs","SaTmpSptCtrl.txt")),
    ("TraneRTU/Equipment~1 - RTU01~Graphic~RTU01.tgml", D("Graphics","RTU01.tgml")),
]

# ============================== UNIT VENTILATOR ===============================
M += [
    ("Unit Ventelator/Calcs.txt", U("Calculations","Calcs.txt")),
    ("Unit Ventelator/DXStage1Cooling.txt", U("Programs","DXStage1Cooling.txt")),
    ("Unit Ventelator/Hot Water Valve with Bypass Damper Heating Control.txt",
        U("Programs","Hot Water Valve with Bypass Damper Heating Control.txt")),
    ("Unit Ventelator/Mixed Air Damper Control.txt", U("Programs","Mixed Air Damper Control.txt")),
    ("Unit Ventelator/Mode.txt", U("Programs","Mode.txt")),
    ("Unit Ventelator/Outside Air Damper Error Code.txt",
        U("Programs","Outside Air Damper Error Code.txt")),
    ("Unit Ventelator/Variable Fan Control.txt", U("Programs","Variable Fan Control.txt")),
]

# ============================== SMARTX ========================================
M += [
    ("SmartX stats/Mode Override with SmartX stats/Updated sHvacMd99 program.txt",
        S("Sensors","Updated sHvacMd99 program.txt")),
    ("SmartX stats/Mode Override with SmartX stats/Notes on implementation.txt",
        S("Sensors","Notes on implementation.txt")),
    ("SmartX stats/Mode Override with SmartX stats/SmartX Stat Hvac Mode values.txt",
        S("Sensors","SmartX Stat Hvac Mode values.txt")),
    ("SmartX stats/Occupancy Override with SmartX stats/sOccOvr99 updated code.txt",
        S("Occupancy","sOccOvr99 updated code.txt")),
    ("SmartX stats/Occupancy Override with SmartX stats/Notes for SmartX stat and Occupancy Override.txt",
        S("Occupancy","Notes for SmartX stat and Occupancy Override.txt")),
    ("SmartX stats/Occupancy Override with SmartX stats/Occupancy Override Notes.txt",
        S("Occupancy","Occupancy Override Notes.txt")),
]

# ============================== SHARED (equipment-agnostic) ==================
M += [
    ("Functions/Dewpoint Function.txt", T("Functions","Dewpoint Function.txt")),
    ("Functions/Enthalpy Function.txt", T("Functions","Enthalpy Function.txt")),
    ("Functions/Input Filter Function.txt", T("Functions","Input Filter Function.txt")),
    ("Functions/MedianFct.txt", T("Functions","MedianFct.txt")),
    ("Functions/PID Loop Function.txt", T("Functions","PID Loop Function.txt")),
    ("Functions/Reset Setpoint Function.txt", T("Functions","Reset Setpoint Function.txt")),
    ("Functions/ResetFct.txt", T("Functions","ResetFct.txt")),
    ("Functions/Old Functions/Dewpoint Function.txt", T("Functions","Old Functions","Dewpoint Function.txt")),
    ("Functions/Old Functions/Enthalpy Function.txt", T("Functions","Old Functions","Enthalpy Function.txt")),
    ("Functions/Old Functions/Input Filter Function.txt", T("Functions","Old Functions","Input Filter Function.txt")),
    ("Functions/Old Functions/ResetFct.txt", T("Functions","Old Functions","ResetFct.txt")),
    ("MedianFct.xml", T("Functions","MedianFct - XML.xml")),
    ("1 Stage DX Control.txt", T("Staging","1 Stage DX Control.txt")),
    ("4 Stage DX Control.txt", T("Staging","4 Stage DX Control.txt")),
    ("Chw Controlled as DX Control.txt", T("Staging","Chw Controlled as DX Control.txt")),
    ("Mode.txt", T("Sequences","Mode.txt")),
    ("RnTmCalcs.txt", T("Utility","RnTmCalcs.txt")),
    ("Schneider Smart Stat Program.txt", T("Controller","Schneider Smart Stat Program.txt")),
    ("Cottingham Butler Old SmartStat Program.txt", T("Controller","Cottingham Butler Old SmartStat Program.txt")),
    ("B3 and I2 Smart Sensor.txt", T("Controller","B3 and I2 Smart Sensor.txt")),
    ("ConvertBINtoDEC.txt", T("Utility","ConvertBINtoDEC.txt")),
    ("ConvertDECtoBIN.txt", T("Utility","ConvertDECtoBIN.txt")),
    ("Bin to Dec/Main~Equipment~Programs~ConvertBINtoDEC_Reg401.txt",
        T("Utility","ConvertBINtoDEC_Reg401.txt")),
    ("Bin to Dec/Main~Equipment~Programs~ConvertBINtoDEC_Reg402.txt",
        T("Utility","ConvertBINtoDEC_Reg402.txt")),
    ("Bin to Dec/Main~Equipment~Programs~ConvertDECtoBIN_Reg001.txt",
        T("Utility","ConvertDECtoBIN_Reg001.txt")),
]

# ============================== DATA (non-code) ===============================
M += [
    ("Point Builder Dual Heat Load down to 1 average value.xlsx",
        D("Points","Point Builder Dual Heat Load down to 1 average value.xlsx")),
    ("UV/Types/MP-C-18A/DxStg1&HwVwithBypassDamper.xml", D("Graphics","MP-C-18A DxStg1&HwVwithBypassDamper.xml")),
    ("Weather API/Weather Data Dashboard.msg", D("Weather","Weather Data Dashboard.msg")),
]

# ============================== ZIP SNAPSHOTS ================================
M += [
    ("Chiller Staging 2 Chillers.zip", LI("Chiller Staging 2 Chillers.zip")),
    ("Secondary Chilled Water Pumping LdLg 2 stages.zip", LI("Secondary Chilled Water Pumping LdLg 2 stages.zip")),
    ("Secondary Chilled Water Pumping LdLg 2 stages (2).zip", LI("Secondary Chilled Water Pumping LdLg 2 stages (2).zip")),
    ("Secondary Chilled Water Pumping LdLg 2 stages (3).zip", LI("Secondary Chilled Water Pumping LdLg 3 stages.zip")),
    ("B3 VAV Programs.zip", LI("B3 VAV Programs.zip")),
    ("TraneRTU.zip", LI("TraneRTU.zip")),
    ("Program Text Dumps.zip", LI("Program Text Dumps.zip")),
]

# ============================== ADDITIONAL FILES (caught above) ==============
ADD = [
    ("Basepoint MP VAV/CfmSptCalcs.txt", V("Calcs","CfmSptCalcs.txt")),
    ("Fan Control/FanFailFanHandPrg.txt", A("Programs","FanFailFanHandPrg.txt")),
    ("Fan Control/SaFanCmdCtrl.txt", A("Programs","SaFanCmdCtrl.txt")),
    ("Fan Control/SaFanSpdCtrl Duct Static.txt", A("Programs","SaFanSpdCtrl - Duct Static.txt")),
    ("Fan Control/SaFanSpdCtrl Duct Static RampUp RampDn.txt",
        A("Programs","SaFanSpdCtrl - Duct Static RampUp RampDn.txt")),
    ("HwVlv Ctrl/Crusher~AHU12~Programs~HwVlvPosCtrl.txt", A("Programs","HwVlvPosCtrl - AHU12.txt")),
    ("HwVlv Ctrl/HwVlvCtrl.txt", A("Programs","HwVlvCtrl.txt")),
    ("MEC Program Text Dumps/Programs/Damper Control Programs/Mixed Air Temp Control EconMd.txt",
        A("Programs","Mixed Air Temp Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Damper Control Programs/Mixed Air Temp Control.txt",
        A("Programs","Mixed Air Temp Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Fan Programs/SaFanSpdCtrl.txt", A("Programs","SaFanSpdCtrl - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Fan Programs/SaStPrSptCtrl.txt", A("Programs","SaStPrSptCtrl - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Airflow Normalization.txt",
        V("Calcs","Airflow Normalization - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Box Size Calcs.txt",
        V("Calcs","Box Size Calcs - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Damper Control.txt",
        V("Programs","Damper Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/Reheat Control.txt",
        V("Programs","Reheat Control - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Old TAB Programs/TAB Calcs.txt",
        V("Calcs","TAB Calcs - MEC.txt")),
    ("MEC Program Text Dumps/Programs/Valve Control Programs/Electric Heat Signal Control.txt",
        V("Programs","Electric Heat Signal Control.txt")),
    ("MEC Program Text Dumps/Programs/Valve Control Programs/HwVlvCtrl.txt",
        ("Shared","Controller","HwVlvCtrl.txt")),
    ("MaDpr Ctrl/Mixed Air Temp Control EconMd.txt", A("Programs","Mixed Air Temp Control - MaDpr.txt")),
    ("SaTmpSpt Ctrl/JDDMW B1 HV Unit SaTmpCalcs.txt", A("Calculations","SaTmpCalcs - B1 HV Unit.txt")),
    ("SaTmpSpt Ctrl/SaTmpSptCtrl Prototype.txt", T("Utility","SaTmpSptCtrl Prototype.txt")),
    ("SaTmpSpt Ctrl/VAV AHU SaTmpSpt Ctrl.txt", V("Programs","SaTmpSptCtrl - VAV AHU.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/Change Leads.txt",
        CH("Programs","Change Leads.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/ChwP01CmdPrg.txt", CH("Pumps","ChwP01CmdPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/ChwP01FailCtrlPrg.txt", CH("Pumps","ChwP01FailCtrlPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/ChwP02CmdPrg.txt", CH("Pumps","ChwP02CmdPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/ChwP02FailCtrlPrg.txt", CH("Pumps","ChwP02FailCtrlPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/PmpAltLdLgPrg.txt", CH("Pumps","PmpAltLdLgPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/PmpFailTestPrg.txt", CH("Pumps","PmpFailTestPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/PmpLdLgPrg.txt", CH("Pumps","PmpLdLgPrg.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/RnTmCalcs_01.txt", CH("Pumps","RnTmCalcs_01.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/RnTmCalcs_02.txt", CH("Pumps","RnTmCalcs_02.txt")),
    ("Secondary Chilled Water Pumping LdLg 3 stages/RnTmCalcs_03.txt", CH("Pumps","RnTmCalcs_03.txt")),
]

# ============================== ASSEMBLE ====================================
all_moves = list(M) + [x for x in ADD if x not in M]
seen = set(); unique = []
for src,dst in all_moves:
    if (src,dst) not in seen:
        seen.add((src,dst)); unique.append((src,dst))
unique = [(a, os.path.join(*b) if isinstance(b, tuple) else b) for a,b in unique]

print("Total file moves to process: %d" % len(unique))
missing = [s for s,d in unique if not os.path.exists(os.path.join(BASE,s))]
print("Missing SRC files (%d):" % len(missing))
for m in missing: print("   -", m)

executed = 0
for src,dst in unique:
    if os.path.exists(os.path.join(BASE,src)):
        git_mv(src,dst); executed += 1
for z in ["Chiller Staging 2 Chillers.zip","Secondary Chilled Water Pumping LdLg 2 stages.zip",
          "Secondary Chilled Water Pumping LdLg 2 stages (2).zip",
          "Secondary Chilled Water Pumping LdLg 2 stages (3).zip","B3 VAV Programs.zip",
          "TraneRTU.zip","Program Text Dumps.zip"]:
    if os.path.exists(os.path.join(BASE,z)):
        zip_snapshot(z)
print("\nExecuted %d moves; zips relocated to Libraries/" % executed)
