bl_info = {  
     "name": "Import Tool",  
     "author": "Rohan (Coolq)",  
     "version": (3, 8),  
     "blender": (2, 7, 7),  
     "location": "View3D > TOOLS > Minecraft Objects",  
     "description": "Add objects from another file.",  
     "warning": "",  
     "wiki_url": "",  
     "tracker_url": "",  
     "category": "Animation"}  

import bpy,os

class MinecraftObjectsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Import Tool"
    bl_idname = "OBJECT_PT_import_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Import Tool"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        
        scn = bpy.context.scene
        


        self.layout.prop(scn,"to_create")
        toCreate = bpy.context.scene.to_create
        op = self.layout.operator("object.append_object",text="Create")
        op.int_index_qadd = -1
        self.layout.prop(scn,"mo_filepath")
        
        row = layout.row()
        col = row.column(align=True)
        
        layout = self.layout.box()
        row = layout.row()
        col = row.column()
        toprow = layout.row()
        expandicon = "TRIA_RIGHT"
        if bpy.context.scene.expand_qadd:
            expandicon = "TRIA_DOWN"
        toprow.prop(scn, "expand_qadd", icon=expandicon, icon_only=True,
                text="", emboss=False)
        toprow.label("Quick add:")
        optionsrow = layout.row()
        optionscol = optionsrow.column(align=True)
        
        if bpy.context.scene.expand_qadd:
            expandicon = "TRIA_DOWN"
            optionscol.label("Add:")
            try:
                f = open("add.txt",'r')
                tmp = []
                count = 0
                for i in f.readlines():
                    if not i.startswith("#") and not i.startswith(" ") and not i.startswith("\n"):
                        i = i.strip('\n')
                        optionsrow = layout.row()
                        optionscol = optionsrow.column(align=True)
                        
                        op = optionscol.operator("object.append_object",text="+ "+str(i))
                        op.int_index_qadd = count
                    count += 1
                #optionsrow = layout.row()
                #optionscol = optionsrow.column(align=True)
                f.close()
            except:
                try:
                    open("add.txt",'a').close()
                except:
                    print("Could not open/edit `add.txt` : Permission Denied.")
                pass
        
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        
        layout = self.layout.box()
        row = layout.row()
        col = row.column()
        toprow = layout.row()
        expandicon = "TRIA_RIGHT"
        if bpy.context.scene.expand_settings:
            expandicon = "TRIA_DOWN"
        toprow.prop(scn, "expand_settings", icon=expandicon, icon_only=True,
                text="", emboss=False)
        toprow.label("Options:")
        optionsrow = layout.row()
        optionscol = optionsrow.column(align=True)
        
        if bpy.context.scene.expand_settings:
            expandicon = "TRIA_DOWN"
            optionscol.label("Position:")
            optionscol.prop(scn,"create_at_3d_cursor")
            optionsrow = layout.row()
            optionscol = optionsrow.column(align=True)
            if bpy.context.scene.create_at_3d_cursor:
                optionscol.enabled = False
            optionscol.prop(scn,"xPos")
            optionscol.prop(scn,"yPos")
            optionscol.prop(scn,"zPos")
            optionsrow = layout.row()
            optionscol = optionsrow.column(align=True)
            optionscol.prop(scn,"mo_select_object")

def register():
    bpy.types.Scene.xPos = bpy.props.FloatProperty( name="X", default=0)
    bpy.types.Scene.yPos = bpy.props.FloatProperty( name="Y", default=0)
    bpy.types.Scene.zPos = bpy.props.FloatProperty( name="Z", default=0)
    bpy.types.Scene.create_at_3d_cursor = bpy.props.BoolProperty( name="Create at 3D cursor", default=True)
    bpy.types.Scene.mo_select_object = bpy.props.BoolProperty( name="Select created object", default=True)
    bpy.types.Scene.expand_settings = bpy.props.BoolProperty( name="Expand", default=False)
    bpy.types.Scene.expand_qadd = bpy.props.BoolProperty( name="Expand", default=False)
    bpy.types.Scene.searchbox = bpy.props.StringProperty( name="Search", default="")
    bpy.types.Scene.to_create = bpy.props.StringProperty( name="To create", default="")
    bpy.types.Scene.mo_filepath = bpy.props.StringProperty(name="Import from", default="", subtype="FILE_PATH")
    bpy.utils.register_class(MinecraftObjectsPanel)
    bpy.utils.register_class(AppendObject)


def unregister():
    bpy.utils.unregister_class(MinecraftObjectsPanel)
    bpy.utils.unregister_class(AppendObject)


def main(self,context,int_index_qadd):
    obj_to_create = bpy.context.scene.to_create
    if int_index_qadd >= 0:
        f = open("add.txt",'r')
        lines = f.readlines()
        obj_to_create = lines[int_index_qadd].strip("\n")
        f.close()
    print(obj_to_create)
    try:
        oldSel = context.scene.objects[-1]
    except:
        oldSel = None
    #'\\'.join(__file__.replace('//','\\').split("\\")[:-2])
    bpy.ops.wm.append(directory=bpy.context.scene.mo_filepath.replace('//','\\'.join(__file__.replace('//','\\').split("\\")[:-2])+"\\").replace('//','\\')+"\\Object\\", filename=obj_to_create)
    if len(context.scene.objects) > 0 and oldSel != context.scene.objects[-1]:
        if bpy.context.scene.create_at_3d_cursor:
            bpy.data.objects[context.scene.objects[-1].name].location = bpy.context.scene.cursor_location
        else:
            bpy.data.objects[context.scene.objects[-1].name].location = (bpy.context.scene.xPos,bpy.context.scene.yPos,bpy.context.scene.zPos)
        if bpy.context.scene.mo_select_object:
            bpy.data.objects[context.scene.objects[-1].name].select = True
        else:
            bpy.data.objects[context.scene.objects[-1].name].select = False
    else:
        self.report({'ERROR'}, "Could not find object - "+str(obj_to_create))
class AppendObject(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.append_object"
    bl_label = "Append Object"
    
    int_index_qadd = bpy.props.IntProperty(default=-1)
    
    def execute(self, context):
        main(self,context,self.int_index_qadd)
        return {'FINISHED'}

if __name__ == "__main__":
    register()
