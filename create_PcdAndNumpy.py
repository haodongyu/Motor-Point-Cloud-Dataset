import bpy 
import os 
import blensor
import numpy as np
from utils_haodong import Operator


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
    
    rename_element('Motor')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = None


def import_ClampingSystem_obj(path):     # for Blender 2.79-Version: need rename and conbination

    bpy.ops.import_scene.obj(filepath=path, filter_glob="*.obj")
    rename_element('Clamping')
    
    bpy.context.scene.objects.active = bpy.data.objects['0000_Clamping_0']
    bpy.ops.object.select_pattern(pattern = "0000")
    bpy.ops.object.join()
    bpy.data.objects['0000_Clamping_0'].name = '0000_ClampingSystem'          # Rename the ClampingSystem's name

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = None


def delete_allElement(): 
    '''
        Delete all elements except Camera, lamp and clympingsystem
    '''
    filter_keep = ['Camera', '0000_ClampingSystem', 'Point', 'Point.001', 'Point.002', 'Camera.001']
    for obj in bpy.data.objects :
        if not obj.name in filter_keep :
            bpy.data.objects.remove(obj)


def intialize_lamp():

    bpy.ops.object.select_all(action='DESELECT')
    # bpy.data.objects['Point'].location = (0, -5.5, 1.6)
    # bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
    # bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)

    if bpy.data.objects['Point'] and bpy.data.objects['Point.001'] and bpy.data.objects['Point.002'] :
            
        bpy.data.objects['Point'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Point']
        bpy.context.object.data.energy = 0.8
        bpy.context.object.data.use_specular = False

        bpy.ops.object.select_all(action='DESELECT')

       # bpy.context.object.data.type = ''                   # ['POINT', 'SUN', 'SPOT', 'HEMI', 'AREA']

        bpy.data.objects['Point.001'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Point.001']
        bpy.context.object.data.energy = 0.8
        bpy.context.object.data.use_specular = False

        bpy.ops.object.select_all(action='DESELECT')

        bpy.data.objects['Point.002'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Point.002']
        bpy.context.object.data.energy = 0.8
        bpy.context.object.data.use_specular = False

        bpy.ops.object.select_all(action='DESELECT')


def lamp_check(objects_name) :


    if 'Point' in objects_name and 'Point.001' in objects_name and 'Point.002' in objects_name:
                intialize_lamp()
                bpy.data.objects['Point'].location = (0, -5.5, 1.6)
                bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
                bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)
    else :
        for _ in range(3) :
            bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location = (5, 5, 5), 
                layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

        intialize_lamp()
        bpy.data.objects['Point'].location = (0, -5.5, 1.6)
        bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
        bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)
        

    
        



def create_new_Camera(location, rotation):
    bpy.ops.object.camera_add(location=location, rotation=rotation, layers=(True, False, False, False, False, False, False, False, False, False, 
        False, False, False, False, False, False, False, False, False, False))


def rename_element(element_type ):      # element_type = ['Clamping', 'Motor']
    k = 0
    if element_type == 'Clamping' :
        for i in range(len(bpy.data.objects)):
            if 'mesh' in bpy.data.objects[i].name:
                bpy.data.objects[i].name = '0000_Clamping_' + str(k)
                k += 1
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
        bpy.data.objects['0000_ClampingSystem'].select = True
        bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), 
            constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    elif element_type == 'Motor' :
        for obj in bpy.data.objects:
            if ('0000' not in obj.name) and ('Camera' not in obj.name) :
                bpy.ops.object.select_all(action='DESELECT')
                obj.select = True
                bpy.ops.transform.resize(value=(0.05, 0.05, 0.05), constraint_axis=(False, False, False), 
                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


def Translate_Rotation_element(element_type, Motor_type) :

    if element_type == 'Clamping' :
        bpy.data.objects['0000_ClampingSystem'].location = (0,0,0)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['0000_ClampingSystem'].select = True
        bpy.ops.transform.translate(value=(-1.85, 0, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', 
            mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    elif element_type == 'Motor' :
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects :
            if ('0000' not in obj.name) and ('Camera' not in obj.name) :
                obj.select = True
                obj.location = (0, 0, 0)
    
        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False),               # Ratotate all the Motor part 90` at Y axis
            constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        if  Motor_type != 'TypeA1' and Motor_type != 'TypeANone':
            bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False),               # Ratotate all the Motor part 90` at x axis
                constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        bpy.ops.transform.translate(value=(-0.18, -1.05, 1.25), constraint_axis=(False, False, False), 
            constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)



def scan(save_dir, save_numpy, Motor_type, scanner, sequence_Motor):

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.camera = bpy.data.objects['Camera']
    bpy.data.objects['Camera'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Camera']

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

    if bpy.data.objects['Camera.001'] :
        bpy.context.scene.camera = bpy.data.objects['Camera.001']
        bpy.data.objects['Camera.001'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['Camera.001']


        image_scene = bpy.context.scene

        save_image_path = image_save_path + '\\' + 'scan_image_' + sequence_Motor + '.png'
        image_scene.render.image_settings.file_format = 'PNG'
        image_scene.render.filepath = save_image_path
        bpy.ops.render.render(write_still = 1)

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
        if bpy.data.objects['Lamp'] :       # Delete the Cube object and Lamp object from Blender's intialization
            bpy.data.objects.remove(bpy.data.objects['Lamp'])
    except KeyError :
        pass
    
    # Translate Camera to the better Location  and rotation
    bpy.data.objects['Camera'].location = (1, -5.4, 0.85)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Camera'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['Camera']
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False),               # Ratotate the Camera object 90` at y axis
        constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.object.select_all(action='DESELECT')


    objects_name = []
    for obj in bpy.data.objects :
        objects_name.append(obj.name)

    if 'data.csv' in List_motor :
        List_motor.remove('data.csv')

    if not '0000_ClampingSystem' in objects_name :
        import_ClampingSystem_obj(Clamping_dir)
        resize_element('Clamping')
        Translate_Rotation_element('Clamping', Motor_type)



    if not 'Camera.001' in objects_name :
        create_new_Camera(location = (0, -4.78, 1.6), rotation = (1.57, 1.57, 0)) 
    else:
        print("There are all ready two cameras")   



    ###################################################
    #   scan all the files from the holder            #
    ###################################################
    if scan_mode == 'all_folders' :
        for dirs in List_motor :

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
            scan(save_dir = save_dir_whole, save_numpy = True, Motor_type = Motor_type, scanner = bpy.data.objects['Camera'], sequence_Motor = k[1])

            ####### Intialize the lamp position ###########
            lamp_check(objects_name)
            # if 'Point' in objects_name and 'Point.001' in objects_name and 'Point.002' in objects_name:
            #     intialize_lamp()
            #     bpy.data.objects['Point'].location = (0, -5.5, 1.6)
            #     bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
            #     bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)
            # else :
            #     for _ in range(3) :
            #         bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location = (5, 5, 5), 
            #             layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            #     intialize_lamp()
            #     bpy.data.objects['Point'].location = (0, -5.5, 1.6)
            #     bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
            #     bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)

            export_png(save_dir_whole, k[1])

            save_dir_motor = save_dir + '\\' + 'motor'
            if not os.path.exists(save_dir_motor) :
                os.makedirs(save_dir_motor)
            bpy.data.objects["0000_ClampingSystem"].hide_render = True
            scan(save_dir = save_dir_motor, save_numpy = True, Motor_type = Motor_type, scanner = bpy.data.objects['Camera'], sequence_Motor = k[1])

            ####### Intialize the lamp position ###########
            lamp_check(objects_name)
            # if 'Point' in objects_name and 'Point.001' in objects_name and 'Point.002' in objects_name:
            #     intialize_lamp()
            #     bpy.data.objects['Point'].location = (0, -5.5, 1.6)
            #     bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
            #     bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)
            # else :
            #     for _ in range(3) :
            #         bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location = (5, 5, 5), 
            #             layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            #     intialize_lamp()
            #     bpy.data.objects['Point'].location = (0, -5.5, 1.6)
            #     bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
            #     bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)

            export_png(save_dir_motor, k[1])
            bpy.data.objects["0000_ClampingSystem"].hide_render = False


            delete_allElement()
    
    elif scan_mode == 'single' :
        dirs = 'MOtor_0001'
        Motor_path = file_path + '\\' + dirs


        # Intialize the Motor's parts and ClampingSystem
        import_MotorPart_obj(Motor_path, filters)
        resize_element('Motor')
        Translate_Rotation_element('Motor', Motor_type)           # elment_Type = ['Motor', 'Clamping']    Motor_type = ['TypeA1', others]

        ####### Intialize the lamp position ###########
        lamp_check(objects_name)
        # if 'Point' in objects_name and 'Point.001' in objects_name and 'Point.002' in objects_name:
        #         intialize_lamp()
        #         bpy.data.objects['Point'].location = (0, -5.5, 1.6)
        #         bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
        #         bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)
        # else :
        #     for _ in range(3) :
        #         bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location = (5, 5, 5), 
        #             layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #     intialize_lamp()
        #     bpy.data.objects['Point'].location = (0, -5.5, 1.6)
        #     bpy.data.objects['Point.001'].location = (0.7, -4.4, 0.78)
        #     bpy.data.objects['Point.002'].location = (0.6, -5.72, 3.35)

       # scan(save_dir = save_dir_whole, save_numpy = True, Motor_type = 'TypeA_1', scanner = bpy.data.objects['Camera'], sequence_Motor = k[1])





if __name__ == '__main__':
    main()
