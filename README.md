# Password Strength Analyzer

## Descrizione
Tool per l'analisi della robustezza delle password. Tramite menù, è possibile valutare sia password singole che file contenenti multiple password.

## Funzionalità Principali
- Analisi di singole password
- Analisi di file con multiple password
- Sistema di punteggio da 0 a 100
- Interfaccia grafica per selezione file
- Esportazione report in formato JSON

## Criteri di Valutazione
- Lunghezza minima (12 caratteri)
- Presenza di maiuscole
- Presenza di minuscole
- Presenza di numeri
- Presenza di caratteri speciali
- Confronto con password comuni

## Requisiti Tecnici
- Python 3.x
- Librerie standard: re, json, tkinter, os
- File di testo (.txt) per input multiple password
