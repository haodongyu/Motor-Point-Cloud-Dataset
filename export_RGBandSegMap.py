import bpy 
import os 
import numpy as np


def import_MotorPart_obj(path, filters):

    need_file_items = []
    need_file_names = []

    filterDict = {}
    for item in filters:
        filterDict[item] = True

    file_lst = os.listdir(path)

    for item in file_lst:
        fileName, fileExtension = os.path.splitext(item)
        if fileExtension == ".obj" and (not item in filterDict):
            need_file_items.append(item)
            need_file_names.append(fileName)

    n = len(need_file_items)
    for i in range(n):
        item = need_file_items[i]
        itemName = need_file_names[i]
        ufilename = path + "\\" + item
        bpy.ops.import_scene.obj(filepath=ufilename, filter_glob="*.obj")
        # if (bpy.data.objects[itemName]):
        #     bpy.data.objects[itemName].hide = False
        #     bpy.data.objects[itemName].hide_render = True
    
    rename_element('Motor', 0)
    set_category_id('Motor')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None


def import_ClampingSystem_obj(path, num_Clamping):     # for Blender 2.79-Version: need rename and conbination

    bpy.ops.import_scene.obj(filepath=path, filter_glob="*.obj")
    rename_element('Clamping', num_Clamping)
    bpy.data.objects['0000_ClampingSystem']["category_id"] = 1

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None


def delete_allElement(): 
    '''
        Delete all elements except Camera, lamp and clympingsystem
    '''
    filter_keep = ['Camera']
    for obj in bpy.data.objects :
        if not obj.name in filter_keep :
            bpy.data.objects.remove(obj)

def set_category_id(element_type) :
    if element_type == 'Motor' :
        k = 2
        for obj in bpy.data.objects :
            if obj.name != '0000_ClampingSystem' and ('6666' not in obj.name) :
                obj['category_id'] = k
                k += 1

            if '6666' in obj.name :
                obj['category_id'] = 6

        



def create_new_Camera(location, rotation):
    bpy.ops.object.camera_add(location=location, rotation=rotation, layers=(True, False, False, False, False, False, False, False, False, False, 
        False, False, False, False, False, False, False, False, False, False))


def rename_element(element_type, i):      # element_type = ['Clamping', 'Motor']
    k = 0
    if element_type == 'Clamping' :
        if i == 0 :
            bpy.data.objects['ClampingSystem'].name = '0000_ClampingSystem'
        else :
            name_ClampingSystem = 'ClampingSystem' + '.00' + str(i)
            bpy.data.objects[name_ClampingSystem].name = '0000_ClampingSystem'

    elif element_type == 'Motor' :
        for i in range(len(bpy.data.objects)):
            if 'Bolt' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '6666_Bolt_' + str(k)
                k += 1
            elif 'Bottom' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '5555_Bottom'
            elif 'Charge' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '4444_Charge'
            elif 'Cover' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '1111_Cover'
            elif 'Gear_Container' in  bpy.data.objects[i].name:
                bpy.data.objects[i].name = '2222_Gear_Container'



