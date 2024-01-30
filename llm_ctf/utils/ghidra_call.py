import os
import subprocess
from pathlib import Path
from typing import Any
import tempfile
import json

SCRIPT_DIR = Path(__file__).parent.parent.parent.resolve()
GHIDRA = SCRIPT_DIR/'ghidra_11.0_PUBLIC/support/analyzeHeadless'

class Ghidra_Call:
    
    def __init__(self, sol_path, binary) -> None:
        self.sol_path = os.path.abspath(sol_path)
        self.binary = os.path.join(self.sol_path, binary)
        self.output = os.path.join(self.sol_path, "decomp")
        self.decomp_output = os.path.join(self.sol_path, "decomp", "decomp.json")
        self.disass_output = os.path.join(self.sol_path, "decomp", "disass.json")
    
    def run_ghidra(self):
        os.mkdir(self.output)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            subprocess.run(
                [GHIDRA, tmpdir, "DummyProj", "-scriptpath", Path(__file__).parent.resolve() / 'ghidra_scripts',
                    "-import", self.binary, "-postscript", "DecompileToJson.java", self.decomp_output],
                check=False, capture_output=True,
            )
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            subprocess.run(
                [GHIDRA, tmpdir, "DummyProj", "-scriptpath", Path(__file__).parent.resolve() / 'ghidra_scripts',
                 "-import", self.binary, "-postscript", "DisassembleToJson.java", self.disass_output],
                check=False, capture_output=True,
            )
            
    
    def _read_dump(self, function=None):
        if function is None:
            function = "main"
        files= os.listdir(self.output)
        s = {}  
        for file in files:
            if not os.path.isdir(file):              
                with open(os.path.join(self.output, file), 'r') as f:
                   code = json.load(f)
                   if "decomp" in file:
                       s["decomp" if "decomp" in file else "disass"] = f"{function}\n{code[function]}"        
        return s