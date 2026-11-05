# -*- coding: utf-8 -*-
"""Домашка — учёт домашних заданий, дедлайнов и напоминаний за день."""

import os
import sqlite3
from datetime import datetime, timedelta

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform


def get_db_path():
    if platform == 'android':
        try:
            from jnius import autoclass
            ctx = autoclass('org.kivy.android.PythonActivity').mActivity
            return os.path.join(ctx.getFilesDir().getAbsolutePath(), 'app', 'hw.db')
        except Exception:
            pass
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hw.db')


KV = '''
ScreenManager:
    TaskListScreen:
        id: list
    TaskFormScreen:
        id: form

<TaskRow@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(92)
    padding: dp(8)
    spacing: dp(2)
    canvas.before:
        Color:
            rgba: 0.97, 0.97, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]
    BoxLayout:
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(1)
            Label:
                id: title_lbl
                font_size: '16sp'
                bold: True
                color: 0.1, 0.1, 0.15, 1
                halign: 'left'
                text_size: self.width, None
            Label:
                id: subject_lbl
                font_size: '13sp'
                color: 0.3, 0.35, 0.6, 1
                halign: 'left'
                text_size: self.width, None
        BoxLayout:
            size_hint_x: None
            width: dp(100)
            orientation: 'vertical'
            Button:
                id: edit_btn
                text: 'Изменить'
                font_size: '12sp'
                background_color: 0.3, 0.5, 0.85, 1
                size_hint_y: None
                height: dp(32)
            Button:
                id: del_btn
                text: 'Удалить'
                font_size: '12sp'
                background_color: 0.85, 0.3, 0.3, 1
                size_hint_y: None
                height: dp(32)
    BoxLayout:
        size_hint_y: None
        height: dp(18)
        Label:
            id: deadline_lbl
            font_size: '13sp'
            color: 0.25, 0.25, 0.25, 1
            halign: 'left'
            text_size: self.size
        Label:
            id: status_lbl
            font_size: '13sp'
            bold: True
            halign: 'right'
            text_size: self.size

<TaskListScreen>:
    name: 'list'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: dp(12), dp(6)
            Label:
                text: 'Домашка'
                font_size: '21sp'
                bold: True
                color: 0.15, 0.15, 0.2, 1
                halign: 'left'
                valign: 'middle'
                text_size: self.size
            Label:
                id: count_lbl
                font_size: '13sp'
                color: 0.45, 0.45, 0.5, 1
                halign: 'right'
                valign: 'middle'
                text_size: self.size
                size_hint_x: None
                width: dp(110)
        Widget:
            size_hint_y: None
            height: dp(1)
            canvas:
                Color:
                    rgba: 0.85, 0.85, 0.9, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        ScrollView:
            GridLayout:
                id: task_box
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: dp(8)
                spacing: dp(8)
        Label:
            id: empty_lbl
            text: 'Заданий нет\\nНажмите "+ Добавить"'
            font_size: '16sp'
            color: 0.55, 0.55, 0.6, 1
        BoxLayout:
            size_hint_y: None
            height: dp(56)
            padding: dp(10), dp(8)
            Button:
                text: '+ Добавить'
                font_size: '18sp'
                bold: True
                background_color: 0.2, 0.6, 0.9, 1
                on_release: app.open_form()

<TaskFormScreen>:
    name: 'form'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(14)
        spacing: dp(8)
        Label:
            id: form_title
            text: 'Новое задание'
            font_size: '20sp'
            bold: True
            color: 0.15, 0.15, 0.2, 1
            size_hint_y: None
            height: dp(36)
            halign: 'left'
            text_size: self.size
        Label:
            text: 'Название задания:'
            size_hint_y: None
            height: dp(20)
            color: 0.3, 0.3, 0.35, 1
            halign: 'left'
            text_size: self.size
        TextInput:
            id: title_input
            multiline: False
            hint_text: 'Например: решить задачи 15-20'
            font_size: '15sp'
            size_hint_y: None
            height: dp(44)
        Label:
            text: 'Предмет / занятие:'
            size_hint_y: None
            height: dp(20)
            color: 0.3, 0.3, 0.35, 1
            halign: 'left'
            text_size: self.size
        TextInput:
            id: subject_input
            multiline: False
            hint_text: 'Например: математика'
            font_size: '15sp'
            size_hint_y: None
            height: dp(44)
        Label:
            text: 'Дедлайн (дата и время):'
            size_hint_y: None
            height: dp(20)
            color: 0.3, 0.3, 0.35, 1
            halign: 'left'
            text_size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(8)
            TextInput:
                id: date_input
                multiline: False
                hint_text: 'ДД.ММ.ГГГГ'
                font_size: '15sp'
            TextInput:
                id: time_input
                multiline: False
                hint_text: 'ЧЧ:ММ'
                font_size: '15sp'
        Label:
            text: 'Заметка (необязательно):'
            size_hint_y: None
            height: dp(20)
            color: 0.3, 0.3, 0.35, 1
            halign: 'left'
            text_size: self.size
        TextInput:
            id: note_input
            multiline: True
            hint_text: 'Например: сдать учителю'
            font_size: '15sp'
            size_hint_y: None
            height: dp(64)
        Label:
            text: 'Напоминание придёт за 1 день до дедлайна.'
            font_size: '12sp'
            color: 0.45, 0.45, 0.5, 1
            size_hint_y: None
            height: dp(16)
        Widget:
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            Button:
                text: 'Отмена'
                font_size: '15sp'
                background_color: 0.65, 0.65, 0.7, 1
                on_release: app.back_to_list()
            Button:
                text: 'Сохранить'
                font_size: '15sp'
                bold: True
                background_color: 0.2, 0.65, 0.35, 1
                on_release: app.save_form()
'''


