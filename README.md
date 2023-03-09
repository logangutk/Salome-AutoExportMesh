# Salome-AutoExportMesh
This snipit of code will automatically export your mesh to JSON files or temp files if appended to the end of the salome dump script.

To use with a single mesh element, copy and paste the contents of ExportMesh.py to the end of the dump script. 
Run salome via TUI and call the edited script. Once loaded, Salome will export the mesh attributes and close the run terminal.


If multiple meshes are contained in the dump file, create a compound mesh named "AssemblyMesh" before dumping.


To run Salome via Terminal:
```
C://SALOME-9.10.0/run_salome.bat -t dumpScript.py
````
