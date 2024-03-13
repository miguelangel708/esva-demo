from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import QuickStart
import os


directorio_credenciales = 'credentials_module.json'

# INICIAR SESION
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

def bajar_archivo_por_id(id_drive,ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_drive}) 
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)

def show_database_info():
    carpeta = 'files'
    # Verificar si la carpeta existe
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        # Obtener la lista de archivos en la carpeta
        archivos = os.listdir(carpeta)
        # Imprimir los nombres de los archivos
        print(f"Archivos en la carpeta {carpeta}:")
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta, archivo)
            tamaño = os.path.getsize(ruta_completa)
            print(f"Archivo: {archivo} - Tamaño: {tamaño} bytes")
    else:
        print("no se encontraron archivos o no se encontró la carpeta")
    
    
def download_and_save_database():
    os.mkdir('./files')
    ruta_absoluta = os.path.abspath('./files') + '/'
    bajar_archivo_por_id('1zRpE_C7rDWdvAynNk1D9C2WrDlHlYS4p',ruta_absoluta)
    bajar_archivo_por_id('1vKXwTgrfjYq9UCsFxx6mZtgnXW0CpF2R',ruta_absoluta)
    bajar_archivo_por_id('1VNvu9-JvO1Z2dz6fXetsjCEzKudq3nrr',ruta_absoluta)
    bajar_archivo_por_id('1NJl98Yo4Lb4N2xLPvbmdG2r2gNRzjHM0',ruta_absoluta)
    bajar_archivo_por_id('1v0uP6l5S2QBVTAE2b40o-U1kVx9fwYaq',ruta_absoluta)
    show_database_info()
