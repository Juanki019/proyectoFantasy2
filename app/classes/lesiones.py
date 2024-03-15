class Lesion:

    def __init__(self, nombre, equipo, fecha_inicio, fecha_fin, tipo_lesion):
        self.nombre = nombre
        self.equipo = equipo
        self.tipo_lesion = tipo_lesion

    def get_info(self):
        return {
            "nombre": self.nombre,
            "equipo": self.equipo,
            "tipo_lesion": self.tipo_lesion
        }
