class KeyValueStore:
    def __init__(self):
        self.store = {}

    def action(self, cmd, key=None, value=None):
        if cmd == "put":
            if key and value:
                self.store[key] = value
                return f"Key '{key}' added/updated with value '{value}'"
            else:
                return "Error: PUT command requires a key and value"
        elif cmd == "get":
            if key:
                return self.store.get(key, "Error: Key not found")
            else:
                return "Error: GET command requires a key"
        elif cmd == "delete":
            if key:
                if key in self.store:
                    del self.store[key]
                    return f"Key '{key}' deleted"
                else:
                    return "Error: Key not found"
            else:
                return "Error: DELETE command requires a key"
        else:
            return "Error: Invalid command"


# Example usage of the KeyValueStore function
kv_store = KeyValueStore()
print(kv_store.action("put", "name", "John"))
print(kv_store.action("get", "name"))
print(kv_store.action("delete", "name"))
print(kv_store.action("get", "name"))
print(kv_store.action("do_something", "name"))