[app]
title = Домашка
package.name = homework
package.domain = dev.sup4ik
source.dir = .
source.include_exts = py
version = 1.1.0
requirements = python3,kivy==2.2.1,plyer,pyjnius==1.6.1
p4a.branch = v2024.01.21
p4a.python_version = 3.11
orientation = portrait
osx.python_version = 3

services = Hw:service.py:foreground

android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.permissions = POST_NOTIFICATIONS,WAKE_LOCK,VIBRATE,FOREGROUND_SERVICE,SCHEDULE_EXACT_ALARM
android.allow_backup = True
android.accept_sdk_license = True

fullscreen = 0
log_level = 2

warn_all_root = False

[buildozer]
log_level = 2
warn_on_root = 1
