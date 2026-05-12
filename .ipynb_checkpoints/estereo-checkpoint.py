"""
Autor: Oriol López Miret

Descripción:
    - Contiene las 4 funciones principales (estero2mono / mono2estereo / codEstereo / decEstereo).
    - Funciones para poder leer los Headers (lectura / Header)
    - Funciones para poder añadir los headers al archivo binario (crear_header_mono / crear_header_estereo)
"""

import struct as st

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
