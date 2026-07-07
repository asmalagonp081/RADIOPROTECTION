import pandas as pd
import numpy as np
import sys
import os

def parse_header(header_filepath):
    """
    Lee y parsea el archivo .header de TOPAS para extraer información sobre el formato
    y las columnas del archivo .phsp.
    """
    if not os.path.exists(header_filepath):
        print(f"Error: El archivo {header_filepath} no existe.")
        return None

    header_info = {
        'Byte order': None,
        'Format': None,
        'Columns': []
    }

    try:
        with open(header_filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('Byte order of each record is'):
                    header_info['Byte order'] = line.split('is')[-1].strip()
                elif 'TOPAS ASCII Phase Space' in line:
                    header_info['Format'] = 'ASCII'
                elif 'TOPAS Binary Phase Space' in line:
                    header_info['Format'] = 'Binary'
                elif line.startswith('Column'):
                    # Ejemplo: Column 1: Position X [cm]
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        col_name = parts[1].strip()
                        header_info['Columns'].append(col_name)
                # Fallback format for columns if it matches standard patterns
                elif 'Position X' in line and not line.startswith('Column'):
                     header_info['Columns'].append(line.strip())
        return header_info
    except Exception as e:
         print(f"Error parseando el archivo de header: {e}")
         return None

def read_phsp(header_filepath, phsp_filepath):
    """
    Lee los archivos .header y .phsp y devuelve un DataFrame de pandas.
    Soporta formato ASCII según la configuración del archivo .header.
    """
    header_info = parse_header(header_filepath)

    if not header_info:
        print("No se pudo obtener información del header. Se asume formato ASCII por defecto.")
        # Try to read as ASCII anyway if possible
        try:
             df = pd.read_csv(phsp_filepath, sep=r'\s+', header=None)
             print(f"Leído {len(df)} filas del archivo phsp asumiendo ASCII sin header explícito.")
             return df
        except pd.errors.EmptyDataError:
             print("El archivo phsp está vacío.")
             return pd.DataFrame()
        except Exception as e:
             print(f"Error leyendo el archivo phsp: {e}")
             return None

    columns = header_info.get('Columns', [])

    if header_info.get('Format') == 'ASCII' or header_info.get('Format') is None:
        # Default to ASCII reading if Binary is not explicitly specified, as per output type in Source file
        print(f"Leyendo archivo .phsp en formato ASCII desde {phsp_filepath}")
        try:
            if columns:
                df = pd.read_csv(phsp_filepath, sep=r'\s+', names=columns)
            else:
                df = pd.read_csv(phsp_filepath, sep=r'\s+', header=None)
            return df
        except pd.errors.EmptyDataError:
             print("El archivo phsp está vacío.")
             return pd.DataFrame(columns=columns)
        except Exception as e:
            print(f"Error leyendo el archivo ASCII .phsp: {e}")
            return None
    elif header_info.get('Format') == 'Binary':
         print(f"Formato Binario detectado. (No implementado en esta versión básica).")
         return None

if __name__ == "__main__":
    if len(sys.argv) == 3:
        header_file = sys.argv[1]
        phsp_file = sys.argv[2]
        df = read_phsp(header_file, phsp_file)
        if df is not None:
             print("\nPrimeras 5 filas del Phase Space:")
             print(df.head())
    else:
        print("Uso: python read_phsp.py <archivo.header> <archivo.phsp>")
