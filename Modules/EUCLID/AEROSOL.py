from Modules.Utils.utils import openJSON
from Modules.Utils.utils import unique
from Modules.processing import processingTimeType

import Modules.Utils.mySettings

from Modules.Utils.utils import convert_file_to_list
from Modules.Utils.utils import processFolder
from Modules.Utils.utils import prepare_folders
from Modules.Utils.utils import resultsFolder
from Modules.Utils.utils import plotResultsFolder
from Modules.Utils.utils import get_derivatives

from Modules.DataBase import transientDataSet

import copy

import os          # для работы с операционной системой

from scipy import constants
constants.value(u'Avogadro constant')

N_Avagadro = constants.value(u'Avogadro constant')


class element():
    def __init__(self, name, molarMass, decayconstant, types, plot_group):
        self.name = name
        self.molarMass = molarMass
        self.decayConstant = decayconstant
        self.types = types
        self.plotGroup = plot_group


    def mass_to_activity(self, mass):
        return (N_Avagadro * mass * self.decayConstant ) / self.molarMass

    def activity_to_mass(self, activity):
        return (activity * self.molarMass) / (N_Avagadro * self.decayConstant )

    def get_name(self):
        return self.name

class elementsDataBase():
    def __init__(self):
        self.elements = []
        self.dict_elements = {}

    def readDataBase(self, elements_data):

        for elem in elements_data:
            types_list = list(("".join(elem["Type"].split())).split(','))
            types_list.sort()
            new_elem = element(elem["Name"], elem["MolarMass"], elem["DecayConstant"], types_list, elem["PlotGroup"])
            self.elements.append(new_elem)
            if  self.dict_elements.get(elem["PlotGroup"]) == None:
                 self.dict_elements.update({elem["PlotGroup"]: []})
            fp_list = self.dict_elements.get(elem["PlotGroup"])
            fp_list.append(new_elem)


    def get_element_by_name(self, element_name):

        for elem in elements_data:
            if elem.get_name() == element_name:
                return copy.deepcopy(elem)

        print("Error: Element " + element_name + " not found")
        return None

    def get_elements(self):
        return (self.elements)

class fissionProductState():

    def __init__(self, time, fp_element):
        self.time = time
        self.mass = 0.0
        self.activity = 0.0
        self.myElement = fp_element

    def set_mass(self, new_mass):
        self.mass = new_mass
        self.activity = self.myElement.mass_to_activity(self.mass)

    def set_acitivity(self, new_acitivity):
        self.acitivity = new_acitivity
        self.mass = self.myElement.activity_to_mass(self.acitivity)


    def add_mass(self, added_mass):
        self.mass += added_mass
        self.activity = self.myElement.mass_to_activity(self.mass)

    def add_acitivity(self, added_acitivity):
        self.acitivity += added_acitivity
        self.mass = self.myElement.activity_to_mass(self.acitivity)

    def get_time(self):
        return self.time

    def get_mass(self):
        return self.mass

    def get_activity(self):
        return self.activity

class fissionProduct():
    def __init__(self, fp_element):
        self.myElementName = fp_element.get_name()
        self.myElement = fp_element
        self.myStates = {'Aer':[],'Vap':[],'Dep':[]}

    def add_state(self, type, fp_state):
        self.myStates[type].append(fp_state)

    def get_name(self):
        return self.myElement.get_name()

    def get_data_list_as_mass(self, type):
        dataList = []
        for state in self.myStates[type]:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)

        return dataList

    def get_data_list_as_activity(self, type):
        dataList = []
        for state in self.myStates[type]:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)

        return dataList

class channel():
    def __init__(self, name, cells_number):
        self.name = name
        self.cellsNumber = cells_number

    def get_name(self):
        return self.name