def resize_element(element_type) :      # Resize ClampingSystem to 5 scale and Motor 0.05 scale

    if element_type == 'Clamping' :
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['0000_ClampingSystem'].select_set(True)
        bpy.ops.transform.resize(value=(5, 5, 5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
            mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    elif element_type == 'Motor' :
        for obj in bpy.data.objects:
            if ('0000' not in obj.name):
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.ops.transform.resize(value=(0.05, 0.05, 0.05), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
                    mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
                    use_proportional_projected=False)


def Translate_Rotation_element(element_type, Motor_type) :

    if element_type == 'Clamping' :
        bpy.data.objects['0000_ClampingSystem'].location = (0,0,0)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['0000_ClampingSystem'].select_set(True)
        bpy.ops.transform.translate(value=(-1.85, -0, -0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
            constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
            use_proportional_projected=False)


    elif element_type == 'Motor' :
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects :
            if ('0000' not in obj.name):
                obj.select_set(True)
                obj.location = (0, 0, 0)
    
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
            constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
            use_proportional_projected=False)

        if  Motor_type != 'TypeA1' and Motor_type != 'TypeANone':
            bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
                constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
                use_proportional_projected=False)

        bpy.ops.transform.translate(value=(-0.18, -1.05, 1.25), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
            constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, 
            use_proportional_projected=False)
        bpy.ops.object.select_all(action='DESELECT')



def scan(save_dir, save_numpy, Motor_type, scanner, sequence_Motor):

    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.object.save_scan = True
    bpy.context.object.scan_type = 'kinect'
    bpy.context.object.kinect_xres = 1080
    bpy.context.object.kinect_yres = 960
    # bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False),               # Ratotate the Camera object 90` at y axis
    #             constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    saved_file_path = save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '.pcd'
    blensor.kinect.scan_advanced(scanner, evd_file= saved_file_path)

    os.remove(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor)
    os.remove(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '_noisy00000' + '.pcd')
    os.rename(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '00000' + '.pcd', save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '.pcd')

    if save_numpy :
        saved_numpy_path = save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '.numpy'
        blensor.kinect.scan_advanced(scanner, evd_file= saved_numpy_path)
        numpy_name = 'scan_' + Motor_type + '_' + sequence_Motor 
        motorNumpy_file = save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '00000' + '.numpy'
       # os.rename(save_dir + '\\' + 'scan_' + Motor_type + '_' + sequence_Motor + '00000' + '.numpy', save_dir + '\\' + numpy_name + '.numpy')

        #########  transform the numpy file  #############
        motor_numpy = np.loadtxt(motorNumpy_file)
        filtered = Operator.CutNumpy(motor_numpy)
        filtered = Operator.ChangeLabel(filtered)
        filtered = Operator.Resort_IDX(filtered)
        np.save(save_dir + '\\' + numpy_name , filtered)
        os.remove(motorNumpy_file)

    bpy.ops.object.select_all(action='DESELECT')


def export_png(image_save_path, sequence_Motor) :
    bpy.ops.object.select_all(action='DESELECT')


    save_blend_file = image_save_path + '\\' + 'render_image_' + sequence_Motor + '.blend'

    if 'render_image_' + sequence_Motor + '.blend' not in os.listdir(image_save_path) :
        bpy.ops.wm.save_as_mainfile(filepath=save_blend_file)            # save the blend file


    #######################

    #######################
    BlenderProc_path = "F:/KIT/Masterarbeit/Dataset_builder/BlenderProc/run.py "
    config_path = "F:/KIT/Masterarbeit/Dataset_builder/BlenderProc/examples/semantic_segmentation/config.yaml "
    camera_position_seg = "F:/KIT/Masterarbeit/Dataset_builder/BlenderProc/examples/semantic_segmentation/camera_positions "
    save_blend_file_1 = save_blend_file + ' '
    seg_output_path = image_save_path.replace('\\', '/')
    seg_run_order = "python " + BlenderProc_path + config_path + camera_position_seg + save_blend_file_1.replace('\\', '/') + seg_output_path
    os.system(seg_run_order)

    

    os.system("python " + "F:/KIT/Masterarbeit/Dataset_builder/BlenderProc/scripts/saveAsImg.py " + seg_output_path + '/' + '0.hdf5')

    if '0.hdf5' in os.listdir(image_save_path) and '0_segmap.png' in os.listdir(image_save_path):
        os.remove(save_blend_file)

    bpy.ops.object.select_all(action='DESELECT')








def main():
    scan_mode = 'all_folders'                             # ['single', 'all_folders']
    file_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA1"
    filters = ["Motor.obj"]                                # No_needed obj file
    Clamping_dir = "F:\KIT\Masterarbeit\Dateset\clampingSystem\ClampingSystem.obj"
    root, Motor_type = os.path.split(file_path)
    save_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\PCD" + '\\' + Motor_type

    List_motor = os.listdir(file_path) # Path List for .obj file
    
    try :
        if bpy.data.objects['Cube'] :       # Delete the Cube object and Lamp object from Blender's intialization
            bpy.data.objects.remove(bpy.data.objects['Cube'])
        if bpy.data.objects['Light'] :       # Delete the Cube object and Lamp object from Blender's intialization
            bpy.data.objects.remove(bpy.data.objects['Light'])
        if bpy.data.objects['Camera'] :       # Delete the Cube object and Lamp object from Blender's intialization
            bpy.data.objects.remove(bpy.data.objects['Camera'])
    except KeyError :
        pass


    objects_name = []
    for obj in bpy.data.objects :
        objects_name.append(obj.name)

    if 'data.csv' in List_motor :
        List_motor.remove('data.csv')



    ###################################################
    #   scan all the files from the holder            #
    ###################################################
    num_Clamping = 0
    if scan_mode == 'all_folders' :
        for dirs in List_motor :

            if not '0000_ClampingSystem' in objects_name :
                import_ClampingSystem_obj(Clamping_dir, num_Clamping)
                resize_element('Clamping')
                Translate_Rotation_element('Clamping', Motor_type)
                num_Clamping += 1

            Motor_path = file_path + '\\' + dirs
            # Translate Camera to the better Location  and rotation
           # bpy.data.objects['Camera'].location = (0, -4.98905, 1.45000)

            # Intialize the Motor's parts and ClampingSystem
            import_MotorPart_obj(Motor_path, filters)
            resize_element('Motor')
            Translate_Rotation_element('Motor', Motor_type)

            # run blensor's scanner and scan motor with clampingsystem
            save_dir = save_path + '\\' + dirs
            k = dirs.split('_')
            save_dir_whole = save_dir + '\\' + 'whole'
            if not os.path.exists(save_dir_whole) :
                os.makedirs(save_dir_whole)
           # scan(save_dir = save_dir_whole, save_numpy = True, Motor_type = Motor_type, scanner = bpy.data.objects['Camera'], sequence_Motor = k[1])

            export_png(save_dir_whole, k[1])


            save_dir_motor = save_dir + '\\' + 'motor'
            if not os.path.exists(save_dir_motor) :
                os.makedirs(save_dir_motor)

            bpy.data.objects.remove(bpy.data.objects['0000_ClampingSystem'])
            export_png(save_dir_motor, k[1])


            delete_allElement()
    
    elif scan_mode == 'single' :
        if not '0000_ClampingSystem' in objects_name :
            import_ClampingSystem_obj(Clamping_dir, num_Clamping = 0)
            resize_element('Clamping')
            Translate_Rotation_element('Clamping', Motor_type)

        dirs = 'MOtor_0001'
        Motor_path = file_path + '\\' + dirs


        # Intialize the Motor's parts and ClampingSystem
        import_MotorPart_obj(Motor_path, filters)
        resize_element('Motor')
        Translate_Rotation_element('Motor', Motor_type)           # elment_Type = ['Motor', 'Clamping']    Motor_type = ['TypeA1', others]




if __name__ == '__main__':
    main()
