# -*- coding: utf-8 -*-
"""Фоновый сервис: раз в 15 минут проверяет дедлайны и присылает
уведомление за один день до дедлайна задания."""

import os
import sqlite3
import time
from datetime import datetime, timedelta

CHECK_INTERVAL = 900  # 15 минут


def get_db_path():
    try:
        from jnius import autoclass
        ctx = autoclass('org.kivy.android.PythonActivity').mActivity
        return os.path.join(ctx.getFilesDir().getAbsolutePath(), 'app', 'hw.db')
    except Exception:
        pass
    try:
        from jnius import autoclass
        ctx = autoclass('org.kivy.android.PythonService').mService
        return os.path.join(ctx.getFilesDir().getAbsolutePath(), 'app', 'hw.db')
    except Exception:
        pass
    return os.path.expanduser('~/hw.db')


def notify_android(title, message):
    from jnius import autoclass
    ctx = autoclass('org.kivy.android.PythonService').mService
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    Builder = autoclass('android.app.Notification$Builder')

    mgr = ctx.getSystemService(NotificationManager.NOTIFICATION_SERVICE)
    channel_id = 'hw_deadlines'
    try:
        channel = NotificationChannel(channel_id, 'Дедлайны',
                                      NotificationManager.IMPORTANCE_DEFAULT)
        mgr.createNotificationChannel(channel)
    except Exception:
        pass

    builder = Builder(ctx, channel_id)
    builder.setContentTitle(title)
    builder.setContentText(message)
    builder.setSmallIcon(ctx.getApplicationInfo().icon)
    try:
        mgr.notify(int(time.time()) % 1000000, builder.build())
    except Exception:
        builder.setSmallIcon(android_api_icon())
        mgr.notify(1, builder.build())


def android_api_icon():
    return 17301519  # базовая иконка android


def try_plyer_notify(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10, app_name='Домашка')
        return True
    except Exception:
        return False


def check_deadlines():
    db = get_db_path()
    if not os.path.exists(db):
        return
    conn = sqlite3.connect(db)
    now = datetime.now()
    rows = conn.execute(
        'SELECT id, title, subject, deadline, notified FROM tasks '
        'WHERE notified = 0').fetchall()
    for rid, title, subject, dl_iso, _ in rows:
        try:
            dl = datetime.fromisoformat(dl_iso)
        except ValueError:
            continue
        if now < dl - timedelta(days=1) or dl < now:
            continue
        subj = (' по ' + subject) if subject else ''
        message = ('Завтра дедлайн%s: %s'
                   % (subj, title) if left_hours(dl, now) > 12
                   else 'Скоро дедлайн%s (%s): %s' % (subj, dl.strftime('%H:%M'), title))
        if try_plyer_notify('Дедлайн по домашке!', message):
            pass
        else:
            try:
                notify_android('Дедлайн по домашке!', message)
            except Exception:
                pass
        conn.execute('UPDATE tasks SET notified = 1 WHERE id = ?', (rid,))
        conn.commit()
    conn.close()


def left_hours(dl, now):
    return (dl - now).total_seconds() / 3600.0


if __name__ == '__main__':
    while True:
        try:
            check_deadlines()
        except Exception:
            pass
        time.sleep(CHECK_INTERVAL)
