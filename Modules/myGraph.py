import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from matplotlib import figure


import matplotlib.ticker as ticker
import numpy as np
import math

import Modules.Utils.mySettings
from Modules.Utils.utils import get_derivativesSeparate
import gc

class myGraph():
    """description of class"""
    users_xTicks = False
    users_yTicks = False
    
    users_xLimits = False
    users_yLimits = False

    axSciFormat = False
    aySciFormat = False

    axScaleFormat = "linear" #function, functionlog, linear, log, logit, symlog
    ayScaleFormat = "linear"
    
    title = ''
    legendLocation = "best" #['best' | 'upper right' | 'upper left' | 'lower left' | 'lower right' | 'right' | 'center left' | 'center right' | 'lower center' | 'upper center' | 'center']

    def __init__(self, xLabel, yLabel):
        self.xLabel = xLabel
        self.yLabel = yLabel

        self.users_xTicks = False
        self.users_yTicks = False
    
        self.users_xLimits = False
        self.users_yLimits = False

        self.axSciFormat = False
        self.aySciFormat = False

    def set_LegendLocation(self,legendLocation):
        self.legendLocation = legendLocation

    def set_Title(self,title):
        self.title = title

    def useSciFormatForAx(self):
        self.axSciFormat = True

    def useSciFormatForAy(self):
        self.aySciFormat = True

    # Set scale format
    def setScaleForAx(self, format):
        self.axScaleFormat = format

    def setScaleForAy(self,format):
        self.ayScaleFormat = format


    # Adds limits
    def set_xLimits(self, xMin,xMax):
        self.users_xLimits = True
        self.xMin = xMin
        self.xMax = xMax

    def set_yLimits(self, yMin,yMax):
        self.users_yLimits = True
        self.yMin = yMin
        self.yMax = yMax

    # Adds ticks
    def set_xAxisTicks(self, MajorTicks,MinorTicks):
        self.users_xTicks = True
        self.xMajorTicks = MajorTicks
        self.xMinorTicks = MinorTicks

    def set_yAxisTicks(self, MajorTicks,MinorTicks):
        self.users_yTicks = True
        self.yMajorTicks = MajorTicks
        self.yMinorTicks = MinorTicks

    def plot(self, myLines, output_name, output_path):
        #reload(plt)


        fig, ax = plt.subplots()
        #fig = figure.Figure()
        #ax = fig.add_subplot(111)
        y_min_data = 1.e+35
        y_max_data = -1.e+35
        for line in myLines :
            #linestyle = [ '-' | '--' | '-.' | ':' | 'steps']
            ax.plot(line.tData, line.fData, label=line.label, color=line.color, linestyle =line.lineStyle,linewidth = line.lineWidth, marker = line.marker, markersize = line.markerSize, markeredgewidth = line.markerEdgeWidth, markerfacecolor = line.markerFaceColor, markeredgecolor =line.markerEdgeColor)
            #ax.plot(t, s2,label="Зона 555", color='red', linestyle ="-",linewidth = 2)
            #'o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd'
            #ax.scatter(t, s2, label = "Зона 555", color='black')
            y_min_data = min(y_min_data, min(line.fData))
            y_max_data = max(y_max_data, max(line.fData))
        ####################SaveDataToFile#######################
        printData = Modules.Utils.mySettings.printDataToFile
        if printData:
            f_output_path = output_path
            if len(f_output_path) != 0: f_output_path +='/'
            line_index = 1
            for line in myLines :
                myStr = line.label
                dasd = myStr.find("/")
                if dasd > 0:
                    myStr = myStr[:dasd] + '' + myStr[dasd+1:]
                f_out = open(f_output_path + output_name + '_' + myStr + '_' + "_line_index_"+str(line_index)+".txt","w")
                #line_index += 1
                i=0
                while i < len(line.tData):
                    f_out.write(str(line.tData[i]) + ' ' + str(line.fData[i]) +'\n')
                    i+=1
                f_out.close()

                der_fData = get_derivativesSeparate(line.tData, line.fData)

                f_outd = open(f_output_path + output_name + '_' + myStr + '_' + "_line_index_"+str(line_index)+"_Derivative.txt","w")
                line_index += 1
                i=0
                while i < len(line.tData):
                    f_outd.write(str(line.tData[i]) + ' ' + str(der_fData[i]) +'\n')
                    i+=1
                f_outd.close()
        #########################################################


        #ax.set(xlabel='Время, с', ylabel='Температура, К', title='')
        ax.set_xlabel(self.xLabel, fontsize = 12) #, fontweight = 'bold'
        ax.set_ylabel(self.yLabel, fontsize = 12)

               
        #ax.get_xaxis().get_major_formatter().set_useOffset(False)

        not_have_x_log_scale = True
        not_have_y_log_scale = True


        if self.axScaleFormat == "log":
            x_min = self.xMin
            if x_min < 0.0: x_min = 0.0000001
            #x_min = 1.0
            x_max = self.xMax
            if x_max > 0.0:
                #ax.set_xlim(x_min, x_max)
                ax.set_xscale(self.axScaleFormat)
                not_have_x_log_scale = False
                ##x_labels = np.linspace(math.floor(math.log10(max(1.0, x_min))), math.floor(math.log10(x_max))+1, math.floor(math.log10(x_max-x_min))+2)
                #ax.set_xticks(np.e**x_labels)
                #ax.set_xticklabels(x_labels)

        if self.ayScaleFormat == "log":
            y_min = y_min_data
            if y_min < 0.0: y_min = 0.0
            y_max = y_max_data
            if y_max > 0.0:
                #ax.set_ylim(y_min, y_max)
                ax.set_yscale(self.ayScaleFormat)
                #plt.tick_params(axis='y', which='minor')
                ax.yaxis.grid(True, which='minor')
                not_have_y_log_scale = True#False
                #y_labels = np.linspace(y_min, y_max, 10)
                #ax.set_yticks(np.e**y_labels)
                #ax.set_yticklabels(y_labels)





        #установить границы области
        #if self.users_xLimits and  not_have_x_log_scale :
        if self.users_xLimits :
            ax.set_xlim(self.xMin, self.xMax)
            #ax.set_xlim(1.0, self.xMax)
        if self.users_yLimits  and not_have_y_log_scale :
            ax.set_ylim(self.yMin, self.yMax)
        
        
        if self.users_xTicks and not_have_x_log_scale :
            #  Устанавливаем интервал основных делений:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xMajorTicks))
            #  Устанавливаем интервал вспомогательных делений:
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(self.xMinorTicks))

        if self.users_yTicks and not not_have_y_log_scale :
            #  Устанавливаем интервал основных делений:
            ax.yaxis.set_major_locator(ticker.MultipleLocator(self.yMajorTicks))
            #  Устанавливаем интервал вспомогательных делений:
            #ax.yaxis.set_minor_locator(ticker.MultipleLocator(self.yMinorTicks))
            ax.yaxis.set_minor_locator(ticker.MaxNLocator(10))

        if self.axSciFormat and not_have_x_log_scale :
            plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

        if self.aySciFormat and not not_have_y_log_scale :
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

        ########################## настройка сетки ############################
        # установить отображение сетки
        #  Добавляем линии основной сетки:
        ax.grid(which='major',
                color = 'black')
        #  Включаем видимость вспомогательных делений:
        ax.minorticks_on()
        #  Теперь можем отдельно задавать внешний вид
        #  вспомогательной сетки:
        ax.grid(which='minor',
                color = 'gray',
                linestyle = ':')


        #ax.yaxis.set_major_locator(ticker.MultipleLocator(self.yMajorTicks))
        #ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())


        # установить отображение легенды
        ax.legend(loc = self.legendLocation)


        plt.title(self.title)
        plt.tight_layout()

        if len(output_path) != 0: output_path +='/'
        fig.savefig(output_path + output_name + ".png")
        #fig.clf()
       # plt.clf()
        #del ax
        #plt.close("all")
       
        plt.close('all')
        #plt.clf()
        #plt.cla()
        

        gc.collect()


    def plotColoredMap(self, my_array_of_data, zone_names, tvs_zones_name, axial_cell_center, axial_cell_center_zones,
                       picture_title, picture_xlabel, picture_ylabel, colorbar_label, colorBarScheme,
                      xMajorTicks, xMinorTicks, colorBarTicks, isUserLimits, limitMin, limitMax,
                      output_name, output_path):
        ## переводим массив из центров ячеек в массив с границами ячеек. Основное условие - первая координата границы ячейки нуль
        def get_array_with_node_coordinates(array_with_cells_center):
            axial_index = [0.0]
            i = 0
            start = 0.0
            while i < len(array_with_cells_center):
                delt = array_with_cells_center[i] - start
                next = start + delt*2
                axial_index.append(next)
                start = next
                i+=1

            return list(axial_index)


        #цветовые схемы
        #cm = ['RdBu_r','seismic', 'bwr','jet']

        #### 
        zone_number = len(zone_names)
        cells_number = len(axial_cell_center)

        radial_index = np.arange(zone_number+1)

        axial_index = get_array_with_node_coordinates(axial_cell_center);
        axial_index_tvs_zones = get_array_with_node_coordinates(axial_cell_center_zones)
        core_height = axial_index[len(axial_index)-1]

        ##

        fig, ax = plt.subplots()
        #fig = figure.Figure()
        #ax = fig.add_subplot(111)
        ay = ax.twinx()
        
        smax = np.arange(zone_number)+0.5
        ax.set_xticks(smax)

        ax.yaxis.set_major_locator(ticker.MultipleLocator(xMajorTicks))
        #  Устанавливаем интервал вспомогательных делений:
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(xMinorTicks))

        ax.set_xticklabels(zone_names, fontsize = 6)
        ax.set_xlabel(picture_xlabel, fontsize = 12)
        ax.set_ylabel(picture_ylabel, fontsize = 12)

        min_value = np.min(my_array_of_data)
        max_value = np.max(my_array_of_data)
        if isUserLimits:
            min_value = limitMin
            max_value = limitMax

        pcm = ax.pcolormesh(radial_index,axial_index,my_array_of_data, cmap=colorBarScheme, shading='auto', vmin = min_value, vmax = max_value) #, vmin = np.min(my_array_of_data), vmax = np.max(my_array_of_data,1.0)
        
        ay.set_xlim(0, zone_number)
        ay.set_ylim(0, core_height)
        ay.set_yticks(axial_cell_center_zones)
        ay.set_yticklabels(tvs_zones_name, fontsize = 8)

        # растановка сетки и областей для
        for point in axial_index_tvs_zones :
            ay.plot([0, zone_number], [point, point], color='black',linewidth = 0.5)

        for point in radial_index :
            ay.plot([point, point], [0, core_height], color='black',linewidth = 0.5)



        fig.colorbar(pcm, ax=ax, ticks = ticker.MultipleLocator(colorBarTicks), label=colorbar_label)
 
        plt.setp(ax.get_xticklabels(), rotation=45, ha="center", rotation_mode="anchor")
        plt.setp(ay.get_yticklabels(), rotation=90, ha="center", rotation_mode="anchor")

        #plt.title(picture_title)
        if len(output_path) != 0: output_path +='/'
        pic_url = output_path + output_name + ".png"
        fig.savefig(pic_url)
        #plt.show()
        plt.close()