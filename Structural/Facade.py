# Facade provides a simplified interface to a complex subsystem. It hides all the moving parts beyond one point.
# ========== COMPLEX SUBSYSTEM CLASSES ==========
# each does one specific thing - callers shouldn't need to know all of these
class Projector:
    def on(self):
        print("[PROJECTOR] turning on")
    
    def off(self):
        print("[PROJECTOR] turning off")
    
    def set_input(self, source: str):
        print(f"[PROJECTOR] Input set to {source}")
    
class SoundSystem:
    def on(self):
        print("[SOUND] Amplifier on")
    
    def off(self):
        print("[SOUND] Amplifier off")
    
    def set_volume(self, level: int):
        print(f"[SOUND] Volume set to {level}")
    
    def set_surround_mode(self, mode: str):
        print(f"[SOUND] Surround mode: {mode}")

class StreamingPlayer:
    def on(self):
        print("[PLAYER] Streaming player on")

    def off(self):
        print("[PLAYER] Streaming player off")

    def play(self, movie: str):
        print(f"[PLAYER] Playing '{movie}'")

    def stop(self):
        print("[PLAYER] Stopped")


class Lights:
    def dim(self, level: int):
        print(f"[LIGHTS] Dimmed to {level}%")

    def on(self):
        print("[LIGHTS] Full brightness")


class AirConditioner:
    def set_temperature(self, temp: int):
        print(f"[AC] Temperature set to {temp}°C")

# ============ FACADE ============
# caller only talks to this - never to subsystem classes directly
class HomeTheatreFacade:
    def __init__(self):
        self.projector  = Projector()
        self.sound      = SoundSystem()
        self.player     = StreamingPlayer()
        self.lights     = Lights()
        self.ac         = AirConditioner()
    
    def watch_movie(self, movie: str):
        print("--- Setting up movie night ---")
        self.lights.dim(10)
        self.ac.set_temperature(22)
        self.projector.on()
        self.projector.set_input("HDMI")
        self.sound.on()
        self.sound.set_volume(30)
        self.sound.set_surround_mode("Dolby Atmos")
        self.player.on()
        self.player.play(movie)
        print("--- Enjoy the movie! ---\n")

    def end_movie(self):
        print("--- Shutting down ---")
        self.player.stop()
        self.player.off()
        self.sound.off()
        self.projector.off()
        self.lights.on()
        print("--- Goodbye! ---")

# ========= USAGE ==========
# caller does ONE thing - never touches subsytem directly
theater = HomeTheatreFacade()
theater.watch_movie("Inception")
theater.end_movie()

# Every Facade is an abstraction but not every abstraction is a Facade. It is just one specific tool
# in the abstraction toolbox used specifically when multiple subsystem classes need to be
# coordinated behind a single entry point.
