# The key difference from Factory is that instead of creating one product, 
# abstract factory creates families of related products.

from abc import ABC, abstractmethod

# ====== ABSTRACT PRODUCTS ====== #
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self) -> str:
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_check(self) -> str:
        pass

class TextInput(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_type(self, text: str) -> str:
        pass

# ========== WINDOWS FAMILY ==========
class WindowsButton(Button):
    def render(self) -> str:
        return "[ Windows Button ]"

    def on_click(self) -> str:
        return "Windows button clicked — sharp corners, blue highlight"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[ Windows Checkbox ]"

    def on_check(self) -> str:
        return "Windows checkbox checked — square box, blue tick"


class WindowsTextInput(TextInput):
    def render(self) -> str:
        return "[ Windows TextInput ]"

    def on_type(self, text: str) -> str:
        return f"Windows input: '{text}' — sharp border, blue focus"


# ========== MAC FAMILY ==========
class MacButton(Button):
    def render(self) -> str:
        return "( Mac Button )"

    def on_click(self) -> str:
        return "Mac button clicked — rounded corners, grey highlight"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "( Mac Checkbox )"

    def on_check(self) -> str:
        return "Mac checkbox checked — rounded box, blue tick"


class MacTextInput(TextInput):
    def render(self) -> str:
        return "( Mac TextInput )"

    def on_type(self, text: str) -> str:
        return f"Mac input: '{text}' — rounded border, blue glow"

# ========== ABSTRACT FACTORY ==========
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

    @abstractmethod
    def create_text_input(self) -> TextInput:
        pass


# ========== CONCRETE FACTORIES ==========
class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

    def create_text_input(self) -> TextInput:
        return WindowsTextInput()


class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

    def create_text_input(self) -> TextInput:
        return MacTextInput()


# ======= CLIENT ======
# Client only talks to abstract factory and abstract products
# never knows about Windows or Mac concrete classes
class LoginForm:
    def __init__(self, factory: UIFactory):
        # entire form built from one factory — guaranteed consistent family
        self.button    = factory.create_button()
        self.checkbox  = factory.create_checkbox()
        self.input     = factory.create_text_input()

    def render(self):
        print(self.input.render())
        print(self.checkbox.render())
        print(self.button.render())

    def submit(self, username: str):
        print(self.input.on_type(username))
        print(self.checkbox.on_check())
        print(self.button.on_click())

# ========== USAGE ==========
import sys

platform = "mac"  # would come from config/env in real system

factory = MacUIFactory() if platform == "mac" else WindowsUIFactory()

form = LoginForm(factory)
form.render()
print()
form.submit("alice")