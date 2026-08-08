#for file in CommonData :
    #    print("Processing " + file["file"])
    #    for zone in zones:
    #        file_name = ''
    #        object_name = '' 
    #        if file["module"]=="BERKUT":
    #            object_name = get_NameForBERKUT(file["file"],zone["name"],zone["tvel"]["name"])
    #        if file["module"]=="HYDRA":
    #            object_name = get_NameForHYDRA(file["file"],zone["name"])

    #        file_name = object_name + '.dat'
    #        path_to_file = r'' + global_folder_with_results
    #        dataList = convert_file_to_list(file_name,path_to_file,file["HeaderLines"],stadyStateTime,True)

    #        if file["dataType"] =="time": # значит имеем только один график от времени
    #            processingTimeType(file, zone, object_name, dataList)
        
    #        if file["dataType"] =="space": # значит имеем только один график от времени
    #            lines_per_figure = 5
    #            processingSpaceType(file, zone, object_name, dataList, lines_per_figure)


    #file_path = r''+"results.js"
    #fileout = open(file_path, "w")
    #fileout.write("var myPics = [\n")
    #res_len = len(results)
    #i = 0
    #while i < res_len - 1:
    #    fileout.write('{'+'url' + ' : "'+ results[i].url +'", '+'title' + ' : "'+ results[i].title + '"},\n')
    #    i = i + 1
    #fileout.write('{'+'url' + ' : "'+ results[i].url +'", '+'title' + ' : "'+ results[i].title + '"}\n')
    #fileout.write("]")
    #fileout.close()

##################################################################################

    #geometry_options = {"tmargin": "1cm", "lmargin": "1cm","rmargin": "1cm", "bmargin": "1cm"}
    #doc = Document(geometry_options=geometry_options,page_numbers=True)
    #doc.packages.add(Package('babel', options=['english','russian']))
    #doc.packages.add(Package('float'))

    #with doc.create(Section('some text')):
    #     with doc.create(Subsection('some text')):
    #        for fig in results :
    #            image_filename = os.path.join(os.path.dirname(__file__), fig.url)
    #            #image_filename = os.path.join(os.path.dirname(__file__), 'myLine.png')
    #            with doc.create(Figure(position='h!')) as kitten_pic:
    #                kitten_pic.add_image(image_filename)
    #                kitten_pic.add_caption(fig.title)#fig.title

    #doc.generate_pdf('BN1200_figures', clean_tex=False,compiler='pdflatex')
##################################################################################

#file_name = 'BERKUT_tvelMaxTemperature_Zone_141_TVEL_Rods'
#path_to_file = r'CalculationResults'
#shift = 0.0
#skiplines = 7
#mylist = convert_file_to_list(file_name,path_to_file,skiplines,shift,True)

#print(mylist)

#t = []
#y = []
#for i in range(len(mylist)):
#    t.append(mylist[i][0])
#    y.append(mylist[i][1])


#my_Graph = myGraph('Время, с','Температура, К')
#my_Graph.set_xLimits(0.0, 200.0)
#my_Graph.set_yLimits(1000, 1700.0)
#my_Graph.set_LegendLocation('lower right')

#my_Graph.set_xAxisTicks(100, 10)
#my_Graph.set_yAxisTicks(50, 10)

#my_Graph.set_Title("Fig 1. some text")

##print(y)
#my_Line = myLine(t,y)
#my_Line.set_label("myLine s")
#my_Line.set_lineWidth(2)
#my_Line.set_color("red")
#my_Line.set_lineStyle("-")

#lines = []
#lines.append(my_Line)

#pathToFolder = ''

#my_Graph.plot(lines ,"myLine", pathToFolder)
