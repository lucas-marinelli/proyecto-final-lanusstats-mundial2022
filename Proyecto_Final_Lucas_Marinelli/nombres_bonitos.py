"""
Modulo de "nombres bonitos" - mapeo de nombres completos StatsBomb a nombres
comerciales/comerciales conocidos para mostrar en graficos.

StatsBomb guarda nombres legales completos ("Lionel Andres Messi Cuccittini")
que son ilegibles en visualizaciones. Este modulo centraliza el mapeo a la
version "conocida" del jugador ("Lionel Messi" / "Messi").

Uso tipico:
    from nombres_bonitos import nombre_bonito

    # Para mostrar en grafico
    label = nombre_bonito("Lionel Andres Messi Cuccittini")  # -> "Messi"

    # Para version completa (apellido_nombre)
    label = nombre_bonito("Rodrigo Javier De Paul", formato="completo")
    # -> "Rodrigo De Paul"

    # Para apellido solamente (el default mas usado en pass networks)
    label = nombre_bonito("Joshko Gvardiol", formato="apellido")
    # -> "Gvardiol"

Mantener este diccionario actualizado cada vez que aparezca un jugador
relevante en analisis futuros.
"""
from __future__ import annotations

# Mapeo nombre_statsbomb -> (apellido_corto, nombre_completo)
# Formato del diccionario: clave = como aparece en StatsBomb, valor = tupla
# Lo armo asi para que la funcion pueda devolver cualquier formato
_MAPEO = {
    # === Argentina ===
    "Lionel Andrés Messi Cuccittini":           ("Messi", "Lionel Messi"),
    "Julián Álvarez":                            ("Álvarez", "Julián Álvarez"),
    "Lautaro Javier Martínez":                    ("Lautaro", "Lautaro Martínez"),
    "Nahuel Molina Lucero":                       ("Molina", "Nahuel Molina"),
    "Ángel Fabián Di María Hernández":            ("Di María", "Ángel Di María"),
    "Nicolás Hernán Otamendi":                    ("Otamendi", "Nicolás Otamendi"),
    "Rodrigo Javier De Paul":                     ("De Paul", "Rodrigo De Paul"),
    "Enzo Jeremías Fernández":                    ("Enzo Fernández", "Enzo Fernández"),
    "Cristian Gabriel Romero":                    ("Romero", "Cristian Romero"),
    "Leandro Daniel Paredes":                     ("Paredes", "Leandro Paredes"),
    "Alexis Mac Allister":                        ("Mac Allister", "Alexis Mac Allister"),
    "Nicolás Alejandro Tagliafico":               ("Tagliafico", "Nicolás Tagliafico"),
    "Marcos Javier Acuña":                        ("Acuña", "Marcos Acuña"),
    "Emiliano Martínez":                          ("Dibu Martínez", "Emiliano Martínez"),
    "Damián Emiliano Martínez":                   ("Dibu Martínez", "Emiliano Martínez"),
    "Papu Gómez":                                  ("Papu Gómez", "Papu Gómez"),
    "Alejandro Darío Gómez":                      ("Papu Gómez", "Papu Gómez"),
    "Germán Pezzella":                             ("Pezzella", "Germán Pezzella"),
    "Guido Rodríguez":                             ("Guido", "Guido Rodríguez"),
    "Lisandro Martínez":                           ("Licha", "Lisandro Martínez"),
    "Marcos Senesi":                               ("Senesi", "Marcos Senesi"),
    "Juan Foyth":                                  ("Foyth", "Juan Foyth"),
    "Gonzalo Montiel":                             ("Cachete", "Gonzalo Montiel"),
    "Geronimo Rulli":                              ("Rulli", "Gerónimo Rulli"),
    "Franco Armani":                               ("Armani", "Franco Armani"),
    "Joaquín Correa":                              ("Correa", "Joaquín Correa"),
    "Thiago Almada":                               ("Almada", "Thiago Almada"),
    "Exequiel Palacios":                           ("Palacios", "Exequiel Palacios"),

    # === Arabia Saudita (con apellidos cortos) ===
    "Salem Mohammed Al-Dawsari":                  ("Al-Dawsari", "Salem Al-Dawsari"),
    "Saud Abdulhamid":                             ("Abdulhamid", "Saud Abdulhamid"),
    "Mohammed Al-Owais":                           ("Al-Owais", "Mohammed Al-Owais"),
    "Abdulelah Al-Malki":                          ("Al-Malki", "Abdulelah Al-Malki"),
    "Mohammed Kanno":                              ("Kanno", "Mohammed Kanno"),
    "Salman Al-Faraj":                             ("Al-Faraj", "Salman Al-Faraj"),
    "Yasser Al-Shahrani":                          ("Al-Shahrani", "Yasser Al-Shahrani"),

    # === Francia ===
    "Kylian Mbappé Lottin":                       ("Mbappé", "Kylian Mbappé"),
    "Olivier Jonathan Giroud":                    ("Giroud", "Olivier Giroud"),
    "Antoine Griezmann":                          ("Griezmann", "Antoine Griezmann"),
    "Aurélien Tchouaméni":                         ("Tchouaméni", "Aurélien Tchouaméni"),
    "Adrien Rabiot":                              ("Rabiot", "Adrien Rabiot"),
    "Hugo Lloris":                                ("Lloris", "Hugo Lloris"),
    "Raphaël Varane":                             ("Varane", "Raphaël Varane"),
    "Theo Hernandez":                             ("Theo", "Theo Hernandez"),

    # === Espana ===
    "Rodrigo Hernández Cascante":                 ("Rodri", "Rodri"),
    "Aymeric Laporte":                            ("Laporte", "Aymeric Laporte"),
    "Álvaro Borja Morata Martín":                 ("Morata", "Álvaro Morata"),
    "Sergio Busquets i Burgos":                   ("Busquets", "Sergio Busquets"),
    "Pedro González López":                       ("Pedri", "Pedri"),
    "Gavi":                                       ("Gavi", "Gavi"),
    "Pablo Martín Páez Gavira":                   ("Gavi", "Gavi"),
    "Marco Asensio Willemsen":                    ("Asensio", "Marco Asensio"),

    # === Inglaterra ===
    "Harry Kane":                                 ("Kane", "Harry Kane"),
    "Bukayo Ayoyinka Temidayo Saka":              ("Saka", "Bukayo Saka"),
    "Marcus Rashford":                            ("Rashford", "Marcus Rashford"),
    "John Stones":                                ("Stones", "John Stones"),
    "Harry Maguire":                              ("Maguire", "Harry Maguire"),
    "Kieran Trippier":                            ("Trippier", "Kieran Trippier"),
    "Luke Shaw":                                  ("Shaw", "Luke Shaw"),
    "Jude Bellingham":                            ("Bellingham", "Jude Bellingham"),
    "Declan Rice":                                ("Rice", "Declan Rice"),
    "Jordan Pickford":                            ("Pickford", "Jordan Pickford"),
    "Phil Foden":                                 ("Foden", "Phil Foden"),

    # === Paises Bajos ===
    "Cody Mathès Gakpo":                          ("Gakpo", "Cody Gakpo"),
    "Denzel Justus Morris Dumfries":              ("Dumfries", "Denzel Dumfries"),
    "Virgil van Dijk":                            ("van Dijk", "Virgil van Dijk"),
    "Frenkie de Jong":                            ("de Jong", "Frenkie de Jong"),
    "Andries Noppert":                            ("Noppert", "Andries Noppert"),

    # === Croacia ===
    "Luka Modrić":                                ("Modrić", "Luka Modrić"),
    "Marcelo Brozović":                           ("Brozović", "Marcelo Brozović"),
    "Joško Gvardiol":                             ("Gvardiol", "Joško Gvardiol"),
    "Mateo Kovačić":                              ("Kovačić", "Mateo Kovačić"),
    "Dominik Livaković":                          ("Livaković", "Dominik Livaković"),
    "Dejan Lovren":                               ("Lovren", "Dejan Lovren"),

    # === Brasil ===
    "Neymar da Silva Santos Júnior":              ("Neymar", "Neymar Jr"),
    "Vinícius José Paixão de Oliveira Júnior":    ("Vinícius Jr", "Vinícius Jr"),
    "Casemiro":                                   ("Casemiro", "Casemiro"),
    "Thiago Emiliano da Silva":                   ("Thiago Silva", "Thiago Silva"),
    "Richarlison de Andrade":                     ("Richarlison", "Richarlison"),

    # === Portugal ===
    "Cristiano Ronaldo dos Santos Aveiro":        ("Cristiano", "Cristiano Ronaldo"),
    "Gonçalo Matias Ramos":                       ("Gonçalo Ramos", "Gonçalo Ramos"),

    # === Marruecos ===
    "Sofiane Boufal":                             ("Boufal", "Sofiane Boufal"),
    "Achraf Hakimi Mouh":                         ("Hakimi", "Achraf Hakimi"),
    "Sofyan Amrabat":                             ("Amrabat", "Sofyan Amrabat"),
    "Hakim Ziyech":                               ("Ziyech", "Hakim Ziyech"),
    "Azzedine Ounahi":                            ("Ounahi", "Azzedine Ounahi"),
    "Selim Amallah":                              ("Amallah", "Selim Amallah"),

    # === Polonia ===
    "Robert Lewandowski":                         ("Lewandowski", "Robert Lewandowski"),

    # === Ecuador ===
    "Enner Remberto Valencia Lastra":             ("Enner Valencia", "Enner Valencia"),

    # === Otros destacados ===
    "Mathew Leckie":                              ("Leckie", "Mathew Leckie"),
    "Breel-Donald Embolo":                        ("Embolo", "Breel Embolo"),
}


def nombre_bonito(player_full: str, formato: str = "apellido") -> str:
    """Devuelve el nombre legible de un jugador.

    Parametros
    ----------
    player_full : nombre completo tal como aparece en StatsBomb
    formato : "apellido" (default, ej "Messi"), "completo" (ej "Lionel Messi"),
              "raw" (devuelve player_full sin tocar)

    Si player_full no esta en el diccionario, hace fallback:
    - formato "apellido" -> ultima palabra del nombre
    - formato "completo" -> "primer_nombre apellido" (primer + ultima palabra)
    - formato "raw" -> tal cual
    """
    if formato == "raw":
        return player_full

    if player_full in _MAPEO:
        apellido, completo = _MAPEO[player_full]
        return apellido if formato == "apellido" else completo

    # Fallback: deducir desde el nombre full
    partes = player_full.split() if isinstance(player_full, str) else []
    if not partes:
        return str(player_full)
    if formato == "apellido":
        return partes[-1]
    # formato "completo"
    return f"{partes[0]} {partes[-1]}" if len(partes) >= 2 else partes[0]
