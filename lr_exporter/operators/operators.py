import bpy, os, math, numpy, bmesh
from . import utils


class OBJECT_OT_lr_hierarchy_exporter(bpy.types.Operator):
    bl_idname = "object.lr_exporter_export"
    bl_label = "Exports obj"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        normalize = numpy.linalg.norm

        #Store initial selection
        selected_objs_init = bpy.context.selected_objects
        active_obj_init = bpy.context.view_layer.objects.active
        
        blender_file_location = bpy.path.abspath('//')

        for selected_obj in selected_objs_init:            
            bpy.ops.object.select_all(action='DESELECT')
            
            bpy.context.view_layer.objects.active = selected_obj
            

            selected_obj.select_set(True)    

            children = selected_obj.children_recursive
            # bpy.ops.object.duplicates_make_real(use_hierarchy=True) WILL BE NEEDED FOR GEOMETRY NODES

            for child in children:
                child.select_set(True)

            obj_info_before = utils.SelectedObjectsInfo()
            obj_info_before.get_info()
            #--- PREPARATION ---


            #After duplication Blender automatically selects nevely created objects
            bpy.ops.object.duplicate(linked=False)

            obj_info_after = utils.SelectedObjectsInfo()
            obj_info_after.get_info()

            print('Names Before: ', obj_info_before.selected_objs_names)
            print('Names After: ', obj_info_after.selected_objs_names)
            
            print('DataNames Before: ', obj_info_before.selected_objs_data_names)
            print('DataNames After: ', obj_info_after.selected_objs_data_names)            
            
            #Naming objects
            
            #Add suffix to old objs
            obj_info_before.add_suffix('_NameBackup')
            obj_info_before.add_data_suffix('_DataNameBackup')
            
            
            obj_info_after.restore_object_names(obj_info_before.selected_objs_names)
            obj_info_after.restore_object_data_names(obj_info_before.selected_objs_data_names)


            #Remove any parents in case of exporting a child object
            obj_info_after.active_obj.parent = None

            #Reset position
            if obj_info_after.active_obj.get("lr_export_reset_position") == 0:
                pass
            else:
                obj_info_after.active_obj.location = 0,0,0
            
            #Reset rotation
            if obj_info_after.active_obj.get("lr_export_reset_rotation") == 0:
                pass
            else:
                obj_info_after.active_obj.rotation_euler = 0,0,0











            #--- NAMING FBX ---

            blend_path = bpy.path.abspath('//')
            ui_export_path = bpy.data.scenes['Scene'].lr_export.export_path
            print('OBJECT INFO ACTIVE BEFORE:'+obj_info_before.active_obj.name)
            file_name = obj_info_after.active_obj.name
            
            prefix = bpy.data.scenes['Scene'].lr_export.export_sm_prefix
            suffix = bpy.data.scenes['Scene'].lr_export.export_sm_suffix
            filename_prefix_suffix = prefix+file_name+suffix
            file_format = '.fbx'
            
            if selected_obj.get("lr_exportsubfolder"):
                object_subbolder = obj_info_after.active_obj['lr_exportsubfolder']
            else:
                object_subbolder = ''


            export_path = os.path.join(bpy.path.abspath(ui_export_path), object_subbolder)
            export_file = os.path.join(export_path,filename_prefix_suffix+file_format)
            if os.path.exists(export_path) == False:
                os.makedirs(export_path)

            bpy.ops.export_scene.fbx(filepath = str(export_file), use_selection=True)
            #--- NAMING END ---


            #--- CLEANUP ---
    
                #Delete selected objects
            bpy.ops.object.delete(use_global=False)

            # Restore obj names
            obj_info_before.restore_object_names()
            obj_info_before.restore_object_data_names()

    
            #--- CLEANUP END ---
    
        #Return initial selection
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected_objs_init:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = active_obj_init

        message = 'Exported file: '+filename_prefix_suffix
        self.report({'INFO'}, message)

        return {'FINISHED'}





