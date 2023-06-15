class KeyValueStore:

    def __init__(self):
        self.store = {}

    def set(self, key, value):
        self.store[key] = value

    def get(self, key):
        if key in self.store:
            return self.store[key]
        else:
            return None

    def delete(self, key):
        if key in self.store:
            del self.store[key]

# Example usage:
kv_store = KeyValueStore()
kv_store.set("example-key", "example-value")
print(kv_store.get("example-key"))  # Output: example-value
kv_store.delete("example-key")
print(kv_store.get("example-key"))  # Output: None