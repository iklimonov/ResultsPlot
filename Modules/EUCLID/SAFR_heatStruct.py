from Modules.Utils.utils import resultsFolder
from Modules.Utils.utils import unique
from Modules.Utils.utils import get_max_from_data
from Modules.processing import processingTimeType
from Modules.processing import processingSpaceType

import copy

from Modules.DataBase import transientDataSet
from Modules.DataBase import transienSpaceDataSet

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

import os          # для работы с операционной системой

class tableData():
    def __init__(self):
        self.time = []
        self.data = []

    def set_timeTable(self, time):
        self.time = list(time)

    def set_valueTable(self, value):
        self.data = list(value)

    def get_timeTable(self):
         return list(self.time)

    def get_valueTable(self):
        return list(self.data)

class zoneData():
    def __init__(self, mat_name):
        self.mat_name = mat_name
        self.data = tableData()

    def set_data(self, time_list, value_list):
        self.data.set_timeTable(time_list)
        self.data.set_valueTable(value_list)

    def getMatName(self):
        return  self.mat_name

    def get_time(self):
        return self.data.get_timeTable()

    def get_data(self):
        return self.data.get_valueTable()

class coreZone():
    def __init__(self, z_name):
        self.zone_name = z_name
        self.materialsLiquid =[]
        self.materialsSolid =[]
        self.materialsTotal =[]
        self.dataUranium = []
        self.dataPlutonium = []
        self.dataDinitrogen = []
        self.dataUPuN = []

    def mergeZone(self, other_zone):
        if self.zone_name != other_zone.zone_name:
            exit("Can not marge different zones")

        self.materialsLiquid = self.materialsLiquid + other_zone.materialsLiquid
        self.materialsSolid = self.materialsSolid + other_zone.materialsSolid
        self.materialsTotal = self.materialsTotal + other_zone.materialsTotal
        self.dataUranium = self.dataUranium + other_zone.dataUranium
        self.dataPlutonium = self.dataPlutonium + other_zone.dataPlutonium
        self.dataDinitrogen = self.dataDinitrogen + other_zone.dataDinitrogen
        self.dataUPuN = self.dataUPuN + other_zone.dataUPuN

    def get_materialsLiquid(self):
        return self.materialsLiquid

    def get_materialsSolid(self):
        return self.materialsSolid

    def get_materialsTotal(self):
        return self.materialsTotal

    def get_dataUranium(self):
        return self.dataUranium

    def get_dataPlutonium(self):
        return self.dataPlutonium

    def get_dataDinitrogen(self):
        return self.dataDinitrogen

    def get_dataUPuN(self):
        return self.dataUPuN

    def add_materialDataForLiquid(self, matname, dataList):
         mat = zoneData(matname)
         time_list = []
         value_list = []

         for line in dataList:
             time_list.append(line[0])
             value_list.append(line[1])

         mat.set_data(time_list, value_list)
         self.materialsLiquid.append(mat)

    def add_materialDataForSolid(self, matname, dataList):
         mat = zoneData(matname)
         time_list = []
         value_list = []

         for line in dataList:
             time_list.append(line[0])
             value_list.append(line[1])

         mat.set_data(time_list, value_list)
         self.materialsSolid.append(mat)

    def add_materialDataForTotalMass(self, matname, dataList):
         mat = zoneData(matname)
         time_list = []
         value_list = []

         for line in dataList:
             time_list.append(line[0])
             value_list.append(line[1])

         mat.set_data(time_list, value_list)
         self.materialsTotal.append(mat)

    def add_DataDissociation(self, matname, dataList):
        mat = zoneData(matname)
        time_list = []
        value_list = []

        for line in dataList:
            time_list.append(line[0])
            value_list.append(line[1])

        mat.set_data(time_list, value_list)

        if matname == "Uranium":
            self.dataUranium.append(mat)
        if matname == "Plutonium":
            self.dataPlutonium.append(mat)
        if matname == "Dinitrogen":
            self.dataDinitrogen.append(mat)
        if matname == "UPuN":
            self.dataUPuN.append(mat)



