Structural design patterns explain how to assemble objects and classes into larger structures, while keeping
these structures flexible and efficient.

Adapter
Intent: translate an incompatible interface into one your code expects — make two things work together without modifying either
When to use: integrating third party libraries, legacy code, or external APIs that have different method names/signatures than your system expects

Decorator
Intent: wrap an object to add behavior dynamically without changing its class
When to use: optional stackable features that can be combined in any order — logging, caching, auth, compression. When subclassing would create too many combinations

Facade
Intent: provide one simple interface to a complex subsystem of many classes
When to use: multiple classes need to be coordinated together for a common operation — hide that coordination behind one clean method so callers don't need to know the internals

Incompatible interface needs to fit your system?         → Adapter
Want to add optional behavior on top of existing?        → Decorator
Many classes working together behind one simple call?    → Facade