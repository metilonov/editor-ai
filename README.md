# EditAI Ultimate Free

Максимально функциональный бесплатный Telegram-бот на Python для поиска интересных моментов и создания вертикальных роликов TikTok / Shorts / Reels.

## Что реализовано

- прием видео и документов из Telegram;
- загрузка по URL через `yt-dlp`;
- очередь, отмена, история и ограничение активных задач;
- индивидуальные настройки пользователя;
- 8 монтажных профилей: Dynamic, Gaming, Anime, Meme, Cinematic, Podcast, Clean, TikTok;
- анализ смен сцен, движения, громкости, аудиопиков, лиц, резкости, яркости, насыщенности и энтропии;
- генерация кандидатов и многокритериальное ранжирование;
- разнообразие клипов и защита от пересечений;
- вертикальный рендер 9:16: размытый фон или центральный crop;
- профили эффектов: зум, контраст, насыщенность, vignette, flash, shake, fade, speed;
- необязательная музыка из локальной папки с ducking исходного звука;
- необязательные субтитры через бесплатный/собственный OpenAI-совместимый STT endpoint;
- превью, обложка, JSON-манифест и JSON-отчет анализа;
- отправка результата пользователю и необязательная публикация в Telegram-канал;
- SQLite: пользователи, настройки, задачи, результаты, метрики;
- админ-команды, health-check, очистка и статистика;
- CLI для анализа и рендера без Telegram;
- unit-тесты и FFmpeg smoke-test.

## Честные ограничения

- Без нейросети бот не понимает сюжет как человек. Он выбирает фрагменты по измеримым признакам.
- Бесплатный безлимитный API распознавания речи не гарантируется. При пустых API-настройках субтитры пропускаются.
- Официальная автопубликация в TikTok не включена: она требует отдельного одобрения TikTok API.
- Python-программа должна где-то выполняться: ПК, Termux или бесплатный Python-хостинг. Отдельный локальный AI-сервер не требуется.
- FFmpeg обязателен: чистый Python не способен надежно кодировать все популярные видеоформаты без внешнего кодека.

## Установка Linux / Zorin / Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python check_install.py
python run.py
```

## Termux

```bash
pkg update
pkg install python ffmpeg
pip install -r requirements.txt
cp .env.example .env
nano .env
python run.py
```

OpenCV в Termux зависит от устройства и версии Python. На Linux надежнее.

## Команды Telegram

- `/start` — меню;
- `/help` — инструкция;
- `/settings` — настройки;
- `/profiles` — стили;
- `/jobs` — история;
- `/cancel ID` — отменить ожидающую задачу;
- `/stats` — статистика администратора;
- `/health` — диагностика администратора;
- `/cleanup` — очистка администратора.

## CLI

```bash
python -m editai.cli.main doctor
python -m editai.cli.main analyze path/to/video.mp4 --profile gaming
python -m editai.cli.main render path/to/video.mp4 --profile dynamic --clips 3
```

## Музыка

Добавьте легально используемые MP3/WAV/M4A в `assets/music/`. В настройках пользователя включите музыку.

## Субтитры

Укажите совместимый endpoint:

```env
TRANSCRIPTION_API_URL=https://example/v1/audio/transcriptions
TRANSCRIPTION_API_KEY=...
TRANSCRIPTION_MODEL=whisper-large-v3
```

Без endpoint бот продолжает работать без автоматических субтитров.
