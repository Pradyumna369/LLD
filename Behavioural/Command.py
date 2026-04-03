# It is used to wrap a request as an object so that it can be queued, logged or undo it.
# Decouples the sender of the request from executor.

from abc import ABC, abstractmethod

# ========== COMMAND INTERFACE =========
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# ========== RECEIVER ===========
# object that actually does the work
class TextEditor:
    def __init__(self):
        self.content = ""
    
    def insert(self, text: str):
        self.content += text
        print(f"Content: '{self.content}")
    
    def delete(self, length: int):
        self.content = self.content[:-length]
        print(f"Content: '{self.content}")

# =========== CONCRETE COMMANDS ============
class InsertCommand(Command):
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.insert(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, length: int):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.content[-self.length:]
        self.editor.delete(self.length)
    
    def undo(self):
        self.editor.insert(self.deleted_text)

# =========== INVOKER ============
# manages command history - doesn't know what commands do
class CommandManager:
    def __init__(self):
        self._history = []      # composition - owns command history
    
    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
    
    def undo(self):
        if not self._history:
            print("Nothing to undo")
            return
        command = self._history.pop()
        command.undo()

# ========== USAGE ===========
editor = TextEditor()       # receiver
manager = CommandManager()  # invoker

manager.execute(InsertCommand(editor, "Hello"))
manager.execute(InsertCommand(editor, " World"))
manager.execute(DeleteCommand(editor, 5))

print("\n---- Undo ----")
manager.undo()

print("\n--- Undo again ---")
manager.undo()

# Without Command pattern, the undo logic is orphaned - it doens't belong anywhere naturally, so it ends up
# polluting the class that's most convenient, which is always the wrong place.
# Command pattern gives it a home - each operation owns its own reversal. TextEditor stays clean.