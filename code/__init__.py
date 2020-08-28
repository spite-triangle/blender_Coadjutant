
bl_info = {
    "name" : "Coadjutant",
    "author" : "triangle",
    "description" : "用于清理多余的材质和图片，图片材质大图标查看",
    "blender" : (2, 80, 0),
    "version" : (0, 2, 2),
    "location" : "",
    "category" : "Material",
    "doc_url" : "https://github.com/spite-triangle/blender_Coadjutant"
}

import bpy
from . Tri_operators import Coadjutant_OT_cleanFakeImages,Coadjutant_OT_cleanFakeMaterials,Coadjutant_OT_cleanImages,Coadjutant_OT_cleanMaterials,Coadjutant_OT_cleanAllOrphan,Coadjutant_OT_createMaterial

# Pie
class Coadjutant_MT_menuPie(bpy.types.Menu):
    bl_idname = "Coadjustant_MT_menuPie"
    bl_label = "Coadjutant"
    

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        # 4 - LEFT
        pie.separator()
        # 6 - RIGHT
        pie.separator()

        # 2 - BOTTOM
        pie.operator("triangle.cleanall", text="Purge All",icon='ORPHAN_DATA')

        # 8 - TOP
        split = pie.row().box().split()
        split.scale_x = 1.2

        if  context.active_object :
            self.draw_changeMaterials(split,context)

        if context.area.ui_type == "ShaderNodeTree" and hasattr(context.active_node,'image'):
            self.draw_changeNodeImages(split,context.active_node)

        if context.area.ui_type in {'UV','VIEW'}:
            self.draw_changeImages(split,context.space_data)

        # 7 - TOP - LEFT
        pie.separator()
        # 9 - TOP - RIGHT
        pie.separator()
        
        # 1 - BOTTOM - LEFT
        box = pie.box()
        col = box.column()
        col.operator("triangle.cleanmaterials", text="Materials",icon="MATERIAL")
        col.operator("triangle.cleanfakematerials", text="Fake Materials")

        # 3 - BOTTOM - RIGHT
        box = pie.box()
        col = box.column()
        col.operator("triangle.cleanimages", text="Images",icon="IMAGE_DATA")
        col.operator("triangle.cleanfakeimages", text="Fake Images")

    # 材质切换界面
    def draw_changeMaterials(self,split,context):
        object = context.active_object

        if object.mode == 'EDIT':
            rows = 5

        rows = 6

        # 单个物体的uilist
        col = split.column()
        subrow = col.row()
        subrow.template_list("MATERIAL_UL_matslots", "", object, "material_slots", object, "active_material_index",rows=rows)
       
        # 按钮：上下，删除
        subcol = subrow.column()
        subcol.scale_x = 0.8
        subcol.operator("triangle.creatematerial", icon='ADD', text="")
        subcol.operator("object.material_slot_remove", icon='REMOVE', text="")
        if len(object.material_slots) >= 2 :
            subcol.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
            subcol.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
       
        if object.mode == 'EDIT':
            subrow = col.row(align=True)
            subrow.alignment= "LEFT"
            subrow.operator("object.material_slot_assign", text="Assign")
            subrow.operator("object.material_slot_select", text="Select")
            subrow.operator("object.material_slot_deselect", text="Deselect")
        
        # 材质
        col = split.column()
        col.alignment = "CENTER"
        col.template_ID_preview(object,"active_material",rows=2,cols=5)

    # 图片切换界面
    def draw_changeNodeImages(self,split,node):
        col = split.column()
        col.template_ID_preview(node,"image",new="image.new", open="image.open",rows=2,cols=5)

    # uv与图片编辑器界面
    def draw_changeImages(self,split,spaceData):
        col = split.column()
        col.template_ID_preview(spaceData, "image",new="image.new", open="image.open",rows=2,cols=5)

classes = (
    Coadjutant_OT_cleanFakeImages,
    Coadjutant_OT_cleanFakeMaterials,
    Coadjutant_OT_cleanImages,
    Coadjutant_OT_cleanMaterials,
    Coadjutant_OT_cleanAllOrphan,
    Coadjutant_OT_createMaterial,
    Coadjutant_MT_menuPie
)

# 定义keymaps
addon_keymaps = []

def bendingKeyMap(wm,name,space_type):
        km = wm.keyconfigs.addon.keymaps.new(name=name, space_type=space_type)
        kmi = km.keymap_items.new("wm.call_menu_pie", 'C', 'PRESS', ctrl=False, alt=True)
        kmi.properties.name = Coadjutant_MT_menuPie.bl_idname
        addon_keymaps.append((km, kmi))


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # 注册3D视图
        bendingKeyMap(wm,'3D View','VIEW_3D')

        # 注册节点编辑器
        bendingKeyMap(wm,'Node Editor','NODE_EDITOR')

        # 注册uv与图片试图快捷键
        bendingKeyMap(wm,'Image','IMAGE_EDITOR')

    ...

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    ...

if __name__ == "__main__":
    register()    
