import os
import sys
import subprocess
import time

# Cartelle e file da monitorare
PATHS_TO_WATCH = ["modules", "core", "config", "main.py"]

def get_mtime(paths):
    """Ottiene l'ultima ora di modifica di tutti i file tracciati."""
    mtimes = {}
    for path in paths:
        if os.path.isfile(path):
            mtimes[path] = os.path.getmtime(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    mtimes[full_path] = os.path.getmtime(full_path)
    return mtimes

def main():
    print("=== Tkinter Live Reload Attivo ===")
    print("Modifica i file in 'modules/' o 'config/' e premi salva per vedere i cambiamenti in tempo reale.\n")
    
    current_mtimes = get_mtime(PATHS_TO_WATCH)
    process = subprocess.Popen([sys.executable, "main.py"])

    try:
        while True:
            time.sleep(1) # Controlla ogni secondo
            new_mtimes = get_mtime(PATHS_TO_WATCH)
            
            # Se un file è stato modificato (tempo di modifica diverso)
            if new_mtimes != current_mtimes:
                print("\n[Rilevata modifica] Riavvio dell'applicazione...")
                
                # Chiude la vecchia istanza di Tkinter
                process.terminate()
                process.wait()
                
                # Aggiorna i timestamp e riavvia
                current_mtimes = new_mtimes
                process = subprocess.Popen([sys.executable, "main.py"])
                
    except KeyboardInterrupt:
        process.terminate()
        print("\nLive reload chiuso.")

if __name__ == "__main__":
    main()