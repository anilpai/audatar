import jprops
import os
file_path = os.path.sep.join(os.path.dirname(__file__).split(os.path.sep)[:-2])

with open(file_path+'/secrets.properties') as fp:
    properties = jprops.load_properties(fp)
