# Домашка

Android-приложение (Python + Kivy) для учёта домашних заданий:
добавляй задание, предмет, дедлайн и заметку — за 1 день до дедлайна
придёт уведомление (фоновый сервис проверяет каждые 15 минут).

## Как получить APK

### Способ 1: через GitHub Actions (рекомендуется)
1. Создай репозиторий на GitHub и залей содержимое этой папки:
   ```
   pip install gh  # не нужно, проще через сайт
   git init && git add . && git commit -m "first" 
   git remote add origin https://github.com/ВАШ_ЛОГИН/homework.git
   git push -u origin main
   ```
2. Workflow соберёт APK автоматически (вкладка Actions), 
   файл появится в Releases (тег v1.0.0).
3. Скачай APK со страницы Releases и установи на телефон.

### Способ 2: локально (Linux/PC с 10+ ГБ места и Java)
```
pip install buildozer cython
buildozer android debug
```
APK появится в папке `bin/`.

## Формат ввода
- Дата: `ДД.ММ.ГГГГ`
- Время: `ЧЧ:ММ`

## Файлы
- `main.py` — интерфейс приложения
- `service.py` — фоновый сервис напоминаний
- `buildozer.spec` — конфигурация сборки APK
- `.github/workflows/build.yml` — авто-сборка APK на GitHub Actions

## Примечания
- На Android 13+ при первом запуске разрешите уведомления (система спросит).
- Данные хранятся локально в SQLite, ничего никуда не отправляется.
