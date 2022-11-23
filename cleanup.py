
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

def remove_file(filename):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
    os.remove(file_path)

try:
    remove_directory('training_data')
    remove_directory('saved_model')
    remove_file('names.json')
    remove_file('attendance.xlsx')
except Exception as e:
    print(e)
    pass
