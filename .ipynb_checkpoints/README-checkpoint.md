# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Oriol López Miret

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`
```` python
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Convierte un fichero WAVE estéreo a mono.
    
    canal=0: canal izquierdo
    canal=1: canal derecho  
    canal=2: semisuma (L+R)/2
    canal=3: semidiferencia (L-R)/2

    Args:
        ficEste, ficMono (str): Nombres de los archivos respectivos.
        canal (int): Valor para escojer el tipo de archivo desado.

    Returns:
        Convierte el archivo estereo (ficEste) en un archivo mono (ficMono).
    """
    header = Header(ficEste)
    
    # Validar que es estéreo
    if header["NumChannels"] != 2:
        raise ValueError("El fichero debe ser estéreo (2 canales)")
    
    # Validar que es PCM de 16 bits
    if header["AudioFormat"] != 1:
        raise ValueError("Solo se soporta PCM lineal")
    if header["BitsPerSample"] != 16:
        raise ValueError("Solo se soportan muestras de 16 bits")

    muestras = []
    
    with open(ficEste, "rb") as fpWAVE:
        # Saltar la cabecera (44 bytes para PCM estándar)
        fpWAVE.seek(44)
        
        # Leer datos del cacho data (tamaño en header["SubChunkDataSize"])
        data_size = header["SubChunkDataSize"]
        bytes_leidos = 0
        
        while bytes_leidos < data_size:
            left_bytes = fpWAVE.read(2)
            right_bytes = fpWAVE.read(2)
            
            if len(left_bytes) < 2 or len(right_bytes) < 2:
                break
                
            left = st.unpack("<h", left_bytes)[0]
            right = st.unpack("<h", right_bytes)[0]
            
            if canal == 0:
                out = left
            elif canal == 1:
                out = right
            elif canal == 2:
                out = (left + right) // 2
            elif canal == 3:
                out = (left - right) // 2
            else:
                raise ValueError("canal debe ser 0, 1, 2 o 3")
            
            muestras.append(out)
            bytes_leidos += 4  # 2 bytes por canal
    
    # Crear archivo de salida
    with open(ficMono, "wb") as fpOUT:
        header_mono = crear_header_mono(header, len(muestras))
        fpOUT.write(header_mono)
        
        for muestra in muestras:
            fpOUT.write(st.pack("<h", muestra))
````

##### Código de `mono2estereo()`
```` python
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Combina dos ficheros mono en un fichero estéreo.

    Args:
        ficIzq, ficDer, ficEste (str): Nombre de los archivos correspondientes.

    Returns:
        Junta el archivo mono izquierdo (ficIzq) con el derecho (ficDer) en el archivo estereo (ficEste).
    """
    header_izq = Header(ficIzq)
    header_der = Header(ficDer)
    
    # Validaciones
    if header_izq["NumChannels"] != 1 or header_der["NumChannels"] != 1:
        raise ValueError("Los ficheros deben ser mono")
    
    if header_izq["AudioFormat"] != 1 or header_der["AudioFormat"] != 1:
        raise ValueError("Solo se soporta PCM lineal")
    
    if header_izq["BitsPerSample"] != 16 or header_der["BitsPerSample"] != 16:
        raise ValueError("Solo se soportan muestras de 16 bits")
    
    if header_izq["SampleRate"] != header_der["SampleRate"]:
        raise ValueError("Las frecuencias de muestreo deben coincidir")
    
    if header_izq["SubChunkDataSize"] != header_der["SubChunkDataSize"]:
        raise ValueError("Los ficheros deben tener la misma longitud")
    
    # Leer datos de ambos canales
    with open(ficIzq, "rb") as fpIZQ, open(ficDer, "rb") as fpDER:
        fpIZQ.seek(44)
        fpDER.seek(44)
        
        data_size = header_izq["SubChunkDataSize"]
        num_muestras = data_size // 2  
        
        muestras_estereo = []
        
        for _ in range(num_muestras):
            left_bytes = fpIZQ.read(2)
            right_bytes = fpDER.read(2)
            
            if len(left_bytes) < 2 or len(right_bytes) < 2:
                break
                
            left = st.unpack("<h", left_bytes)[0]
            right = st.unpack("<h", right_bytes)[0]
            
            muestras_estereo.append(left)
            muestras_estereo.append(right)
    
    # Crear fichero estéreo
    with open(ficEste, "wb") as fpOUT:
        header_este = crear_header_estereo(header_izq, len(muestras_estereo) // 2)
        fpOUT.write(header_este)
        
        for m in muestras_estereo:
            fpOUT.write(st.pack("<h", m))
````

##### Código de `codEstereo()`
```` python
def codEstereo(ficEste, ficCod):
    """
    Codifica una señal estéreo de 16 bits en una señal de 32 bits.
    Los 16 bits MSB contienen la semisuma, los 16 bits LSB la semidiferencia.

    Args:
        ficEste, ficCod (str): Nombre de los archivos correspondientes.

    Returns:
        Devuelve el archivo codificado.
    """
    header = Header(ficEste)
    
    if header["NumChannels"] != 2:
        raise ValueError("El fichero debe ser estéreo")
    if header["AudioFormat"] != 1:
        raise ValueError("Solo se soporta PCM lineal")
    if header["BitsPerSample"] != 16:
        raise ValueError("Solo se soportan muestras de 16 bits")
    
    # Leer muestras estéreo
    samples = []
    with open(ficEste, "rb") as fp:
        fp.seek(44)
        data_size = header["SubChunkDataSize"]
        bytes_leidos = 0
        
        while bytes_leidos < data_size:
            left_bytes = fp.read(2)
            right_bytes = fp.read(2)
            
            if len(left_bytes) < 2 or len(right_bytes) < 2:
                break
            
            left = st.unpack("<h", left_bytes)[0]
            right = st.unpack("<h", right_bytes)[0]
            samples.append((left, right))
            bytes_leidos += 4
    
    # Calcular semisuma y semidiferencia
    codificado = []
    for left, right in samples:
        semisuma = (left + right) // 2
        semidif = (left - right) // 2
        
        # Empaquetar en 32 bits: MSB = semisuma (16 bits), LSB = semidif (16 bits)
        valor_32 = ((semisuma & 0xFFFF) << 16) | (semidif & 0xFFFF)
        codificado.append(valor_32)
        
    with open(ficCod, "wb") as fp:
        # Crear header manualmente para 32 bits
        sample_rate = header["SampleRate"]
        bits = 32
        num_muestras = len(codificado)
        byte_rate = sample_rate * 1 * bits // 8
        block_align = 1 * bits // 8
        subchunk2 = num_muestras * block_align
        chunk_size = 36 + subchunk2
        
        # RIFF
        fp.write(b"RIFF")
        fp.write(st.pack("<I", chunk_size))
        fp.write(b"WAVE")
        
        # FMT
        fp.write(b"fmt ")
        fp.write(st.pack("<I", 16))
        fp.write(st.pack("<H", 1))
        fp.write(st.pack("<H", 1))  # 1 canal
        fp.write(st.pack("<I", sample_rate))
        fp.write(st.pack("<I", byte_rate))
        fp.write(st.pack("<H", block_align))
        fp.write(st.pack("<H", bits))
        
        # DATA
        fp.write(b"data")
        fp.write(st.pack("<I", subchunk2))
        
        # Escribir datos codificados
        for val in codificado:
            fp.write(st.pack("<I", val))
````

##### Código de `decEstereo()`
```` python
def decEstereo(ficCod, ficEste):
    """
    Decodifica una señal codificada y recupera la señal estéreo original.

    Args:
        ficCod, ficEste (str): Nombre de los archivos correspondientes.

    Returns:
        Devuelve el archivo estereo sin codificar.
    """
    header = Header(ficCod)
    
    if header["NumChannels"] != 1:
        raise ValueError("El fichero codificado debe ser mono")
    if header["BitsPerSample"] != 32:
        raise ValueError("El fichero codificado debe tener muestras de 32 bits")
    
    # Leer datos codificados
    codificado = []
    with open(ficCod, "rb") as fp:
        fp.seek(44)
        data_size = header["SubChunkDataSize"]
        num_muestras = data_size // 4  # 4 bytes por muestra
        
        for _ in range(num_muestras):
            val_bytes = fp.read(4)
            if len(val_bytes) < 4:
                break
            val = st.unpack("<i", val_bytes)[0]
            codificado.append(val)
    
    # Decodificar
    izquierdo = []
    derecho = []
    
    for val in codificado:
        semisuma = (val >> 16) & 0xFFFF
        semidif = val & 0xFFFF
        
        # Convertir a signed de 16 bits
        if semisuma >= 32768:
            semisuma -= 65536
        if semidif >= 32768:
            semidif -= 65536
        
        # Reconstruir canales
        L = semisuma + semidif
        R = semisuma - semidif
        
        # Limitar al rango de 16 bits
        L = max(-32768, min(32767, L))
        R = max(-32768, min(32767, R))
        
        izquierdo.append(L)
        derecho.append(R)
    
    # Crear fichero estéreo
    with open(ficEste, "wb") as fp:
        sample_rate = header["SampleRate"]
        bits = 16
        num_muestras = len(izquierdo)
        byte_rate = sample_rate * 2 * bits // 8
        block_align = 2 * bits // 8
        subchunk2 = num_muestras * block_align
        chunk_size = 36 + subchunk2
        
        # RIFF
        fp.write(b"RIFF")
        fp.write(st.pack("<I", chunk_size))
        fp.write(b"WAVE")
        
        # FMT
        fp.write(b"fmt ")
        fp.write(st.pack("<I", 16))
        fp.write(st.pack("<H", 1))
        fp.write(st.pack("<H", 2))  # 2 canales
        fp.write(st.pack("<I", sample_rate))
        fp.write(st.pack("<I", byte_rate))
        fp.write(st.pack("<H", block_align))
        fp.write(st.pack("<H", bits))
        
        # DATA
        fp.write(b"data")
        fp.write(st.pack("<I", subchunk2))
        
        # Escribir datos intercalados
        for L, R in zip(izquierdo, derecho):
            fp.write(st.pack("<h", L))
            fp.write(st.pack("<h", R))
````
##### Codigo Extra utilizado en las funciones principales: (`lectura()` / `Header()` / `crear_header_mono()` / `crear_header_estereo()`)
```` python
def lectura(formato, file):
    """
    Pequeña funcion para hacer más limpio el codigo a la hora de leer en el header.

    Args:
        formato (str): formato para con el que se lee la cadena de bits.
        file (str): nombre del archivo WAVE.

    Returns:
        Devuelve la información en su respectivo formato.
    """
    return st.unpack(formato, file.read(st.calcsize(formato)))[0]

def Header(file):
    """
    Permite desglosar el header de cualquier archivo WAVE.

    Args:
        file (str): nombre del archivo WAVE.

    Returns:
        header (dic): diccionario con todo el header guardado con su respectivo nombre.
    """
    with open(file, "rb") as fpWAVE:
        header = {}

        # RIFF
        header["ChunkId"]          = fpWAVE.read(4).decode("ASCII")
        header["ChunkSize"]        = lectura("<I", fpWAVE)
        header["Format"]           = fpWAVE.read(4).decode("ASCII")
    
        # FMT
        header["SubChunkFmtId"]    = fpWAVE.read(4).decode("ASCII")
        header["SubChunkFmtSize"]  = lectura("<I", fpWAVE)
        header["AudioFormat"]      = lectura("<H", fpWAVE)
        header["NumChannels"]      = lectura("<H", fpWAVE)
        header["SampleRate"]       = lectura("<I", fpWAVE)
        header["ByteRate"]         = lectura("<I", fpWAVE)
        header["BlockAlign"]       = lectura("<H", fpWAVE)
        header["BitsPerSample"]    = lectura("<H", fpWAVE)
    
        # DATA
        header["SubChunkDataId"]   = fpWAVE.read(4).decode("ASCII")
        header["SubChunkDataSize"] = lectura("<I", fpWAVE)

        return header

def crear_header_mono(header_original, num_muestras):
    """
    Mediante el header del archivo original, se genera uno nuevo para archivos mono.

    Args:
        header_original (dic): Diccionario con el header del archivo estereo que se quiere convertir.
        num_muestras (int): Numero de muestras del archivo.

    Returns:
        header (bytarray): Cadena de bits en orden con todo el header almazenado.
    """
    header = bytearray()

    # Parámetros originales
    sample_rate = header_original["SampleRate"]
    bits = header_original["BitsPerSample"]
    byte_rate = sample_rate * 1 * bits // 8
    block_align = 1 * bits // 8
    subchunk2 = num_muestras * block_align
    chunk_size = 36 + subchunk2

    # RIFF
    header += b"RIFF"
    header += st.pack("<I", chunk_size)
    header += b"WAVE"

    # FMT
    header += b"fmt "
    header += st.pack("<I", 16)              
    header += st.pack("<H", 1)               
    header += st.pack("<H", 1)               
    header += st.pack("<I", sample_rate)
    header += st.pack("<I", byte_rate)
    header += st.pack("<H", block_align)
    header += st.pack("<H", bits)

    # DATA
    header += b"data"
    header += st.pack("<I", subchunk2)

    return header

def crear_header_estereo(header_original, num_muestras):
    """
    Mediante el header del archivo original, se genera uno nuevo para archivos estereo.

    Args:
        header_original (dic): Diccionario con el header del archivo que se quiere convertir.
        num_muestras (int): Numero de muestras del archivo.

    Returns:
        header (bytarray): Cadena de bits en orden con todo el header almazenado.
    """
    header = bytearray()

    # Parámetros originales
    sample_rate = header_original["SampleRate"]
    bits = header_original["BitsPerSample"]
    byte_rate = sample_rate * 2 * bits // 8
    block_align = 2 * bits // 8
    subchunk2 = num_muestras * block_align
    chunk_size = 36 + subchunk2

    # RIFF
    header += b"RIFF"
    header += st.pack("<I", chunk_size)
    header += b"WAVE"

    # FMT
    header += b"fmt "
    header += st.pack("<I", 16)              
    header += st.pack("<H", 1)               
    header += st.pack("<H", 2)               
    header += st.pack("<I", sample_rate)
    header += st.pack("<I", byte_rate)
    header += st.pack("<H", block_align)
    header += st.pack("<H", bits)

    # DATA
    header += b"data"
    header += st.pack("<I", subchunk2)

    return header

````

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