class TaskListScreen(Screen):
    pass


class TaskFormScreen(Screen):
    pass


class MainApp(App):

    tasks = ListProperty([])
    title = 'Домашка'

    def build(self):
        self.current_id = None
        root = Builder.load_string(KV)
        self.load_tasks()
        return root

    def on_start(self):
        self.refresh_list()
        if platform == 'android':
            try:
                self.start_service()
            except Exception as e:
                print('cannot start service: %s' % e)

    def on_resume(self):
        self.refresh_list()

    def start_service(self):
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ServiceHw = autoclass('org.test.homework.ServiceHw')
        ServiceHw.start(PythonActivity.mActivity, '')

    def load_tasks(self):
        conn = sqlite3.connect(get_db_path())
        conn.execute(
            'CREATE TABLE IF NOT EXISTS tasks ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'title TEXT, subject TEXT, deadline TEXT, note TEXT, '
            'notified INTEGER DEFAULT 0)')
        conn.commit()
        self.tasks = conn.execute(
            'SELECT id, title, subject, deadline, note, notified FROM tasks '
            'ORDER BY deadline').fetchall()
        conn.close()

    def refresh_list(self):
        self.load_tasks()
        screen = self.root.ids['list']
        task_box = screen.ids['task_box']
        while len(task_box.children) > 0:
            task_box.remove_widget(task_box.children[0])
        for task in self.tasks:
            self.add_task_row(screen, task)
        empty = screen.ids['empty_lbl']
        empty.opacity = 0 if self.tasks else 1
        count = screen.ids['count_lbl']
        now = datetime.now()
        soon = sum(1 for t in self.tasks
                   if datetime.fromisoformat(t[3]) >= now - timedelta(hours=2)
                   and datetime.fromisoformat(t[3]) <= now + timedelta(days=1))
        count.text = '%d шт., скоро %d' % (len(self.tasks), soon) if self.tasks else ''
        count.opacity = 1 if self.tasks else 0

    def add_task_row(self, screen, task):
        from kivy.factory import Factory
        app_inst = self
        rid, title, subject, dl_iso, note, notified = task
        now = datetime.now()
        try:
            dl = datetime.fromisoformat(dl_iso)
        except ValueError:
            dl = now
        left = dl - now
        if left < timedelta(0):
            status = 'ПРОСРОЧЕНО'
            color = (0.85, 0.2, 0.2, 1)
        elif left < timedelta(hours=1):
            status = 'Осталось %d мин!' % max(1, left.seconds // 60)
            color = (0.9, 0.4, 0.05, 1)
        elif left < timedelta(days=1):
            status = 'Осталось %d ч!' % (left.seconds // 3600 + 1)
            color = (0.95, 0.55, 0.05, 1)
        elif left < timedelta(days=2):
            status = 'Дедлайн завтра'
            color = (0.9, 0.7, 0.05, 1)
        else:
            status = 'Осталось %d дн.' % (left.days + 1)
            color = (0.2, 0.6, 0.2, 1)
        row = Factory.TaskRow()
        row.ids['title_lbl'].text = title
        row.ids['subject_lbl'].text = subject
        row.ids['deadline_lbl'].text = dl.strftime('%d.%m.%Y %H:%M')
        row.ids['status_lbl'].text = status + ('  •  напомню' if notified else '')
        row.ids['status_lbl'].color = color
        row.ids['edit_btn'].bind(
            on_release=lambda *a: app_inst.open_form(rid))
        row.ids['del_btn'].bind(
            on_release=lambda *a: app_inst.delete_task(rid))
        screen.ids['task_box'].add_widget(row)

    def open_form(self, task_id=None):
        self.current_id = task_id
        form = self.root.ids['form']
        if task_id is None:
            form.ids['form_title'].text = 'Новое задание'
            form.ids['title_input'].text = ''
            form.ids['subject_input'].text = ''
            form.ids['date_input'].text = ''
            form.ids['time_input'].text = '23:59'
            form.ids['note_input'].text = ''
        else:
            task = [t for t in self.tasks if t[0] == task_id][0]
            dl = datetime.fromisoformat(task[3])
            form.ids['form_title'].text = 'Изменить задание'
            form.ids['title_input'].text = task[1]
            form.ids['subject_input'].text = task[2]
            form.ids['date_input'].text = dl.strftime('%d.%m.%Y')
            form.ids['time_input'].text = dl.strftime('%H:%M')
            form.ids['note_input'].text = task[4]
        self.root.current = 'form'

    def back_to_list(self):
        self.root.current = 'list'

    def save_form(self):
        form = self.root.ids['form']
        title = form.ids['title_input'].text.strip()
        subject = form.ids['subject_input'].text.strip()
        note = form.ids['note_input'].text.strip()
        try:
            dl = datetime.strptime(
                form.ids['date_input'].text.strip() + ' ' +
                form.ids['time_input'].text.strip(), '%d.%m.%Y %H:%M')
        except ValueError:
            self.show_popup('Проверьте дату (ДД.ММ.ГГГГ) и время (ЧЧ:ММ)')
            return
        if not title:
            self.show_popup('Введите название задания')
            return
        conn = sqlite3.connect(get_db_path())
        if self.current_id is None:
            conn.execute(
                'INSERT INTO tasks (title, subject, deadline, note) '
                'VALUES (?, ?, ?, ?)',
                (title, subject, dl.isoformat(), note))
        else:
            conn.execute(
                'UPDATE tasks SET title=?, subject=?, deadline=?, note=?, '
                'notified=0 WHERE id=?',
                (title, subject, dl.isoformat(), note, self.current_id))
        conn.commit()
        conn.close()
        self.current_id = None
        self.back_to_list()
        self.refresh_list()

    def delete_task(self, task_id):
        conn = sqlite3.connect(get_db_path())
        conn.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()
        conn.close()
        self.refresh_list()

    def show_popup(self, text):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        Popup(title='Внимание',
              content=Label(text=text, color=(0.2, 0.2, 0.2, 1)),
              size_hint=(0.85, 0.35)).open()


if __name__ == '__main__':
    MainApp().run()
