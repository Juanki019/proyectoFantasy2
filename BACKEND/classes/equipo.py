class Equipo:

    def __init__(self, nombre, jugadores, puntos, posicion_liga):
        self.nombre = nombre
        self.jugadores = jugadores
        self.puntos = puntos
        self.posicion_liga = posicion_liga

    def get_info(self):
        return {
            "nombre": self.nombre,
            "jugadores": [jugador.get_info() for jugador in self.jugadores],
            "puntos": self.puntos,
            "posicion_liga": self.posicion_liga
        }

    def get_mejor_jugador(self):
        mejor_jugador = None
        mayor_puntuacion = 0
        for jugador in self.jugadores:
            if jugador.puntos > mayor_puntuacion:
                mayor_puntuacion = jugador.puntos
                mejor_jugador = jugador
        return mejor_jugador

    def get_promedio_puntos(self):
        if len(self.jugadores) == 0:
            return 0
        return sum(jugador.puntos for jugador in self.jugadores) / len(self.jugadores)
