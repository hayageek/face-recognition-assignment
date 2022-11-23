
import os
import glob

def remove_directory(dirname):
    try:
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),dirname)
        files = glob.glob('{}/*.jpg'.format(dir_path))
        for f in files:
            os.remove(f)
        os.rmdir(dir_path)
    except:
        pass

try:
    remove_directory('training_data')
    remove_directory('saved_model')
    names_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'names.json')
    print(names_file_path)
    os.remove(names_file_path)
except Exception as e:
    print(e)
    pass
