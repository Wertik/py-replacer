import os
import os.path as path
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to edit")
parser.add_argument("key", help="key to look for")
parser.add_argument("--add", help="number to add to found result(s)", type=int)
args = parser.parse_args()

def load_yaml(file):

    if path.exists(file) is False:
        print("Could not find file " + path)
        return None

    with open(file, 'r') as data:
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError as e:
            print(e)

def save_yaml(file, data):
    with open(file, 'w') as f:
        yaml.dump(data, f)
        print("Saved " + file)

results = {}

def search(where, param, path, parent):
    path += "." + parent

    for key in where:

        value = where[key]

        parent = key

        if key == param:
            if args.add != None:
                if isinstance(value, int):
                    val = int(value)
                    val += args.add
                    where[key] = val
                    results[path[2:]] = [value, val]
        elif isinstance(value, dict):
            search(value, param, path, parent)

def main():
    data = load_yaml(args.file)

    if data == None:
        return

    search(data, args.key, "", "")

    print("\nResults ( " + str(len(results)) + " ):")
    for key in results: print(key + " : " + str(results[key][0]) + " - > " + str(results[key][1]))  

    save_yaml(args.file, data)

if __name__=="__main__":
    main()