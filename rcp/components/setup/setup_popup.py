import os

from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput

log = Logger.getChild(__name__)
kv_file = os.path.join(os.path.dirname(__file__), __file__.replace(".py", ".kv"))
if os.path.exists(kv_file):
    log.info(f"Loading KV file: {kv_file}")
    Builder.load_file(kv_file)


class SelectableButton(Button):
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.2, 0.2, 1)  # Dark gray when not selected
        self.bind(selected=self._on_selected)

    def _on_selected(self, instance, value):
        if value:
            self.background_color = (0.3, 0.3, 0.5, 1)  # Blue-gray when selected
        else:
            self.background_color = (0.2, 0.2, 0.2, 1)  # Dark gray when not selected


class SetupPopup(Popup):
    screen_manager = ObjectProperty(None)
    screen_selector = ObjectProperty(None)
    current_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(current_screen=self._on_screen_change)
        # Set initial selection after the popup is fully initialized
        self.bind(on_open=self._set_initial_selection)

    def _set_initial_selection(self, instance):
        # Set initial selection based on current screen
        if self.screen_manager and self.screen_manager.current:
            self._on_screen_change(None, self.screen_manager.current)

    def _on_screen_change(self, instance, value):
        # Update button states
        for child in self.screen_selector.children:
            if isinstance(child, SelectableButton):
                child.selected = (child.text.lower().replace(' ', '_') == value)

    def on_dismiss(self):
        current_app = App.get_running_app()
        # current_app.manual_full_update()
        log.info("Close setup page")


class AxisNameInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '48sp'  # Increased to 48sp for much larger text
        self.multiline = False
        self.hint_text = "Axis Name"
        self.hint_text_color = [0.5, 0.5, 0.5, 1]
        self.background_color = [0.2, 0.2, 0.2, 1]
        self.foreground_color = [1, 1, 1, 1]
        self.cursor_color = [1, 1, 1, 1]
        self.padding = [20, 20]  # Increased padding
        self.size_hint_y = None
        self.height = '72dp'  # Increased height to match larger text
        self.font_name = 'Roboto'  # Ensure we're using a clear font
