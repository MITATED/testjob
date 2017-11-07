# MITATED.github.io
Имеется стандартная база пользователей (добавляются через админку, регистрацию делать не нужно). У каждого пользователя есть блог (пара базовых полей). Нужно, чтобы у пользователей была возможность смотреть записи других пользователей (которые опубликованы), чтобы пользователь мог добавлять и редактировать свои записи. На всех страницах должна требоваться авторизация. В качестве дизайна можно использовать Bootstrap, но и можно использовать plain HTML.

Структура urls:

/blog/users/ — список всех пользователей
/blog/users/2/ — список записей пользователя с ID 2
/blog/2/ — Страница Post с ID 2
/blog/2/update/ — Страница редактирования Post с ID 2
/blog/create/ — Страница добавления поста

Структура модели Post:
— Название записи
— Текст записи (в форме ввода можно обычный textarea, но на страницах выводить форматированный код)
— Дата и время добавления
— Дата и время последнего изменения
— Флаг, который хранит информацию, опубликован ли пост
— Автор (FK)

С результатом теста нужно указать затраченное время, залить результат в репозиторий и указать ссылку. Желательна поддержка python3.
