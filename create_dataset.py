import pandas as pd
import numpy as np
import sys
import os
from read_phsp import parse_header, read_phsp

def create_dataset(header_filepath, phsp_filepath, output_filename="dataset_dosis_energia.csv"):
    """
    Lee un archivo phase space de TOPAS y crea un dataset con la energía y calcula dosis.
    Si los archivos están vacíos o no existen, usa los datos mock como contingencia,
    pero procesa los verdaderos si están presentes.
    """
    df_phsp = None

    if os.path.exists(header_filepath) and os.path.exists(phsp_filepath) and os.path.getsize(phsp_filepath) > 0:
        print(f"Leyendo datos reales de {phsp_filepath}...")
        df_phsp = read_phsp(header_filepath, phsp_filepath)

    if df_phsp is not None and not df_phsp.empty:
        # Check if 'Energy' or similar is in columns
        energy_col = None
        for col in df_phsp.columns:
            if isinstance(col, str) and ('Energy' in col or 'energy' in col):
                energy_col = col
                break

        if energy_col:
             # Calculate dose based on energy (proportional for demonstration, as actual dose
             # depends on mass and volume of scoring region)
             # Dose (Gy) = Energy (J) / Mass (kg). 1 MeV = 1.602e-13 J.
             # Assuming a 1g scoring volume for demonstration: Mass = 0.001 kg
             mass_kg = 0.001
             mev_to_joules = 1.602e-13

             energia_depositada = df_phsp[energy_col]
             dosis = (energia_depositada * mev_to_joules) / mass_kg

             df = pd.DataFrame({
                 'Energia_Total_Depositada_MeV': energia_depositada,
                 'Dosis_Gy': dosis
             })

             # Optionally keep position columns if they exist
             pos_cols = [c for c in df_phsp.columns if isinstance(c, str) and ('Position' in c or 'X' in c or 'Y' in c or 'Z' in c)]
             for c in pos_cols:
                  df[c] = df_phsp[c]

             print("Datos extraídos del Phase Space real.")
        else:
             print("No se encontró columna de energía. Usando toda la data.")
             df = df_phsp
    else:
        print(f"Archivos phase space vacíos o no encontrados. Generando 1000 muestras de datos simulados para demostración...")
        # Generar datos aleatorios simulando los resultados
        num_samples = 1000
        energia_depositada = np.random.uniform(0.0, 10.0, num_samples)

        # Dosis en Gy (por ejemplo, proporcional a la energía pero escalada)
        mass_kg = 0.001
        mev_to_joules = 1.602e-13
        dosis = (energia_depositada * mev_to_joules) / mass_kg

        # Crear un DataFrame
        df = pd.DataFrame({
            'Evento_ID': np.arange(1, num_samples + 1),
            'Energia_Total_Depositada_MeV': energia_depositada,
            'Dosis_Gy': dosis
        })

    # Guardar en CSV
    df.to_csv(output_filename, index=False)
    print(f"Dataset creado exitosamente: {output_filename}")

    # Mostrar las primeras filas
    print("\nPrimeras 5 filas del dataset:")
    print(df.head())

if __name__ == "__main__":
    header_file = "Source/PhaseSpace_Galactic.header"
    phsp_file = "Source/PhaseSpace_Galactic.phsp"
    output_file = "dataset_dosis_energia.csv"

    if len(sys.argv) == 4:
        header_file = sys.argv[1]
        phsp_file = sys.argv[2]
        output_file = sys.argv[3]
    elif len(sys.argv) > 1:
        print("Uso: python create_dataset.py [archivo.header archivo.phsp salida.csv]")
        print("Usando valores por defecto.")

    create_dataset(header_file, phsp_file, output_file)
