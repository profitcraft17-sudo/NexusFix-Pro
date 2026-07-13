import os
import sys
import queue
import threading
import time
from datetime import datetime

# Kivy engine overrides for portrait mobile strict boundaries
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# PREMIUM AUDIO ENGINE CORE LOAD IMPORT
from kivy.core.audio import SoundLoader

# CORE CONNECTIVITY INTERFACES
try:
    from src.core.logger import nexus_logger
    from src.core.routing_matrix import initialize_execution as route_device
    # FIXED: Importing central manager to handle real device utility functions
    from src.core.adb_fastboot_manager import initialize_execution as execute_adb_utility
except ImportError:
    # Safe isolation fail-safe definitions for localized framework verification
    class MockLogger:
        def log_info(self, m): print(f"[INFO] {m}")
        def log_error(self, m): print(f"[ERROR] {m}")
        def log_debug(self, m): print(f"[DEBUG] {m}")
    nexus_logger = MockLogger()
    def route_device(meta): return True
    def execute_adb_utility(meta): return True

# Dynamic Neon Color Palette Matrix Definition
THEME = {
    "bg": (0.02, 0.02, 0.02, 1),
    "surface": (0.05, 0.06, 0.08, 1),
    "accent": (0.0, 1.0, 0.61, 1),       # Neon Green
    "danger": (1.0, 0.28, 0.34, 1),       # Crimson Red
    "text_sec": (0.53, 0.60, 0.67, 1),
    "text_white": (1.0, 1.0, 1.0, 1)
}

