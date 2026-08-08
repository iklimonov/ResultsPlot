import os

from Modules.Utils.utils import convert_file_to_list
from Modules.Utils.utils import prepare_folders
from Modules.Utils.utils import resultsFolder
from Modules.Utils.utils import isTrueFalse
from Modules.Utils.utils import check_SAFR_Tvel_file
from Modules.Utils.utils import check_SAFR_Canister_file
from Modules.Utils.utils import plotResultsFolder

from Modules.processing import processingTimeType
from Modules.processing import processingSpaceType

from Modules.EUCLID.SAFR_heatStruct import heatStruct
from Modules.EUCLID.SAFR_heatStruct import coreMelt
from Modules.EUCLID.SAFR_heatStruct import coreZone
from Modules.EUCLID.SAFR_utils import mapParametersSAFR
from Modules.EUCLID.SAFR_utils import material
from Modules.EUCLID.SAFR_utils import materialCollection

from Modules.DataBase import transientDataSet
from Modules.DataBase import transienSpaceDataSet


def processingSAFR(SAFR_data, coreZones, stadyStateTime, linesPerFigure, DtPlot, TimeToStop, inputFileName, myOut, MyCoreData):
    
    prepare_folders(SAFR_data)
        
    letCalculateTvel = isTrueFalse(SAFR_data["haveTvel"])
    letCalculateCanister = isTrueFalse(SAFR_data["haveCanister"])
    letCalculateDissociation = isTrueFalse(SAFR_data["haveDissociation"])

    canist_name = SAFR_data["canisterName"]

    parametersTvel = mapParametersSAFR(SAFR_data["parametersTvel"]["PixelSizeAxial"],
                                   SAFR_data["parametersTvel"]["PixelSizeRadial"],
                                   SAFR_data["parametersTvel"]["Length"],
                                   SAFR_data["parametersTvel"]["innerRadius"],
                                   SAFR_data["parametersTvel"]["externalRadius"],
                                   SAFR_data["parametersTvel"]["PixelFreeSpaceAxial"],
                                   SAFR_data["parametersTvel"]["PixelFreeSpaceRadial"])

    parametersCanister = mapParametersSAFR(SAFR_data["parametersCanister"]["PixelSizeAxial"],
                                   SAFR_data["parametersCanister"]["PixelSizeRadial"],
                                   SAFR_data["parametersCanister"]["Length"],
                                   SAFR_data["parametersCanister"]["innerRadius"],
                                   SAFR_data["parametersCanister"]["externalRadius"],
                                   SAFR_data["parametersCanister"]["PixelFreeSpaceAxial"],
                                   SAFR_data["parametersCanister"]["PixelFreeSpaceRadial"])

    materials_for_tvel = SAFR_data["materials"]
    materials = materialCollection()
     
    for mat in materials_for_tvel:
        myMat = material(mat["name"], mat["type"], mat["colorSolid"], mat["colorLiquid"])
        materials.add_material(myMat)

    myCore = coreMelt()
    #for resultsGroup in SAFR_data["data"] :
    for zone in coreZones:
        print("Processing " +SAFR_data["module"] + ' ' + zone["name"]) 
        Tvel_is_calculated = check_SAFR_Tvel_file(zone["tvel"]["name"], zone["id"], zone["name"], inputFileName)
        if Tvel_is_calculated and  letCalculateTvel:
            myHS = heatStruct(zone["tvel"]["name"], zone["id"], zone["name"], parametersTvel, materials, inputFileName)
            myHS.readTvel(stadyStateTime, TimeToStop)

            tvel_number_in_zone = zone["tvsNumber"] * zone["tvelNumber"] # вынести количество твэло

            title = SAFR_data["liquidMap"]["graphParameters"]["title"] + " в твэле в зоне " + str(zone["id"])
            group = SAFR_data["liquidMap"]
            path = r'' + plotResultsFolder + '/' + SAFR_data["module"]
            #path = os.path.join(plotResultsFolder, SAFR_data["module"])
            myHS.plot_liquid_map(path, DtPlot, TimeToStop,title, group, myOut)

            title = SAFR_data["temperatureMap"]["graphParameters"]["title"] + " в твэле в зоне " + str(zone["id"])
            group = SAFR_data["temperatureMap"]
            path = r'' + plotResultsFolder + '/' + SAFR_data["module"]
            #path = os.path.join(plotResultsFolder, SAFR_data["module"])
            myHS.plot_temp_map(path, DtPlot, TimeToStop,title, group, myOut)

            myZone = coreZone(zone["name"])

            if letCalculateDissociation:
                haveData = myHS.readDissociationData(stadyStateTime, TimeToStop)
                if haveData:
                    graph_parameters = SAFR_data["DissociationMassUranium"]
                    myHS.PlotUranium(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone)
                    graph_parameters = SAFR_data["DissociationMassPlutonium"]
                    myHS.PlotPlutonium(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone)
                    graph_parameters = SAFR_data["DissociationMassDinitrogen"]
                    myHS.PlotDinitrogen(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone)
                    graph_parameters = SAFR_data["DissociationMassUPuN"]
                    myHS.PlotUPuN(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone)

            graph_parameters = SAFR_data["liquidMass"]
            myHS.plot_mass_liquid(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone, "твэле")
            graph_parameters = SAFR_data["solidMass"]
            myHS.plot_mass_solid(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone, "твэле")
            graph_parameters = SAFR_data["totalMass"]
            myHS.plot_mass_total(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone, "твэле")


            graph_parameters = SAFR_data["maxTemperature"]
            myHS.plot_max_temperature(graph_parameters, myOut, MyCoreData, "твэле")

            myCore.add_zone(myZone)

        Canister_is_calculated = check_SAFR_Canister_file(canist_name, zone["id"], inputFileName)
        if Canister_is_calculated and  letCalculateCanister:
            myHS = heatStruct(canist_name, zone["id"], zone["name"], parametersCanister, materials, inputFileName)
            myHS.readCanister(stadyStateTime, TimeToStop)

            title = SAFR_data["liquidMap"]["graphParameters"]["title"] + " в чехле в зоне " + str(zone["id"])
            group = SAFR_data["liquidMap"]
            path = r'' + SAFR_data["module"]
            myHS.plot_liquid_map(path, DtPlot, TimeToStop,title, group, myOut)

            title = SAFR_data["temperatureMap"]["graphParameters"]["title"] + " в чехле в зоне " + str(zone["id"])
            group = SAFR_data["temperatureMap"]
            path = r'' + SAFR_data["module"]
            myHS.plot_temp_map(path, DtPlot, TimeToStop,title, group, myOut)

            myZone = coreZone(zone["name"])

            tvel_number_in_zone = zone["tvsNumber"] # вынести количество твэло
            graph_parameters = SAFR_data["liquidMass"]
            myHS.plot_mass_liquid(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone, "чехле")
            graph_parameters = SAFR_data["solidMass"]
            myHS.plot_mass_solid(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone, "чехле")
            graph_parameters = SAFR_data["totalMass"]
            myHS.plot_mass_total(graph_parameters, tvel_number_in_zone, myOut, MyCoreData, myZone, "чехле")

            myCore.add_zone(myZone)
        
            graph_parameters = SAFR_data["maxTemperature"]
            myHS.plot_max_temperature(graph_parameters, myOut, MyCoreData, "чехле")


    print("Processing " + "fullLiquidMassCore") 
    graph_parameters = SAFR_data["fullLiquidMassCore"]
    myCore.plotFullMassLiquid(graph_parameters, myOut)

    print("Processing " + "fullSolidMassCore") 
    graph_parameters = SAFR_data["fullSolidMassCore"]
    myCore.plotFullMassSolid(graph_parameters, myOut)

    print("Processing " + "fullMassCore")
    graph_parameters = SAFR_data["fullMassCore"]
    myCore.plotFullMassCore(graph_parameters, myOut)

    if letCalculateDissociation:
        print("Processing " + "FullDissociationMass")
        myCore.plotFullDissociationMass(SAFR_data, myOut)


