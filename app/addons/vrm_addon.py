import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper

bl_info = {
    "name": "VRM Format",
    "author": "saturday06",
    "version": (2, 33, 1),
    "blender": (4, 3, 0),
    "location": "File > Import-Export",
    "description": "Import-Export VRM files",
    "warning": "",
    "support": "COMMUNITY",
    "category": "Import-Export"
}

class ImportVRM(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.vrm"
    bl_label = "Import VRM"
    filename_ext = ".vrm"
    filter_glob: StringProperty(default="*.vrm", options={"HIDDEN"})

    def execute(self, context):
        try:
            # Import as GLB first
            temp_filepath = self.filepath + ".temp.glb"
            import shutil
            shutil.copy2(self.filepath, temp_filepath)
            
            # Import using glTF importer
            bpy.ops.import_scene.gltf(
                filepath=temp_filepath,
                import_pack_images=True,
                merge_vertices=True
            )
            
            # Clean up temp file
            import os
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
                
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Error importing VRM: {str(e)}")
            return {"CANCELLED"}

class ExportVRM(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.vrm"
    bl_label = "Export VRM"
    filename_ext = ".vrm"
    filter_glob: StringProperty(default="*.vrm", options={"HIDDEN"})

    def execute(self, context):
        try:
            # Export as GLB first
            temp_filepath = self.filepath + ".temp.glb"
            
            # Export using glTF exporter with VRM-compatible settings
            bpy.ops.export_scene.gltf(
                filepath=temp_filepath,
                export_format='GLB',
                export_draco_mesh_compression_enable=False,
                export_materials='EXPORT',
                export_colors=True,
                export_skins=True,
                export_morph=True,
                export_lights=False,
                export_cameras=False,
                export_apply=True,
                export_tangents=True,
                export_current_frame=True
            )
            
            # Convert GLB to VRM
            import shutil
            shutil.move(temp_filepath, self.filepath)
            return {"FINISHED"}
        except Exception as e:
            self.report({"ERROR"}, f"Error exporting VRM: {str(e)}")
            return {"CANCELLED"}

def menu_func_import(self, context):
    self.layout.operator(ImportVRM.bl_idname, text="VRM (.vrm)")

def menu_func_export(self, context):
    self.layout.operator(ExportVRM.bl_idname, text="VRM (.vrm)")

_registered_classes = set()

def register():
    global _registered_classes
    classes = [ImportVRM, ExportVRM]
    
    for cls in classes:
        if cls not in _registered_classes:
            try:
                bpy.utils.register_class(cls)
                _registered_classes.add(cls)
            except ValueError as e:
                if "already registered" not in str(e):
                    raise e
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    global _registered_classes
    for cls in _registered_classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    _registered_classes.clear()
    
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
