# MIT License
#
# Copyright (c) 2025 xtreme byte
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy
import os
from .gta_sa_ipl_importer import parse_ipl, import_dff, place_objects, export_ipl, export_ide, check_errors
from .water import WATER_OT_Import, WATER_OT_Export, WATER_OT_SetParameters, WATER_OT_GetParameters, WATER_OT_CheckFile

class Xtreme_Byte_PT_Panel(bpy.types.Panel):
    bl_label = "Xtreme Byte"
    bl_idname = "XTREME_PT_BYTE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Xtreme Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        lang = scene.language 

        layout.prop(scene, "language", text="Language" if lang == 'EN' else "Язык")

        box = layout.box()
        box.label(text="Object Settings" if lang == 'EN' else "Настройка объектов", icon='OBJECT_DATA')
        split = box.split(factor=0.5)
        col1 = split.column()
        col1.prop(scene, "id_start", text="Start ID" if lang == 'EN' else "Начальный ID")
        col2 = split.column()
        col2.operator("gta.set_values", text="Apply Settings" if lang == 'EN' else "Применить настройки", icon='CHECKMARK')

        # Секция Параметры моделей
        box = layout.box()
        box.label(text="Model Parameters" if lang == 'EN' else "Параметры моделей", icon='MODIFIER')
        col = box.column_flow(columns=2, align=True)
        col.prop(scene, "txd_name", text="TXD Name" if lang == 'EN' else "Имя TXD")
        col.prop(scene, "interior", text="Interior" if lang == 'EN' else "Интерьер")
        col.prop(scene, "distance", text="Distance" if lang == 'EN' else "Дистанция")
        col.prop(scene, "flag", text="Flag" if lang == 'EN' else "Флаг")
        col.prop(scene, "lod_start", text="LOD Start" if lang == 'EN' else "Начало LOD")

        row = box.row()
        row.operator("gta.get_all", text="Apply All" if lang == 'EN' else "Применить все", icon='FILE_TICK')
        row.operator("gta.reset_all", text="Reset All" if lang == 'EN' else "Сбросить все", icon='CANCEL')

        box = layout.box()
        box.label(text="Water Parameters" if lang == 'EN' else "Параметры воды", icon='MATFLUID')
        col = box.column(align=True)
        col.label(text="Flow Direction" if lang == 'EN' else "Направление течения:")
        row = col.row(align=True)
        row.prop(scene, "water_speed_x", text="X")
        row.prop(scene, "water_speed_y", text="Y")
        col.prop(scene, "wave_height", text="Wave Height" if lang == 'EN' else "Высота волн")
        col.prop(scene, "unk_height", text="Unknown Height" if lang == 'EN' else "Неизвестная высота")
        col.prop(scene, "water_type", text="Water Type" if lang == 'EN' else "Тип воды")
        row = box.row(align=True)
        row.operator("water.get_parameters", text="Get" if lang == 'EN' else "Получить", icon='EYEDROPPER')
        row.operator("water.set_parameters", text="Set" if lang == 'EN' else "Установить", icon='CHECKMARK')

        box = layout.box()
        box.label(text="Import and Export" if lang == 'EN' else "Импорт и Экспорт", icon='FILE')
        col = box.column(align=True)
        col.prop(scene, "ipl_path", text="IPL Path" if lang == 'EN' else "Путь к IPL")
        col.prop(scene, "dff_folder", text="DFF Folder" if lang == 'EN' else "Папка DFF")
        col.prop(scene, "img_path", text="IMG Path" if lang == 'EN' else "Путь к IMG")
        col.prop(scene, "dir_path", text="DIR Path (optional)" if lang == 'EN' else "Путь к DIR (опционально)")
        col.prop(scene, "import_textures", text="Import Textures from TXD" if lang == 'EN' else "Импорт текстур из TXD")
        col.operator("import.ipl", text="Import IPL" if lang == 'EN' else "Импортировать IPL", icon='IMPORT')

        col = box.column(align=True)
        col.prop(scene, "export_ipl_path", text="Export IPL Path" if lang == 'EN' else "Экспорт IPL")
        col.prop(scene, "export_ide_path", text="Export IDE Path" if lang == 'EN' else "Экспорт IDE")
        col.prop(scene, "lod_autosearch", text="LOD Autosearch" if lang == 'EN' else "Автпоиск LOD")

        row = box.row()
        row.operator("export.ipl", text="Export IPL" if lang == 'EN' else "Экспорт IPL", icon='EXPORT')
        row.operator("export.ide", text="Export IDE" if lang == 'EN' else "Экспорт IDE", icon='EXPORT')

        col = box.column(align=True)
        col.prop(scene, "water_path", text="WATER.DAT Path" if lang == 'EN' else "Путь к WATER.DAT")
        col.prop(scene, "water_path_export", text="Export WATER.DAT Path" if lang == 'EN' else "Экспорт WATER.DAT")
        row = box.row(align=True)
        row.operator("water.import", text="Import" if lang == 'EN' else "Импорт", icon='IMPORT')
        row.operator("water.export", text="Export" if lang == 'EN' else "Экспорт", icon='EXPORT')
        col.operator("water.check_file", text="Check WATER.DAT" if lang == 'EN' else "Проверить WATER.DAT", icon='ERROR')

        layout.operator("gta.reset_all_params", text="Reset All Parameters" if lang == 'EN' else "Сбросить все параметры", icon='LOOP_BACK')

        if scene.error_log:
            box = layout.box()
            box.label(text="Errors and Warnings" if lang == 'EN' else "Ошибки и предупреждения", icon='ERROR')
            col = box.column(align=True)
            for error in scene.error_log.split('\n')[:5]: 
                col.label(text=error)

