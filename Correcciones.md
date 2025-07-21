# TPF Lincic - Bunge - Gasco

## Reporte

### **General**

Los códigos del proyecto muestran un excelente nivel técnico, con una estructura modular clara y un uso efectivo muy avanzado de conceptos vistos en el aula como clases, herencia y otros que tuvieron que investigar por cuenta del grupo como eventos personalizados de Pygame y otras implementaciones concretas. La lógica es robusta, con una buena separación de responsabilidades entre entidades del juego (plantas, zombis, proyectiles, etc.). Los comentarios y docstrings estan en un buen nivel y facilitan la lectura del código incluso en funciones complejas. Sin embargo, el nivel de fragmentación y responsabilidades asignadas a cada función se mantiene inconsistente a lo largo del proyecto: algunas funciones mu extensas como `update_plants` o `plant_placement` podrían beneficiarse de una mayor segmentación para mejorar su mantenibilidad. Los nombres de las variables son en general claros y consistentes, aunque ocasionalmente se utilizan abreviaturas (`temp`, `tag`) que podrían ser más descriptivas. Un punto importante a considerar es la dependencia fuerte de rutas relativas para cargar imágenes y sonidos, lo que puede causar errores si el proyecto se ejecuta desde otro directorio. Sería recomendable verificar la existencia de los archivos y normalizar las rutas con funciones como `os.path.abspath` y asegurarse que funcionen en todos los sistemas operativos. Tuve que modifica un par de rutas para que funcione correctamente.

Por otro lado, el repositorio está muy bien organizado, con una estructura de carpetas lógica que separa recursos (`Images`, `Audio`, `Docs`) del código fuente. La documentación en el `README.md` es clara, incluye descripciones de los modos de juego, requisitos, instrucciones de uso y detalles sobre las plantas y zombis, lo que lo hace accesible tanto para docentes como para otros estudiantes. En conjunto, el proyecto está presentado con un muy buen nivel y transmite la dedicación y comprensión profunda de los conceptos vistos en clase y los que tuvieron que ver por su cuenta.

**Puntos positivos:**

* Entrega completa y algo más: dos modos de juego implementados con mecánicas distintas.
* Excelente uso de documentación dentro del código y un `README.md` bien redactado, detallando tanto modos como instrucciones.
* Código modular, estructurado en archivos independientes con roles bien definidos.
* Se nota bastante el trabajo grupal colaborativo. Quizás demasiado.

**Aspectos a mejorar:**

* Aunque la estructura es modular, hay cierta repetición entre los modos que podría encapsularse mejor.
* La carga y gestión de archivos (imágenes, sonidos) está muy atada a rutas relativas sin verificación de errores (si falta un asset, crashea D:).

**Recomendaciones:**

* Incluir manejo de errores al cargar archivos externos (con mensajes claros).
* Añadir en el `README` alguna descripción sobre decisiones de diseño, estructuras de datos y distribución de tareas.

---

### **Backend**

**Puntos positivos:**

* Excelente uso de las herencias entre clases (ej. `Plants`, `Boomerang`, `PeaShooter`), con separación clara entre entidades. Incluso las herencias de herencias están bien pensadas e implementadas.
* Estructura bien pensada para `update_*` del `Gameloop`, delegando responsabilidades específicas. Muy buena modularización general.
* Implementación de eventos personalizados (`pygame.USEREVENT + n`) bien aprovechada. Uso de componentes avanzados y complejos de la librería.

**Aspectos a mejorar:**

* La lógica para la creación de oleadas de zombis está duplicada en ambos modos de juego y podría unificarse, liberarían espacio y podría pensarse como algo modular para expandir y crear nuevos niveles.
* Algunas funciones (`plant_placement`, `update_plants`) son extensas y podrían beneficiarse de mayor subdivisión o simplificación.
* Usar alguna lógica más concreta y evitar anidar tantos condicionales.

**Recomendaciones:**

* Considerar una clase controladora para las oleadas y eventos comunes entre modos.

---

### **Frontend**

**Puntos positivos:**

* Interfaz visual muy atractiva y original, con uso de fuentes personalizadas, cursores gráficos, y HUD funcional.
* El pixelart esta excelentemente logado y da una sensación de inmmersión muy linda.
* Gran detalle el agregado de zombies docentes.
* El menú principal es dinámico, con soporte de pantalla completa y botones interactivos con hover. Da una sensación de juego completo de alto nivel.
* El feedback visual y la interacción son muy fluidos.

**Recomendaciones:**

* Mostrar un mensaje claro cuando no se pueden plantar por falta de soles o cooldown.

---

### **Extras**

**Puntos positivos:**

* Implementación de un modo **Papapapapum**, con mecánicas nuevas, cinta transportadora y nueces giratorias. Este nuevo sistema está inspirado en el juego original y es un extra muy bienvenido.
* Incorporación de efectos de sonido, múltiples tipos de zombis, y variaciones reales de juego.
* Comentarios detallados en todas las clases y funciones, con explicaciones bien centradas.