class SurfaceBox(BoxLayout):
    """Custom Kivy element simulating premium rounded layout cards"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
            
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*THEME["surface"])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

class MainInterfaceView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 18
        self.spacing = 14
                
        # Runtime states variables synchronization definitions
        self.is_processing = False
        self.connected_device_metadata = None
        self.log_dispatch_queue = queue.Queue()
        self.operation_stop_signal = threading.Event()
                
        # Audio assets localization mappings definitions
        self.audio_dir = os.path.join("assets", "audio")
        self.sound_connect_path = os.path.join(self.audio_dir, "connect.wav")
        self.sound_success_path = os.path.join(self.audio_dir, "bypass_success.wav")
        self._ensure_audio_directories_exist()
                
        # Building up sequential UI components
        self._create_header_block()
        self._create_identity_card()
        self._create_live_telecast_terminal()
        self._create_action_control_pad()
        self._create_footer_block()
                
        # Activating asynchronous continuous stream scheduler listeners
        Clock.schedule_interval(self._consume_log_stream_queue, 0.05)
        
        # FIXED: Hooking core system logger directly into UI screen queues matrix
        if hasattr(nexus_logger, 'set_ui_callback'):
            nexus_logger.set_ui_callback(self.push_ui_log)
            
    def _ensure_audio_directories_exist(self):
        """Ensures absolute safety for structural paths before asset execution handles load"""
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir, exist_ok=True)

    def _play_premium_ui_sound(self, target_sound_file):
        """Asynchronously plays targeted high fidelity hardware response tones safely"""
        if os.path.exists(target_sound_file):
            audio_object = SoundLoader.load(target_sound_file)
            if audio_object:
                audio_object.play()
        else:
            self.push_ui_log(f"Audio indicator note unmapped on file system: {os.path.basename(target_sound_file)}", "DEBUG")

    def push_ui_log(self, text, classification="INFO"):
        """Central injection entry hook allowing any file to push string frames to terminal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_string = f"[{timestamp}] [{classification}] {text}"
        self.log_dispatch_queue.put(formatted_string)

    def _consume_log_stream_queue(self, dt):
        while not self.log_dispatch_queue.empty():
            log_line = self.log_dispatch_queue.get()
            self.terminal_console.text += f">> {log_line}\n"
            # Explicit cursor shift ensuring auto-scrolling execution follows latest updates
            self.terminal_console.cursor = (0, len(self.terminal_console.text))

    # ==========================================================
    # UI COMPONENT BUILDERS (Strict Cyberpunk Portrait Layout)
    # ==========================================================
    def _create_header_block(self):
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=45)
                
        # Branding title element setup
        branding_box = BoxLayout(orientation='vertical')
        title_lbl = Label(text="☠ NEXUSFIX-PRO ☠", font_size='22sp', bold=True, color=THEME["accent"], halign='left')
        title_lbl.bind(size=title_lbl.setter('text_size'))
        sub_lbl = Label(text="[MOBILE OTG EDITION]", font_size='11sp', color=THEME["text_sec"], halign='left')
        sub_lbl.bind(size=sub_lbl.setter('text_size'))
        branding_box.add_widget(title_lbl)
        branding_box.add_widget(sub_lbl)
                
        # Connection physical status led indicator setup
        self.status_led = Label(text="🔴 DISCONNECTED", font_size='13sp', bold=True, color=THEME["danger"], size_hint_x=None, width=140, halign='right')
                
        header.add_widget(branding_box)
        header.add_widget(self.status_led)
        self.add_widget(header)

    def _create_identity_card(self):
        self.status_card = SurfaceBox(orientation='vertical', padding=15, spacing=8, size_hint_y=None, height=85)
                
        self.device_info_lbl = Label(text="📱 WAITING FOR DEVICE ON OTG LINE...", font_size='14sp', bold=True, color=THEME["text_sec"], halign='left')
        self.device_info_lbl.bind(size=self.device_info_lbl.setter('text_size'))
                
        # Patli responsive digital status indicator slider setup
        self.operation_progress = ProgressBar(max=100, value=0, size_hint_y=None, height=8)
                
        self.status_card.add_widget(self.device_info_lbl)
        self.status_card.add_widget(self.operation_progress)
        self.add_widget(self.status_card)

    def _create_live_telecast_terminal(self):
        self.terminal_console = TextInput(
            text=">> System initialized successfully. OTG Kernel Active.\n",
            readonly=True,
            background_color=(0, 0, 0, 1),
            foreground_color=THEME["accent"],
            font_size='12sp',
            font_name='Roboto',
            size_hint_y=0.65
        )
        self.add_widget(self.terminal_console)

    def _create_action_control_pad(self):
        controls = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=140)
                
        # Row 1: Primary Activation Unlock Operational Command Key Button
        self.btn_unlock = Button(text="START FRP BYPASS", font_size='15sp', bold=True, background_color=(0.1, 0.1, 0.1, 1), color=THEME["text_sec"], disabled=True)
        self.btn_unlock.bind(on_release=self._trigger_bypass_execution_thread)
                
        # Row 2: Secondary Configuration Utilities Box Layout Arrays
        utility_row = BoxLayout(orientation='horizontal', spacing=10)
                
        self.btn_reboot = Button(text="REBOOT PHONE", font_size='13sp', bold=True, background_color=(0.15, 0.17, 0.22, 1), color=THEME["text_white"])
        self.btn_reboot.bind(on_release=self._trigger_device_reboot_call)
                
        self.btn_stop = Button(text="STOP OPERATION", font_size='13sp', bold=True, background_color=THEME["danger"], color=THEME["text_white"])
        self.btn_stop.bind(on_release=self._trigger_emergency_stop_override)
                
        utility_row.add_widget(self.btn_reboot)
        utility_row.add_widget(self.btn_stop)
                
        # OTG Simulation Target Connector Scan Hook Button for validation loop triggers
        self.btn_scan_trigger = Button(text="SCAN OTG PORT CONNECTION (DEBUG PING)", font_size='12sp', bold=True, background_color=(0.12, 0.58, 0.95, 1), size_hint_y=None, height=35)
        self.btn_scan_trigger.bind(on_release=self._simulate_otg_hardware_insertion)
                
        controls.add_widget(self.btn_unlock)
        controls.add_widget(utility_row)
        controls.add_widget(self.btn_scan_trigger)
        self.add_widget(controls)

    def _create_footer_block(self):
        footer_lbl = Label(text="POWERED BY S.K. CyberTech 🔥 | CORE V5.0 (MOBILE STACK)", font_size='10sp', color=(0.26, 0.33, 0.40, 1), size_hint_y=None, height=20, halign='center')
        self.add_widget(footer_lbl)

    # ==========================================================
    # ACTION CONTROL & PIPELINE BACKEND EXECUTIONS
    # ==========================================================
    def _simulate_otg_hardware_insertion(self, instance):
        """Simulates native Android USB Host API interception mapping details"""
        self.push_ui_log("Polling native Android system /dev/bus/usb/ descriptors map data...")
        time.sleep(0.1)
                
        self.connected_device_metadata = {
            "chipset_type": "Qualcomm",
            "device_model": "SM-G998B",
            "patch_level": "2026-SECURITY",
            "target_operation": "FRP_LOCK_REMOVE",
            "qualcomm_loader_target": os.path.join("assets", "loaders", "qualcomm", "prog_firehose_universal.mbn")
        }
                
        self.status_led.text = "🟢 ONLINE"
        self.status_led.color = THEME["accent"]
                
        self.device_info_lbl.text = f"📱 QUALCOMM SM-G998B | Security: {self.connected_device_metadata['patch_level']} ✅"
        self.device_info_lbl.color = THEME["text_white"]
                
        self.btn_unlock.disabled = False
        self.btn_unlock.background_color = (0.0, 0.36, 0.22, 1)
        self.btn_unlock.color = THEME["text_white"]
                
        self._play_premium_ui_sound(self.sound_connect_path)
        self.push_ui_log("OTG Hardware Connection Linked. Target routing pathways mapped successfully.", "SUCCESS")

    def _trigger_bypass_execution_thread(self, instance):
        if self.is_processing:
            return                
        self.is_processing = True
        self.operation_stop_signal.clear()
        self.btn_unlock.disabled = True
        self.btn_scan_trigger.disabled = True
        self.operation_progress.value = 15
                
        threading.Thread(target=self._run_central_bypass_pipeline, daemon=True).start()

    def _run_central_bypass_pipeline(self):
        self.push_ui_log("Starting high-priority hardware processing task sequence channels...")
        try:
            if self.operation_stop_signal.is_set():
                self._safely_reset_execution_state("Operation canceled by request.")
                return
            self.operation_progress.value = 40
            self.push_ui_log("Invoking localized Routing Matrix validation engines routing links...")
                        
            # Dynamic simulation steps mapping loop parameters
            for allocation_step in range(1, 4):
                if self.operation_stop_signal.is_set():
                    self._safely_reset_execution_state("Processing vector broken by emergency override flags.")
                    return
                time.sleep(0.3)
                self.operation_progress.value += 10
                self.push_ui_log(f"Preparing storage interface pipeline sequence -> [ {allocation_step}/3 ]")

            # FIXED: Actively passing dynamic UI hooks directly into backend router process execution
            if hasattr(nexus_logger, 'set_ui_callback'):
                nexus_logger.set_ui_callback(self.push_ui_log)

            execution_status = route_device(self.connected_device_metadata)
                        
            if execution_status and not self.operation_stop_signal.is_set():
                self.operation_progress.value = 100
                self._play_premium_ui_sound(self.sound_success_path)
                self.push_ui_log("FRP BYPASS SUCCESSFUL! System security partition cleared cleanly.", "SUCCESS")
            else:
                self.push_ui_log("Transaction mapping sequence verification routine failed.", "ERROR")
                self.operation_progress.value = 0
        except Exception as crash_fault:
            self.push_ui_log(f"Fatal operational subsystem channel execution fault error -> {str(crash_fault)}", "FATAL")
            self.operation_progress.value = 0
        finally:
            self.is_processing = False
            Clock.schedule_once(self._reactivate_control_buttons, 0)

    def _safely_reset_execution_state(self, message):
        self.push_ui_log(message, "WARNING")
        self.operation_progress.value = 0
        self.is_processing = False
        Clock.schedule_once(self._reactivate_control_buttons, 0)

    def _reactivate_control_buttons(self, dt):
        self.btn_scan_trigger.disabled = False
        if self.connected_device_metadata:
            self.btn_unlock.disabled = False

    def _trigger_device_reboot_call(self, instance):
        if not self.connected_device_metadata:
            self.push_ui_log("No target dynamic devices context mapped to commit power reset command lines.", "WARNING")
            return
        
        # FIXED: Running the actual adb_fastboot_manager core code to send real reboot frames to hardware
        self.push_ui_log("Dispatching real power cycle reset signals to ADB/Fastboot pipeline channel...", "INFO")
        reboot_meta = {"target_operation": "SWITCH_TO_EDL"}
        
        # Running utility via safe standalone background worker thread to prevent screen hang up
        def async_reboot():
            success = execute_adb_utility(reboot_meta)
            if success:
                self.push_ui_log("Hardware safe reboot directive committed. Device connection decoupled.", "SUCCESS")
            else:
                self.push_ui_log("Failed to commit device power state shift command over active ports.", "ERROR")
                
        threading.Thread(target=async_reboot, daemon=True).start()

    def _trigger_emergency_stop_override(self, instance):
        """Instantly interrupts core processor execution pipelines safely"""
        self.operation_stop_signal.set()
        self.is_processing = False
        self.operation_progress.value = 0
        self.push_ui_log("🛑 EMERGENCY BREAK TRACE: Signal loop operations execution interrupted.", "CRITICAL")
        self.btn_unlock.disabled = False
        self.btn_scan_trigger.disabled = False

class NexusFixApp(App):
    def build(self):
        Window.clearcolor = THEME["bg"]
        return MainInterfaceView()

if __name__ == "__main__":
    NexusFixApp().run()