class IMPORT_OT_IPL(bpy.types.Operator):
    bl_idname = "import.ipl"
    bl_label = "Import IPL File"
    bl_description = "Import an IPL file and place objects in the scene"
    def execute(self, context):
        ipl_path = context.scene.ipl_path
        dff_folder = context.scene.dff_folder
        img_path = context.scene.img_path
        dir_path = context.scene.dir_path
        
        if not os.path.exists(ipl_path):
            context.scene.error_log = f"ERROR: IPL file not found at {ipl_path}. Please check the path."
            self.report({'ERROR'}, context.scene.error_log)
            return {'CANCELLED'}
        
        if not img_path and not os.path.exists(dff_folder):
            context.scene.error_log = "ERROR: Invalid DFF folder or IMG path. Please provide a valid path."
            self.report({'ERROR'}, context.scene.error_log)
            return {'CANCELLED'}
        
        bpy.context.window_manager.progress_begin(0, 100)
        objects = parse_ipl(ipl_path)
        place_objects(objects, dff_folder if not img_path else None, img_path, dir_path)
        bpy.context.window_manager.progress_end()
        self.report({'INFO'}, f"Imported {len(objects)} objects")
        context.scene.error_log = ""
        return {'FINISHED'}

class EXPORT_OT_IPL(bpy.types.Operator):
    bl_idname = "export.ipl"
    bl_label = "Export IPL File"
    bl_description = "Export selected objects to an IPL file"
    def execute(self, context):
        export_ipl_path = context.scene.export_ipl_path
        if not export_ipl_path:
            context.scene.error_log = "ERROR: No export IPL path specified. Please select a valid path."
            self.report({'ERROR'}, context.scene.error_log)
            return {'CANCELLED'}
            
        if not export_ipl_path.lower().endswith('.ipl'):
            export_ipl_path += '.ipl'
        objects = bpy.context.selected_objects
        if not objects:
            context.scene.error_log = "WARNING: No objects selected for export."
            self.report({'WARNING'}, context.scene.error_log)
            return {'CANCELLED'}
        
        bpy.context.window_manager.progress_begin(0, 100)
        export_ipl(export_ipl_path, objects, context.scene.lod_autosearch)
        bpy.context.window_manager.progress_end()
        self.report({'INFO'}, f"Exported {len(objects)} objects to IPL: {export_ipl_path}")
        context.scene.error_log = ""
        return {'FINISHED'}

class EXPORT_OT_IDE(bpy.types.Operator):
    bl_idname = "export.ide"
    bl_label = "Export IDE File"
    bl_description = "Export selected objects to an IDE file"
    def execute(self, context):
        export_ide_path = context.scene.export_ide_path
        if not export_ide_path:
            context.scene.error_log = "ERROR: No export IDE path specified. Please select a valid path."
            self.report({'ERROR'}, context.scene.error_log)
            return {'CANCELLED'}
   
        if not export_ide_path.lower().endswith('.ide'):
            export_ide_path += '.ide'
        objects = bpy.context.selected_objects
        if not objects:
            context.scene.error_log = "WARNING: No objects selected for export."
            self.report({'WARNING'}, context.scene.error_log)
            return {'CANCELLED'}
        
        bpy.context.window_manager.progress_begin(0, 100)
        export_ide(export_ide_path, objects)
        bpy.context.window_manager.progress_end()
        self.report({'INFO'}, f"Exported {len(objects)} objects to IDE: {export_ide_path}")
        context.scene.error_log = ""
        return {'FINISHED'}

