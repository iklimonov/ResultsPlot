class mapParametersSAFR():
    def __init__(self, size_axial, size_radial, axial_length, inner_radius, external_radius, free_space_axial, free_space_radial):
        self.size_axial = size_axial + free_space_axial
        self.size_radial = size_radial + free_space_radial + 250
        self.axial_ratio = (size_axial) / axial_length 
        self.radial_ratio = (size_radial) / (external_radius - inner_radius)
        self.axial_length = axial_length
        self.inner_radius = inner_radius

class material():
    def __init__(self, name, type, color_solid, color_liquid):
        self.name = name
        self.type = type
        self.color_solid = color_solid
        self.color_liquid = color_liquid

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_color_solid(self):
        return self.color_solid

    def get_color_liquid(self):
        return self.color_liquid

class materialCollection():
    def __init__(self):
        self.materials = []

    def add_material(self, materia):
        self.materials.append(materia)

    def get_color_solid(self, mat_name):
        color = "black"
        for material in self.materials:
            if material.get_name() == mat_name :
                color = material.get_color_solid()
                break
        return color

    def get_color_liquid(self, mat_name):
        color = "black"
        for material in self.materials:
            if material.get_name() == mat_name :
                color = material.get_color_liquid()
                break
        return color

    def get_material_by_name(self, mat_name):
        for mat in self.materials:
            if mat.get_name() == mat_name :
                return mat

        print("parameters for mat " + mat_name + " not found")
        return None

    def get_materials(self):
        return self.materials

    def delete_unused_materials(self, used_mat_names_list):
        used_mat_list = []        
        for used_mat_name in used_mat_names_list:
            for mat in self.materials:
                if mat.get_name() == used_mat_name :
                    used_mat_list.append(mat)
        self.materials = used_mat_list