class OBJECT_OT_store_object_data_json(bpy.types.Operator):
    bl_idname = "object.lr_store_object_data_json"
    bl_label = "Creates a list of object names,location,rotation and scale."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        '''File is saved next to a .blend file'''

        
        #Store initial selection
        selected_objs_init = bpy.context.selected_objects
        active_obj_init = bpy.context.view_layer.objects.active
        
        blender_file_location = bpy.path.abspath('//')
        if blender_file_location == None:
            self.report({'ERROR'}, 'Please save blender file. Aborting.')
            return {'FINISHED'}

        # print('LOCATION: ',blender_file_location)
        import json  

        active_obj = bpy.context.selected_objects[0]
        active_obj_children = active_obj.children_recursive
        object_list = active_obj_children
        
        object_assembly = {}

        lr_assembly_ids = []
        id_s = 0


        obj_prefix = ''


        for index,object in enumerate(object_list):
            id_s +=1

            # #Add Unique id for linking object between Unreal and Blender
            # if object.get('lr_assembly_id') is None:
            #     while id_s in lr_assembly_ids:
            #         id_s +=1
            #     object['lr_assembly_id'] = id_s
            #     lr_assembly_ids.append(id_s)
            

            if str(object.name.rsplit('.')[0]).startswith('SM_'):
                obj_name = object.name.rsplit('.')[0]
            else:
                obj_name = 'SM_'+object.name.rsplit('.')[0]


            object_assembly[index] = {'name': obj_name,
                                    'transform': (object.matrix_local.translation[0]*100,object.matrix_local.translation[1]*100,object.matrix_local.translation[2]*100),
                                    'rotation':(object.rotation_euler[0]*180/math.pi,object.rotation_euler[1]*180/math.pi,object.rotation_euler[2]*180/math.pi), 
                                    'scale':(object.scale[0],object.scale[1],object.scale[2]), 
                                    'id':'lr_assembly'
                                    } 


        json_object = json.dumps(object_assembly, indent= 2)

        blender_filename = bpy.path.basename(bpy.context.blend_data.filepath).rsplit('.')[0]
        filename_base = bpy.data.scenes['Scene'].lr_export.lr_assembly_filename
        temp_filename = filename_base
        extension = '.json'
        count = 0


        if bpy.data.scenes['Scene'].lr_export.lr_assembly_replace_file == False:
            while os.path.isfile(blender_file_location+temp_filename+extension):
                count += 1 
                temp_filename = filename_base+str("{:02d}".format(count))
            with open(blender_file_location+temp_filename+extension, "w") as outfile:
                outfile.write(json_object)

        else:
            with open(blender_file_location+filename_base+extension, "w") as outfile:
                outfile.write(json_object)


        return {'FINISHED'}









