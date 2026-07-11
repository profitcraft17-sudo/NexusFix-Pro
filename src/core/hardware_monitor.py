import os
import json
import time
import logging

# Fallback mechanism agar pyusb local compilation parameters par setup na ho
try:
    import usb.core
    import usb.util
    USB_SUPPORTED = True
) except ImportError:
    USB_SUPPORTED = False

# Logger setup operations logs display ke liye
logging.basicConfig(level=logging.INFO, format='[NexusFix Pro] %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HardwareMonitor")

class NexusHardwareMonitor:
    def __init__(self, database_path=None):
        # Explicit baseline path alignment logic
        if database_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.database_path = os.path.join(base_dir, "config", "global_signatures.json")
        else:
            self.database_path = database_path
            
        self.signatures = self.load_database()
            
    def load_database(self):
        """Central global signatures library JSON file ko safely load karti hai"""
        if not os.path.exists(self.database_path):
            logger.error(f"Critical Error: Database file absent at {self.database_path}")
            return None
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Database parsing validation failed: {str(e)}")
            return None

    def format_id(self, value):
        """USB dynamic integer values ko matching 4-character hex strings mein format karti hai"""
        return f"{value:04x}".lower()

    def identify_device(self, vid, pid):
        """Connected signatures ko database matrix block se map karti hai"""
        if not self.signatures:
            logger.error("Signature database context is empty. Aborting routing evaluation.")
            return None
                    
        # Stage 1: Explicit Devices List match logic
        for device in self.signatures.get("devices", []):
            hw = device.get("hardware_identifiers", {})
            if hw.get("vid") == vid and hw.get("pid") == pid:
                logger.info(f"Target Identity Resolved: {device['brand']} {device['model']} ({device['chipset']})")
                return {
                    "status": "EXPLICIT_MATCH",
                    "brand": device["brand"],
                    "model": device["model"],
                    "driver_node": device["driver_node"],
                    "memory_mapping": device.get("memory_mapping", {})
                }
                        
        # Stage 2: Pattern Fallback identification logic matrix
        for rule in self.signatures.get("fallback_rules", []):
            condition = rule.get("condition", "")
            if condition.startswith("vid_startswith_"):
                target_prefix = condition.split("vid_startswith_")[1]
                if vid == target_prefix:
                    logger.warning(f"Fallback Core Interface Hit: Generic {rule['brand']} Protocol Active")
                    return {
                        "status": "FALLBACK_ROUTED",
                        "brand": rule["brand"],
                        "model": "Generic Variant",
                        "fallback_node": rule.get("fallback"),
                        "security_profile": rule.get("security")
                    }
                            
        return None

    def start_monitoring_loop(self, interval_seconds=2):
        """Active connection nodes ko real-time standard ports par scan karti hai"""
        logger.info("NexusFix Pro Hardware USB Scanning Bus System Operational...")
        
        if not USB_SUPPORTED:
            logger.error("Core USB drivers missing or platform environment restrictions active.")
            return

        processed_devices = set()

        while True:
            try:
                # Connected subsystem backend validation node scan
                devices = usb.core.find(find_all=True)
                current_active_ports = set()

                if devices:
                    for dev in devices:
                        try:
                            vid_str = self.format_id(dev.idVendor)
                            pid_str = self.format_id(dev.idProduct)
                            port_key = f"{vid_str}:{pid_str}"
                            current_active_ports.add(port_key)

                            if port_key not in processed_devices:
                                logger.info(f"Port Node Intercepted -> USB VID: {vid_str} | PID: {pid_str}")
                                result = self.identify_device(vid_str, pid_str)
                                
                                if result:
                                    logger.info("Routing Pipeline State initialized for execution stream node.")
                                    # Task delegation point: Next file layer link target location
                                processed_devices.add(port_key)
                        except Exception as dev_err:
                            # Individual node connection stream validation bypass protection
                            continue

                # Disconnected nodes memory cleaner stack cleanup logic
                processed_devices = processed_devices.intersection(current_active_ports)
                            
            except Exception as e:
                logger.error(f"Hardware controller stack scan interrupted: {str(e)}")
                            
            time.sleep(interval_seconds)

if __name__ == "__main__":
    monitor = NexusHardwareMonitor()
    monitor.start_monitoring_loop()
