import bpy
import bmesh

bl_info = {
    "name": "Mesh Data Insight",
    "author": "Chuck Norris",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Add > Mesh",
    "tracker_url": "https://github.com/BaalNetbek/Mesh-Data-Insight/issues",
    "description": "Allows lookup of mesh data",
    "warning": "You are a tester.",
    "category": "Development",
}

def update_vertex_selection(self, context):
        index = context.scene.vertex_index
        if 0 <= index < len(context.object.data.vertices):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            context.object.data.vertices[index].select = True
            bpy.ops.object.mode_set(mode='EDIT')

def update_face_selection(self, context):
        index = context.scene.face_index
        if 0 <= index < len(context.object.data.polygons):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            context.object.data.polygons[index].select = True
            bpy.ops.object.mode_set(mode='EDIT')

class MeshInfoPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_mesh_info"
    bl_label = "Mesh Info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    '''
    bl_idname = "OBJECT_PT_mesh_info"
    bl_label = "Mesh Info"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    '''

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        mesh = obj.data

        scene = context.scene

        # Vertices tab
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_vertices", icon='VERTEXSEL')

        if scene.show_vertices:
            row = box.row()
            row.label(text="Vertex Index:")
            row.prop(scene, "vertex_index", text="")

            # Display selected vertex coordinates
            i=0
            selected_vertex = None
            for v in mesh.vertices:
                if v.select:
                    selected_vertex = v
                    break
                i+=1

            if selected_vertex:
                row = box.row()
                row.alignment = 'EXPAND'
                #row.label(text="x,y,z=")
                subrow = row.row()
                subrow.alignment = 'EXPAND'
                subrow.label(text=f"{i}")
                subrow.label(text=f"{selected_vertex.co.x:.2f}")
                subrow.label(text=f"{selected_vertex.co.y:.2f}")
                subrow.label(text=f"{selected_vertex.co.z:.2f}")
                subrow.alert = True

            vertices_box = box.box()
            vertices_data = [(v.co.x, v.co.y, v.co.z) for v in mesh.vertices]
            
            row = vertices_box.row()
            col_i = row.column()
            col_x = row.column()
            col_y = row.column()
            col_z = row.column()

            col_i.label(text="idx")
            col_x.label(text="X")
            col_y.label(text="Y")
            col_z.label(text="Z")
            
            for idx, vertex in enumerate(vertices_data):
                row = vertices_box.row()
                if idx == scene.vertex_index:
                    row.alert = True
                op = row.operator("mesh.select_vertex", text=f"{idx}")
                op.index = idx
                row.label(text=f"{vertex[0]:.2f}")
                row.label(text=f"{vertex[1]:.2f}")
                row.label(text=f"{vertex[2]:.2f}")

        # Faces tab
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_faces", icon='FACESEL')
        
        if scene.show_faces:
            row = box.row()
            row.label(text="Face Index:")
            row.prop(scene, "face_index", text="")

            faces_box = box.box()
            for idx, face in enumerate(mesh.polygons):
                row = faces_box.row()
                if idx == scene.face_index:
                    row.alert = True
                op = row.operator("mesh.select_face", text=f"{idx}")
                op.index = idx
                for vertex_index in face.vertices:
                    row.label(text=str(vertex_index))

        # UV tab
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_uvs", icon='UV')
        
        if bpy.context.mode == 'OBJECT':
            if scene.show_uvs:
                uv_box = box.box()
                uv_layer = mesh.uv_layers.active
                if uv_layer:
                    uvs_data = [uv.uv for uv in uv_layer.data]
                    
                    row = uv_box.row()
                    col_i = row.column()
                    col_u = row.column()
                    col_v = row.column()
                    
                    col_i.label(text="idx")
                    col_u.label(text="U")
                    col_v.label(text="V")
                    for idx, uv in enumerate(uvs_data):
                        row = uv_box.row()
                        row.label(text=f"{idx}.")
                        row.label(text=f"{uv[0]:.4f}")
                        row.label(text=f"{uv[1]:.4f}")
                else:
                    uv_box.label(text="No UV layers found")
        
        #Vertex Normals tab        
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_vertex_normals", text="Vertex Normals", icon='NORMALS_VERTEX')

        if scene.show_vertex_normals:
            
            bpy.context.space_data.overlay.show_vertex_normals = True

            row = box.row()
            row.label(text="Vert Normal Index:")
            row.prop(scene, "vertex_index", text="")

            # Display selected vertex coordinates
            i=0
            selected_vertex = None
            for v in mesh.vertices:
                if v.select:
                    selected_vertex = v
                    break
                i+=1

            if selected_vertex:
                row = box.row()
                row.alignment = 'EXPAND'
                #row.label(text="x,y,z=")
                subrow = row.row()
                subrow.alignment = 'EXPAND'
                subrow.label(text=f"{i}")
                subrow.label(text=f"{selected_vertex.normal.x:.3f}")
                subrow.label(text=f"{selected_vertex.normal.y:.3f}")
                subrow.label(text=f"{selected_vertex.normal.z:.3f}")
                subrow.alert = True

            vertex_normals_box = box.box()
            vertices_normals_data = [(v.normal.x, v.normal.y, v.normal.z) for v in mesh.vertices]
            
            row = vertex_normals_box.row()
            col_i = row.column()
            col_x = row.column()
            col_y = row.column()
            col_z = row.column()

            col_i.label(text="idx")
            col_x.label(text="X")
            col_y.label(text="Y")
            col_z.label(text="Z")
            
            for idx, vertex_normal in enumerate(vertices_normals_data):
                row = vertex_normals_box.row()
                if idx == scene.vertex_index:
                    row.alert = True
                op = row.operator("mesh.select_vertex", text=f"{idx}")
                op.index = idx
                row.label(text=f"{vertex_normal[0]:.3f}")
                row.label(text=f"{vertex_normal[1]:.3f}")
                row.label(text=f"{vertex_normal[2]:.3f}")
        else:
            bpy.context.space_data.overlay.show_vertex_normals = False
                
        #Face Normals tab
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_face_normals", text="Face Normals", icon='NORMALS_FACE')        

        if scene.show_face_normals:
            
            bpy.context.space_data.overlay.show_face_normals = True
            
            row = box.row()
            row.label(text="Face Normal Idx:")
            row.prop(scene, "face_index", text="")

            face_normals_box = box.box()
            row = face_normals_box.row()
            col_i = row.column()
            col_x = row.column()
            col_y = row.column()
            col_z = row.column()

            col_i.label(text="idx")
            col_x.label(text="X")
            col_y.label(text="Y")
            col_z.label(text="Z")
            
            for idx, face in enumerate(mesh.polygons):
                row = face_normals_box.row()
                if idx == scene.face_index:
                    row.alert = True
                op = row.operator("mesh.select_face", text=f"{idx}")
                op.index = idx

                row.label(text=f"{face.normal.x:.3f}")
                row.label(text=f"{face.normal.y:.3f}")
                row.label(text=f"{face.normal.z:.3f}")
        else:
            bpy.context.space_data.overlay.show_face_normals = False
                    

class MESH_OT_SelectVertex(bpy.types.Operator):
    bl_idname = "mesh.select_vertex"
    bl_label = "Select Vertex"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        # Deselect all vertices first
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Select the specific vertex
        mesh.vertices[self.index].select = True
        context.scene.vertex_index = self.index
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}

class MESH_OT_SelectFace(bpy.types.Operator):
    bl_idname = "mesh.select_face"
    bl_label = "Select Face"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        # Deselect all faces first
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Select the specific face
        mesh.polygons[self.index].select = True
        context.scene.face_index = self.index
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}

def get_vertex_index(self):
   return self.get('vertex_index', 0)

def set_vertex_index(self, value):
    value = max(0, min(value, len(bpy.context.object.data.vertices)))
    self['vertex_index'] = value

def get_face_index(self):
    return self.get('face_index', 0)

def set_face_index(self, value):
    value = max(0, min(value, len(bpy.context.object.data.polygons)))
    self['face_index'] = value
    

def register():
    bpy.utils.register_class(MeshInfoPanel)
    bpy.utils.register_class(MESH_OT_SelectVertex)
    bpy.utils.register_class(MESH_OT_SelectFace)
   
   
    bpy.types.Scene.show_vertices = bpy.props.BoolProperty(name="Vertices", default=True)
    bpy.types.Scene.show_faces = bpy.props.BoolProperty(name="Faces", default=True)
    bpy.types.Scene.show_uvs = bpy.props.BoolProperty(name="UVs", default=True)
    bpy.types.Scene.show_vertex_normals = bpy.props.BoolProperty(name="Vertex Normals", default=False)
    bpy.types.Scene.show_face_normals = bpy.props.BoolProperty(name="Face Normals", default=False)
    bpy.types.Scene.vertex_index = bpy.props.IntProperty(name="Vertex Index", min=0, get=get_vertex_index, set=set_vertex_index, update=update_vertex_selection)
    bpy.types.Scene.face_index = bpy.props.IntProperty(name="Face Index",min=0, get=get_face_index, set=set_face_index, update=update_face_selection)


def unregister():
    bpy.utils.unregister_class(MeshInfoPanel)
    bpy.utils.unregister_class(MESH_OT_SelectVertex)
    bpy.utils.unregister_class(MESH_OT_SelectFace)
   
    del bpy.types.Scene.show_vertices
    del bpy.types.Scene.show_faces
    del bpy.types.Scene.show_uvs
    del bpy.types.Scene.vertex_index
    del bpy.types.Scene.face_index

if __name__ == "__main__":
    register()