class OBJECT_OT_lr_pivot_painter_export(bpy.types.Operator):
    bl_idname = "object.lr_pivot_painter_export"
    bl_label = "Export textures for pivot painter 2.0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        '''File is saved next to a .blend file'''

        selected_obj = bpy.context.selected_objects



        object_list = []
        for obj in selected_obj:
            if obj.parent:
                continue
            object_list.append(obj)
            object_list.extend(obj.children_recursive)
        
        image_name_base = object_list[0].name


        def pixels_for_pivot_position_16_bit(objects):
            pixels= []            
            for i in range(0,len(objects)):
                pixels.append([objects[i].location[0]*100, ((objects[i].location[1]*100)*-1)+1, objects[i].location[2]*100,0])
            return pixels


        def pixels_for_vector_ld(objects, axis):
            '''
            Axis: 0 = X, 1 = Y, 2 = Z axis
            '''
            pixels = []

            for index,obj in enumerate(objects):
                matrix_copy = obj.matrix_world.normalized()
                #MAX HAS TRANSPOSED MATRIX
                matrix_copy_transposed = matrix_copy.transposed()
                matrix_copy_transposed.normalize()

                pixels.append(findConstantBiasScaleVectorValues(matrix_copy_transposed[axis]))
            return pixels


        #Alpa Stuff
        def extend_divided_by2048():
            pass

        def wrapFindMaxBoundingDistanceWithLDScale(curVal):
            (clamp(ceil(curVal/8.0))) / 256.0 # up to 2048 units
            #clamp (curVal/(16.0 * 256.0)) 0.005 1.0 # 16 * 256  with a min scale of 16 or the smallest possible unit without hitting 0


        #Universal
        def constantBiasScaleScalar(my_scalar):
                ((my_scalar+1.0)/2.0)


        def findConstantBiasScaleVectorValues(objectArray):
            temp_array = []
            normalizedI = normalize(ob_array)
            temp_array.append([constantBiasScaleScalar(normalizedI[1]),(1.0-(constantBiasScaleScalar(normalizedI[2]))),constantBiasScaleScalar(normalizedI[3])])
            return temp_array











        def create_image(name,img_format, pixels, resolution=None, hdr = False, sRGB = False, alpha = True):
            ''' name: str
                img_format: TGA,OPEN_EXR
                pixels: [[R,G,B,A],[R,G,B,A],[R,G,B,A]...]
                resolution: [x,y] optional else automatically generated

                returns = resolution [x,y]
            '''
            
            if img_format == 'TGA':
                img_extension = '.TGA'

            elif img_format == 'OPEN_EXR':
                img_extension = '.EXR'


            if name is None:
                name = 'PivotPainterImage'


            #Create resolution for an Image
            if resolution == None:
                size = utils.get_closest_resolution(len(pixels))
            else:
                size = resolution
                
            # Create blank Image
            image = bpy.data.images.new(name, width=size[0], height=size[1], alpha = True, float_buffer=hdr, is_data = sRGB)

            #Empty Pixels value
            empty_pixel = [0,0,0,0]


            #Fill remaining pixels with black
            redundant_pixes_amount = size[0]*size[1]-len(pixels)
            for i in range(0,redundant_pixes_amount):
                pixels.append(empty_pixel)

            #Flip image vertically using numpy (blender by default starts in bottom left corner)
            np_array = numpy.array(pixels)
            np_array = np_array.reshape(size[1],size[0],4)
            np_array = numpy.flipud(np_array)
            np_array = np_array.flatten()
            pixels = np_array.tolist()

            # Assign pixels
            image.pixels = pixels

            # Write Image
            blender_file_location = bpy.path.abspath('//')
            if blender_file_location == None:
                self.report({'ERROR'}, 'Please save blender file. Aborting.')
                return {'FINISHED'}


            image.filepath_raw = blender_file_location+name+img_extension
            image.file_format = img_format
            image.save()
            return size
        
        #Including 0
        uv_index = 1


        image_resolution = create_image(name =f'{image_name_base}_UV{uv_index}', img_format = 'OPEN_EXR', pixels = pixels_for_pivot_position_16_bit(object_list), hdr = True, sRGB = False)
      

        # Create list of UVs
        resolution_x = image_resolution[0]
        resolution_y = image_resolution[1]

        np_uv = numpy.array([[0.0,0.0]]*(resolution_x*resolution_y))
        np_uv = np_uv.reshape(resolution_y,resolution_x,2)

        uv_u = 0.5
        uv_v = 0.5
        for V in range(0,len(np_uv)):
            uv_u_t = uv_u
            for U in range(0,len(np_uv[0])):
                np_uv[V][U][0]= uv_u_t
                np_uv[V][U][1]= uv_v
                uv_u_t +=1.0                
            
            uv_v -=1

        np_uv = np_uv.reshape(resolution_x*resolution_y,2)
        #Rescale
        for i in np_uv:
            i[0] = i[0]/resolution_x
            i[1] = ((i[1]-1)/resolution_y)+1

        uv_list = np_uv.tolist()
        # ----------------------------------



        #EDIT UVs


        # ------------------
        uv_pp_name = 'PPIndex'
        
        for index,obj in enumerate(object_list):

            bm_obj = bmesh.new()
            bm_obj.from_mesh(obj.data)
    


            while len(bm_obj.loops.layers.uv)-1 < uv_index-1:
                bm_obj.loops.layers.uv.new('UVMap')


            if uv_index > len(bm_obj.loops.layers.uv)-1:
                bm_obj.loops.layers.uv.new(uv_pp_name)

            uv = bm_obj.loops.layers.uv[uv_index]

            for face in bm_obj.faces:
                for loop in face.loops:
                    loop[uv].uv = uv_list[index][0],uv_list[index][1]


            #Write bmesh
            bm_obj.to_mesh(obj.data)
        return {'FINISHED'}

























