import os, json, getpass

BASE_PATH = "/Users/" + getpass.getuser() + "/capstone_data/raw_data/"
os.system("mkdir " + "/".join(BASE_PATH.split("/")[:-2]))
os.system("mkdir " + BASE_PATH)
DATA_SOURCE = "data_source.txt"
source_paths = json.load(open(DATA_SOURCE))

## Vaccination
os.system("mkdir " + BASE_PATH + "school_vaccination")
vaccination_paths = source_paths['vaccination']

for folder, paths in vaccination_paths.items():
    folder_path = BASE_PATH + "school_vaccination/" + folder + "/"
    os.system("mkdir " + folder_path)
    for i, path in enumerate(paths):
        cmd = "curl " + path + " -o " + folder_path + path.split("/")[-1]
        os.system(cmd)
        
## Census
os.system("mkdir " + BASE_PATH + "census/")
census_paths = source_paths['census']