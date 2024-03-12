class Jugador:

    def __init__(self, nombre, equipo, posicion, puntos, valoracion, lesionado, partidos_jugados, goles_marcados, asistencias, tarjetas_amarillas, tarjetas_rojas):
        self.nombre = nombre
        self.equipo = equipo
        self.posicion = posicion
        self.puntos = puntos
        self.valoracion = valoracion
        self.lesionado = lesionado
        self.partidos_jugados = partidos_jugados
        self.goles_marcados = goles_marcados
        self.asistencias = asistencias
        self.tarjetas_amarillas = tarjetas_amarillas
        self.tarjetas_rojas = tarjetas_rojas

    def get_info(self):
        return {
            "nombre": self.nombre,
            "equipo": self.equipo,
            "posicion": self.posicion,
            "puntos": self.puntos,
            "valoracion": self.valoracion,
            "lesionado": self.lesionado,
            "partidos_jugados": self.partidos_jugados,
            "goles_marcados": self.goles_marcados,
            "asistencias": self.asistencias,
            "tarjetas_amarillas": self.tarjetas_amarillas,
            "tarjetas_rojas": self.tarjetas_rojas
        }

    def get_promedio_puntos(self):
        if self.partidos_jugados == 0:
            return 0
        return self.puntos / self.partidos_jugados

    def es_titular(self):
        # Criterio para determinar si un jugador es titular (se puede modificar)
        return self.partidos_jugados >= 10 and self.valoracion >= 7
