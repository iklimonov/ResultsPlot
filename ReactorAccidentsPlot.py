import Modules.Utils.mySettings

from Modules.outputs import outputs
from Modules.outputs import jsScriptGroups
from Modules.Utils.utils import openJSON
from Modules.Utils.utils import exportCalculationParameters
from Modules.Utils.utils import isOn

from Modules.EUCLID.BERKUT import processingBERKUT
from Modules.EUCLID.BERKUT_N import processingBERKUT_N
from Modules.EUCLID.HYDRA import processingCORE
from Modules.EUCLID.DN3D import processingDN3D
from Modules.EUCLID.SAFR import processingSAFR
from Modules.EUCLID.SAFR import processingSAFR_CF
from Modules.EUCLID.COMMON import processingCOMMON
from Modules.EUCLID.AEROSOL import processingAEROSOL
from Modules.EUCLID.COMBINED import processingCOMBINED

from Modules.DataBase import DataBase
from Modules.DataBase import CoreDataModule
from Modules.DataBase import zoneData
from Modules.DataBase import commonDataModule

######################## MAIN ###################################################################################################################################
if __name__ == '__main__':

    ########################
    #from Modules.myGraph import myGraph

    #my_Graph = myGraph("myOx","myOy")
   # my_Graph.plotColoredMap("", "", "")
    ########################


    Modules.Utils.mySettings.init()
    

    mainParameters = openJSON("mainParameters","")
    folderWithPlotParameters = mainParameters["folderWithPlotParameters"]
    exportCalculationParameters(mainParameters)

    stadyStateTime = mainParameters["stadyStateDuration"]
    endTime = mainParameters["endTime"] - stadyStateTime
    inputFileName = mainParameters["InputFileName"]


    Modules.Utils.mySettings.printDataToFile =  isOn(mainParameters["printDataToFile"])
    if Modules.Utils.mySettings.printDataToFile:
        print("Ouput data tables to files set On")
    else:
        print("Ouput data tables to files set Off")

    Modules.Utils.mySettings.limitCalculationTime =  isOn(mainParameters["limitCalculationTime"])
    if Modules.Utils.mySettings.limitCalculationTime:
        print("limitCalculationTime set On")
    else:
        print("limitCalculationTime set Off")

    Modules.Utils.mySettings.limitSpaceCalculationTime =  isOn(mainParameters["limitSpaceCalculationTime"])
    if Modules.Utils.mySettings.limitSpaceCalculationTime:
        print("limitSpaceCalculationTime set On")
    else:
        print("limitSpaceCalculationTime set Off")

    Modules.Utils.mySettings.endTime =  endTime

    coreZones = openJSON(mainParameters["inputCoreZones"], folderWithPlotParameters)


    ###########################################
    MyData = DataBase(mainParameters["fuelType"], mainParameters["accident"])
    MyCore = CoreDataModule()
    OverAllData = commonDataModule()
    
    js_sript_files = jsScriptGroups()

    for zone in coreZones:
        newZone = zoneData(zone["id"], zone["plotGroup"], zone["name"], zone["axialCellNumber"], zone["tvsNumber"], zone["tvelNumber"])
        MyCore.addZone(newZone)
        
    #################  Обработка данных заданных модулей  ##########################

    myModule = mainParameters["ModulesData"]["BERKUT"]
    if isOn(myModule["dataProcessing"]):
        BERKUT_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(BERKUT_data["module"], BERKUT_data["title"])
        processingBERKUT(BERKUT_data, coreZones, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, MyCore)
        myOut.printResults()
        js_sript_files.addModule(BERKUT_data["module"])

    myModule = mainParameters["ModulesData"]["BERKUT_N"]
    if isOn(myModule["dataProcessing"]):
        BERKUT_N_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(BERKUT_N_data["module"], BERKUT_N_data["title"])
        processingBERKUT_N(BERKUT_N_data, coreZones, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, MyCore)
        myOut.printResults()
        js_sript_files.addModule(BERKUT_N_data["module"])

    myModule = mainParameters["ModulesData"]["CORE"]
    if isOn(myModule["dataProcessing"]):
        CORE_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(CORE_data["module"], CORE_data["title"])
        processingCORE(CORE_data, coreZones, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, MyCore)

        MyCore.plotCoreDataMap("AxialCoolantTemperatureFluidInZone", myModule["DtPlotSpace"], CORE_data, myOut)
        #MyCore.plotCoreDataMap("AxialCoolantVoidInZone", myModule["DtPlotSpace"], CORE_data, myOut)

        myOut.printResults()
        js_sript_files.addModule(CORE_data["module"])

    myModule = mainParameters["ModulesData"]["DN3D"]
    if isOn(myModule["dataProcessing"]):
        DN3D_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(DN3D_data["module"], DN3D_data["title"])
        processingCOMMON(DN3D_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
        myOut.printResults()
        js_sript_files.addModule(DN3D_data["module"])

    myModule = mainParameters["ModulesData"]["SAFR"]
    if isOn(myModule["dataProcessing"]):

        endTimePlotSAFR = 1.e+30
        
        if Modules.Utils.mySettings.limitSpaceCalculationTime:
            endTimePlotSAFR = Modules.Utils.mySettings.endTime

        SAFR_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(SAFR_data["module"], SAFR_data["title"])
        processingSAFR(SAFR_data, coreZones, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], endTimePlotSAFR, inputFileName, myOut, MyCore)
        if isOn(mainParameters["BERKUT"]["dataProcessing"]):

            BERKUT_data = openJSON(mainParameters["BERKUT"]["jsonFile"], folderWithPlotParameters)

            berkut_data_group = "tvelMaxFuelTemperature"
            safr_data_group = "MaxTemperature_fuel"
            MyCore.plotCombinedMaxTemperatureForTvel(BERKUT_data, berkut_data_group, safr_data_group, myOut)

            berkut_data_group = "TvelMaxCladdingTemperature"
            safr_data_group = "MaxTemperature_structure"
            MyCore.plotCombinedMaxTemperatureForTvel(BERKUT_data, berkut_data_group, safr_data_group, myOut)

        myOut.printResults()
        js_sript_files.addModule(SAFR_data["module"])

    myModule = mainParameters["ModulesData"]["SAFR_CF"]
    if isOn(myModule["dataProcessing"]):
        SAFR_CF_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(SAFR_CF_data["module"], SAFR_CF_data["title"])
        processingSAFR_CF(SAFR_CF_data, coreZones, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut)
        myOut.printResults()
        js_sript_files.addModule(SAFR_CF_data["module"])

    myModule = mainParameters["ModulesData"]["AEROSOL"]
    if isOn(myModule["dataProcessing"]):
        AEROSOL_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        AEROSOL_FPDataBase = openJSON(myModule["jsonFileFPDataBase"], folderWithPlotParameters)
        AEROSOL_ControlVolumes = openJSON(myModule["jsonFileFPControlVolumes"], folderWithPlotParameters)

        myOut = outputs()
        myOut.initModule(AEROSOL_data["module"], AEROSOL_data["title"])
        processingAEROSOL(AEROSOL_data, AEROSOL_FPDataBase, AEROSOL_ControlVolumes, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
        myOut.printResults()
        js_sript_files.addModule(AEROSOL_data["module"])


#################  Обработка данных для заданных групп  ##########################


    for controlGroupName in mainParameters["ControlGroupData"]:
        js_sript_files.addModule(controlGroupName)
        myModule = mainParameters["ControlGroupData"][controlGroupName]
        if isOn(myModule["dataProcessing"]):
            CONTROLGROUP_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
            myOut = outputs()
            myOut.initModule(CONTROLGROUP_data["module"], CONTROLGROUP_data["title"])
            processingCOMMON(CONTROLGROUP_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
            myOut.printResults()
            #js_sript_files.addModule(CONTROLGROUP_data["module"])



#################  Оставил как пример на всякий случай  ##########################
    #myModule = mainParameters["FIRSTLOOP"]
    #if isOn(myModule["dataProcessing"]):
    #    FIRSTLOOP_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
    #    myOut = outputs()
    #    myOut.initModule(FIRSTLOOP_data["module"], FIRSTLOOP_data["title"])
    #    processingCOMMON(FIRSTLOOP_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
    #    myOut.printResults()

    #myModule = mainParameters["SECLOOP"]
    #if isOn(myModule["dataProcessing"]):
    #    SECLOOP_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
    #    myOut = outputs()
    #    myOut.initModule(SECLOOP_data["module"], SECLOOP_data["title"])
    #    processingCOMMON(SECLOOP_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
    #    myOut.printResults()


    #myModule = mainParameters["THIRDLOOP"]
    #if isOn(myModule["dataProcessing"]):
    #    THIRDLOOP_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
    #    myOut = outputs()
    #    myOut.initModule(THIRDLOOP_data["module"], THIRDLOOP_data["title"])
    #    processingCOMMON(THIRDLOOP_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
    #    myOut.printResults()


    #myModule = mainParameters["SAOT"]
    #if isOn(myModule["dataProcessing"]):
    #    SAOT_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
    #    myOut = outputs()
    #    myOut.initModule(SAOT_data["module"], SAOT_data["title"])
    #    processingCOMMON(SAOT_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
    #    myOut.printResults()
 
    #myModule = mainParameters["REACTORSIGNALS"]
    #if isOn(myModule["dataProcessing"]):
    #    REACTORSIGNALS_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
    #    myOut = outputs()
    #    myOut.initModule(REACTORSIGNALS_data["module"], REACTORSIGNALS_data["title"])
    #    processingCOMMON(REACTORSIGNALS_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
    #    myOut.printResults()

    #myModule = mainParameters["COMMONFILES"]
    #if isOn(myModule["dataProcessing"]):
    #    COMMONFILES_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
    #    myOut = outputs()
    #    myOut.initModule(COMMONFILES_data["module"], COMMONFILES_data["title"])
    #    processingCOMMON(COMMONFILES_data, stadyStateTime, myModule["linesPerFigure"], myModule["DtPlotSpace"], myOut, OverAllData)
    #    myOut.printResults()


    myModule = mainParameters["COMBINED"]
    if isOn(myModule["dataProcessing"]):
        COMBINED_data = openJSON(myModule["jsonFile"], folderWithPlotParameters)
        myOut = outputs()
        myOut.initModule(COMBINED_data["module"], COMBINED_data["title"])
        processingCOMBINED(COMBINED_data, myOut, OverAllData)
        myOut.printResults()
        js_sript_files.addModule(COMBINED_data["module"])


    js_sript_files.printJSFiles()