class GTA_OT_SetValues(bpy.types.Operator):
    bl_idname = "gta.set_values"
    bl_label = "Set Values"
    bl_description = "Apply settings to selected objects"
    def execute(self, context):
        id_start = context.scene.id_start
        selected = bpy.context.selected_objects
        for i, obj in enumerate(selected):
            obj['id'] = id_start + i
            obj['txd_name'] = context.scene.txd_name
            obj['interior'] = context.scene.interior
            obj['distance'] = context.scene.distance
            obj['flag'] = context.scene.flag
            obj['lod'] = context.scene.lod_start + i if obj.name.lower().startswith('lod') else -1
        self.report({'INFO'}, f"Applied settings to {len(selected)} objects")
        context.scene.error_log = ""
        return {'FINISHED'}

class GTA_OT_GetAll(bpy.types.Operator):
    bl_idname = "gta.get_all"
    bl_label = "Get All"
    bl_description = "Apply model parameters to selected objects"
    def execute(self, context):
        selected = bpy.context.selected_objects
        for obj in selected:
            obj['txd_name'] = context.scene.txd_name
            obj['interior'] = context.scene.interior
            obj['distance'] = context.scene.distance
            obj['flag'] = context.scene.flag
            if obj.name.lower().startswith('lod'):
                obj['lod'] = context.scene.lod_start
        self.report({'INFO'}, f"Applied settings to {len(selected)} objects")
        context.scene.error_log = ""
        return {'FINISHED'}

class GTA_OT_ResetAll(bpy.types.Operator):
    bl_idname = "gta.reset_all"
    bl_label = "Reset All Values"
    bl_description = "Reset model parameters for selected objects"
    def execute(self, context):
        selected = bpy.context.selected_objects
        for obj in selected:
            obj['txd_name'] = context.scene.txd_name
            obj['interior'] = context.scene.interior
            obj['distance'] = context.scene.distance
            obj['flag'] = context.scene.flag
            if obj.name.lower().startswith('lod'):
                obj['lod'] = context.scene.lod_start
        self.report({'INFO'}, f"Reset settings for {len(selected)} objects")
        context.scene.error_log = ""
        return {'FINISHED'}

class GTA_OT_ResetAllParams(bpy.types.Operator):
    bl_idname = "gta.reset_all_params"
    bl_label = "Reset All Parameters"
    bl_description = "Reset all panel parameters to default values"
    def execute(self, context):
        scene = context.scene
        scene.id_start = 0
        scene.txd_name = ""
        scene.interior = 0
        scene.distance = 300.0
        scene.flag = 0
        scene.lod_start = 0
        scene.lod_autosearch = False
        scene.water_speed_x = 0.0
        scene.water_speed_y = 0.0
        scene.wave_height = 0.0
        scene.unk_height = 0.0
        scene.water_type = '1'
        scene.import_textures = False
        self.report({'INFO'}, "All parameters reset to default")
        context.scene.error_log = ""
        return {'FINISHED'}

class GTA_OT_CheckErrors(bpy.types.Operator):
    bl_idname = "gta.check_errors"
    bl_label = "Check Errors"
    bl_description = "Check selected objects for errors and warnings"
    def execute(self, context):
        objects = bpy.context.selected_objects
        errors, warnings = check_errors(objects)
        error_log = ""
        for error in errors:
            error_log += f"ERROR: {error}\n"
        for warning in warnings:
            error_log += f"WARNING: {warning}\n"
        context.scene.error_log = error_log if error_log else "No errors or warnings found."
        self.report({'INFO' if not errors else 'WARNING'}, f"Found {len(errors)} errors, {len(warnings)} warnings")
        return {'FINISHED'}

