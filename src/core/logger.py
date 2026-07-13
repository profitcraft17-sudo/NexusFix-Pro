import os
import sys
import time
import logging

class NexusLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self._ensure_log_directory()
        
        # Central logging setup initialize karte hain
        self.logger = logging.getLogger("NexusFixProCore")
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers in multiple sub-module calls
        if not self.logger.handlers:
            self._setup_handlers()
            
        # UI components binding metadata storage matrix
        self.ui_callback = None

    def _ensure_log_directory(self):
        """Log storage workspace directories ko framework architecture ke safety bounds mein check karti hai"""
        try:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
        except Exception:
            # Android sandboxed standard internal app structures compatibility mode fallback
            # FIXED: Android private internal data path fallback setup to prevent permission crashes
            if 'ANDROID_ARGUMENT' in os.environ:
                from android.storage import app_storage_path
                self.log_dir = os.path.join(app_storage_path(), "logs")
            else:
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                self.log_dir = os.path.join(base_dir, "logs")
                
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

    def _setup_handlers(self):
        """Terminal streams, local files aur thread queues ke liye logger endpoints initialize karti hai"""
        # Formatter config logic matching global console system
        log_format = logging.Formatter('[NexusFix Pro] %(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # 1. Console stream endpoint handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)
        
        # 2. Local permanent storage file archiver handler
        log_filename = f"nexusfix_session_{int(time.time())}.log"
        file_path = os.path.join(self.log_dir, log_filename)
        
        try:
            file_handler = logging.FileHandler(file_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(log_format)
            self.logger.addHandler(file_handler)
            self.logger.info(f"Diagnostics session trace node attached: {file_path}")
        except Exception as e:
            self.logger.warning(f"Storage path locked. File logging operating inside memory buffer array only -> {str(e)}")

    def register_ui_callback(self, callback_function):
        """Future UI layer/frontend streams ko active logs pass-through karne ka handler hook registration"""
        if callable(callback_function):
            self.ui_callback = callback_function
            self.logger.info("Frontend observer interface handshake initialized successfully.")

    def log_info(self, message):
        self.logger.info(message)
        self._dispatch_to_ui("INFO", message)

    def log_warning(self, message):
        self.logger.warning(message)
        self._dispatch_to_ui("WARNING", message)

    def log_error(self, message):
        self.logger.error(message)
        self._dispatch_to_ui("ERROR", message)

    def log_debug(self, message):
        self.logger.debug(message)
        self._dispatch_to_ui("DEBUG", message)

    def print_progress_bar(self, current, total, prefix='Flashing Operation', suffix='Complete', length=30):
        """Flashing data payload transfer blocks ke liye precision terminal standard progress calculation output"""
        percent = ("{0:.1f}").format(100 * (current / float(total)))
        filled_length = int(length * current // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        
        sys.stdout.write(f'\r[NexusFix Pro] {prefix} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
        
        # Agar interface synchronized hook runtime engine active ho
        if self.ui_callback:
            try:
                # FIXED: Thread dispatcher safety check to protect Kivy terminal loops
                self.ui_callback("PROGRESS", {"percent": float(percent), "task": prefix})
            except Exception:
                pass
                
        if current == total:
            sys.stdout.write('\n')

    def _dispatch_to_ui(self, level, message):
        """Background pipelines se updates frontend data loops par safely route karti hai"""
        if self.ui_callback:
            try:
                self.ui_callback("LOG", {"level": level, "message": message, "timestamp": time.time()})
            except Exception:
                # Shield UI thread crash triggers if background context interrupts runtime pipe
                pass

# Global execution instance pool access handle mapping
nexus_logger = NexusLogger()

if __name__ == "__main__":
    # Local unit testing execution block verification logic check ke liye
    nexus_logger.log_info("Executing pipeline subsystem checks.")
    nexus_logger.log_warning("Verifying device handshake timeout offset buffers.")
    
    # Simulating data execution steps validation block
    total_blocks = 100
    for i in range(0, total_blocks + 1, 20):
        time.sleep(0.1)
        nexus_logger.print_progress_bar(i, total_blocks, prefix='Partition Writing [system.img]', length=25)
        
    nexus_logger.log_info("Diagnostics verification complete. Clean status state resolved.")
