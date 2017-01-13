import arcpy
import arcpy_metadata


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Metadata"
        self.alias = "Metadata"

        # List of tool classes associated with this toolbox
        self.tools = [MXDMetadata]


class MXDMetadata(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "MxdMetadata"
        self.description = "Update layer metadata using its data source"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input MXD",
            name="in_gdbs",
            datatype="DEMapDocument",
            parameterType="Required",
            direction="Input")

        #param0.filter.type = "File"
        #param0.filter.list = ["mxd"]
        #param0.value = "CURRENT"

        params = [param0]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        mxd_path = parameters[0].valueAsText

        mxd = arcpy.mapping.MapDocument(mxd_path)

        layers = arcpy.mapping.ListLayers(mxd)

        for l in layers:
            if l.supports("dataSource") and l.supports("description") and l.supports("credits"):
                messages.AddMessage(u"Update {}".format(l.name))
                md = arcpy_metadata.MetadataEditor(l.dataSource)
                l.description = md.abstract
                l.credits = md.credits
        mxd.save()
        #arcpy.RefreshTOC()

        return

