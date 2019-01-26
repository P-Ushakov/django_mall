from django.contrib import admin
from . import models

# Register your models here.
# Группировка объектов по свойствам (помещения, вентустановки, лифты, ...)
admin.site.register(models.MlGroup)
# Распорядитель объекта (для комнаты - арендатор)
admin.site.register(models.ObjDisposer)
# Статус объекта (работает, нужен_аудит, нужен_ремонт, неработает, законсервирован, выключен)
admin.site.register(models.ObjStatus)
# Объект учета системой (все в системе есть объект: от ТРЦ до двигателя вентустановки)
admin.site.register(models.MlObject)
# Группировка элементов пасспорта (вес, размер, мощность, производительность, .. и еденицы группировки):
admin.site.register(models.MlObjectPassportKey)
# Элементы пасспортных данных объекта
admin.site.register(models.MlObjPassportData)
# Группировка контролируемых параметров объекта (например для помещений - температура)
# так же может быть скорость потока в воздуховоде, или влажность
admin.site.register(models.MlObjControlledParamKey)
# Параметры объекта, их верхняя и нижняя граница (например температура в помещении бассена)
admin.site.register(models.MlObjControlledParam)
# Периодически снимаемые показания датчиков, сведения об ошибке, если не в норме
admin.site.register(models.MlObjectControlledParamValues)
# Группировка приборов учета (например учет эл. энергии, тепла, воды, газа)
admin.site.register(models.MlObjCounterParamKey)
# Счетчик
admin.site.register(models.MlObjCounter)
# Периодически снимаемые показания счетчиков
# (всегда вводятся начальные и конечные, т.к. счетчик может быть заменен)
admin.site.register(models.MlObjCounterValues)
# Документы, приложенные к объекту (чертежи, фото, схемы, ...)
admin.site.register(models.AddedDocs)
# Стандартные группы сервисного обслуживания.
# Например Ежемесячное ТО, Ежеквартальное ТО, Ежегодное ТО, Консервация, Расконсервация, ...
admin.site.register(models.MlServiceGroup)
# Сгруппированный перечень стандартых операций по объекту
admin.site.register(models.MlObjServiceGroup)
# Полный перечень возможных сервисных операций
admin.site.register(models.MlServiceList)
# Все что входит в конкретное ТО
# Все обслуживание объекта делится на ТО, а ТО состоит из оперций.
admin.site.register(models.MlObjServiceWork)
# Способы определения даты обслуживания (в конкретоном квартале, в конкретном времени года,
# в конкретном месяце, раз в Х лет,  раз в Х месяцев, # раз в Х недель, раз в Х дней)
admin.site.register(models.FreqType)
# Регламент бслуживания объекта (частота проведения разных видов ТО по объекту)
admin.site.register(models.MlObjReglament)
# Событийная система - срабатывает при определенном событии
# (потеплело, похолодало, открылся ТРЦ, закрылся ТРЦ, ...)
admin.site.register(models.MlTriggeredEventBook)
# Журнал задач (задачи на день висят списком на главной странице.
# При считывании QR кода, появляются ближайшие задачи
# по объекту. При вызове задачи можно "выполнить задачу", "отменить задачу", "вернуться".
# При выполнении задачи или отмене, задача уходит с меню,
# в лог объекта пишется что задача выполнена или отменена
admin.site.register(models.MlObjTaskBook)
# Журнал Обслуживания объекта (автоматический лог)
admin.site.register(models.MlObjServiceBook)