class chamber():
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class controlVolume():

    def __init__(self, name, title, elemntsDataBase):
        self.name = name
        self.title = title
        self.channels = []
        self.chambers = []
        self.fissionProducts = []
        self.fissionProductsAsDict = {}

        for elem in elemntsDataBase.get_elements():
            new_fp = fissionProduct(elem)
            self.fissionProducts.append(new_fp)
            if  self.fissionProductsAsDict.get(elem.plotGroup) == None:
                 self.fissionProductsAsDict.update({elem.plotGroup: []})
            fp_list = self.fissionProductsAsDict.get(elem.plotGroup)
            fp_list.append(new_fp)



    def add_channel(self, channel):
        self.channels.append(channel)

    def add_chamber(self, chamber):
        self.chambers.append(chamber)

    def readFPdata(self, stadyStateTime):

        for fp in self.fissionProducts:

            for type in fp.myElement.types:
                got_first_data = False
                time = []
                value = []

                for chan in self.channels:

                    path_to_file = r'' + resultsFolder
                    file_name = ""

                    if type == "Dep":
                        file_name = chan.get_name() + '_' + fp.get_name() + '_mass_dep_in_gas.out'
                    elif type == "Aer":
                        file_name = chan.get_name() + '_' + fp.get_name() + '_mass_aer_in_gas.out'
                    else:
                        file_name = chan.get_name() + '_' + fp.get_name() + '_mass_vap_in_gas.out'
                    dataList = convert_file_to_list(file_name, path_to_file, 1, stadyStateTime, True)

                    if len(dataList) == 0:
                        continue

                    if got_first_data:

                        if len(time) != len(dataList):
                            print("Different data size for channel " + file_name + " comparing to others in control volume " + self.name + ".\n Lines for channel - " + str(len(dataList)) + " and for other - " + str(len(time)))
                            exit()

                        i = 0
                        while i < len(dataList):
                            #time.append(dataList[i][0])
                            if time[i] != dataList[i][0]:
                                print("Different time value for same data line for channel " + file_name + " comparing to others in control volume " + self.name + ".\n Time for channel - " + str(dataList[i][0]) + " and for other - " + str(len(time[i])))
                                exit()

                            total_value = 0.0
                            for j in range(1,len(dataList[i])):
                                total_value+=dataList[i][j]
                            value[i]+=total_value
                            i+=1
                    else :
                        got_first_data = True
                        i = 0
                        while i < len(dataList):
                            time.append(dataList[i][0])
                            total_value = 0.0
                            for j in range(1,len(dataList[i])):
                                total_value+=dataList[i][j]
                            value.append(total_value)
                            i+=1

                for cham in self.chambers:

                    path_to_file = r'' + resultsFolder
                    file_name = ""
                    if type == "Dep":
                        file_name = cham.get_name() + '_' + fp.get_name() + '_mass_dep_in_gas.out'
                    elif type == "Aer":
                        file_name = cham.get_name() + '_' + fp.get_name() + '_mass_aer_in_gas.out'
                    else:
                        file_name = cham.get_name() + '_' + fp.get_name() + '_mass_vap_in_gas.out'

                    dataList = convert_file_to_list(file_name, path_to_file, 1, stadyStateTime, True)

                    if len(dataList) == 0:
                        continue

                    if got_first_data:
                        if len(time) != len(dataList):
                            print("Different data size for chamber " + file_name + " comparing to others in control volume " + self.name + ".\n Lines for chamber - " + str(len(dataList)) + " and for other - " + str(len(time)))
                            exit()

                        i = 0
                        while i < len(dataList):
                            #time.append(dataList[i][0])

                            if time[i] != dataList[i][0]:
                                print("Different time value for same data line for chamber " + file_name + " comparing to others in control volume " + self.name + ".\n Time for chamber - " + str(dataList[i][0]) + " and for other - " + str(len(time[i])))
                                exit()
                            total_value = 0.0
                            for j in range(1,len(dataList[i])):
                                total_value+=dataList[i][j]
                            value[i]+=total_value
                            i+=1
                    else :
                        got_first_data = True
                        i = 0
                        while i < len(dataList):
                            time.append(dataList[i][0])
                            total_value = 0.0
                            for j in range(1,len(dataList[i])):
                                total_value+=dataList[i][j]
                            value.append(total_value)
                            i+=1

                i = 0
                while i < len(time):
                    new_fp_state = fissionProductState(time[i], fp.myElement)
                    new_fp_state.set_mass(value[i])
                    fp.add_state(type, new_fp_state)
                    i+=1

