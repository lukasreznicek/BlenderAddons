# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy

bl_info = {
    "name" : "PivotPainter2",
    "author" : "Lukas Reznicek, Jonathan Lindquist",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}



from .operators.operators import OBJECT_OT_lr_pivot_painter_export
from bpy.props import IntProperty, CollectionProperty, StringProperty,FloatVectorProperty,BoolProperty,EnumProperty


def img1_alpha_callback(scene, context):
    painter2 = bpy.context.scene.pivot_painter_2

    items = []
    if painter2.image_1_rgb == 'OP0':
        items = []
    elif painter2.image_1_rgb == 'OP1' or painter2.image_1_rgb == 'OP2' or painter2.image_1_rgb == 'OP3': #LDR
        items.append(('OP1', 'Parent Index (Int as Float)',''))
        # items.append(('OP2', 'Number of Steps From Root',''))
        items.append(('OP3', 'Random 0-1 Value Per Element',''))
        # items.append(('OP4', 'Bounding Box Diameter',''))
        # items.append(('OP5', 'Selection Order (Int as Float)',''))
        items.append(('OP6', 'Normalized 0-1 Hierarchy position',''))
        # items.append(('OP7', 'Object X Width',''))
        # items.append(('OP8', 'Object Y Depth',''))
        # items.append(('OP9', 'Object Z Height',''))
        items.append(('OP10', 'Parent Index (Float - Up to 2048)',''))

    elif painter2.image_1_rgb == 'OP4' or painter2.image_1_rgb == 'OP5' or painter2.image_1_rgb == 'OP6': #HDR
        items.append(('OP6', 'Normalized 0-1 Hierarchy position',''))
        items.append(('OP3', 'Random 0-1 Value Per Element',''))
        # items.append(('OP11', 'X Extent Divided by 2048 - 2048 Max',''))
        # items.append(('OP12', 'Y Extent Divided by 2048 - 2048 Max',''))
        # items.append(('OP13', 'Z Extent Divided by 2048 - 2048 Max',''))
    return items


def img2_alpha_callback(scene, context):
    painter2 = bpy.context.scene.pivot_painter_2

    items = []
    if painter2.image_2_rgb == 'OP0':
        items = []
    elif painter2.image_2_rgb == 'OP1' or painter2.image_2_rgb == 'OP2' or painter2.image_2_rgb == 'OP3': #LDR
        items.append(('OP1', 'Parent Index (Int as Float)',''))
        # items.append(('OP2', 'Number of Steps From Root',''))
        items.append(('OP3', 'Random 0-1 Value Per Element',''))
        # items.append(('OP4', 'Bounding Box Diameter',''))
        # items.append(('OP5', 'Selection Order (Int as Float)',''))
        items.append(('OP6', 'Normalized 0-1 Hierarchy position',''))
        # items.append(('OP7', 'Object X Width',''))
        # items.append(('OP8', 'Object Y Depth',''))
        # items.append(('OP9', 'Object Z Height',''))
        items.append(('OP10', 'Parent Index (Float - Up to 2048)',''))

    elif painter2.image_2_rgb == 'OP4' or painter2.image_2_rgb == 'OP5' or painter2.image_2_rgb == 'OP6': #HDR
        items.append(('OP6', 'Normalized 0-1 Hierarchy position',''))
        items.append(('OP3', 'Random 0-1 Value Per Element',''))
        # items.append(('OP11', 'X Extent Divided by 2048 - 2048 Max',''))
        # items.append(('OP12', 'Y Extent Divided by 2048 - 2048 Max',''))
        # items.append(('OP13', 'Z Extent Divided by 2048 - 2048 Max',''))
    return items

# Properties 
# To acess properties: bpy.data.scenes['Scene'].pivot_painter_2
# Is assigned by pointer property below in class registration.
class pivot_painter2_settings(bpy.types.PropertyGroup):
    # export_sm_prefix: bpy.props.StringProperty(name="Prefix", description="Name of the new UV set on selected", default="SM_", maxlen=1024,)
    # export_sm_suffix:bpy.props.StringProperty(name="Suffix", description="Name of the new UV set on selected", default="", maxlen=1024,)

    image_1_rgb:bpy.props.EnumProperty(name= 'RGB', description= '',default = 1, items= [
    ('OP0', 'Do Not Render',''),
    ('OP1', 'Pivot Position (16-bit)',''),
    #('OP2', 'Origin Position(16-bit)',''),
    #('OP3', 'Origin Extents(16-bit)',''),
    ('OP4', 'X Vector(8-bit)',''),
    ('OP5', 'Y Vector(8-bit)',''),
    ('OP6', 'Z Vector(8-bit)','')])
    image_1_alpha:bpy.props.EnumProperty(name= 'Alpha', description= '', items= img1_alpha_callback)
 
    image_2_rgb:bpy.props.EnumProperty(name= 'RGB', description= '',default = 4, items= [
    ('OP0', 'Do Not Render',''),
    ('OP1', 'Pivot Position (16-bit)',''),
    #('OP2', 'Origin Position(16-bit)',''),
    #('OP3', 'Origin Extents(16-bit)',''),
    ('OP4', 'X Vector(8-bit)',''),
    ('OP5', 'Y Vector(8-bit)',''),
    ('OP6', 'Z Vector(8-bit)','')])

    
    image_2_alpha:bpy.props.EnumProperty(name= 'Alpha', description= '', items= img2_alpha_callback)

    export_path:bpy.props.StringProperty(name="Folder", description="Texture output location. \n// = .blend file location\n//..\ = .blend file parent folder", default="//", maxlen=1024,subtype='DIR_PATH')
    select_texture_coordinate: bpy.props.IntProperty(name="Texture Coordinate", description="Location of Pivot Painter custom UVs", default=1, min = 1, soft_max = 5)
    
    #image_2_alpha:bpy.props.EnumProperty(name= 'Alpha', description= '', items= [('OP1', 'Parent Index (Int as Float)',''),('OP2', 'Number Of Steps From Root',''),('OP3', 'Random 0-1 Value Per Element','')])


    #texture_coordinate:bpy.props.EnumProperty(name= 'Export Type', description= '', items= [('OP1', 'Option 1',''),('OP2', 'Option 2',''),('OP3', 'Option 3','')])
    # lr_assembly_replace_file: bpy.props.BoolProperty(name="Replace File", default=True)
    # lr_assembly_filename: bpy.props.StringProperty(name="JSON filename", default = 'Assembly')



    # name_to_uv_index_set: bpy.props.StringProperty(name="  Name", description="Set uv index by name", default="UVMap Name", maxlen=1024,)
    # uv_map_rename: bpy.props.StringProperty(name="  To", description="Rename uv on selected objects", default="New Name", maxlen=1024,)
    # uv_map_delete_by_name: bpy.props.StringProperty(name="  Name", description="Name of the UV Map to delete on selected objects", default="UV Name", maxlen=1024,)

    # remove_uv_index: bpy.props.IntProperty(name="Index to remove", description="UV Map index to remove on selected objects", default=1, min = 1, soft_max = 5)
    # vertex_color_offset_amount: bpy.props.FloatProperty(name="Offset amount", default=0.1, min = 0, max = 1)
    # lr_vc_swatch: FloatVectorProperty(name="object_color",subtype='COLOR',default=(1.0, 1.0, 1.0),min=0.0, max=1.0,description="color picker")
    # lr_vc_alpha_swatch: bpy.props.FloatProperty(name="Alpha Value", step = 5, default=0.5, min = 0, max = 1)



