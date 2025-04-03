import os
import sys
import argparse
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
from pdf2image import convert_from_path
import numpy as np
from tqdm import tqdm

def parse_arguments():
    """Analizza gli argomenti da linea di comando."""
    parser = argparse.ArgumentParser(description='Ruota automaticamente le pagine capovolte in un PDF.')
    parser.add_argument('input_pdf', help='Percorso del file PDF di input')
    parser.add_argument('-o', '--output', help='Percorso del file PDF di output. Se non specificato, verrà aggiunto "_corrected" al nome del file di input.')
    parser.add_argument('-c', '--confidence', type=float, default=65.0, help='Livello di confidenza minima (percentuale) per considerare una pagina come orientata correttamente. Default: 65.0')
    parser.add_argument('-d', '--dpi', type=int, default=200, help='DPI per la conversione delle pagine PDF in immagini. Valori più alti migliorano la precisione ma richiedono più memoria. Default: 200')
    return parser.parse_args()

def get_output_path(input_path, output_path=None):
    """Genera il percorso del file di output."""
    if output_path:
        return output_path
    
    directory = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    return os.path.join(directory, f"{name}_corrected{ext}")

def detect_orientation(image, i, total):
    """
    Rileva l'orientamento di una pagina usando OCR.
    Restituisce un valore di confidenza per ogni orientamento (0, 90, 180, 270).
    """
    print(f"\rAnalisi pagina {i+1}/{total}...", end="", flush=True)
    
    try:
        # Analisi OCR con orientamento automatico
        osd = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
        return osd
    except pytesseract.TesseractError as e:
        print(f"\nErrore OCR nella pagina {i+1}: {str(e)}")
        # In caso di errore, presumi che la pagina sia orientata correttamente
        return {'orientation': 0, 'orientation_conf': 0.0}

def should_rotate(osd_data, confidence_threshold):
    """
    Determina se una pagina deve essere ruotata in base ai dati OCR.
    Restituisce l'angolo di rotazione necessario.
    """
    # Se la confidenza è bassa, non ruotare (lasciare com'è)
    if osd_data['orientation_conf'] < confidence_threshold:
        return 0
    
    # Se l'orientamento rilevato è 180°, dobbiamo ruotare
    if osd_data['orientation'] == 180:
        return 180
    
    # In tutti gli altri casi, lasciamo la pagina com'è
    return 0

def rotate_pdf(input_path, output_path, confidence_threshold, dpi):
    """
    Analizza ogni pagina del PDF e ruota quelle che sono capovolte.
    """
    # Carica il PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()
    num_pages = len(reader.pages)
    
    print(f"Analisi di {num_pages} pagine del PDF...")
    
    # Converti le pagine PDF in immagini
    try:
        images = convert_from_path(input_path, dpi=dpi)
    except Exception as e:
        print(f"Errore nella conversione del PDF in immagini: {str(e)}")
        print("Assicurati di avere 'poppler' installato sul tuo sistema.")
        return False
    
    if len(images) != num_pages:
        print(f"Avviso: Il numero di immagini convertite ({len(images)}) non corrisponde al numero di pagine nel PDF ({num_pages}).")
    
    # Lista per tenere traccia delle pagine da ruotare
    pages_to_rotate = []
    
    # Analizza ogni pagina
    for i, image in enumerate(images):
        osd_data = detect_orientation(image, i, len(images))
        rotation_angle = should_rotate(osd_data, confidence_threshold)
        
        if rotation_angle != 0:
            pages_to_rotate.append(i)
    
    print("\n")  # Nuova riga dopo la barra di progresso
    
    # Se non ci sono pagine da ruotare, copia semplicemente il PDF
    if not pages_to_rotate:
        print("Nessuna pagina capovolta rilevata.")
        with open(output_path, 'wb') as output_file:
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.write(output_file)
        return True
    
    # Ruota le pagine necessarie e crea il nuovo PDF
    print(f"Rotazione di {len(pages_to_rotate)} pagine capovolte...")
    for i, page in tqdm(enumerate(reader.pages), total=num_pages, desc="Creazione PDF"):
        if i in pages_to_rotate:
            page.rotate(180)
        writer.add_page(page)
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"PDF corretto salvato in: {output_path}")
    print(f"Pagine ruotate: {len(pages_to_rotate)}")
    if pages_to_rotate:
        print(f"Numeri di pagina ruotate: {[p+1 for p in pages_to_rotate]}")
    return True

def main():
    """Funzione principale."""
    args = parse_arguments()
    
    input_path = args.input_pdf
    output_path = get_output_path(input_path, args.output)
    confidence_threshold = args.confidence
    dpi = args.dpi
    
    if not os.path.exists(input_path):
        print(f"Errore: Il file '{input_path}' non esiste.")
        return 1
    
    print(f"Elaborazione del file: {input_path}")
    print(f"Il file corretto sarà salvato in: {output_path}")
    print(f"Livello di confidenza minimo: {confidence_threshold}%")
    
    success = rotate_pdf(input_path, output_path, confidence_threshold, dpi)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