class totalMassForFP():
    def __init__(self, fp_element):
        self.myElementName = fp_element.get_name()
        self.myElement = fp_element

        self.vaporSource = []
        self.vapor = []
        self.aerosol = []
        self.aerosolSedimentation = []
        self.vaporLoss = []
        self.fluidSource = []
        self.fluid = []
        self.fluidSedimentation = []
        self.fluidLoss = []

        self.fluidCristalization = []
        self.aerosolLoss = []
        self.massInFilter = []
        self.massInFluidFilter = []
        self.bubble = []
        self.bubbleLoss = []


    def readTotalMass(self, stadyStateTime):
            path_to_file = r'' + resultsFolder
            file_name = self.myElementName + '_TotalMass.out'

            dataList = convert_file_to_list(file_name, path_to_file, 1, stadyStateTime, True)

            i = 0
            while i < len(dataList):
                new_vaporSource_state = fissionProductState(dataList[i][0], self.myElement)
                new_vaporSource_state.set_mass(dataList[i][1])
                self.vaporSource.append(new_vaporSource_state)

                new_vapor_state = fissionProductState(dataList[i][0], self.myElement)
                new_vapor_state.set_mass(dataList[i][2])
                self.vapor.append(new_vapor_state)

                new_aerosol_state = fissionProductState(dataList[i][0], self.myElement)
                new_aerosol_state.set_mass(dataList[i][3])
                self.aerosol.append(new_aerosol_state)

                new_aerosolSedimentation_state = fissionProductState(dataList[i][0], self.myElement)
                new_aerosolSedimentation_state.set_mass(dataList[i][4])
                self.aerosolSedimentation.append(new_aerosolSedimentation_state)

                new_vaporLoss_state = fissionProductState(dataList[i][0], self.myElement)
                new_vaporLoss_state.set_mass(dataList[i][5])
                self.vaporLoss.append(new_vaporLoss_state)

                new_fluidSource_state = fissionProductState(dataList[i][0], self.myElement)
                new_fluidSource_state.set_mass(dataList[i][6])
                self.fluidSource.append(new_fluidSource_state)

                new_fluid_state = fissionProductState(dataList[i][0], self.myElement)
                new_fluid_state.set_mass(dataList[i][7])
                self.fluid.append(new_fluid_state)

                new_fluidSedimentation_state = fissionProductState(dataList[i][0], self.myElement)
                new_fluidSedimentation_state.set_mass(dataList[i][8])
                self.fluidSedimentation.append(new_fluidSedimentation_state)

                new_fluidLoss_state = fissionProductState(dataList[i][0], self.myElement)
                new_fluidLoss_state.set_mass(dataList[i][9])
                self.fluidLoss.append(new_fluidLoss_state)

                new_fluidCristalization_state = fissionProductState(dataList[i][0], self.myElement)
                new_fluidCristalization_state.set_mass(dataList[i][10])
                self.fluidCristalization.append(new_fluidCristalization_state)

                new_aerosolLoss_state = fissionProductState(dataList[i][0], self.myElement)
                new_aerosolLoss_state.set_mass(dataList[i][11])
                self.aerosolLoss.append(new_aerosolLoss_state)

                new_massInFilter_state = fissionProductState(dataList[i][0], self.myElement)
                new_massInFilter_state.set_mass(dataList[i][12])
                self.massInFilter.append(new_massInFilter_state)

                new_massInFluidFilter_state = fissionProductState(dataList[i][0], self.myElement)
                new_massInFluidFilter_state.set_mass(dataList[i][13])
                self.massInFluidFilter.append(new_massInFluidFilter_state)

                new_bubble_state = fissionProductState(dataList[i][0], self.myElement)
                new_bubble_state.set_mass(dataList[i][14])
                self.bubble.append(new_bubble_state)

                new_bubbleLoss_state = fissionProductState(dataList[i][0], self.myElement)
                new_bubbleLoss_state.set_mass(dataList[i][15])
                self.bubbleLoss.append(new_bubbleLoss_state)

                i+=1

    ###vaporSource
    def get_vaporSourceData_as_mass(self):
        dataList = []
        for state in self.vaporSource:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_vaporSourceData_as_activity(self):
        dataList = []
        for state in self.vaporSource:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###vapor
    def get_vaporData_as_mass(self):
        dataList = []
        for state in self.vapor:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_vaporData_as_activity(self):
        dataList = []
        for state in self.vapor:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###aerosol
    def get_aerosolData_as_mass(self):
        dataList = []
        for state in self.aerosol:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_aerosolData_as_activity(self):
        dataList = []
        for state in self.aerosol:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###aerosolSedimentation
    def get_aerosolSedimentationData_as_mass(self):
        dataList = []
        for state in self.aerosolSedimentation:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_aerosolSedimentationData_as_activity(self):
        dataList = []
        for state in self.aerosolSedimentation:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###vaporLoss
    def get_vaporLossData_as_mass(self):
        dataList = []
        for state in self.vaporLoss:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_vaporLossData_as_activity(self):
        dataList = []
        for state in self.vaporLoss:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###fluidSource
    def get_fluidSourceData_as_mass(self):
        dataList = []
        for state in self.fluidSource:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_fluidSourceData_as_activity(self):
        dataList = []
        for state in self.fluidSource:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###fluid
    def get_fluidData_as_mass(self):
        dataList = []
        for state in self.fluid:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_fluidData_as_activity(self):
        dataList = []
        for state in self.fluid:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###fluidSedimentation
    def get_fluidSedimentationData_as_mass(self):
        dataList = []
        for state in self.fluidSedimentation:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_fluidSedimentationData_as_activity(self):
        dataList = []
        for state in self.fluidSedimentation:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###fluidLoss
    def get_fluidLossData_as_mass(self):
        dataList = []
        for state in self.fluidLoss:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_fluidLossData_as_activity(self):
        dataList = []
        for state in self.fluidLoss:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList


    ###fluidCristalization
    def get_fluidCristalizationData_as_mass(self):
        dataList = []
        for state in self.fluidCristalization:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_fluidCristalizationData_as_activity(self):
        dataList = []
        for state in self.fluidCristalization:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###aerosolLoss
    def get_aerosolLossData_as_mass(self):
        dataList = []
        for state in self.aerosolLoss:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_aerosolLossData_as_activity(self):
        dataList = []
        for state in self.aerosolLoss:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###massInFilter
    def get_massInFilterData_as_mass(self):
        dataList = []
        for state in self.massInFilter:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_massInFilterData_as_activity(self):
        dataList = []
        for state in self.massInFilter:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###massInFluidFilter
    def get_massInFluidFilterData_as_mass(self):
        dataList = []
        for state in self.massInFluidFilter:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_massInFluidFilterData_as_activity(self):
        dataList = []
        for state in self.massInFluidFilter:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###bubble
    def get_bubbleData_as_mass(self):
        dataList = []
        for state in self.bubble:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_bubbleData_as_activity(self):
        dataList = []
        for state in self.bubble:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList

    ###bubbleLoss
    def get_bubbleLossData_as_mass(self):
        dataList = []
        for state in self.bubbleLoss:
            data = [state.get_time(), state.get_mass()]
            dataList.append(data)
        return dataList

    def get_bubbleLossData_as_activity(self):
        dataList = []
        for state in self.bubbleLoss:
            data = [state.get_time(), state.get_activity()]
            dataList.append(data)
        return dataList



