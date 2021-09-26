import os

print("hah")
directory = 'pobeda/server/yaml'

yamlfiles = []
for subdir, dirs, files in os.walk(directory):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".yaml") or filepath.endswith(".yaml"):
            yamlfiles.append(filepath)


print(yamlfiles)

import yaml
import json

for yamlfile in yamlfiles:
    data = []
    with open(yamlfile) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        data = yaml.load(file, Loader=yaml.FullLoader)

    with open(yamlfile[:-4] + "json", 'w') as outfile:
        json.dump(data, outfile)