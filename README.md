# PDF Auto-Rotation Tool

Questo strumento ruota automaticamente le pagine capovolte in un documento PDF utilizzando OCR per rilevare l'orientamento del testo.

## Come utilizzare questo repository

1. Vai alla scheda "Actions" di questo repository
2. Seleziona il workflow "Rotate PDF Pages" dalla lista dei workflow
3. Clicca sul pulsante "Run workflow"
4. (Opzionale) Modifica i parametri:
   - **Confidence threshold**: Soglia di confidenza per il rilevamento dell'orientamento (default: 65)
   - **DPI**: Risoluzione per la conversione del PDF in immagini (default: 200)
   - **Language**: Lingua del documento per OCR (default: ita)
5. Clicca su "Run workflow" per avviare il processo

Il workflow si interromperà dopo il primo passo. A questo punto:

1. Apri il job nella pagina di dettaglio del workflow
2. Scorri fino alla sezione "Artifacts" in basso
3. Clicca sul bottone "input-pdf-placeholder" per scaricare un file di segnaposto
4. Nella scheda "Summary" del job, clicca sul pulsante "Upload artifact"
5. Carica il tuo file PDF e assegna il nome "pdf-to-process"
6. Esegui nuovamente il workflow cliccando su "Re-run jobs"
7. Attendi che il workflow completi l'elaborazione
8. Scarica il PDF elaborato dalla sezione "Artifacts" del job completato

Il PDF elaborato avrà il suffisso "_corrected" aggiunto al nome del file originale.
