import threading

# ========== BASIC SINGLETON ==========
class DatabaseConnectionPool:
    _instance = None        # holds the single instance
    _lock = threading.Lock() # thread safety

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:                    # acquire lock
                if cls._instance is None:      # double-checked locking
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:      # prevent re-initialization
            return
        self.pool = []
        self.max_connections = 10
        self.active_connections = 0
        self._initialized = True
        print("Connection pool created")

    def get_connection(self):
        if self.active_connections < self.max_connections:
            self.active_connections += 1
            print(f"Connection granted. Active: {self.active_connections}")
            return f"connection_{self.active_connections}"
        raise Exception("Connection pool exhausted")

    def release_connection(self):
        if self.active_connections > 0:
            self.active_connections -= 1
            print(f"Connection released. Active: {self.active_connections}")

    def get_status(self):
        return f"Active: {self.active_connections}/{self.max_connections}"


# ========== USAGE ==========
pool1 = DatabaseConnectionPool()
pool2 = DatabaseConnectionPool()

print(pool1 is pool2)   # True — exact same object

conn1 = pool1.get_connection()
conn2 = pool2.get_connection()   # pool2 IS pool1 — same counter

print(pool1.get_status())   # Active: 2/10
print(pool2.get_status())   # Active: 2/10 — identical, same object

pool1.release_connection()
print(pool2.get_status())   # Active: 1/10 — reflected in pool2 too