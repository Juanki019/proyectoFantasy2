class Lesion:

    def __init__(self, nombre, equipo, fecha_inicio, fecha_fin, tipo_lesion):
        self.nombre = nombre
        self.equipo = equipo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo_lesion = tipo_lesion

    def get_info(self):
        return {
            "nombre": self.nombre,
            "equipo": self.equipo,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "tipo_lesion": self.tipo_lesion
        }