classes = [
    Xtreme_Byte_PT_Panel, IMPORT_OT_IPL, EXPORT_OT_IPL, EXPORT_OT_IDE,
    GTA_OT_SetValues, GTA_OT_GetAll, GTA_OT_ResetAll, GTA_OT_ResetAllParams,
    GTA_OT_CheckErrors, WATER_OT_Import, WATER_OT_Export, WATER_OT_SetParameters,
    WATER_OT_GetParameters, WATER_OT_CheckFile
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ipl_path = bpy.props.StringProperty(
        name="IPL Path", subtype='FILE_PATH', description="Path to the IPL file to import")
    bpy.types.Scene.dff_folder = bpy.props.StringProperty(
        name="DFF Folder", subtype='DIR_PATH', description="Folder containing DFF files")
    bpy.types.Scene.export_ipl_path = bpy.props.StringProperty(
        name="Export IPL Path", subtype='FILE_PATH', description="Path to export IPL file")
    bpy.types.Scene.export_ide_path = bpy.props.StringProperty(
        name="Export IDE Path", subtype='FILE_PATH', description="Path to export IDE file")
    bpy.types.Scene.id_start = bpy.props.IntProperty(
        name="ID Start", default=0, description="Starting ID for objects")
    bpy.types.Scene.txd_name = bpy.props.StringProperty(
        name="TXD Name", default="", description="Texture dictionary name")
    bpy.types.Scene.interior = bpy.props.IntProperty(
        name="Interior", default=0, description="Interior ID for objects")
    bpy.types.Scene.distance = bpy.props.FloatProperty(
        name="Distance", default=300.0, description="Draw distance for objects")
    bpy.types.Scene.flag = bpy.props.IntProperty(
        name="Flag", default=0, description="Object flag value")
    bpy.types.Scene.lod_start = bpy.props.IntProperty(
        name="LOD Start", default=0, description="Starting LOD ID")
    bpy.types.Scene.lod_autosearch = bpy.props.BoolProperty(
        name="LOD AutoSearch", default=False, description="Enable automatic LOD search")
    bpy.types.Scene.img_path = bpy.props.StringProperty(
        name="IMG Path", subtype='FILE_PATH', description="Path to IMG archive")
    bpy.types.Scene.dir_path = bpy.props.StringProperty(
        name="DIR Path (optional)", subtype='FILE_PATH', description="Optional path to DIR file")
    bpy.types.Scene.water_path = bpy.props.StringProperty(
        name="Water Path", subtype='FILE_PATH', description="Path to WATER.DAT file")
    bpy.types.Scene.water_path_export = bpy.props.StringProperty(
        name="Export Water Path", subtype='FILE_PATH', description="Path to export WATER.DAT file")
    bpy.types.Scene.water_speed_x = bpy.props.FloatProperty(
        name="Water Speed X", default=0.0, description="Water flow speed in X direction")
    bpy.types.Scene.water_speed_y = bpy.props.FloatProperty(
        name="Water Speed Y", default=0.0, description="Water flow speed in Y direction")
    bpy.types.Scene.wave_height = bpy.props.FloatProperty(
        name="Wave Height", default=0.0, description="Height of water waves")
    bpy.types.Scene.unk_height = bpy.props.FloatProperty(
        name="Unk Height", default=0.0, description="Unknown water height parameter")
    bpy.types.Scene.water_type = bpy.props.EnumProperty(
        name="Water Type",
        items=[
            ('0', "Default / Invisible", "Default / Invisible water type"),
            ('1', "Default / Visible", "Default / Visible water type"),
            ('2', "Shallow / Invisible", "Shallow / Invisible water type"),
            ('3', "Shallow / Visible", "Shallow / Visible water type")
        ],
        default='1',
        description="Type of water to apply"
    )
    bpy.types.Scene.import_textures = bpy.props.BoolProperty(
        name="Import Textures from TXD",
        description="Extract and apply textures from TXD files",
        default=False
    )
    bpy.types.Scene.language = bpy.props.EnumProperty(
        name="Language",
        items=[
            ('EN', "English", "Use English interface"),
            ('RU', "Русский", "Использовать русский интерфейс")
        ],
        default='EN',
        description="Select interface language"
    )
    bpy.types.Scene.error_log = bpy.props.StringProperty(
        name="Error Log", default="", description="Log of errors and warnings"
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ipl_path
    del bpy.types.Scene.dff_folder
    del bpy.types.Scene.export_ipl_path
    del bpy.types.Scene.export_ide_path
    del bpy.types.Scene.id_start
    del bpy.types.Scene.txd_name
    del bpy.types.Scene.interior
    del bpy.types.Scene.distance
    del bpy.types.Scene.flag
    del bpy.types.Scene.lod_start
    del bpy.types.Scene.lod_autosearch
    del bpy.types.Scene.img_path
    del bpy.types.Scene.dir_path
    del bpy.types.Scene.water_path
    del bpy.types.Scene.water_path_export
    del bpy.types.Scene.water_speed_x
    del bpy.types.Scene.water_speed_y
    del bpy.types.Scene.wave_height
    del bpy.types.Scene.unk_height
    del bpy.types.Scene.water_type
    del bpy.types.Scene.import_textures
    del bpy.types.Scene.language
    del bpy.types.Scene.error_log