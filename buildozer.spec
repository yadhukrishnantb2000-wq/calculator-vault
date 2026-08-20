[app]

# (str) Title of your application
title = Calculator Vault

# (str) Package name
package.name = calculatorvault

# (str) Package domain (needed for android packaging)
package.domain = org.yadhukrishnan

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,dat

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# WARNING: 'cryptography' requires 'openssl' or it will fail to compile on Android!
requirements = python3, kivy, cryptography, openssl

# (str) Supported orientations (valid options are: landscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk options
# This can be useful to avoid any auto-updates breaking a working build.
android.skip_update = False

# (bool) Copy library instead of making a symbolic link
android.copy_libs = 1

# (str) The Android architectural target (arm64-v8a is the modern standard)
android.archs = arm64-v8a

# (list) The Android themes to apply
android.theme = @android:style/Theme.NoTitleBar.Fullscreen

# =============================================================================
# Buildozer basic configuration
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
