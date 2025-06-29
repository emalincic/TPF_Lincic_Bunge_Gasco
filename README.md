# Trabajo Practico Final - Plants vs Zombies
### Integrantes: Bunge Santos Ignacio, Facundo Esteban Gasco y Lincic Emanuel
### Docentes: Caccia Matias y Perlin Matias
--------------------
## Descripción del trabajo:
Nuestro objetivo fue crear la mejor version posible del juego Plants vs Zombies. Ispirandonos en las plantas, zombis y modos del juego. 
### Overview general:
Nuestro juego cuenta con dos modos principales:
1. El modo Clasico
2. El modo Papapapapum
    ### Clásico 🌻 vs 🧟
    El modo clasico funciona de la siguiente manera: el usuario comienza con 50 soles y puedo ir recolectando mas a medida que caen del cielo, o si sus girasoles los fabrican. Zombies empiezan a acercarse y el usuario cuenta con un arsenal de plantas (cada una con sus habilidades y costos) para defenderse. A su vez, existe una ultima linea de defensa, las podadoras. 

    La siguiente es una lista de las plantas:
    1. Lanzaguisantes: dispara proyectiles de fuerte impacto.
    2. Girasol: produce soles para comprar mas plantas.
    3. Nuez: robusta planta que frena zombies.
    4. Cereza bomba: todo zombi en un radio cercano a ella explota.
    5. Papapum: luego de despertarse es una peligrosa mina de tierra.
    6. Boomerang: dispara proyectiles de ida y vuelta!

    Sin embargo, exsiste una fuerte oleada de zombis compuesta por:
    1. Perlin Zombie: avanza lentamente hacia las plantas para devorarlas.
    2. Cono Caccia: zombie protejido por su cono
    3. Zombie Balde: gran resistencia
    4. Zombie Globo: Sobrepasa por encima a las plantas hasta reventar su globo
    5. Zombie Bandera: anuncia la llegada de las ordas
    ### Papapapapum 🥜
    Los zombies se acercan pero las Nueces aprendieron el arte de rodar y pueden derribar a los zombis en su trayecto. Nadie puede frenarlas, pero ellas tampoco saben como frenar...
-----
### Instalación y Requierments:
El repositorio cuenta con requirements.txt que incluye la libreria externa pygame. Se espera que el usuario tengo instalados modulos basicos como json, os, random y sys. El usuario debe ejecutar el codigo desde Main.py. 
Requisitos del sistema:
- Python 3.8 o superior
- 4 GB de RAM
- 50 MB de espacio en disco
- AMD Athlon con interfaz gráfica o superior

## Estructura del proyecto

/TPF_Lincic_Gasco_Bunge/
├── Images/            # Sprites y fondos
├── Audio/             # Música y SFX
├── Docs/              # Capturas, GIFs y README extra
├── requirements.txt   # Requerimientos del proyecto
├── README.md          # Documentación del proyecto
├── Main.py            # Lanzador y menú principal
├── Clasic_mode.py     # Modo Clásico
├── Papapapapum.py     # Modo Papapapapum
├── Gameloop.py        # Actualizaciones del bucle principal del juego
├── Plants.py          # Clases de plantas
├── zombies.py         # Clases de zombis
└── utils.py           # Helpers y constantes
