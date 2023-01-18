import argparse
import json
import os
import tempfile
import pprint

def read_key(key_name):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if os.path.isfile(storage_path):
        with open(storage_path, 'r') as f:
            try:
                data = f.read()
                d = json.loads(data)
                val_list = []
                for key_value in d:
                    if key_value['key'] == key_name:
                        val_list.append(key_value['val'])
                print(', '.join(val_list))
            except json.decoder.JSONDecodeError:
                print("Файл пустой")
    else:
        return {}

def set_key(key_name, value):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if os.path.isfile(storage_path):
        with open(storage_path, 'r+') as f:
            data = f.read()
            d = json.loads(data)
            f.seek(0)
            d.append({'key': key_name, 'val': value})
            json.dump(d, f, indent=4)

    else:
        with open(storage_path, 'w') as f:
            json.dump([{'key': key_name, 'val': value}], f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", dest="key_name")
    parser.add_argument("--val", dest="value")
    args = parser.parse_args()

    if not args.value is None:
        set_key(args.key_name, args.value)
    elif not args.key_name is None:
        read_key(args.key_name)