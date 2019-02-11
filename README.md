# django_mall
mall management system

Добро пожаловать в альфа версию программы Django Mall

Программа позволяет вести учет состояния недвижимости и в первую очередь может быть интерестна эксплуатирующим компаниям.

Принцип работы следующий: Вносятся все объекты, за состоянием которых планируется вестись контроль.

Нример помещения под аренду, оборудование магазина, лифты, вентустановки, эскалаторы прочее...

Логика состоит из страниц, каждая из которых представляет объект или группу объектов и связана древовидной структурой с "родителями" (объектами, частью которых является данный объект) и "детьми" (группой объектов из которых состоит этот объект.

Объекты имеют маркеры состояния (работает, сломан, обслужен, нужен ремонт, ...) и поведение (определяется в группах). Поведение определяет как маркеры состояния передаются на объект "родитель"

Дерево может бесконечно масштабироваться. Таким образом: если у вас сломалась шестерня редуктора лифта, так как редуктор не может работать без шестерни - его маркер тоже "сломан", так как лифт не может работать без редуктора, его маркер тоже "сломан", магазин может работать без лифта - значит у магазина будет маркер "требуется ремонт"

Таким образом, внеся все элемены - можно наблюдать: когда и что то сломалось, когда его отремонтировали, на что влияет поломка.

Интерфейс состоит из 3-х разделов:

    Фронтенд сайта
    Пользовательский админ интерфейс (по умолчанию (/admin login|passw: admin admin)
    Интерфейс администратора сайта (/django-admin login|passw: admin admin)

Под капотом, программа использует:

    локально - Django, Pillow, Wagteil, wagtailautocomplete
    удаленно - Bootstrap 4, JQuery 3, Fontsawesome

Установка:

    Установить виртуальную машину питона (Python 3.6 или новее)
    Установить зависимости так: pip install -r requarements.txt
    Для запуска демо - запустить python manage.py runserver
    Для запуска вашего приложения, удалите базу sqlite3 и migrations,
        выполните комманды:
            python manage.py makemigrations
            python manage.py migrate
            python manage.py runserver

В альфа-версии функционал минимален. В дальнейшем планируется его значительное расширение

In alfa-version: interface, program menus and data fields is written in Russian and not localized. Im sorry, it will be done in next versions of program.

© Pavel Ushakov, BSD License

phone: +38 067 644 48 04 e-mail: p.v.ushakov@gmail.com