class aerosol():

    def __init__(self, module_name, myElemntsDataBase):
        self.myName = module_name
        self.myElemntsDataBase = myElemntsDataBase
        self.controlVolumes = []
        self.totalMass = []
        self.totalMassAsDict = {}

    def creatControlVolumes(self, myControlVolumesData):

        for cv in myControlVolumesData:
            my_CV = controlVolume(cv["Name"], cv["Title"], self.myElemntsDataBase)
            for chan in cv["Channels"]:
                my_channel = channel(chan["Name"], chan["CellsNumber"])
                my_CV.add_channel(my_channel)

            for cham in cv["Chambers"]:
                my_chamber = chamber(cham["Name"])
                my_CV.add_chamber(my_chamber)
            self.controlVolumes.append(my_CV)

    def readControlVolumes(self, stadyStateTime):

        for cv in self.controlVolumes:
            cv.readFPdata(stadyStateTime)

    def readTotalMassForFP(self, stadyStateTime):

        self.totalMassAsDict.clear()
        for fp in self.myElemntsDataBase.get_elements():
            new_total_mass = totalMassForFP(fp)
            new_total_mass.readTotalMass(stadyStateTime)
            self.totalMass.append(new_total_mass)
            if  self.totalMassAsDict.get(fp.plotGroup) == None:
                 self.totalMassAsDict.update({fp.plotGroup: []})
            fp_list = self.totalMassAsDict.get(fp.plotGroup)
            fp_list.append(new_total_mass)

    def plotControlVolumesForFP(self, AEROSOL_data, myOut, commonDataBase):
        module_name = self.myName

        myDataGroup = [AEROSOL_data["ControlVolumeActivity"]] #[AEROSOL_data["ControlVolumeMass"], AEROSOL_data["ControlVolumeActivity"]]

        fp_type_transform = {'Aer':"Аэрозоли",'Vap':"Пары/Газы",'Dep':"Осаждённые"}


        for myData in myDataGroup:


            for cv in self.controlVolumes:

                resultsGroup = copy.deepcopy(myData)
                figure_title = copy.deepcopy(myData["graphParameters"]["title"])

                print("Processing " + self.myName + ' ' + resultsGroup["name"] + '_' + cv.name)
                
                resultsGroupName = resultsGroup["name"] + '_' + cv.name
                resultsGroup["name"] = resultsGroupName
                resultsGroup["title"] = cv.title + ". " +  resultsGroup["title"]

                subfolder = plotResultsFolder + '/' + module_name + '/' + resultsGroupName
                processFolder(subfolder)




                lines_per_figure = 4 # 0..5 # 0 - одна линия на картинку
                individual = False

                if individual:

                    for type in ["Aer", "Dep", "Vap"]:

                        count = 0
                        fp_count = 0
                        data_to_plot = []
                        data_legends = []

                        object_name = ""

                        for fp in cv.fissionProducts:

                    
                            fucn_name = "get_data_list_as_" + myData["valueType"]
                            #print(fucn_name + " " + fp.myElementName)
                            myFunctionForData = getattr(fissionProduct, fucn_name)
                            dataList = myFunctionForData(fp, type)
                            if len(dataList) == 0:
                                if len(data_to_plot) !=0 and (fp_count == (len(cv.fissionProducts)-1)):
                                    myDataHTML = transientDataSet(module_name, resultsGroupName)
                                    processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                    commonDataBase.addData(myDataHTML,"time")
                                fp_count+=1
                                continue

                            

                            fp_name = fp.myElementName

                            #if fp_name == "NaI131": fp_name = "I131"

                            if count == 0:
                                object_name = resultsFolder + '/' + module_name + '_' + resultsGroupName + '_' + fp_name
                                resultsGroup["graphParameters"]["title"] = figure_title + " " + fp_name
                                data_to_plot = []
                                data_legends = []
                            else:
                                object_name += ', ' + fp_name
                                resultsGroup["graphParameters"]["title"] += ', ' + fp_name
                    
                            data_to_plot.append(dataList)
                    
                            #data_legends.append(resultsGroup["graphParameters"]["legend"])
                            data_legends.append(fp_name)
                            if count == lines_per_figure or (fp_count == (len(cv.fissionProducts)-1)):

                                object_name+= '_' + type
                                resultsGroup["graphParameters"]["title"]+= '( ' + fp_type_transform[type] + ')'

                                myDataHTML = transientDataSet(module_name, resultsGroupName)
                                processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                commonDataBase.addData(myDataHTML,"time")
                            count+=1
                            fp_count+=1
                            if count > lines_per_figure:
                                count = 0
                                object_name = ""
                else:
                    for group in cv.fissionProductsAsDict:

                        for type in ["Aer", "Dep", "Vap"]:
                            count = 0
                            fp_count = 0
                            data_to_plot = []
                            data_legends = []
                            object_name = ""
                            for fp in cv.fissionProductsAsDict[group]:

                    
                                fucn_name = "get_data_list_as_" + myData["valueType"]
                                #print(fucn_name + " " + fp.myElementName)
                                myFunctionForData = getattr(fissionProduct, fucn_name)
                                dataList = myFunctionForData(fp, type)
                                if len(dataList) == 0:
                                    if len(data_to_plot) !=0 and (fp_count == (len(cv.fissionProductsAsDict[group])-1)):
                                        myDataHTML = transientDataSet(module_name, resultsGroupName)
                                        processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                        commonDataBase.addData(myDataHTML,"time")
                                    fp_count+=1
                                    continue

                                

                                fp_name = fp.myElementName

                                #if fp_name == "NaI131": fp_name = "I131"

                                if count == 0:
                                    object_name = module_name + '_' + resultsGroupName + '_' + fp_name
                                    resultsGroup["graphParameters"]["title"] = figure_title + " " + fp_name
                                    data_to_plot = []
                                    data_legends = []
                                else:
                                    object_name += ', ' + fp_name
                                    resultsGroup["graphParameters"]["title"] += ', ' + fp_name
                    
                                data_to_plot.append(dataList)
                                
                                #data_legends.append(resultsGroup["graphParameters"]["legend"])
                                data_legends.append(fp_name)
                                if count == lines_per_figure or (fp_count == (len(cv.fissionProductsAsDict[group])-1)):

                                    object_name+= '_' + type
                                    resultsGroup["graphParameters"]["title"]+= '( ' + fp_type_transform[type] + ')'

                                    myDataHTML = transientDataSet(module_name, resultsGroupName)
                                    processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                    commonDataBase.addData(myDataHTML,"time")
                                count+=1
                                fp_count+=1
                                if count > lines_per_figure:
                                    count = 0
                                    object_name = ""

    def plotControlVolumesForFPasDerivatives(self, AEROSOL_data, myOut, commonDataBase):
        module_name = self.myName

        myDataGroup = [AEROSOL_data["ControlVolumeMass"], AEROSOL_data["ControlVolumeActivity"]]

        for myData in myDataGroup:


            for cv in self.controlVolumes:

                resultsGroup = copy.deepcopy(myData)
                figure_title = copy.deepcopy(myData["graphParameters"]["title"])

                print("Processing derivatives for " + self.myName + ' ' + resultsGroup["name"] + '_' + cv.name)
                
                resultsGroupName = resultsGroup["name"] + '_' + "derivatives" + '_' + cv.name
                resultsGroup["name"] = resultsGroupName
                resultsGroup["title"] = "Производные. " + cv.title + ". " +  resultsGroup["title"]

                subfolder = plotResultsFolder + '/' + module_name + '/' + resultsGroupName
                processFolder(subfolder)


                for fp in cv.fissionProducts:

                    object_name = module_name + '_' + resultsGroupName + '_' + fp.myElementName
                    
                    fucn_name = "get_data_list_as_" + myData["valueType"]
                    #print(fucn_name + " " + fp.myElementName)
                    myFunctionForData = getattr(fissionProduct, fucn_name)
                      
                    resultsGroup["graphParameters"]["title"] = figure_title + " " + fp.myElementName

                    dataList = myFunctionForData(fp)
                    if len(dataList) == 0:
                        continue
                    dataList = get_derivatives(dataList)

                    data_to_plot = []
                    data_to_plot.append(dataList)
                    data_legends = []
                    data_legends.append(resultsGroup["graphParameters"]["legend"])

                    myDataHTML = transientDataSet(module_name, resultsGroupName)
                    processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                    commonDataBase.addData(myDataHTML,"time")
 
    def plotTotalMassForFP(self, AEROSOL_data, myOut, commonDataBase):
        module_name = self.myName

        myDataGroup = [AEROSOL_data["TotalDataActivity"], AEROSOL_data["TotalDataMass"]] #[AEROSOL_data["TotalDataMass"], AEROSOL_data["TotalDataActivity"]]

        for myData in myDataGroup:


            for plotData in AEROSOL_data["totalDataList"]:

                resultsGroup = copy.deepcopy(myData)
                figure_title = copy.deepcopy(myData["graphParameters"]["title"])

                print("Processing " + self.myName + ' ' + resultsGroup["name"] + '_' + plotData["name"])
                
                resultsGroupName = resultsGroup["name"] + '_' + plotData["name"]
                resultsGroup["name"] = resultsGroupName
                resultsGroup["title"] = resultsGroup["title"] + " " +  plotData["title"]

                subfolder = plotResultsFolder + '/' + module_name + '/' + resultsGroupName
                processFolder(subfolder)

                lines_per_figure = 6 # 0..5 # 0 - одна линия на картинку

                individual = False

                if individual:
                    count = 0
                    fp_count = 0
                    data_to_plot = []
                    data_legends = []
                    object_name = ""
                    for fp in self.totalMass:

                        fucn_name = "get_" + plotData["name"] + "Data_as_" + resultsGroup["valueType"]
                        #print(fucn_name + " " + fp.myElementName)
                        myFunctionForData = getattr(totalMassForFP, fucn_name)
                        dataList = myFunctionForData(fp)
                        if len(dataList) == 0:
                            if len(data_to_plot) !=0 and (fp_count == (len(self.totalMass)-1)):
                                myDataHTML = transientDataSet(module_name, resultsGroupName)
                                processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                commonDataBase.addData(myDataHTML,"time")
                            fp_count+=1
                            continue


                        #object_name = module_name + '_' + resultsGroupName + '_' + fp.myElementName
                    
                        #resultsGroup["graphParameters"]["title"] = figure_title + " " + fp.myElementName
                        
                        fp_name = fp.myElementName

                        #if fp_name == "NaI131": fp_name = "I131"

                        if count == 0:
                            object_name = module_name + '_' + resultsGroupName + '_' + fp_name
                            resultsGroup["graphParameters"]["title"] = figure_title + " " + fp_name
                            data_to_plot = []
                            data_legends = []
                        else:
                            object_name += ', ' + fp_name
                            resultsGroup["graphParameters"]["title"] += ', ' + fp_name

                        data_to_plot.append(dataList)
                        #data_legends.append(resultsGroup["graphParameters"]["legend"])

                        data_legends.append(fp_name)
                        if count == lines_per_figure or (fp_count == (len(self.totalMass)-1)):
                            myDataHTML = transientDataSet(module_name, resultsGroupName)
                            processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                            commonDataBase.addData(myDataHTML,"time")
                        count+=1
                        fp_count+=1
                        if count > lines_per_figure:
                            count = 0
                            object_name = ""
                else:
                    for group in self.totalMassAsDict:
                        count = 0
                        fp_count = 0
                        data_to_plot = []
                        data_legends = []
                        object_name = ""
                        for fp in self.totalMassAsDict[group]:

                            fucn_name = "get_" + plotData["name"] + "Data_as_" + resultsGroup["valueType"]
                            #print(fucn_name + " " + fp.myElementName)
                            myFunctionForData = getattr(totalMassForFP, fucn_name)
                            dataList = myFunctionForData(fp)
                            if len(dataList) == 0:
                                if len(data_to_plot) !=0 and (fp_count == (len(self.totalMassAsDict[group])-1)):
                                    myDataHTML = transientDataSet(module_name, resultsGroupName)
                                    processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                    commonDataBase.addData(myDataHTML,"time")
                                fp_count+=1
                                continue


                            #object_name = module_name + '_' + resultsGroupName + '_' + fp.myElementName
                    
                            #resultsGroup["graphParameters"]["title"] = figure_title + " " + fp.myElementName

                            fp_name = fp.myElementName

                            #if fp_name == "NaI131": fp_name = "I131"

                            if count == 0:
                                object_name = module_name + '_' + resultsGroupName + '_' + fp_name
                                resultsGroup["graphParameters"]["title"] = figure_title + " " + fp_name
                                data_to_plot = []
                                data_legends = []
                            else:
                                object_name += ', ' + fp_name
                                resultsGroup["graphParameters"]["title"] += ', ' + fp_name

                            data_to_plot.append(dataList)
                            #data_legends.append(resultsGroup["graphParameters"]["legend"])

                            data_legends.append(fp_name)
                            if count == lines_per_figure or (fp_count == (len(self.totalMassAsDict[group])-1)):
                                myDataHTML = transientDataSet(module_name, resultsGroupName)
                                processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myDataHTML)
                                commonDataBase.addData(myDataHTML,"time")
                            count+=1
                            fp_count+=1
                            if count > lines_per_figure:
                                count = 0
                                object_name = ""


