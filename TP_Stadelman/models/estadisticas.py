
from GUI.GUI_form_menu_score import FormMenuScore




class Estadisticas:
    def __init__(self):
        self.estadisticas_jugadores = {}
    """bueno empecemos a meter daatos estadisicos
    el nombre quiero que venga desde el menu GUI en un menu start
    #
    """
    def agregar_puntuacion(self, score):
        if "score" not in self.estadisticas_jugadores:
            self.estadisticas_jugadores["score"] = 0

        # Agrega la puntuación al diccionario
        self.estadisticas_jugadores["score"] += score
        
        
        
    def obtener_puntuaciones(self):
            # Devuelve las puntuaciones acumuladas en un diccionario
            return self.estadisticas_jugadores
