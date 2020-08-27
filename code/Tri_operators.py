import bpy

# 删除多余材质
class Coadjutant_OT_cleanMaterials(bpy.types.Operator):
    bl_idname = "triangle.cleanmaterials"
    bl_label = "clean materials"
    bl_description = "清除多余的材质"

    @classmethod
    def poll(cls, context):
        # 多余两个才进行清理
        if len(bpy.data.materials) >2:
            return True
        return False

    def execute(self, context):
        # 获取所有的材质
        materials = bpy.data.materials
        
        for mat in materials:
            if mat.users == 0 and mat.use_fake_user == False:
                # 清除材质
                materials.remove(mat)
        return {'FINISHED'}

# 清理掉多余的图片
class Coadjutant_OT_cleanImages(bpy.types.Operator):
    bl_idname = "triangle.cleanimages"
    bl_label = "clean images"
    bl_description = "清除多余的图片"

    @classmethod
    def poll(cls, context):
        # 多余两个才进行清理
        if len(bpy.data.images) >2:
            return True
        return False

    def execute(self, context):
        # 获取所有的图片
        images = bpy.data.images

        for img in images:
            if img.users == 0 and img.use_fake_user == False:
                # 清除图片 
                images.remove(img)
        return {'FINISHED'}

# 删除保护材质
class Coadjutant_OT_cleanFakeMaterials(bpy.types.Operator):
    bl_idname = "triangle.cleanfakematerials"
    bl_label = "clean fake materials"
    bl_description = "清除材质的保护"


    def execute(self, context):
        # 获取所有的材质
        materials = bpy.data.materials
        
        for mat in materials:
            if mat.use_fake_user == True:
                # 清除fake
                mat.use_fake_user = False
        return {'FINISHED'}

# 清理掉保护的贴图
class Coadjutant_OT_cleanFakeImages(bpy.types.Operator):
    bl_idname = "triangle.cleanfakeimages"
    bl_label = "clean fake images"
    bl_description = "清除图片的保护"


    def execute(self, context):
        # 获取所有的图片
        images = bpy.data.images

        for img in images:
            if img.use_fake_user == True:
                # 清除图片fake
                img.use_fake_user = False
        return {'FINISHED'}