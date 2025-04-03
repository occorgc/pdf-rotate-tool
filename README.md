# PDF Auto-Rotation Tool

Questo strumento ruota automaticamente le pagine capovolte in un documento PDF utilizzando OCR per rilevare l'orientamento del testo.

## Come utilizzare questo repository

### Metodo 1: Caricare un PDF tramite l'interfaccia web di GitHub

1. Vai alla cartella `pdf_input` nel repository
2. Clicca sul pulsante "Add file" e seleziona "Upload files"
3. Carica il tuo file PDF
4. Aggiungi un messaggio di commit (es. "Aggiungi PDF da elaborare")
5. Clicca su "Commit changes"
6. Il workflow di GitHub Actions si avvierà automaticamente
7. Una volta completato, il PDF elaborato sarà disponibile nella cartella `pdf_output`

### Metodo 2: Avviare manualmente il workflow

Utilizza questo metodo se hai già caricato i PDF nella cartella `pdf_input` e vuoi rielaborarli:

1. Vai alla scheda "Actions" del repository
2. Seleziona il workflow "Process PDF Files"
3. Clicca sul pulsante "Run workflow"
4. (Opzionale) Modifica i parametri:
   - **Confidence threshold**: Soglia di confidenza per il rilevamento dell'orientamento (default: 65)
   - **DPI**: Risoluzione per la conversione del PDF in immagini (default: 200)
   - **Language**: Lingua del documento per OCR (default: ita)
5. Clicca su "Run workflow" per avviare il processo
6. Una volta completato, i PDF elaborati saranno disponibili nella cartella `pdf_output`

## Parametri disponibili

- **Confidence threshold**: Valore compreso tra 0 e 100 che indica la confidenza minima richiesta per ruotare una pagina. Un valore più alto richiede una maggiore certezza prima di ruotare la pagina.
- **DPI**: Valore che determina la risoluzione usata per convertire il PDF in immagini per l'analisi OCR. Un valore più alto fornisce risultati migliori ma rallenta l'elaborazione.
- **Language**: Codice lingua per il motore OCR (es. eng per inglese, ita per italiano, fra per francese, ecc.)