class coreMelt():
    zones = []
    materialNames = []

    def __init__(self):
        self.zones = []
        self.materialNames = []

    def add_zone(self, zone):
        have_same_zone = False
        index = 0
        while index < len(self.zones):
            if self.zones[index].zone_name == zone.zone_name:
                have_same_zone = True
                break
            index+=1
        if not have_same_zone:
            self.zones.append(zone)
        else:
            self.zones[index].mergeZone(zone)

        #self.zones.append(zone)
        zone_matLiq = list(zone.get_materialsLiquid())
        for mat in zone_matLiq:
             self.materialNames.append(mat.getMatName())

        zone_matSol = list(zone.get_materialsSolid())
        for mat in zone_matSol:
             self.materialNames.append(mat.getMatName())
        
        self.materialNames = unique(self.materialNames) ## оставляем только уникальные имена

    def plotFullMassLiquid(self, graph_parameters, myOut):

        ######################################
        def getMassTableForMaterial(mat_name):
            ###################################
            def check_timeTable(tt1, tt2):
                if len(tt1) != len(tt2):
                    return False
                i = 0
                while i < len(tt1):
                    dif = abs(tt1[i] - tt2[i])
                    if dif != 0.0 :
                        return False
                    i+=1
                return True
            ###################################
            def summ_data(datT1, datT2):
                if len(datT1) != len(datT2):
                    print("ERROR: SAFR. Different data tables")
                    return
                i = 0
                while i < len(datT1):
                    datT1[i] += datT2[i]
                    i+=1
            ###################################

            time_table_all = []
            for zone in self.zones :
                zone_mats = zone.get_materialsLiquid()
                for mat in zone_mats:
                    if mat.getMatName() == mat_name:
                        time_table_all = list(set(time_table_all + mat.get_time()))
            time_table = [float(x) for x in time_table_all]
            time_table.sort()
            data_table = [0] * len(time_table)

            for zone in self.zones:
                zone_mats = zone.get_materialsLiquid()
                for mat in zone_mats:
                    if mat.getMatName() == mat_name:
                        index_local = 0
                        for time in mat.get_time():
                            index_global = time_table.index(time)
                            data_table[index_global] += mat.get_data()[index_local]
                            index_local+=1

            datalist =[]
            i = 0
            while i < len(time_table):
                line = []
                line.append(time_table[i])
                line.append(data_table[i])
                datalist.append(line)
                i+=1
            return datalist
        ######################################

        for matName in self.materialNames:
            object_name = 'full_mass_liquid' + '_' + matName
            my_str = ' для материала ' + matName

            dataList = getMassTableForMaterial(matName)
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])

            myData = transientDataSet("SAFR", graph_parameters["name"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)

    def plotFullMassSolid(self, graph_parameters, myOut):

        ######################################
        def getMassTableForMaterial(mat_name):
            ###################################
            def check_timeTable(tt1, tt2):
                if len(tt1) != len(tt2):
                    return False
                i = 0
                while i < len(tt1):
                    dif = abs(tt1[i] - tt2[i])
                    if dif != 0.0 :
                        return False
                    i+=1
                return True
            ###################################
            def summ_data(datT1, datT2):
                if len(datT1) != len(datT2):
                    print("ERROR: SAFR. Different data tables")
                    return
                i = 0
                while i < len(datT1):
                    datT1[i] += datT2[i]
                    i+=1
            ###################################

            time_table_all = []
            for zone in self.zones :
                zone_mats = zone.get_materialsSolid()
                for mat in zone_mats:
                    if mat.getMatName() == mat_name:
                        time_table_all = list(set(time_table_all + mat.get_time()))
            time_table = [float(x) for x in time_table_all]
            time_table.sort()
            data_table = [0] * len(time_table)

            for zone in self.zones:
                zone_mats = zone.get_materialsSolid()
                for mat in zone_mats:
                    if mat.getMatName() == mat_name:
                        index_local = 0
                        for time in mat.get_time():
                            index_global = time_table.index(time)
                            data_table[index_global] += mat.get_data()[index_local]
                            index_local+=1

            datalist =[]
            i = 0
            while i < len(time_table):
                line = []
                line.append(time_table[i])
                line.append(data_table[i])
                datalist.append(line)
                i+=1
            return datalist
        ######################################

        for matName in self.materialNames:
            object_name = 'full_mass_solid' + '_' + matName

            dataList = getMassTableForMaterial(matName)

            my_str = ' для материала ' + matName
            myData = transientDataSet("SAFR", graph_parameters["name"])
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)


    def plotFullMassCore(self, graph_parameters, myOut):

        ######################################
        def getMassTableForMaterial(mat_name):
            ###################################
            def check_timeTable(tt1, tt2):
                if len(tt1) != len(tt2):
                    return False
                i = 0
                while i < len(tt1):
                    dif = abs(tt1[i] - tt2[i])
                    if dif != 0.0 :
                        return False
                    i+=1
                return True
            ###################################
            def summ_data(datT1, datT2):
                if len(datT1) != len(datT2):
                    print("ERROR: SAFR. Different data tables")
                    return
                i = 0
                while i < len(datT1):
                    datT1[i] += datT2[i]
                    i+=1
            ###################################

            time_table_all = []
            for zone in self.zones :
                zone_mats = zone.get_materialsTotal()
                for mat in zone_mats:
                    if mat.getMatName() == mat_name:
                        time_table_all = list(set(time_table_all + mat.get_time()))
            time_table = [float(x) for x in time_table_all]
            time_table.sort()
            data_table = [0] * len(time_table)

            for zone in self.zones:
                zone_mats = zone.get_materialsTotal()
                for mat in zone_mats:
                    if mat.getMatName() == mat_name:
                        index_local = 0
                        for time in mat.get_time():
                            index_global = time_table.index(time)
                            data_table[index_global] += mat.get_data()[index_local]
                            index_local+=1

            datalist =[]
            i = 0
            while i < len(time_table):
                line = []
                line.append(time_table[i])
                line.append(data_table[i])
                datalist.append(line)
                i+=1
            return datalist
        ######################################

        for matName in self.materialNames:
            object_name = 'full_mass_core' + '_' + matName

            dataList = getMassTableForMaterial(matName)

            my_str = ' для материала ' + matName
            myData = transientDataSet("SAFR", graph_parameters["name"])
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)

    def plotFullDissociationMass(self, SAFR_Data, myOut):

        ######################################
        def getMassTableForMaterial(mat_name):
            ###################################
            def check_timeTable(tt1, tt2):
                if len(tt1) != len(tt2):
                    return False
                i = 0
                while i < len(tt1):
                    dif = abs(tt1[i] - tt2[i])
                    if dif != 0.0 :
                        return False
                    i+=1
                return True
            ###################################
            def merge_two_data_set(time_main, time_two, data_main, data_two):
                #поскольку расчёт в SAFR передаётся в разные моменты, то к длинному массиву прибавляем короткий
                #предполагается, что временые точки с какого то момента совпадают
                #найдём момент совпадения и с него сложим данные

                if len(time_main) > len(time_two):
                    new_time_table = list(time_main)
                    new_data_table = list(data_main)
                    index = 0
                    for i in range(len(time_main)):
                        if abs(time_main[i] - time_two[0]) < 1.e-13:
                            index = i
                            break
                    i = 0
                    while index < len(time_main):
                        new_data_table[index]+=data_two[i]
                        index+=1
                        i+=1

                    return [new_time_table, new_data_table]

                else:
                    new_time_table = list(time_two)
                    new_data_table = list(data_two)
                    index = 0
                    for i in range(len(time_two)):
                        if abs(time_two[i] - time_main[0]) < 1.e-13:
                            index = i
                            break
                    i = 0
                    while index < len(time_two):
                        new_data_table[index]+=data_main[i]
                        index+=1
                        i+=1

                    return [new_time_table, new_data_table]


            ###################################
            def summ_data(datT1, datT2):
                if len(datT1) != len(datT2):
                    print("ERROR: SAFR. Different data tables")
                    return
                i = 0
                while i < len(datT1):
                    datT1[i] += datT2[i]
                    i+=1
            ###################################

            time_table = []
            data_table = []

            start = True
            for zone in self.zones :
                zone_mats = []
                if mat_name == "Uranium":
                    zone_mats = zone.get_dataUranium()
                if mat_name == "Plutonium":
                    zone_mats = zone.get_dataPlutonium()
                if mat_name == "Dinitrogen":
                    zone_mats = zone.get_dataDinitrogen()
                if mat_name == "UPuN":
                    zone_mats = zone.get_dataUPuN()

                for dat in zone_mats:
                    if dat.getMatName() == mat_name:
                        if start:
                            time_table = list(dat.get_time())
                            data_table = list(dat.get_data())
                            start = False
                        else:
                            if check_timeTable(time_table, dat.get_time()):
                                data_d = dat.get_data()
                                summ_data(data_table, data_d)
                            else:
                                results = merge_two_data_set(time_table, dat.get_time(), data_table, dat.get_data())
                                time_table = list(results[0])
                                data_table = list(results[1])

                                #print("ERROR: SAFR. Different time tables")
                                #return 
            datalist =[]
            i = 0
            while i < len(time_table):
                line = []
                line.append(time_table[i])
                line.append(data_table[i])
                datalist.append(line)
                i+=1
            return datalist
        ######################################

        
        module_name = "SAFR"

        dissMaterials = ["Uranium", "Plutonium", "Dinitrogen", "UPuN"]

        for matName in dissMaterials:
            graph_parameters = copy.copy(SAFR_Data["DissociationMass" + matName])
            graph_parameters["name"] = "FullDissociationMass"
            graph_parameters["title"] = "Изменение массы материалов при диссоциации"
            object_name = 'full_diss_mass' + '_' + matName
            my_str = ". " + matName

            dataList = getMassTableForMaterial(matName)
            if len(dataList)==0:
                kgdf+=1
            max_data = get_max_from_data(dataList)

            useYSci = False
            if max_data < graph_parameters["graphParameters"]["criteriaForAxSciFormat"]:
                useYSci = True
            
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])

            myData = transientDataSet(module_name, graph_parameters["name"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, module_name, myOut, myData, add_to_title = my_str, useySciFormat = useYSci)


class cell():
    #material_name, volume, liquid_fraction, up, down, inner, external, mass, temperature
    def __init__(self, material_name, volume, liquid_fraction, up, down, inner, external, mass, temperature):
        self.material_name = material_name
        self.volume = volume
        self.liquid_fraction = liquid_fraction
        self.up = up
        self.down = down
        self.inner = inner
        self.external = external
        self.mass = mass
        self.temperature = temperature

    def get_name(self):
        return self.material_name

    def get_volume(self):
        return self.volume

    def get_liquidFraction(self):
        return self.liquid_fraction

    def get_up(self):
        return self.up

    def get_down(self):
        return self.down

    def get_inner(self):
        return self.inner

    def get_external(self):
        return self.external

    def get_mass(self):
        return self.mass

    def get_mass_solid(self):
        return self.mass * (1.0 - self.liquid_fraction)

    def get_mass_liquid(self):
        return self.mass * self.liquid_fraction

    def get_temperature(self):
        return self.temperature

class heatStructState():
    def __init__(self, time):
        self.time = time
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def get_time(self):
        return self.time

    def get_mass(self, mat_name):
        mass = 0.0
        for cell in self.cells:
            if cell.get_name() == mat_name :
                mass += cell.get_mass()
        return mass

    def get_mass_solid(self, mat_name):
        mass = 0.0
        for cell in self.cells:
            if cell.get_name() == mat_name :
                mass += cell.get_mass_solid()
        return mass

    def get_mass_liquid(self, mat_name):
        mass = 0.0
        for cell in self.cells:
            if cell.get_name() == mat_name :
                mass += cell.get_mass_liquid()
        return mass

    def get_max_temperature_for_mat(self, mat_name):
        temp = 0.0
        for cell in self.cells:
            if cell.get_name() == mat_name :
                temp = max(temp, cell.get_temperature())
        return temp

    def get_min_temperature(self):
        minimum = 100000.0 # ну больше уже не должно же быть
        for cell in self.cells:
            minimum = min(minimum, cell.get_temperature())
        return minimum

    def get_max_temperature(self):
        maximum = -100000.0 # ну меньше уже не должно же быть
        for cell in self.cells:
            maximum = max(maximum, cell.get_temperature())
        return maximum

    def get_min_temperature_for_material(self, mat_name):
        minimum = 100000.0 # ну больше уже не должно же быть
        for cell in self.cells:
            if cell.get_name() == mat_name :
                minimum = min(minimum, cell.get_temperature())
        return minimum

    def get_max_temperature_for_material(self, mat_name):
        maximum = -100000.0 # ну меньше уже не должно же быть
        for cell in self.cells:
            if cell.get_name() == mat_name :
                maximum = max(maximum, cell.get_temperature())
        return maximum

    def drow_liq_state(self, parameters, materials_collection, file_name, title, group, myOut):
        #parameters[0] -  parameters.axial_length
        #parameters[1] -  parameters.size_radial
        #parameters[2] -  parameters.size_axial
        #parameters[3] -  parameters.radial_ratio
        #parameters[4] -  parameters.axial_ratio
        #parameters[5] -  parameters.inner_radius
        #0 - material_name
        #1 - volume
        #2 - liquid_fraction
        #3 - up
        #4 - down
        #5 - inner
        #6 - external
        #7 - mass
        #8 - temperature

        size = (parameters.size_radial, parameters.size_axial)#800,457
        legend_size = 250 
        color = (255, 255, 255)
        font = ImageFont.truetype("arial.ttf", 20)
        fontMat = ImageFont.truetype("arial.ttf", 16)
        img = Image.new('RGB', size, "white")
        imgDrawer = ImageDraw.Draw(img)

        usedMatInHS = []

        for cell in self.cells :
            #cell.get_name()
            mat_cell = materials_collection.get_material_by_name(cell.get_name())
            
            usedMatInHS.append(mat_cell)

            usedMatInHS = unique(usedMatInHS)
            
            x0=int(((parameters.axial_length-cell.get_up())*parameters.axial_ratio)//1)
            y0=int(((cell.get_inner()-parameters.inner_radius)*parameters.radial_ratio)//1)
            x1=int(((parameters.axial_length-cell.get_down())*parameters.axial_ratio)//1)
            y1=int(((cell.get_external()-parameters.inner_radius)*parameters.radial_ratio)//1)

            cell_color = mat_cell.get_color_solid()
            if float(cell.get_liquidFraction()) >0.0000001 :
                cell_color = mat_cell.get_color_liquid()
            else : 
                cell_color = mat_cell.get_color_solid()
            imgDrawer.rectangle((y0,x0,y1,x1), fill=cell_color, outline="black")

        imgDrawer.line((parameters.size_radial-250+50, 0,parameters.size_radial-legend_size+50,parameters.size_axial), fill="black")

        # делаем подпись для линейки
        img = img.rotate(-90, expand=1)
        imgDrawer = ImageDraw.Draw(img)
        imgDrawer.text(( parameters.size_axial // 2 - 47, parameters.size_radial-250+50+5 ), 'Высота, м','black',font=font)
        img = img.rotate(90, expand=1)
        imgDrawer = ImageDraw.Draw(img)


        mat_count = len(usedMatInHS)
        mat_block_axial_size = 3 * 40 * mat_count
        mat_block_radial_size = 80
        
        start_point_of_axial_block = (parameters.size_axial - mat_block_axial_size) // 2
        start_point_of_radial_block = parameters.size_radial - legend_size + 110

        imgDrawer.text(( start_point_of_radial_block, start_point_of_axial_block + 40 ), 'Время:','black',font=font)
        imgDrawer.text(( start_point_of_radial_block + 70, start_point_of_axial_block + 40 ), str(round(self.time,4)),'black',font=font)


        w_start = start_point_of_axial_block + 80
        w_step = 30
        i = 0
        for mat in usedMatInHS: #materials_collection.get_materials():
            if mat.get_type()=="gas":
                imgDrawer.text(( start_point_of_radial_block,w_start + i*w_step),mat.get_name()+':' ,'black',font=font)

                imgDrawer.rectangle((start_point_of_radial_block,w_start + (i+1)*w_step,start_point_of_radial_block+20,w_start + (i+1)*w_step + 20), fill=mat.get_color_solid(), outline="black")
                imgDrawer.text(( start_point_of_radial_block+30,w_start + (i+1)*w_step),"Газовая фаза" ,'black',font=fontMat)
                i+=2
            else:
                imgDrawer.text(( start_point_of_radial_block,w_start + i*w_step),mat.get_name()+':' ,'black',font=font)

                imgDrawer.rectangle((start_point_of_radial_block,w_start + (i+1)*w_step,start_point_of_radial_block+20,w_start + (i+1)*w_step + 20), fill=mat.get_color_solid(), outline="black")
                imgDrawer.text(( start_point_of_radial_block+30,w_start + (i+1)*w_step),"Твёрдая фаза" ,'black',font=fontMat)

                imgDrawer.rectangle((start_point_of_radial_block,w_start + (i+2)*w_step,start_point_of_radial_block+20,w_start + (i+2)*w_step + 20), fill=mat.get_color_liquid(), outline="black")
                imgDrawer.text(( start_point_of_radial_block+30,w_start + (i+2)*w_step),"Жидкая фаза" ,'black',font=fontMat)
                i+=3


        mesh_points = 20
        mesh_start = 0.0
        mesh_step_coordinate = parameters.axial_length / (mesh_points*1.0)
        mesh_step_points = parameters.size_axial // mesh_points
        
        for i in range(mesh_points+1):
            imgDrawer.line((parameters.size_radial-legend_size + 30, parameters.size_axial - mesh_step_points*i,parameters.size_radial-legend_size + 50,parameters.size_axial - mesh_step_points*i), fill="black")
            text = "{value:.2f}".format(value = mesh_start + mesh_step_coordinate * i)
            imgDrawer.text(( parameters.size_radial-legend_size + 2, parameters.size_axial - 2 - mesh_step_points*i ), text,'black',font=font)

        #name_of_pic = r'pictures_liquid_map_'+ hst +'/liq_map'+str(round(current_time,4)*10000)+'.png'
        sec = str(int(self.time // 1))
        msec = str(round(self.time,4) % 1)
        msec = msec[2:5]
        name_of_pic = file_name + '_time_step_' + sec +'s' + msec +'.png'
        img.save(name_of_pic)
        title += ' в ' + sec +'.' + msec + ' секунду'
        myOut.addFigure("SAFR", group["name"], group["title"], name_of_pic, title)

    def drow_temp_state(self, parameters, materials_collection, file_name, title, group, myOut):
        #----------------------------------------------
        def get_color(temp_min, temp_max, temp):
            fraction = 0.0
            if ((temp_max-temp_min)<1.0e-9):
                fraction = 1.0
            else:
                fraction = 1.0 - (temp - temp_min) / (temp_max - temp_min)
            if (fraction <= 0.25):
                color_fraction = fraction/0.25
                return (255,int(255*color_fraction),0)
            if (fraction <= 0.5 and fraction > 0.25):
                color_fraction = (fraction-0.25)/0.25
                return (255,255,int(255*color_fraction))
            if (fraction <= 0.75 and fraction > 0.5):
                color_fraction = (fraction-0.5)/0.25
                return (int(255*(1.0-color_fraction)),255,255)
            if (fraction > 0.75):
                color_fraction = (fraction-0.75)/0.25
                return (0,int(255*(1.0-color_fraction)),255)
                drow = 0
        #----------------------------------------------
        def draw_temp_plate(imgDrawer,pixels_axial,pixels_radial_mid,temp_min,temp_max,number_of_squares):
            size_of_square = 20
            temp_step = (temp_max - temp_min)/(number_of_squares-1)
            start = int(pixels_axial*0.5)-size_of_square*int(number_of_squares*0.5)
            font = ImageFont.truetype("arial.ttf", 15)
            i = 0
            while (i<number_of_squares):
                color = get_color(temp_min,temp_max,float(temp_min+i*temp_step))
                imgDrawer.rectangle((pixels_radial_mid-int(size_of_square*0.5),start+i*size_of_square,pixels_radial_mid+int(size_of_square*0.5),start+(i+1)*size_of_square), fill=color, outline=color)
                imgDrawer.text(( pixels_radial_mid+size_of_square,start+i*size_of_square + int(size_of_square*0.25)), str(int(temp_min+i*temp_step)),'black',font)
                i = i+1
        #----------------------------------------------
        #parameters[0] -  parameters.axial_length
        #parameters[1] -  parameters.size_radial
        #parameters[2] -  parameters.size_axial
        #parameters[3] -  parameters.radial_ratio
        #parameters[4] -  parameters.axial_ratio
        #parameters[5] -  parameters.inner_radius
        #0 - material_name
        #1 - volume
        #2 - liquid_fraction
        #3 - up
        #4 - down
        #5 - inner
        #6 - external
        #7 - mass
        #8 - temperature

        size = (parameters.size_radial+100, parameters.size_axial)#800,457
        color = (255, 255, 255)
        font = ImageFont.truetype("arial.ttf", 20)
        img = Image.new('RGB', size, "white")
        imgDrawer = ImageDraw.Draw(img)
        min_temp = self.get_min_temperature()
        max_temp = self.get_max_temperature()

        usedMatInHS = []

        for cell in self.cells :
            #cell.get_name()
            
            x0=int(((parameters.axial_length-cell.get_up())*parameters.axial_ratio)//1)
            y0=int(((cell.get_inner()-parameters.inner_radius)*parameters.radial_ratio)//1)
            x1=int(((parameters.axial_length-cell.get_down())*parameters.axial_ratio)//1)
            y1=int(((cell.get_external()-parameters.inner_radius)*parameters.radial_ratio)//1)

            color_cell = get_color(min_temp, max_temp, cell.get_temperature())
            imgDrawer.rectangle((y0,x0,y1,x1), fill=color_cell, outline="black")

            mat_cell = materials_collection.get_material_by_name(cell.get_name())
            
            usedMatInHS.append(mat_cell)

            usedMatInHS = unique(usedMatInHS)



        draw_temp_plate(imgDrawer,parameters.size_axial,parameters.size_radial + 100 - 75,min_temp,max_temp,20)

        imgDrawer.rectangle((0, parameters.size_axial-42,parameters.size_radial,parameters.size_axial), fill="white", outline="white")
        imgDrawer.text(( 20, parameters.size_axial-30 ), 'Время:','black',font=font)
        imgDrawer.text(( 90, parameters.size_axial-30 ), str(round(self.time,4)),'black',font=font)

        w_start=190
        w_step=120
        i = 0
        for mat in usedMatInHS: #materials_collection.get_materials():
            imgDrawer.rectangle((w_start+w_step*i,parameters.size_axial-31,w_start+w_step*i+20,parameters.size_axial-11), fill=mat.get_color_solid(), outline="black")
            imgDrawer.text(( w_start+30+w_step*i,parameters.size_axial-30 ),mat.get_name() ,'black',font=font)
            i+=1
        #name_of_pic = r'pictures_liquid_map_'+ hst +'/liq_map'+str(round(current_time,4)*10000)+'.png'
        sec = str(int(self.time // 1))
        msec = str(round(self.time,4) % 1)
        msec = msec[2:5]
        name_of_pic = file_name + '_time_step_' + sec +'s' + msec +'.png'
        img.save(name_of_pic)
        title += ' в ' + sec +'.' + msec + ' секунду'
        myOut.addFigure("SAFR",group["name"], group["title"], name_of_pic, title)

class dissociationLayer():
    #total_mass_U, total_mass_Pu, total_mass_N2, total_mass_UPuN
    def __init__(self, coordinate, massUranium, massPlutonium, massNitrogen, massUPuN):
        self.coordinate = coordinate
        self.mUranium = massUranium
        self.mPlutonium = massPlutonium
        self.Dinitrogen = massNitrogen
        self.mUPuN = massUPuN

    def get_coordinate(self):
        return self.coordinate

    def get_massUranium(self):
        return self.mUranium

    def get_massPlutonium(self):
        return self.mPlutonium

    def get_massDinitrogen(self):
        return self.Dinitrogen

    def get_massUPuN(self):
        return self.mUPuN

class heatStructDissociationState():
    def __init__(self, time):
        self.time = time
        self.layers = []

    def addLayer(self, new_layer):
        have_same_layer = False

        for layer in self.layers:
            if layer.get_coordinate() == new_layer.get_coordinate():
                have_same_layer = True

        if not have_same_layer:
            self.layers.append(new_layer)
        else:
            print("ERROR: Error reading dissociation data. Layer with coordinate " + str(new_layer.get_coordinate()) + " alredy exist\n")

    def get_time(self):
        return self.time

    def get_massUranium(self):
        total_mass = 0.0

        for layer in self.layers:
            total_mass+=layer.get_massUranium()

        return total_mass

    def get_massPlutonium(self):
        total_mass = 0.0

        for layer in self.layers:
            total_mass+=layer.get_massPlutonium()

        return total_mass

    def get_massDinitrogen(self):
        total_mass = 0.0

        for layer in self.layers:
            total_mass+=layer.get_massDinitrogen()

        return total_mass

    def get_massUPuN(self):
        total_mass = 0.0

        for layer in self.layers:
            total_mass+=layer.get_massUPuN()

        return total_mass


class heatStruct():
    def __init__(self, hs_name, zone_id, zone_name, parameters, materials, input_file_name):
        self.hs_name = hs_name
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.parameters = parameters
        self.materials = copy.copy(materials)
        self.input_file_name = input_file_name
        self.time_states = []
        self.dissociation_time_states = []
        self.initial_UPuN_mass = 0.0

    def __readFile(self, file_path, stadyStateTime, TimeToStop):
        if os.path.exists(file_path): 
            filein = open(file_path, "r")      
        else: 
            print("ERROR: no file ",file_path)
        if filein == None:
            print("ERROR: can not open file ",file_path)
            return

        file_data = []
        for line in filein:
            line = line.strip()
            file_data.append(line)
        i = 0
        block_start = 'Time:'
        line_start = 'Axial line:'

        usedMaterials = []

        while i < len(file_data):
            line_data = file_data[i].split(",")
            if line_data[0] == block_start :
                current_time = float(line_data[1]) - stadyStateTime
                if current_time < 0.0  or current_time > TimeToStop:
                    i = i+1
                    continue
                hs_state = heatStructState(current_time)
                #init heatstructState
                i+=1

                while i < len(file_data):
                    line_data = file_data[i].split(",")
                    if line_data[0] == line_start :
                        i = i+1
                        continue
                    else:
                        if line_data[0] == block_start :
                            break
                        else:
                            material_name = line_data[0]
                            volume = float(line_data[1])
                            liquid_fraction = float(line_data[2])
                            up = float(line_data[3])
                            down = float(line_data[4])
                            inner = float(line_data[5])
                            external = float(line_data[6])
                            mass = float(line_data[7])
                            temperature = float(line_data[8])
                            #init cell
                            #material_name, volume, liquid_fraction, up, down, inner, external, mass, temperature
                            new_cell = cell(material_name, volume, liquid_fraction, up, down, inner, external, mass, temperature)
                            hs_state.add_cell(new_cell)

                            usedMaterials.append(material_name)
                            usedMaterials = unique(usedMaterials)

                    i = i+ 1
                self.time_states.append(hs_state)
            else :
                i = i + 1

        self.materials.delete_unused_materials(usedMaterials)

    def readTvel(self, stadyStateTime, TimeToStop):
        #BN1200_SNUP_boec_utop _ 141 _ Zone_141 _ TVEL_Rods _cell_information.csv
        file_path = r'' + resultsFolder + '/' + self.input_file_name + '_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name + '_cell_information.csv'
        self.__readFile(file_path, stadyStateTime, TimeToStop)

    def readCanister(self, stadyStateTime, TimeToStop):
        #BN1200_SNUP_boec_utop _ 141 _ Zone_141 _ TVEL_Rods _cell_information.csv
        file_path = r'' + resultsFolder + '/' + self.input_file_name + '_' + self.hs_name + '_' + str(self.zone_id) + '_cell_information.csv'
        self.__readFile(file_path, stadyStateTime, TimeToStop)

    def readDissociationData(self, stadyStateTime, TimeToStop):
        #BN1200_full_utop _ 141 _ Zone_141 _ TVEL_Rods _total_mass_flows
        file_path = r'' + resultsFolder + '/' + self.input_file_name + '_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name + '_total_mass_flows.csv'

        if os.path.exists(file_path): 
            filein = open(file_path, "r")      
        else: 
            print("ERROR: no file ",file_path)
        if filein == None:
            print("ERROR: can not open file ",file_path)
            return

        file_data = []
        for line in filein:
            line = line.strip()
            file_data.append(line)
        i = 0
        block_start = "=============================================================================================================="
        data_start = "Axial coordinate:"

        while i < len(file_data):
            line_data = file_data[i].split(",")
            str_len = len(line_data)
            if str_len > 1 and line_data[2] == data_start :
                current_time = float(line_data[0]) - stadyStateTime
                if current_time < 0.0 or current_time > TimeToStop:
                    i = i+1
                    continue
                hs_D_state = heatStructDissociationState(current_time)
                #init heatstructState
                i+=1

                while i < len(file_data):
                    line_data = file_data[i].split(",")
                    if line_data[0] == block_start :
                        break
                    else:
                        coordinate = float(line_data[2])
                        massUranium = float(line_data[3])
                        massPlutonium = float(line_data[4])
                        massNitrogen = float(line_data[5])
                        if len(line_data) < 9: print("check elements number in total_mass_flows. Should be 7.")
                        massUPuN = float(line_data[8]) # возможно, количество элементов в строке при выводе в SAFR плавает.

                        new_layer = dissociationLayer(coordinate, massUranium, massPlutonium, massNitrogen, massUPuN)
                        hs_D_state.addLayer(new_layer)

                    i = i+ 1
                self.dissociation_time_states.append(hs_D_state)
            else :
                i = i + 1

        if(len( self.time_states) == 0):
            return True
        if (self.dissociation_time_states[0].get_time() == self.time_states[0].get_time()):
            self.initial_UPuN_mass = self.time_states[0].get_mass("UPN")
        if len(self.dissociation_time_states) > 0:
            return True
        print("No data for Zone " + str(self.zone_id))
        return False

    def plot_liquid_map(self, path, DtPlot, TimeToStop, title, group, myOut):
        if path != "" : path += '/'
        path += group["name"] + '/'
        fileout_name = path + 'liquid_map_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name
        Index = 0
        while Index < len(self.time_states):
            
            self.time_states[Index].drow_liq_state(self.parameters, self.materials, fileout_name, title, group, myOut)

            if DtPlot>0.0 :
                current_time = self.time_states[Index].get_time()
                next_time = current_time + DtPlot - 0.00001
                while current_time < next_time :
                    Index+=1
                    if Index >=len(self.time_states): break
                    current_time = self.time_states[Index].get_time()
                if current_time > TimeToStop:
                    Index = len(self.time_states) + 1
                    break
            else :
               Index+=1

    def plot_temp_map(self, path, DtPlot, TimeToStop, title, group, myOut):
        if path != "" : path += '/'
        path += group["name"] + '/'
        fileout_name = path + 'temp_map_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name
        Index = 0
        while Index < len(self.time_states):
            
            self.time_states[Index].drow_temp_state(self.parameters, self.materials, fileout_name, title, group, myOut)

            if DtPlot>0.0 :
                current_time = self.time_states[Index].get_time()
                next_time = current_time + DtPlot - 0.00001
                while current_time < next_time :
                    Index+=1
                    if Index >=len(self.time_states): break
                    current_time = self.time_states[Index].get_time()
                if current_time > TimeToStop:
                    Index = len(self.time_states) + 1
                    break
            else :
               Index+=1

    def plot_mass_liquid(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):

        for mat in self.materials.get_materials():
            if mat.get_type() == "gas": continue
            object_name = 'liquid_mass_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name + '_' + mat.get_name()
            dataList = []
            for time_state in self.time_states:
                time_step_data = []
                time_step_data.append(time_state.get_time())
                time_step_data.append(time_state.get_mass_liquid(mat.get_name()) * tvel_number)
                dataList.append(time_step_data)

            #if dataList[0][0] > 0.0:
            #    time_step_data = list(dataList[0])
            #    time_step_data[0] = 0.0
            #    dataList.insert(0, time_step_data)
            
            my_str = " в " + add_to_title + " в зоне " + str(self.zone_id) + " для материала " + mat.get_name()
            myData = transientDataSet("SAFR", graph_parameters["name"] + '_' + mat.get_type())
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)
            MyCore.addDataToZone(self.zone_name, myData, "time")

            myZone.add_materialDataForLiquid(mat.get_name(), dataList)

    def plot_mass_solid(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):

        for mat in self.materials.get_materials():
            if mat.get_type() == "gas": continue
            object_name = 'solid_mass_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name + '_' + mat.get_name()
            dataList = []
            for time_state in self.time_states:
                time_step_data = []
                time_step_data.append(time_state.get_time())
                time_step_data.append(time_state.get_mass_solid(mat.get_name()) * tvel_number)
                dataList.append(time_step_data)

            my_str = " в " + add_to_title + " в зоне " + str(self.zone_id) + " для материала " + mat.get_name()
            myData = transientDataSet("SAFR", graph_parameters["name"] + '_' + mat.get_type())
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)
            MyCore.addDataToZone(self.zone_name, myData, "time")

            myZone.add_materialDataForSolid(mat.get_name(), dataList)

    def plot_mass_total(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):

        for mat in self.materials.get_materials():
            if mat.get_type() == "gas": continue
            object_name = 'total_mass_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name + '_' + mat.get_name()
            dataList = []
            for time_state in self.time_states:
                time_step_data = []
                time_step_data.append(time_state.get_time())
                time_step_data.append(time_state.get_mass(mat.get_name()) * tvel_number)
                dataList.append(time_step_data)

            my_str = " в " + add_to_title + " в зоне " + str(self.zone_id) + " для материала " + mat.get_name()
            myData = transientDataSet("SAFR", graph_parameters["name"] + '_' + mat.get_type())
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)
            MyCore.addDataToZone(self.zone_name, myData, "time")

            myZone.add_materialDataForTotalMass(mat.get_name(), dataList)

    def plot_max_temperature(self, graph_parameters, myOut, MyCore, add_to_title = ''):

        for mat in self.materials.get_materials():
            if mat.get_type() == "gas": continue
            object_name = 'max_temperature_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name + '_' + mat.get_name()
            dataList = []
            for time_state in self.time_states:
                time_step_data = []
                time_step_data.append(time_state.get_time())
                time_step_data.append(time_state.get_max_temperature_for_mat(mat.get_name()))
                if time_step_data[1] != 0.0:
                    dataList.append(time_step_data)

            my_str = " в " + add_to_title + " в зоне " + str(self.zone_id) + " для материала " + mat.get_name()
            myData = transientDataSet("SAFR", graph_parameters["name"] + '_' + mat.get_type())
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(graph_parameters["graphParameters"]["legend"])
            processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, "SAFR", myOut, myData, add_to_title = my_str)
            MyCore.addDataToZone(self.zone_name, myData, "time")


    def PlotUranium(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):
        module_name = "SAFR"
        mat_name = "Uranium"
        object_name = 'DissociationMassUranium_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name

        dataList = []
        for time_state in self.dissociation_time_states:
            time_step_data = []
            time_step_data.append(time_state.get_time())
            time_step_data.append(time_state.get_massUranium() * tvel_number)
            dataList.append(time_step_data)

        my_str = " в зоне " + str(self.zone_id)
        myData = transientDataSet(module_name, graph_parameters["name"])

        max_data = get_max_from_data(dataList)
        useYSci = False
        if max_data < graph_parameters["graphParameters"]["criteriaForAxSciFormat"]:
            useYSci = True

        data_to_plot = []
        data_to_plot.append(dataList)
        data_legends = []
        data_legends.append(graph_parameters["graphParameters"]["legend"])
        processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, module_name, myOut, myData, add_to_title = my_str, useySciFormat = useYSci)
        MyCore.addDataToZone(self.zone_name, myData, "time")

        myZone.add_DataDissociation(mat_name, dataList)


    def PlotPlutonium(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):
        module_name = "SAFR"
        mat_name = "Plutonium"
        object_name = 'DissociationMassPlutonium_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name
        
        dataList = []
        for time_state in self.dissociation_time_states:
            time_step_data = []
            time_step_data.append(time_state.get_time())
            time_step_data.append(time_state.get_massPlutonium() * tvel_number)
            dataList.append(time_step_data)

        max_data = get_max_from_data(dataList)

        useYSci = False
        if max_data < graph_parameters["graphParameters"]["criteriaForAxSciFormat"]:
            useYSci = True

        my_str = " в зоне " + str(self.zone_id)
        myData = transientDataSet(module_name, graph_parameters["name"])
        data_to_plot = []
        data_to_plot.append(dataList)
        data_legends = []
        data_legends.append(graph_parameters["graphParameters"]["legend"])
        processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, module_name, myOut, myData, add_to_title = my_str, useySciFormat = useYSci)
        MyCore.addDataToZone(self.zone_name, myData, "time")

        myZone.add_DataDissociation(mat_name, dataList)

    def PlotDinitrogen(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):
        module_name = "SAFR"
        mat_name = "Dinitrogen"
        object_name = 'DissociationMassDinitrogen_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name

        dataList = []
        for time_state in self.dissociation_time_states:
            time_step_data = []
            time_step_data.append(time_state.get_time())
            time_step_data.append(time_state.get_massDinitrogen() * tvel_number)
            dataList.append(time_step_data)

        max_data = get_max_from_data(dataList)

        useYSci = False
        if max_data < graph_parameters["graphParameters"]["criteriaForAxSciFormat"]:
            useYSci = True

        my_str = " в зоне " + str(self.zone_id)
        myData = transientDataSet(module_name, graph_parameters["name"])
        data_to_plot = []
        data_to_plot.append(dataList)
        data_legends = []
        data_legends.append(graph_parameters["graphParameters"]["legend"])
        processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, module_name, myOut, myData, add_to_title = my_str, useySciFormat = useYSci)
        MyCore.addDataToZone(self.zone_name, myData, "time")

        myZone.add_DataDissociation(mat_name, dataList)


    def PlotUPuN(self, graph_parameters, tvel_number, myOut, MyCore, myZone, add_to_title = ''):
        module_name = "SAFR"
        mat_name = "UPuN"
        object_name = 'DissociationMassUPuN_' + str(self.zone_id) + '_' + self.zone_name + '_' + self.hs_name

        dataList = []
        for time_state in self.dissociation_time_states:
            time_step_data = []
            time_step_data.append(time_state.get_time())
            time_step_data.append((self.initial_UPuN_mass + time_state.get_massUPuN()) * tvel_number)
            dataList.append(time_step_data)

        max_data = get_max_from_data(dataList)

        useYSci = False
        if max_data < graph_parameters["graphParameters"]["criteriaForAxSciFormat"]:
            useYSci = True

        my_str = " в зоне " + str(self.zone_id)
        myData = transientDataSet(module_name, graph_parameters["name"])
        data_to_plot = []
        data_to_plot.append(dataList)
        data_legends = []
        data_legends.append(graph_parameters["graphParameters"]["legend"])
        processingTimeType(graph_parameters, "", object_name, data_to_plot, data_legends, module_name, myOut, myData, add_to_title = my_str, useySciFormat = useYSci)
        MyCore.addDataToZone(self.zone_name, myData, "time")

        myZone.add_DataDissociation(mat_name, dataList)