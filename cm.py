from cml import utils
from cml import Project

script_dir = utils.script_dir()
print(script_dir)

data_dir = utils.data_dir()
print(data_dir)

project = Project()
print(project.f())
