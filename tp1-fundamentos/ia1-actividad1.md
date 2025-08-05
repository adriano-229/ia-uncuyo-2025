# Actividad Preliminar 1

## 1. Buscar 2 ejemplos de aplicaciones de inteligencia artificial.

### 1. **Csmart (Brasil) – Clasificación de café verde mediante visión artificial**

Csmart es una startup brasileña cuyo producto principal, el [Csmart Digit](https://www.csmart.ai/) (también llamado Csmart‑G1), combina visión por computadora, IA y análisis de datos para automatizar la clasificación de granos de café verde según estándares internacionales (como SCA) o criterios personalizados.

El dispositivo cuenta con una cámara CMOS de alta velocidad, iluminación LED integrada, alimentador electromagnético automático y un sistema embebido con GPU Nvidia Jetson Nano de 128 núcleos. Cada grano se analiza **individualmente**: forma, color, textura y defectos, construyendo una base de datos visual que permite entrenar redes neuronales con miles de imágenes etiquetadas.

El software genera informes estadísticos sobre calidad del lote (cantidad y tipo de defectos, distribución de tamaños, color dominante), comparaciones entre lotes, estimación de precios e indicadores de eficiencia operativa ([Digital Coffee Future](https://www.digitalcoffeefuture.com/magazinees/cinco-herramientas-de-ia-que-redefinen-el-panorama-del-control-de-calidad-del-cafe?utm_source=chatgpt.com "Cinco herramientas de IA que redefinen el panorama del control de calidad del café — Digital Coffee Future")). Además, al digitalizar el proceso, facilita la trazabilidad y reduce la necesidad de enviar muestras físicas a compradores —lo cual disminuye retrasos y emisiones de carbono— un impacto que ha sido aprovechado incluso por la compañía suiza Sucafina para acelerar la evaluación de café exportado.

---

### 2. **ProRuka – Control por IA de prótesis de mano usando sonomiografía**

[ProRuka](https://arxiv.org/abs/2407.19859) (2024) es una investigación que demuestra un sistema de prótesis de mano con control mediante sonomiografía (SMG): imágenes ultrasónicas de los músculos del antebrazo usadas para interpretar gestos mediante IA.

El prototipo es una mano protésica de bajo costo con seis grados de libertad (6‑DOF). Un pequeño dispositivo portátil captura imágenes ultrasónicas del antebrazo mientras el usuario realiza gestos. Un sistema de IA que combina algoritmos como K‑Nearest Neighbors, Random Forest, máquinas de soporte vectorial e incluso red neural previa VGG16 realiza clasificación y regresión para decodificar los movimientos deseados.

En pruebas offline con participantes sanos, el sistema logró identificar nueve gestos distintos con precisión del 100 %. En ensayos en tiempo real con amputados, permitió controlar la prótesis para realizar tareas cotidianas usando cuatro gestos predeterminados con alta fiabilidad.

Este enfoque basado en SMG ofrece ventajas sobre métodos tradicionales como electromiografía superficial (EMG): mayor estabilidad, menor ruido, no requiere electrodos pegados, y reduce la fatiga mental del usuario.

---

## 2. ¿Qué se entiende por **inteligencia**?

**Definición:**  
La inteligencia es la capacidad de adquirir, comprender y aplicar conocimientos, resolver problemas, adaptarse a entornos nuevos y utilizar el pensamiento abstracto, lógico y creativo.

**Etimología:**  
Proviene del latín *intelligentia*, derivado de *intelligere*, que significa “entender, comprender”, compuesto por *inter-* ("entre") y *legere* ("escoger", "leer"). Así, etimológicamente, *inteligencia* es la capacidad de elegir entre (alternativas) o de leer entre líneas.

**Fecha de aparición del término:**  
El uso del término *intelligentia* se encuentra en textos latinos clásicos, como en Cicerón (siglo I a.C.).

**Evolución del significado:**  
En la Antigüedad clásica, inteligencia estaba asociada al alma racional (Platón, Aristóteles).  
Durante la Edad Media, se vinculó al entendimiento como parte del alma inmortal (Agustín, Tomás de Aquino).  
En la modernidad, Descartes, Locke y Kant reconfiguraron la inteligencia como una facultad racional del sujeto pensante.  
A partir del siglo XX, la psicología la abordó desde perspectivas empíricas: como coeficiente intelectual (IQ), como habilidades múltiples (Gardner), o inteligencia emocional (Goleman).

**Uso:**  
Siempre ha sido un término clave en filosofía y psicología, pero su uso general se mantuvo estable hasta el siglo XX. Con el auge de la informática y la inteligencia artificial desde mediados del siglo XX, el término ganó nueva relevancia, especialmente en entornos académicos y tecnológicos.

**Impacto:**  
La inteligencia es un concepto central en educación, filosofía, psicología, neurociencia y ahora en ciencias de la computación. Define criterios de aprendizaje, adaptación, desarrollo personal y diseño de sistemas inteligentes.

---

## 3. ¿Qué se entiende por **artificial**?

**Definición:**  
Aquello que es hecho por el ser humano, imitando o sustituyendo lo natural, o creado con una intención o diseño deliberado.

**Etimología:**  
Del latín *artificialis*, derivado de *artificium* ("arte", "oficio", "habilidad manual"), que a su vez proviene de *ars* ("arte") y *facere* ("hacer"). Así, *artificial* significa "hecho con arte" o "producto del hacer humano".

**Fecha de aparición del término:**  
En castellano, aparece en el siglo XV, influido por el latín medieval. En inglés, *artificial* aparece documentado desde el siglo XIV.

**Evolución del significado:**  
Originalmente tenía una connotación positiva: algo creado con habilidad. Con la Ilustración y la Revolución Industrial, se empezó a contraponer a lo “natural”. En el siglo XX, ganó connotaciones tanto negativas (falsedad, superficialidad) como positivas (tecnología, innovación).

**Uso:**  
El uso del término creció con los avances tecnológicos. Desde mediados del siglo XX, con el desarrollo de computadoras, robótica, y síntesis de materiales, *artificial* pasó a formar parte de muchos conceptos clave, especialmente en ciencia y tecnología.

**Impacto:**  
Es central en debates sobre autenticidad, tecnología, ética, y humanidad. En disciplinas como biotecnología, filosofía de la mente, estética o IA, lo artificial confronta lo natural, abriendo interrogantes sobre qué es genuino, vivo, o consciente.

---

## 4. ¿Qué se entiende por **inteligencia artificial (IA)**?

**Definición:**  
Rama de la informática que estudia y desarrolla sistemas capaces de realizar tareas que, si fueran realizadas por humanos, requerirían inteligencia: razonamiento, aprendizaje, reconocimiento de patrones, procesamiento del lenguaje, planificación, etc.

**Etimología:**  
Combinación de *inteligencia* (ver arriba) y *artificial* (ver arriba). Literalmente, “inteligencia creada por el ser humano”.

**Fecha de creación del término:**  
El término *Artificial Intelligence* fue acuñado por John McCarthy en 1955, en una propuesta para una conferencia celebrada en 1956 en Dartmouth College, considerada el punto de partida oficial de la disciplina.

**Evolución del significado:**  
En los años 50 y 60, IA era sinónimo de programación simbólica y lógica. En los 80, se popularizaron los sistemas expertos. Desde 2000, se asocia principalmente con aprendizaje automático (*machine learning*) y redes neuronales profundas (*deep learning*).  
Hoy, IA incluye subcampos como visión por computadora, procesamiento de lenguaje natural, razonamiento automatizado, y robótica.

**Uso:**  
Ha tenido “inviernos” (fases de estancamiento), especialmente en los años 70 y finales de los 80. Desde 2010, con avances en big data, GPU y deep learning, la IA ha experimentado un auge sin precedentes. Su presencia mediática, científica y económica se ha disparado.

**Impacto:**  
Transforma sectores como medicina, transporte, finanzas, educación, arte, y seguridad. Despierta debates éticos sobre conciencia artificial, automatización laboral, sesgo algorítmico, privacidad y límites morales del diseño tecnológico.  
Además, desafía definiciones tradicionales de inteligencia, conciencia, y creatividad.

**Otras consideraciones:**  
La IA es interdisciplinaria: combina ciencias de la computación, matemática, filosofía, lingüística, neurociencia, y más. Ha motivado redefiniciones del conocimiento, de la subjetividad y de la relación humano-máquina.

---
