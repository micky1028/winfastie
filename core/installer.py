import subprocess
import logging

class SystemInstaller:
    @staticmethod
    def install_via_winget(package_id: str):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # Sfruttiamo PowerShell per un'esecuzione pulita e dettagliata senza finestre nere esterne
        command = [
            "powershell", "-NoProfile", "-Command",
            f"winget install --id {package_id} --silent --accept-package-agreements --accept-source-agreements"
        ]
        
        yield f"Starting PowerShell stream for {package_id}..."
        
        try:
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding="utf-8", 
                errors="ignore",
                startupinfo=startupinfo
            )
            
            for line in process.stdout:
                clean_line = line.strip()
                if clean_line:
                    yield clean_line
                    
            process.wait()
            
            if process.returncode == 0:
                yield f"Successfully installed {package_id}"
            else:
                yield f"Finished with code {process.returncode}"
                
        except Exception as e:
            yield f"Error: {str(e)}"