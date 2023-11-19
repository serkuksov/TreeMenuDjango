[![Build Statys](https://github.com/serkuksov/treemenudjango/actions/workflows/checks.yml/badge.svg?branch=master)](https://github.com/serkuksov/treemenudjango/actions/workflows/checks.yml)

# TreeMenuDjango

TreeMenuDjango - это Django-приложение для создания и отображения древовидных меню выполненое в рамках тестового задания.

## Особенности

- Реализация древовидных меню через template tag.
- Хранение данных в БД Django.
- Редактирование меню через стандартную админку Django.
- Активный пункт меню определяется исходя из URL текущей страницы.
- Возможность размещения нескольких меню на одной странице.
- переход на уровень менб по клику на `+`.
- Ровно 1 запрос к БД для отрисовки каждого меню (отследить можно на странице http://localhost:8000/silk/, на тестовой главной странице 2 меню).
- дополнительно настроен pre-commit (ruff, mypy, black) + CI GitHab Action (unittest)

## Запуск с Docker

1. Убедитесь, что Docker установлен на вашем компьютере.

2. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/serkuksov/treemenudjango.git
   cd treemenudjango

3. Запустите приложение с использованием Docker Compose:
   ```bash
   docker-compose up -d

4. Приложение будет доступно по адресу http://localhost:8000/.

5. В тестовой БД SQLite создано 2 меню доступные на главной странице.

6. Админ панель доступна по адресу http://localhost:8000/admin/.
* Логин: admin
* Пароль: admin


## Использование

1. Для добавления своего функционала зарегистрируйте ваше меню в админке Django.
2. Используйте template tag для отображения меню в шаблонах:

    ```html
    {% load menu %}
    {% draw_menu 'main_menu' %}
    ```
где `main_menu` - слаг меню указываемый в админке Django.

## Лицензия

TreeMenuDjango распространяется под лицензией [MIT](LICENSE.md).
