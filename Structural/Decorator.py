# Decorator pattern lets you attach new behaviors to objects by placing these objects inside special 
# wrapper objects that contain behaviors. It is a "wrapper". Uses aggregation/composition like many design patterns.
# Used to add behaviour to an object dynamically without changing its class or creating subclasses.

from abc import ABC, abstractmethod

# ========= BASE INTERFACE ==========
class DataService(ABC):
    @abstractmethod
    def fetch(self, query: str) -> str:
        pass

# ============ CONCRETE COMPONENT =============
class DatabaseService(DataService):
    def fetch(self, query: str) -> str:
        print(f"[DB] Fetching: {query}")
        return f"data for '{query}"

# ============ BASE DECORATOR =============
class DataServiceDecorator(DataService):
    def __init__(self, service: DataService):
        self._service = service     # wraps any DataService
    
    def fetch(self, query: str) -> str:
        return self._service.fetch(query)    # delegates by default

# ========= CONCRETE DECORATORS ==========
class LoggingDecorator(DataServiceDecorator):
    def fetch(self, query: str) -> str:
        print(f"[LOG] Request started: {query}")
        result = self._service.fetch(query)
        print(f"[LOG] Request completed")
        return result

class CachingDecorator(DataServiceDecorator):
    def __init__(self, service: DataService):
        super().__init__(service)
        self._cache = {}
    
    def fetch(self, query: str) -> str:
        if query in self._cache:
            print(f"[CACHE] Hit for: {query}")
            return self._cache[query]
        
        print(f"[CACHE] Miss for: {query}")
        result = self._service.fetch(query)
        self._cache[query] = result
        return result

class AuthDecorator(DataServiceDecorator):
    def __init__(self, service: DataService, token: str):
        super().__init__(service)
        self.token = token
    
    def fetch(self, query: str) -> str:
        if self.token != "valid-token":
            print("[AUTH] Unauthorized")
            return None
        print("[AUTH] Authorized")
        return self._service.fetch(query)

# ========== USAGE ===========
# start with base service
service = DatabaseService()

# wrap with decorators - order matters, outermost runs first
service = AuthDecorator(service, token="valid-token")
service = CachingDecorator(service)
service = LoggingDecorator(service)

print("--- First call ---")
result = service.fetch("SELECT * FROM users")

print("\n--- Second call (same query) ---")
result = service.fetch("SELECT * FROM users")

# Each decorator wraps the one inside it. When fetch() is called, it ripples inward - logging first,
# then cache check, then auth, then finally the real DB call.
# The key benefit is mix and match at runtime 
# - need just caching? service = CachingDecorator(DatabaseService())
# need logging + auth but no cache?
# service = LoggingDecorator(AuthDecorator(DatabaseService(), "token")) 