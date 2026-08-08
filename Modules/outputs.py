import os
import codecs

class picture():
    def __init__(self, url, discription):
        self.url = url
        self.discription = discription

    def prints(self):
        return '{"url" : "'+self.url+'", "discription" : "'+self.discription+'"}'

class subgroup():
    name = ''
    pictures = []
    def __init__(self, name, title, url, discription):
        self.name = name
        self.title = title
        self.pictures = []
        new_pic = picture(url, discription)
        self.pictures.append(new_pic)

    def addPicture(self, url, discription):
        is_added = False
        for sub_pics in self.pictures:
            if url == sub_pics.url:
                is_added = True
                break
        if is_added == False :
            new_sub_pics = picture(url, discription)
            self.pictures.append(new_sub_pics)

    def prints(self):
        mystr = '{"name" : "'+self.name+'","title" : "'+self.title+'", "pictures" : ['
        indx = 0
        for pic in self.pictures:
            indx += 1
            mystr+=pic.prints()
            if indx != len(self.pictures) :
                mystr +=', '
        mystr += ']}'
        return mystr

class module():
    name = ''
    title = ''
    subgroups = []
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.subgroups = []

    def set_title(self, title):
        self.title = title

    def addSubgroup(self, subgroup_name, subgroup_title, url, discription):
        is_added = False
        for subg in self.subgroups:
            if subgroup_name == subg.name:
                is_added = True
                subg.addPicture(url, discription)
                break
        if is_added == False :
            new_subgr = subgroup(subgroup_name, subgroup_title, url, discription)
            self.subgroups.append(new_subgr)

    def prints(self):
        mystr = '{"name" : "'+self.name + '", "title" : "'+self.title + '", "subgroups" : ['
        indx = 0
        for subg in self.subgroups:
            indx += 1
            mystr+=subg.prints()
            if indx != len(self.subgroups) :
                mystr +=', '
        mystr += ']}'
        return mystr

class outputs():

    modules = []
    def __init__(self):
        self.modules = []

    def initModule(self, module_name, module_title):
        is_added = False
        for mod in self.modules:
            if module_name == mod.name:
                is_added = True
                mod.set_title(module_title)
                break

        if is_added == False :
            new_mod = module(module_name, module_title)
            self.modules.append(new_mod)


    def setModuleTitle(self, module_name, module_title):
        is_added = False
        for mod in self.modules:
            if module_name == mod.name:
                is_added = True
                mod.set_title(module_title)
                break

        if is_added == False :
            new_mod = module(module_name, module_title)
            self.modules.append(new_mod)

    def addFigure(self, module_name, subgroup, subgroup_title, url, discription):
        is_added = False
        for mod in self.modules:
            if module_name == mod.name:
                is_added = True
                mod.addSubgroup(subgroup, subgroup_title, url, discription)
                break
        if is_added == False :
            new_mod = module(module_name, '')
            new_mod.addSubgroup(subgroup, subgroup_title, url, discription)
            self.modules.append(new_mod)

    def printResults(self):
        for mod in self.modules:

            #file_path = r'' + mod.name + '.js'
            file_path = os.path.join("PlotResults", mod.name + '.js')
            fileout = codecs.open(file_path, "w", "utf-8")
            mystr = 'var my'+mod.name+' = \''

            mystr += mod.prints()
            #indx = 0
            #for mod in self.modules:
            #    indx += 1
            #    mystr += mod.prints()
            #    if indx != len(self.modules) :
            #        mystr +=', '

            mystr += '\';'
            fileout.write(mystr)
            fileout.close()

class jsScriptGroups():
    def __init__(self):
        self.groups = []

    def addModule(self, module_name):
        is_added = False
        for mod in self.groups:
            if module_name == mod:
                is_added = True
                break

        if is_added == False :
            self.groups.append(module_name)

    def printJSFiles(self):
        file_pathModulesList = os.path.join("PlotResults", "ModulesList" + '.js')
        file_pathPreModulesList = os.path.join("PlotResults", "PreModulesList" + '.js')


        file_pathPML = os.path.join("PlotResults", "PreModulesList" + '.js')
        fileout = codecs.open(file_pathPML, "w", "utf-8")
        fileout.write("function loadScript(filePath) {"+'\n')
        fileout.write("    const script = document.createElement('script');"+'\n')
        fileout.write("    script.src = filePath;"+'\n')
        fileout.write('    script.type = "text/javascript";'+'\n')
        fileout.write('    script.async = "true";'+'\n')
        fileout.write('    script.charset = "UTF-8"'+'\n')
        fileout.write("    document.head.appendChild(script);"+'\n')
        fileout.write("}"+'\n')
        fileout.write('\n')
        for g_name in self.groups:
            file_path = os.path.join("PlotResults", g_name + '.js')
            #fileout.write("loadScript('"+file_path+"');"+'\n')
            fileout.write("loadScript('"+"PlotResults" + '/'+ g_name + '.js'+"');"+'\n')
        #fileout.write("loadScript('"+"PlotResults"+'/'+"ModulesList" + '.js'+"');"+'\n')
        fileout.write('\n')

        fileout.close()

        ###############################################
        fileout = codecs.open(file_pathModulesList, "w", "utf-8")

        fileout.write('myModules = [];'+'\n')
        fileout.write('\n')

        for g_name in self.groups:

            fileout.write("var "+g_name+"_data = [];"+'\n')
            fileout.write("if (typeof my"+g_name+" != 'undefined' ) {"+'\n')
            fileout.write("    "+g_name+"_data = JSON.parse(my"+g_name+");"+'\n')
            fileout.write("    myModules.push("+g_name+"_data);"+'\n')
            fileout.write("}"+'\n')
            fileout.write('\n')

        fileout.close()






