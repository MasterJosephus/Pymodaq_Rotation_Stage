
from pathlib import Path
import clr

HERE = Path(__file__).resolve().parent
DLL_PATH = HERE / "RgbDriverKit.dll"
print(DLL_PATH)
clr.AddReference(str(DLL_PATH))

# Import namespaces from DLL
import RgbDriverKit

import System.Reflection

assembly = System.Reflection.Assembly.LoadFile(str(DLL_PATH))

for t in assembly.GetTypes():
    print(t.FullName)