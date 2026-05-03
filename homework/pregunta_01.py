"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import numpy as np

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    # Leer el archivo CSV
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    # Eliminar la columna de índice
    df = df.drop(columns=["Unnamed: 0"])

    # Normalizar texto
    text_columns = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]
    for col in text_columns:
        df[col] = df[col].str.lower()
        df[col] = df[col].str.replace("_", " ", regex=False)
        df[col] = df[col].str.replace("-", " ", regex=False)

    # Limpiar monto_del_credito
    df["monto_del_credito"] = df["monto_del_credito"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).str.replace(r"\.00$", "", regex=True).str.strip()
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")

    # Normalizar fechas
    def parse_date(date_str):
        if pd.isna(date_str):
            return pd.NaT
        try:
            parts = date_str.split("/")
            if len(parts) == 3:
                if len(parts[0]) == 4:
                    return pd.to_datetime(date_str, format="%Y/%m/%d")
                else:
                    return pd.to_datetime(date_str, format="%d/%m/%Y")
            parts = date_str.split("-")
            if len(parts) == 3:
                if len(parts[0]) == 4:
                    return pd.to_datetime(date_str, format="%Y-%m-%d")
                else:
                    return pd.to_datetime(date_str, format="%d-%m-%Y")
        except:
            return pd.NaT

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(parse_date).dt.strftime("%Y-%m-%d")

    # Eliminar filas con valores faltantes
    df = df.dropna()

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Escribir el archivo limpio
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)
