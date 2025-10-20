import os
import sys

DATA_FILE = "data.db"

def load_data():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.rstrip("\n").split(" ", 2)
                if len(parts) == 3 and parts[0].upper() == "SET":
                    key, value = parts[1], parts[2]
                    data.append((key, value))
    return data

def append_to_file(key, value):
    # Append and force to disk immediately
    with open(DATA_FILE, "a") as f:
        f.write(f"SET {key} {value}\n")
        f.flush()
        os.fsync(f.fileno())

def build_index(pairs):
    index = []  # list[(key, value)]
    for key, value in pairs:
        replaced = False
        for i, (k, _) in enumerate(index):
            if k == key:
                index[i] = (key, value)
                replaced = True
                break
        if not replaced:
            index.append((key, value))
    return index

def get_value(index, key):
    for k, v in index:
        if k == key:
            return v
    return None

def main():
    index = build_index(load_data())

    # Read commands strictly from STDIN; output ONLY for GET
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        parts = line.split(" ", 2)
        cmd = parts[0].upper()

        if cmd == "SET" and len(parts) == 3:
            key, value = parts[1], parts[2]
            append_to_file(key, value)
            # update in-memory index without full reload
            updated = False
            for i, (k, _) in enumerate(index):
                if k == key:
                    index[i] = (key, value)
                    updated = True
                    break
            if not updated:
                index.append((key, value))
            # no output for SET

        elif cmd == "GET" and len(parts) == 2:
            val = get_value(index, parts[1])
            print(val if val is not None else "NULL")

        elif cmd == "EXIT":
            break

if __name__ == "__main__":
    main()
