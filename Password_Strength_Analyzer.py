# Importazione delle librerie necessarie
import re          # Per le espressioni regolari, usate nel controllo dei pattern delle password
import json        # Per l'esportazione dei risultati in formato JSON
from typing import Dict, List  # Per il type hinting, migliora la leggibilità e il supporto IDE
import tkinter as tk           # Per l'interfaccia grafica di selezione file
from tkinter import filedialog # Per i dialog di apertura/salvataggio file
import os                      # Per operazioni sul filesystem

class PasswordAnalyzer:
    def __init__(self):
        # Lista di password comuni da controllare
        self.common_passwords = [
            "password123", "12345678", "qwerty", "admin123",
            "letmein", "welcome", "monkey123", "football"
        ]
        
    def analyze_password(self, password: str) -> Dict:
        """
        Analizza una singola password e restituisce un dizionario con score, forza e feedback
        Args:
            password: La password da analizzare
        Returns:
            Dict contenente score, strength e lista di feedback
        """
        score = 0
        feedback = []
        
        # Controllo lunghezza minima (12 caratteri)
        if len(password) >= 12:
            score += 20
            feedback.append("[OK] Lunghezza sufficiente")
        else:
            feedback.append("[X] La password dovrebbe essere lunga almeno 12 caratteri")
        
        # Controllo presenza maiuscole usando regex
        if re.search(r'[A-Z]', password):
            score += 20
            feedback.append("[OK] Contiene maiuscole")
        else:
            feedback.append("[X] Mancano lettere maiuscole")
        
        # Controllo presenza minuscole
        if re.search(r'[a-z]', password):
            score += 20
            feedback.append("[OK] Contiene minuscole")
        else:
            feedback.append("[X] Mancano lettere minuscole")
        
        # Controllo presenza numeri
        if re.search(r'\d', password):
            score += 20
            feedback.append("[OK] Contiene numeri")
        else:
            feedback.append("[X] Mancano numeri")
        
        # Controllo caratteri speciali
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 20
            feedback.append("[OK] Contiene caratteri speciali")
        else:
            feedback.append("[X] Mancano caratteri speciali")
        
        # Controllo se è una password comune
        if password.lower() in self.common_passwords:
            score = 0  # Azzera il punteggio se la password è comune
            feedback.append("[X] Password troppo comune")
        
        # Determina la forza della password basata sullo score
        strength = "Debole"
        if score >= 80:
            strength = "Forte"
        elif score >= 60:
            strength = "Media"
        
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }

    def analyze_file(self, filename: str) -> List[Dict]:
        """
        Analizza un file contenente password (una per riga)
        Args:
            filename: Percorso del file da analizzare
        Returns:
            Lista di dizionari con i risultati dell'analisi
        """
        results = []
        try:
            with open(filename, 'r') as f:
                passwords = f.read().splitlines()
                for password in passwords:
                    if password.strip():  # Salta le righe vuote
                        result = self.analyze_password(password)
                        results.append({
                            "password": password,
                            **result})
                        """ **result = Unpack del risultato dell'analisi: espande il dizionario result nella nuova struttura. 
                            Se result contiene ad es. {"score": 80, "strength": "Forte"}, 
                            l'espressione diventa equivalente a:
                            {
                                "password": password,
                                "score": 80,
                                "strength": "Forte"
                            }
                        """
                                    
        except FileNotFoundError:
            print(f"Errore: File {filename} non trovato")
        except UnicodeDecodeError:
            print("Errore: Il file contiene caratteri non supportati")
        return results

    def export_report(self, results: List[Dict], export_path: str = None):
        """
        Esporta i risultati dell'analisi in formato JSON
        Args:
            results: Lista dei risultati da esportare
            export_path: Percorso dove salvare il file JSON
        """
        if export_path is None:
            export_path = "password_report.json"
        
        try:
            # Utilizzo encoding UTF-8 per supportare caratteri speciali
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Errore durante il salvataggio: {e}")

def select_file() -> str:
    """
    Mostra una finestra di dialogo per selezionare un file
    Returns:
        Percorso del file selezionato o stringa vuota se annullato
    """
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale di tkinter
    file_path = filedialog.askopenfilename(
        title="Seleziona il file delle password",
        filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
    )
    return file_path

def select_save_location() -> str:
    """
    Mostra una finestra di dialogo per scegliere dove salvare il report
    Returns:
        Percorso dove salvare il file o stringa vuota se annullato
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Salva report JSON",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("Tutti i file", "*.*")]
    )
    return file_path

def display_results(results):
    """
    Visualizza i risultati dell'analisi in formato leggibile
    Args:
        results: Risultato singolo o lista di risultati da visualizzare
    """
    if isinstance(results, list):
        for result in results:
            print(f"\nPassword: {result['password']}")
            print(f"Punteggio: {result['score']}/100")
            print(f"Sicurezza: {result['strength']}")
            print("Feedback:")
            for item in result['feedback']:
                print(item)
    else:
        print(f"\nPunteggio: {results['score']}/100")
        print(f"Sicurezza: {results['strength']}")
        print("Feedback:")
        for item in results['feedback']:
            print(item)

def main():
    """
    Funzione principale che gestisce il menu e il flusso del programma
    """
    analyzer = PasswordAnalyzer()
    
    while True:
        # Menu principale
        print("\n--------Password Analyzer--------")
        print("1. Analizza una password")
        print("2. Analizza file di password")
        print("3. Esci")
        
        choice = input("\nScegli un'opzione (1-3): ")
        
        if choice == "1":
            # Analisi singola password
            password = input("Inserisci la password da analizzare: ")
            results = analyzer.analyze_password(password)
            display_results(results)
            
        elif choice == "2":
            # Analisi file di password
            file_path = select_file()
            if file_path:  # Se è stato selezionato un file
                results = analyzer.analyze_file(file_path)
                if results:  # Se ci sono risultati
                    display_results(results)
                    export = input("Vuoi esportare i risultati in JSON? (s/n): ")
                    if export.lower() == 's':
                        save_path = select_save_location()
                        if save_path:  # Se è stato selezionato un percorso di salvataggio
                            analyzer.export_report(results, save_path)
                            print(f"Report esportato in: {save_path}")
            
        elif choice == "3":
            break
            
        else:
            print("Scelta non valida. Riprova.")

# Entry point del programma
if __name__ == "__main__":
    main()
