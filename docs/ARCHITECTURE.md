# Архитектура

E2E UI-тесты внешней LMS: Python 3.11, pytest, синхронный Playwright, Pydantic Settings, Allure и `ui-coverage-tool`.

```text
tests -> pages -> components -> elements -> Playwright data-testid
```

| Каталог | Назначение |
|---|---|
| `tests/` | Сценарии: авторизация, регистрация, дашборд, курсы. |
| `pages/` | Page Object и навигация. |
| `components/` | Повторно используемые регионы и рабочие потоки. |
| `elements/` | Локаторы, проверки, Allure, логирование, UI coverage. |
| `fixtures/` | Браузер, авторизованное состояние, Page Object, Allure environment. |
| `tools/` | Маршруты, создание страниц, моки, метаданные отчёта. |
| `scripts/` | Отладочные примеры, не часть pytest-набора. |

## Конфигурация

`config.py` загружает `.env` через Pydantic. Ключи: `APP_URL`, `HEADLESS`, `BROWSERS`, `TEST_USER.*`, `TEST_DATA.IMAGE_PNG_FILE`, `UI_COVERAGE_*`. Разрешённые браузеры: `chromium`, `firefox`, `webkit`.

При импорте создаются `videos/`, `tracing/`, `allure-results/` и корневой `browser-state.json`.

## Выполнение

`page` создаёт независимый браузерный контекст для каждого браузера из `BROWSERS`, включает trace и запись WebM. После теста trace и видео прикладываются к Allure.

`page_with_state` использует состояние, которое один раз за сессию создаётся регистрацией `TEST_USER` в Chromium. Маршруты описаны в `tools/routes.py`; переходы выполняются через `BasePage.visit()`.

Статические `ico`, изображения, медиа и шрифты отменяются роутом Playwright. Тесты не подтверждают успешную загрузку этих ресурсов.

## CI

GitHub Actions запускает `pytest -m regression --numprocesses 2`, формирует UI coverage и загружает HTML-отчёт с Allure results. Allure report публикуется в `gh-pages`.