def processingSAFR_CF(module_data, coreZones, stadyStateTime, linesPerFigure, DtPlot, myOut):
    
    prepare_folders(module_data)

    module_name = module_data["module"]

    for resultsGroup in module_data["data"] :

        resultsGroupName = resultsGroup["name"]
        print("Processing " + module_name + ' ' + resultsGroupName)
        path_to_file = r'' + resultsFolder

        if resultsGroup["dataType"] =="time": # значит имеем только один график от времени
            for zone in coreZones:
                zone_name = zone["name"]
                tvel_materials = zone["tvel"]["MaterialComposition"]
                for mat in tvel_materials:
                    file_name = ''
                    #SAFR_AveTemperature_Zone_114_TVEL_Rods_EK164.dat
                    #object_name = module_name + '_' + resultsGroupName + '_' + zone_name + '_' + zone["tvel"]["name"] + '_' + mat
                    object_name = "SAFR" + '_' + resultsGroupName + '_' + zone_name + '_' + zone["tvel"]["name"] + '_' + mat

                    file_name = object_name + '.dat'
                    dataList = convert_file_to_list(file_name, path_to_file, resultsGroup["HeaderLines"],stadyStateTime,True)
                    data_to_plot = []
                    data_to_plot.append(dataList)
                    data_legends = []
                    data_legends.append(resultsGroup["graphParameters"]["legend"])

                    myData = transientDataSet(module_name, resultsGroupName)
                    processingTimeType(resultsGroup, zone_name, object_name, data_to_plot, data_legends, module_name, myOut, myData, add_to_title = ' Материал: '+mat)


  
        if resultsGroup["dataType"] =="space": # значит имеем только один график от времени

            for zone in coreZones:
                zone_name = zone["name"]
                file_name = ''
                object_name = module_name + '_' + resultsGroupName + '_' + zone_name

                file_name = object_name + '.dat'

                dataList = convert_file_to_list(file_name, path_to_file, resultsGroup["HeaderLines"],stadyStateTime,True)
                lines_per_figure = linesPerFigure
                timeStepPlot = DtPlot
                myData = transienSpaceDataSet(module_name, resultsGroupName)
                processingSpaceType(resultsGroup, zone_name, object_name, dataList, lines_per_figure, timeStepPlot, module_name, zone["tvel"]["grid"], myOut, myData)