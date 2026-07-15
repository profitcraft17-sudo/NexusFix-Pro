import os
import sys

# Android environment check karne ke liye (Kivy standard)
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android import activity
    
    # Android Native Classes ko import karna
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    Intent = autoclass('android.content.Intent')
    PendingIntent = autoclass('android.app.PendingIntent')
    IntentFilter = autoclass('android.content.IntentFilter')
    UsbManager = autoclass('android.hardware.usb.UsbManager')
    
    # Custom BroadcastReceiver class (Bina iske Android permission dialog ka response register nahi karta)
    # Note: Android background receiver handle karne ke liye Java-level bridge zaroori hota hai.
else:
    # Desktop environment testing fail-safe
    PythonActivity = None

class USBPermissionManager:
    def __init__(self, ui_log_callback=None):
        self.log = ui_log_callback if ui_log_callback else print
        self.usb_manager = None
        self.current_context = None
        
        if platform == 'android':
            self._initialize_android_usb()

    def _initialize_android_usb(self):
        """Android native USB subsystem access initiate karna"""
        try:
            self.current_context = PythonActivity.mActivity
            self.usb_manager = self.current_context.getSystemService(Context.USB_SERVICE)
            self.log("Android USB Host Subsystem Initialized Successfully.")
        except Exception as e:
            self.log(f"USB Init Error: {str(e)}", "ERROR")

    def check_and_request_usb_permission(self, vendor_id: int, product_id: int):
        """Standard USB device access validation map routine"""
        if platform != 'android':
            self.log("Desktop Environment Detected: Skipping native Android USB permissions.", "INFO")
            return True

        if not self.usb_manager:
            self.log("USB Manager unavailable.", "ERROR")
            return False

        # Connected USB devices ki list scan karna
        device_list = self.usb_manager.getDeviceList()
        device_iterator = device_list.values().iterator()
        
        target_device = None
        while device_iterator.hasNext():
            device = device_iterator.next()
            # VID and PID verification checks match bounds
            if device.getVendorId() == vendor_id and device.getProductId() == product_id:
                target_device = device
                break

        if not target_device:
            self.log(f"Target Device (VID: {vendor_id}, PID: {product_id}) not found on OTG bus.", "WARNING")
            return False

        # Check karna ki kya permission pehle se mili hui hai
        if self.usb_manager.hasPermission(target_device):
            self.log("USB Access Permission already granted by user.", "SUCCESS")
            return True
        else:
            self.log("Requesting dynamic Android runtime USB Host access permission...", "INFO")
            
            # Intent implementation for runtime dialog triggers
            # Android OS yahan user ko ek dynamic pop-up dikhaega: "Allow app to access USB device?"
            try:
                ACTION_USB_PERMISSION = "com.nexusfix.USB_PERMISSION"
                intent = Intent(ACTION_USB_PERMISSION)
                
                # PendingIntent wrapper configuration rules
                flags = PendingIntent.FLAG_UPDATE_CURRENT
                # Android 12+/2026 guidelines ke mutabik mutable flags explicitly enforce hote hain
                if hasattr(PendingIntent, "FLAG_MUTABLE"):
                    flags |= PendingIntent.FLAG_MUTABLE
                    
                pending_intent = PendingIntent.getBroadcast(
                    self.current_context, 0, intent, flags
                )
                
                # Native Dialog Trigger
                self.usb_manager.requestPermission(target_device, pending_intent)
                return False  # Response handle automatic asynchronous standard par chalta hai
            except Exception as ex:
                self.log(f"Failed to launch native permission prompt: {str(ex)}", "ERROR")
                return False
