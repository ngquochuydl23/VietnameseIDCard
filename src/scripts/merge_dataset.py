import os
import shutil

def copy_files(path):
    for file in os.listdir(path):
        print(file)

def merge_dataset(dir_collection, dest_dir):
    # if not os.path.exists(dest_dir):
    #     os.mkdir(dest_dir)

    # for dir in dir_collection:
    #     for sub_dir in os.listdir(dir):

    #         if os.path.isdir(os.path.join(dir, sub_dir)) and os.path.exists(os.path.join(dir, sub_dir)):
    #             copy_files(os.path.join(dir, sub_dir))

    for index, dir in enumerate(dir_collection):
        print(f'index: {index}')
                
def rename_datesets(dir_path, type):

    root = os.path.join(dir_path, type)
    images = os.path.join(root, 'images')
    labels = os.path.join(root, 'labels')


    for idx, file in enumerate(os.listdir(images)):
        current_img_path = os.path.join(images, os.listdir(images)[idx])
        current_label_path = os.path.join(labels, os.listdir(labels)[idx])
        #print(current_img_path)
        os.rename(current_img_path, os.path.join(dir_path, type, 'images', f'cancuoccongdan-{idx}.jpg'))

        if os.path.exists(current_img_path):
            os.remove(current_img_path)

        os.rename(current_label_path, os.path.join(dir_path, type, 'labels', f'cancuoccongdan-{idx}.txt'))
   
        if os.path.exists(current_label_path):
            os.remove(current_label_path)
            

if __name__ == '__main__':
    #merge_dataset(['CCCD_Word_Detection.v2i.yolov8'], 'merge_dataset_v1')
    rename_datesets('merge_dataset_v1', type='train')
    rename_datesets('merge_dataset_v1', type='test')
    rename_datesets('merge_dataset_v1', type='valid')

