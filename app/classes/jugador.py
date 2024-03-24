class Jugador:
    def __init__(self, id_jugador, nombre, puntos, equipo, posicion, precio, media, partidos, minutos, goles, asistencias, asistencias_sin_gol,
                 balones_al_area, despejes, regates, tiros_a_puerta, balones_recuperados, posesiones_perdidas, penaltis_fallados,
                 goles_en_contra, tarjetas_rojas, paradas, penaltis_cometidos, tarjetas_amarillas, segundas_amarillas, penaltis_provocados,
                 penalties_parados, goles_en_propia, antepenultima_jornada, penultima_jornada, ultima_jornada, flecha):
        self.id_jugador = id_jugador
        self.nombre = nombre
        self.puntos = puntos
        self.equipo = equipo
        self.posicion = posicion
        self.precio = precio
        self.media = media
        self.partidos = partidos
        self.minutos = minutos
        self.goles = goles
        self.asistencias = asistencias
        self.asistencias_sin_gol = asistencias_sin_gol
        self.balones_al_area = balones_al_area
        self.despejes = despejes
        self.regates = regates
        self.tiros_a_puerta = tiros_a_puerta
        self.balones_recuperados = balones_recuperados
        self.posesiones_perdidas = posesiones_perdidas
        self.penaltis_fallados = penaltis_fallados
        self.goles_en_contra = goles_en_contra
        self.tarjetas_rojas = tarjetas_rojas
        self.paradas = paradas
        self.penaltis_cometidos = penaltis_cometidos
        self.tarjetas_amarillas = tarjetas_amarillas
        self.segundas_amarillas = segundas_amarillas
        self.penaltis_provocados = penaltis_provocados
        self.penalties_parados = penalties_parados
        self.goles_en_propia = goles_en_propia
        self.antepenultima_jornada = antepenultima_jornada
        self.penultima_jornada = penultima_jornada
        self.ultima_jornada = ultima_jornada
        self.flecha = flecha

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
