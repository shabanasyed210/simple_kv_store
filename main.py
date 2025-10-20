import os

DATA_FILE = "data.db"

# ---------------------------
# Load existing data from disk
# ---------------------------
def load_data():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 2)
                if len(parts) == 3 and parts[0] == "SET":
                    key, value = parts[1], parts[2]
                    data.append((key, value))
    return data


# ---------------------------
# Save a new SET command
# ---------------------------
def append_to_file(key, value):
    with open(DATA_FILE, "a") as f:
        f.write(f"SET {key} {value}\n")


# ---------------------------
# Build in-memory index (no dicts allowed)
# ---------------------------
def build_index(data):
    index = []  # list of (key, value)
    for key, value in data:
        # if key already exists, replace old value
        found = False
        for i, (k, v) in enumerate(index):
            if k == key:
                index[i] = (key, value)
                found = True
                break
        if not found:
            index.append((key, value))
    return index


# ---------------------------
# Find value for a key
# ---------------------------
def get_value(index, key):
    for k, v in index:
        if k == key:
            return v
    return None


# ---------------------------
# Main program loop
# ---------------------------
def main():
    data = load_data()
    index = build_index(data)

    print("Simple Key-Value Store started. Type SET <key> <value> or GET <key>.")
    while True:
        try:
            command = input("> ").strip()
            if not command:
                continue

            parts = command.split(" ", 2)
            cmd = parts[0].upper()

            if cmd == "SET" and len(parts) == 3:
                key, value = parts[1], parts[2]
                append_to_file(key, value)
                index = build_index(load_data())
                print("OK")

            elif cmd == "GET" and len(parts) == 2:
                key = parts[1]
                value = get_value(index, key)
                if value is not None:
                    print(value)
                else:
                    print("NULL")

            elif cmd == "EXIT":
                print("Exiting...")
                break

            else:
                print("Invalid command. Use SET <key> <value>, GET <key>, or EXIT.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
