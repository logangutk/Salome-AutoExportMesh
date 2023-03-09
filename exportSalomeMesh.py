def ExportScript(AssemblyMesh):
    import sys
    import SMESH
    from salome.smesh import smeshBuilder
    import os, time
    import json

    debug = 1
    verify = False

    def ExportMeshToJSON(mesh, dirname="SalomeToVMAP"):
        """
        VMAP meshing consists of the following containers

        """
        tstart = time.time()

        # Mesh: Nodes
        points = mesh.GetNodesId()
        VMAP_meshNodes = {}
        for n, ni in enumerate(points):
            pos = mesh.GetNodeXYZ(ni)

            ## VMAP FORMAT
            VMAP_meshNodes["Node-" + str(ni)] = [pos[0], pos[1], pos[2]]

        # # Mesh: Elements
        elems = mesh.GetElementsId()
        VMAP_meshElements = {}
        for e, ei in enumerate(elems):
            con = mesh.GetElemNodes(ei)
            # 1D elements
            if len(con) == 2:
                #         ## VMAP FORMAT
                VMAP_meshElements["Element-" + str(ei)] = [con[0], con[1]]
            #     #2D elements
            if len(con) == 4:
                #         ## VMAP FORMAT
                VMAP_meshElements["Element-" + str(ei)] = [
                    con[0],
                    con[1],
                    con[2],
                    con[3],
                ]
            #     #3D elements
            if len(con) == 8:
                #         ## VMAP FORMAT
                VMAP_meshElements["Element-" + str(ei)] = [
                    con[0],
                    con[1],
                    con[2],
                    con[3],
                    con[4],
                    con[5],
                    con[6],
                    con[7],
                ]

        # Mesh: Sets/Groups
        # setID = enumerated index of set in list
        # setName = manual name of set
        # setTypes = elements (3D), elementBoundaries (2D), and 1D
        # setIndexTypes =
        # SetData = elements for set
        instance = 1
        instancelist = []
        i = 1
        sets = {}
        for group in mesh.GetGroups():
            SetName = group.GetName()
            SetData = tuple(group.GetIDs())
            if group.GetType() == SMESH.VOLUME:  # 3D group (component)
                SetTypes = "elements"
                setIndexTypes = "TBD"

            if group.GetType() == SMESH.FACE:  # 2D group (Boundary)
                SetTypes = "elementBoundaries"
                setIndexTypes = "TBD"
            instancelist.append([i, SetName, SetTypes, setIndexTypes, SetData])
            sets[instance] = instancelist
            i = i + 1

        #   os.chdir(tempFilePath)

        ### Writing out nodes, elements, and sets to temp files, and temp file directory links to JSON file
        tempfileNames = []
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as nodefile:
            json.dump(obj=VMAP_meshNodes, fp=nodefile)
            tempfileNames.append(nodefile.name)
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as elementfile:
            json.dump(obj=VMAP_meshElements, fp=elementfile)
            tempfileNames.append(elementfile.name)
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as setsfile:
            json.dump(obj=sets, fp=setsfile)
            tempfileNames.append(setsfile.name)

        with open("tempLocations.json", "w") as f:
            f.write(json.dumps(tempfileNames))


        # Un-comment if you want JSON files with mesh contents
        # with open('MeshNodes.json','w') as f:
        #     f.write(json.dumps(VMAP_meshNodes))
        # with open('MeshElements.json','w') as f:
        #     f.write(json.dumps(VMAP_meshElements))
        # with open('MeshSets.json', 'w') as f:
        #     f.write(json.dumps(sets))

    def __debugPrint__(msg, level=1):
        """Print only if level >= debug"""
        if debug >= level:
            print(msg)

    def findSelectedMeshes():
        meshes = list()
        smesh = smeshBuilder.New()
        nrSelected = salome.sg.SelectedCount()  # Total Number of selected items

        foundMesh = False
        for i in range(nrSelected):
            selected = salome.sg.getSelected(i)  # 0:1:2:3
            selobjID = salome.myStudy.FindObjectID(selected)
            selobj = selobjID.GetObject()
            if (
                selobj.__class__ == SMESH._objref_SMESH_Mesh
                or selobj.__class__ == salome.smesh.smeshBuilder.meshProxy
            ):
                mName = selobjID.GetName().replace(" ", "_")
                foundMesh = True
                mesh = smesh.Mesh(selobj)
                meshes.append(mesh)

            if not foundMesh:
                print("Error: Mesh is not selected.")
                return list()
            else:
                return meshes

    def main(meshes):
        """
        Exporting selected mesh to file

        """
        #   print(meshes)
        #   for mesh in meshes:
        # if not meshes == None:
        mName = meshes.GetName()
        outdir = os.getcwd() + "/" + mName
        __debugPrint__("Exporting " + mName + " mesh to " + outdir + "\n", 1)
        ExportMeshToJSON(meshes, outdir)

    main(AssemblyMesh)
    return


ExportScript(AssemblyMesh)
