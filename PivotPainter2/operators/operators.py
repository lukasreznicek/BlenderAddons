import bpy, os, math, numpy, bmesh, random
from . import utils


class OBJECT_OT_lr_pivot_painter_export(bpy.types.Operator):
    bl_idname = "object.lr_pivot_painter_export"
    bl_label = "Export textures for pivot painter 2.0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        '''File is saved next to a .blend file'''
        
        myprops = bpy.context.scene.pivot_painter_2

    
        if bpy.data.is_saved == False:
            self.report({'ERROR'}, 'Please save blender file. Aborting.')
            return {'FINISHED'}

        selected_obj = bpy.context.selected_objects

        object_list = []
        for obj in selected_obj:
            if obj.parent:
                continue
            object_list.append(obj)
            object_list.extend(obj.children_recursive)
        
        #Get image resolution based on number of objects
        resolution = utils.find_texture_dimensions(len(object_list))



        # Create list of UVs
        resolution_x = resolution[0]
        resolution_y = resolution[1]

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



        #EDIT UVs ----------------------------
        
        uv_index = 1 #Including 0
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


        def pixels_for_pivot_position_16_bit(objects):
            pixels= []            
            for i in range(0,len(objects)):
                pixels.append([objects[i].location[0]*100, ((objects[i].location[1]*100)*-1)+1, objects[i].location[2]*100])
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



        def pixels_for_alpha_random_value_per_element(number_of_objects):
            rand_val = []
            for value in range(0,number_of_objects):
                rand_val.append(random.uniform(0,1))

            return rand_val

        #Alpa Stuff
        def extend_divided_by2048():
            pass

        def wrapFindMaxBoundingDistanceWithLDScale(curVal):
            (clamp(ceil(curVal/8.0))) / 256.0 # up to 2048 units
            #clamp (curVal/(16.0 * 256.0)) 0.005 1.0 # 16 * 256  with a min scale of 16 or the smallest possible unit without hitting 0


        #Universal
        def constantBiasScaleScalar(my_scalar):
            return (my_scalar+1.0)/2.0


        def findConstantBiasScaleVectorValues(objectArray):
            normalizedI = objectArray
            return [constantBiasScaleScalar(normalizedI[0]),(1.0-(constantBiasScaleScalar(normalizedI[1]))),constantBiasScaleScalar(normalizedI[2])]

	    def pixels_for_alpha_find_parent_object_array_index(object_array): #Parent Index ( Float - Up to 2048 )
            array_index = []
            for obj in object_array:
                if obj.parent == None:
                    array_index.append(object_array.index(obj)-0.5)
                else:
                    array_index.append(object_array.index(obj.parent)-0.5)
            return array_index



        # #packTextureBits f16
        # def packTextureBits():
        #     f16= f16 as integer
        #     f16+=1024
        #     sign = bit.shift  (bit.and f16 0x8000) 16
        #     expVar =if (bit.and f16 0x7fff) == 0 then (0) else (bit.shift ((bit.and (bit.shift f16 -10) 0x1f)-15+127) 23)
        #     mant =bit.shift (bit.and f16 0x3ff) 13
        #     f16= bit.or (bit.or sign expVar) mant 
        #     bit.intAsFloat f16  



        # def pack_ints_into_floats(value_array):
        #     tArray=[]
        #     for value in value_array:
        #         tArray.append(packTextureBits(value))
        #     return tArray


        def create_image(name,image_format, pixels,alpha_values = None, resolution=None, hdr = False, sRGB = False, alpha = True, image_location = None):
            ''' name: str
                image_format: TARGA,OPEN_EXR
                pixels: [[R,G,B,A],[R,G,B,A],[R,G,B,A]...]
                resolution: [x,y] optional else automatically generated

                returns = resolution [x,y]
            '''
            if alpha_values == None:
                for pixel in pixels:
                    pixel.append(0)
            else:
                
                if len(pixels) == len(alpha_values):
                    for pixel,alpha_value in zip(pixels,alpha_values):
                        pixel.append(alpha_value)
                else:
                    self.report({'INFO'}, 'Alpha values and Pixel values mismatch')



            if image_location == None:
                image_location = bpy.path.abspath('//')
            elif image_location.startswith('//'):
                image_location = bpy.path.abspath(image_location)

            if bpy.data.is_saved == False:
                self.report({'ERROR'}, 'Please save blender file. Aborting.')
                return {'FINISHED'}    
            
            if image_format == 'TARGA':
                img_extension = '.TGA'

            elif image_format == 'OPEN_EXR':
                img_extension = '.EXR'


            if name is None:
                name = 'PivotPainterImage'


            #Create resolution for an Image
            if resolution == None:
                size = utils.find_texture_dimensions(len(pixels))
            else:
                size = resolution



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

            # Create blank Image
            image = bpy.data.images.new(name, width=size[0], height=size[1], alpha = True, float_buffer=hdr, is_data = sRGB)

            # Assign pixels
            image.pixels = pixels

            # Write Image
            blender_file_location = image_location

            image.filepath_raw = blender_file_location+name+img_extension
            image.file_format = image_format
            image.save()
            return size
        


        #ASSEMBLY

        image_name_base = object_list[0].name

        # ---- IMAGE 1 RGB ----
        if myprops.image_1_rgb != 'OP0' : 
            if myprops.image_1_rgb == 'OP1': #Pivot Position (16-bit)
                img_pixels = pixels_for_pivot_position_16_bit(object_list)
                img_hdr = True
                img_sRGB = False
                img_format = 'OPEN_EXR'
                img_name = f'{image_name_base}_PivotPosition16bit_UV{uv_index}'
   
            if myprops.image_1_rgb == 'OP4': #X Vector (8-bit)
                img_name = f'{image_name_base}_XVector8bit_UV{uv_index}'
                img_pixels = pixels_for_vector_ld(object_list,0)
                img_hdr = False
                img_sRGB = False
                img_format = 'TARGA'

            if myprops.image_1_rgb == 'OP5': #Y Vector (8-bit)
                img_name = f'{image_name_base}_YVector8bit_UV{uv_index}'
                img_pixels = pixels_for_vector_ld(object_list,1)
                img_hdr = False
                img_sRGB = False
                img_format = 'TARGA'

            if myprops.image_1_rgb == 'OP6': #Z Vector (8-bit)
                img_name = f'{image_name_base}_ZVector8bit_UV{uv_index}'
                img_pixels = pixels_for_vector_ld(object_list,2)
                img_hdr = False
                img_sRGB = False
                img_format = 'TARGA'


        #---- IMAGE 1 Alpha ----

            if myprops.image_1_alpha == 'OP1': #Parent Index (Int as Float)
                img_alpha_values = None
            
            if myprops.image_1_alpha == 'OP3': #Random 0-1 Value Per Element
                img_alpha_values = pixels_for_alpha_random_value_per_element(len(object_list))


            if myprops.image_1_rgb == 'OP10': #Parent Index ( Float - Up to 2048 )
                img_alpha_values = pixels_for_alpha_find_parent_object_array_index(object_list)


            create_image(name =img_name, image_format = img_format, resolution=resolution, pixels = img_pixels, alpha_values = img_alpha_values, hdr = img_hdr, sRGB = img_sRGB,image_location=myprops.export_path)
            


        #IMAGE 2

        #---- IMAGE 2 RGB ---

        if myprops.image_2_rgb != 'OP0' : 
            if myprops.image_2_rgb == 'OP1': #Pivot Position (16-bit)
                img_pixels = pixels_for_pivot_position_16_bit(object_list)
                img_hdr = True
                img_sRGB = False
                img_format = 'OPEN_EXR'
                img_name = f'{image_name_base}_PivotPosition16bit_UV{uv_index}'


            if myprops.image_2_rgb == 'OP4': #X Vector (8-bit)
                img_name = f'{image_name_base}_XVector8bit_UV{uv_index}'
                img_pixels = pixels_for_vector_ld(object_list,0)
                img_hdr = False
                img_sRGB = False
                img_format = 'TARGA'


            if myprops.image_2_rgb == 'OP5': #Y Vector (8-bit)
                img_name = f'{image_name_base}_YVector8bit_UV{uv_index}'
                img_pixels = pixels_for_vector_ld(object_list,1)
                img_hdr = False
                img_sRGB = False
                img_format = 'TARGA'

            if myprops.image_2_rgb == 'OP6': #Z Vector (8-bit)
                img_name = f'{image_name_base}_ZVector8bit_UV{uv_index}'
                img_pixels = pixels_for_vector_ld(object_list,2)
                img_hdr = False
                img_sRGB = False
                img_format = 'TARGA'

            #---- IMAGE 2 Alpha ----

            if myprops.image_2_alpha == 'OP3': #Random 0-1 Value Per Element
                img_alpha_values = pixels_for_alpha_random_value_per_element(len(object_list))

            if myprops.image_1_rgb == 'OP10': #Parent Index ( Float - Up to 2048 )
                img_alpha_values = pixels_for_alpha_find_parent_object_array_index(object_list)



            create_image(name =img_name, image_format = img_format,resolution=resolution, pixels = img_pixels,alpha_values = img_alpha_values, hdr = False, sRGB = False, image_location=myprops.export_path)



        self.report({'INFO'}, 'Done')


        return {'FINISHED'}
