################################################################################################################################################
def processingAEROSOL(AEROSOL_data, AEROSOL_FPDataBase, AEROSOL_ControlVolumes, stadyStateTime, linesPerFigure, DtPlot, myOut, commonDataBase):
   

    module_name = AEROSOL_data["module"]
    print('Processing ' + module_name)
    moduleFolder = os.path.join(plotResultsFolder, module_name)
    processFolder(moduleFolder) #очистили папки с предыдущими графиками
    #prepare_folders(module_name) #очистили папки с предыдущими графиками
    #subfolder = module_name
    #processFolder(subfolder)


    #считали базу со списокм ПД
    print('    Reading FP data base...\n', end ="")
    myElementsDB = elementsDataBase()
    myElementsDB.readDataBase(AEROSOL_FPDataBase)
    print(' ok\n', end ="")

    #создали объёкт и контрольные объёмы
    myAerosol = aerosol(module_name, myElementsDB)
    myAerosol.creatControlVolumes(AEROSOL_ControlVolumes)

    #считали результаты расчёта
    print('    Reading data for control volumes...\n', end ="")
    myAerosol.readControlVolumes(stadyStateTime)
    print(' ok\n', end ="")
    print('    Reading data for total mass...\n', end ="")
    myAerosol.readTotalMassForFP(stadyStateTime)
    print(' ok\n', end ="")


    #закончили считывание
    myAerosol.plotTotalMassForFP(AEROSOL_data, myOut, commonDataBase)
    myAerosol.plotControlVolumesForFP(AEROSOL_data, myOut, commonDataBase)
    #myAerosol.plotControlVolumesForFPasDerivatives(AEROSOL_data, myOut, commonDataBase)


    print("AEROSOL is done")