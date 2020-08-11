import bpy

bl_info = {
    "name" : "Cleaner",
    "author" : "triangle",
    "description" : "用于清理多余的材质和图片",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "category" : "Material",
    "doc_url" : "https://github.com/spite-triangle/Cleaner"
}

# 删除多余材质
class cleanMaterialsOperator(bpy.types.Operator):
    bl_idname = "triangle.cleanmaterials"
    bl_label = "clean materials"
    bl_description = "清除多余的材质"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # 获取所有的材质
        materials = bpy.data.materials
        
        for mat in materials:
            if mat.users == 0 and mat.use_fake_user == False:
                # 清除材质
                materials.remove(mat)
        return {'FINISHED'}

# 清理掉多余的图片
class cleanImagesOperator(bpy.types.Operator):
    bl_idname = "triangle.cleanimages"
    bl_label = "clean images"
    bl_description = "清除多余的图片"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # 获取所有的图片
        images = bpy.data.images

        for img in images:
            if img.users == 0 and img.use_fake_user == False:
                # 清除图片 
                images.remove(img)

        return {'FINISHED'}

# 删除保护材质
class cleanFakeMaterialsOperator(bpy.types.Operator):
    bl_idname = "triangle.cleanfakematerials"
    bl_label = "clean fake materials"
    bl_description = "清除材质的保护"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # 获取所有的材质
        materials = bpy.data.materials
        
        for mat in materials:
            if mat.use_fake_user == True:
                # 清除fake
                mat.use_fake_user = False

        return {'FINISHED'}

# 清理掉保护的贴图
class cleanFakeImagesOperator(bpy.types.Operator):
    bl_idname = "triangle.cleanfakeimages"
    bl_label = "clean fake images"
    bl_description = "清除图片的保护"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # 获取所有的图片
        images = bpy.data.images

        for img in images:
            if img.use_fake_user == True:
                # 清除图片fake
                img.use_fake_user = False

        return {'FINISHED'}

# Pie
class cleanerMenuPie(bpy.types.Menu):
    bl_idname = "triangle.cleanermenu"
    bl_label = "cleaner Menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("triangle.cleanfakeimages", text="Fake Images")
        # 6 - RIGHT
        pie.operator("triangle.cleanfakematerials", text="Fake Materials")
        # 2 - BOTTOM
        pie.operator("triangle.cleanimages", text="Images",icon="TEXTURE")
        # 8 - TOP
        pie.operator("triangle.cleanmaterials", text="Materials",icon="MATERIAL")



classes = (
    cleanFakeImagesOperator,
    cleanFakeMaterialsOperator,
    cleanImagesOperator,
    cleanMaterialsOperator,
    cleanerMenuPie
)

# 定义keymaps
addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", 'C', 'PRESS', ctrl=False, alt=True)
        kmi.properties.name = cleanerMenuPie.bl_idname
        addon_keymaps.append((km, kmi))
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
