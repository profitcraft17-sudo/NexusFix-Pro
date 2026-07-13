[app]

# (string) Title of your application
title = NexusFix-Pro

# (string) Package name
package.name = nexusfix_pro

# (string) Package domain (needed for android packaging)
package.domain = com.nexusfix.pro

# (string) Source code directory where main.py resides
source.dir = .

# (list) Source files to include (comma separated)
source.include_exts = py,png,jpg,kv,atlas,json,wav

# (list) List of inclusions filters for assets paths
source.include_patterns = assets/*, config/*, src/*

# (string) Application versioning
version = 5.0.0

# (list) Application requirements
# FIXED: Dynamic packages alignment for Kivy 2.3.0 and pyjnius core android layer
requirements = python3,kivy==2.3.0,pyjnius>=1.6.0,pyusb>=1.2.1

# (str) Custom source folders separation logic rules
source.include_dirs = src, assets, config

# (list) Supported orientations (landscape, portrait or all)
orientation = portrait

# ==========================================================
# CRITICAL ANDROID SPECIFIC SECURITY PERMISSIONS & FEATURES
# ==========================================================

# (list) Android permissions to request directly from user
# FIXED: Added strict low-level system USB Host tracking permissions handles
android.permissions = android.permission.USB_PERMISSION, android.permission.FOREGROUND_SERVICE, INTERNET

# (list) Features required by the app to filter compatible devices in Play Store / Package manager
# FIXED: Forces Android OS to recognize this app as an active hardware OTG flashing host controller
android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
# FIXED: Set to API 34 (Android 14) to maintain strict compatibility with modern safety tokens flags
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 26

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version preferred by Kivy/PyJnius toolchain stability maps
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk layout configurations
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements loops
android.accept_sdk_license = True

# (str) The Android architectural targets to compile binary packages files for (.so libs)
# FIXED: Compiling for both arm64-v8a (Modern phones) and armeabi-v7a (Older target devices)
android.archs = arm64-v8a, armeabi-v7a

# (list) The whitelist configuration patterns to ensure assets aren't stripped by compiler optimizer
android.asset_filters = *.wav, *.json, *.mbn

# ==========================================================
# ADVANCED PYJNIUS / SYSTEM STRIP COMPLIANCE DEFINITIONS
# ==========================================================

# (list) Java classes to build inside python-for-android distribution layers frameworks
# It handles implicit boot parameters mappings smoothly
android.add_src_dirs = 

# (bool) Indicate if the application should be launchable as a system service matrix
android.meta_data = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and big outputs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