#UI -------------------------------------------------------------------------------------
# class VIEW3D_PT_pivot_painter2_setup(bpy.types.Panel):
#     bl_label = "PivotPainter2"
#     bl_idname = "OBJECT_PT_pivot_painter_setup"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'PivotPainter2'





#     def draw(self, context):

#         #pivot_painter_2 = context.scene.pivot_painter_2

#         layout = self.layout.box()
#         # layout.label(text="Settings")



#         #EXPORT MODE TEMP DISABLED
#         # row = layout.row(align=True)
#         # if context.object:
#         #     row.prop(context.object,'pivot_painter_2_type')
#         row = layout.row(align=True)
        
#         if context.object:
#             row.prop(context.object,'lr_exportsubfolder')
 


class VIEW3D_PT_pivot_painter2(bpy.types.Panel):
    bl_label = "Pivot Painter 2"
    bl_idname = "OBJECT_PT_pivot_painter2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PivotPainter2'


    # bpy.types.Object.lr_export_type = EnumProperty(
    #     name="Export mode",
    #     description="Export mode",
    #     override={'LIBRARY_OVERRIDABLE'},
    #     items=[
    #         ("auto",
    #             "Auto",
    #             "Export with the parent if the parents is \"Export recursive\"",
    #             "BOIDS",
    #             1),
    #         ("export_recursive",
    #             "Export recursive",
    #             "Export self object and all children",
    #             "KEYINGSET",
    #             2),
    #         ("dont_export",
    #             "Not exported",
    #             "Will never export",
    #             "CANCEL",
    #             3)
    #         ]
    #     )

    # bpy.types.Object.lr_exportsubfolder = StringProperty(
    #     name="Sub folder name",
    #     description=(
    #         'The name of sub folder.' +
    #         ' You can now use ../ for up one directory.'
    #         ),
    #     override={'LIBRARY_OVERRIDABLE'},
    #     maxlen=64,
    #     default="",
    #     subtype='FILE_NAME'
    #     )


    # bpy.types.Object.lr_export_reset_position = BoolProperty(
    #     name="Move to zero",
    #     description=('Main object will be positioned to zero before exporting'),
    #     default=True
    #     )

    # bpy.types.Object.lr_export_reset_rotation = BoolProperty(
    #     name="Reset Rotation",
    #     description=('Main object rotation will have rotation set to zero'),
    #     default=True
    #     )


    def draw(self, context):

        pivot_painter_2 = context.scene.pivot_painter_2
        #myprops = bpy.context.scene['pivot_painter_2']

        layout = self.layout.box()
        layout.label(text="UVs")

        row = layout.row(align=True)
        row.prop(pivot_painter_2, "select_texture_coordinate")



        #IMAGE 1 ----
        layout = self.layout.box()
        layout.label(text="Image 1")

        row = layout.row(align=True)
        row.prop(pivot_painter_2, "image_1_rgb")
        row = layout.row(align=True)
        if pivot_painter_2.image_1_rgb != 'OP0': 
            row.prop(pivot_painter_2, "image_1_alpha")


        #IMAGE 2 ----
        layout = self.layout.box()
        layout.label(text="Image 2")

        row = layout.row(align=True)
        row.prop(pivot_painter_2, "image_2_rgb")
        row = layout.row(align=True)
        if pivot_painter_2.image_2_rgb != 'OP0': 
            row.prop(pivot_painter_2, "image_2_alpha")





        layout = self.layout.box()
        row = layout.row(align=True)
        row.prop(pivot_painter_2, "export_path")
        row = layout.row(align=True)
        row.scale_y = 2
        row.operator("object.lr_pivot_painter_export", text="Process Hierarchy", icon = 'EXPORT')





        


classes = [pivot_painter2_settings,VIEW3D_PT_pivot_painter2, OBJECT_OT_lr_pivot_painter_export]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pivot_painter_2 = bpy.props.PointerProperty(type=pivot_painter2_settings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.pivot_painter_2
