# Extends page_models
from mall.page_models import *


# Create your models here.
# Группировка объектов по свойствам (помещения, вентустановки, лифты, ...)
@register_snippet
class MlCategory(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="имя")
    description = models.TextField(blank=True,
                                   verbose_name="описание")
    panels = [
        FieldPanel('name'),
        FieldPanel('description', classname='full')
    ]

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = "object group"
        verbose_name = "категория группы объектов"
        # verbose_name_plural = "object groups"
        verbose_name_plural = "категория группы объектов"


# Распорядитель объекта (для комнаты - арендатор)
class MlObjDisposer(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="имя")
    description = models.TextField(blank=True,
                                   verbose_name="описание")

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = "object disposer"
        verbose_name = "распорядитель объекта"
        # verbose_name_plural = "object disposers"
        verbose_name_plural = "распорядители объектов"


# Статус объекта (работает, нужен_аудит, нужен_ремонт, неработает, законсервирован, выключен)
class MlObjStatus(models.Model):
    status_code = models.CharField(max_length=255,
                                   verbose_name="код статуса")
    name = models.CharField(max_length=255,
                            verbose_name="имя")
    description = models.TextField(blank=True,
                                   verbose_name="Описание")

    def __str__(self):
        return '{} {}'.format(self.status_code, self.name)

    class Meta:
        # verbose_name = "object status"
        verbose_name = "статус объекта"
        # verbose_name_plural = "object statuses"
        verbose_name_plural = "статусы объектов"

"""
# Объект учета системой (все в системе есть объект: от ТРЦ до двигателя вентустановки)
class MlObject(models.Model):
    name = models.CharField(max_length=255)
    obj_upp_expense_cat = models.CharField(max_length=255, blank=True)
    obj_parents = models.ManyToManyField('self', blank=True)
    obj_groups = models.ManyToManyField(MlCategory, blank=True)
    obj_status_id = models.ForeignKey(MlObjStatus,
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True, )
    obj_disposer_id = models.ForeignKey(MlObjDisposer,
                                        on_delete=models.SET_NULL,
                                        blank=True,
                                        null=True, )
    obj_location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")
    created = models.DateTimeField(blank=True)

    def __str__(self):
        return '{} {}'.format(self.obj_upp_expense_cat, self.name)

    class Meta:
        # verbose_name = "object"
        verbose_name = "объект"
        # verbose_name_plural = "object"
        verbose_name_plural = "объекты"


# Группировка элементов пасспорта (вес, размер, мощность, производительность, .. и еденицы группировки):
class MlObjPassportKey(models.Model):
    name = models.CharField(max_length=255)
    units = models.CharField(max_length=255, blank=True)
    can_be_grouped = models.BooleanField(blank=True)

    def __str__(self):
        return '{}, {}'.format(self.name, self.units)

    class Meta:
        # verbose_name = "object passport key"
        verbose_name = "пасспорт объекта (ключ)"
        # verbose_name_plural = "object passport keys"
        verbose_name_plural = "пасспорт объекта (ключи)"


# Элементы пасспортных данных объекта
class MlObjPassportData(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    ml_object_passport_key_id = models.ForeignKey(MlObjPassportKey, on_delete=models.CASCADE)
    ml_object_passport_key_value = models.CharField(max_length=50)

    def __str__(self):
        return '{} {}'.format(self.ml_object_passport_key_id, self.ml_object_passport_key_value)

    class Meta:
        # verbose_name = "object passport value"
        verbose_name = "пасспорт объекта (значение)"
        # verbose_name_plural = "object passport values"
        verbose_name_plural = "пасспорт объекта (значения)"


# Группировка контролируемых параметров объекта (например для помещений - температура)
# так же может быть скорость потока в воздуховоде, или влажность
class MlObjControlledParamKey(models.Model):
    name = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")

    def __str__(self):
        return '{}, {}'.format(self.name, self.units)

    class Meta:
        # verbose_name = "common controlled parameter"
        verbose_name = "общий контроллируемый параметр"
        # verbose_name_plural = "common controlled parameters"
        verbose_name_plural = "общие контроллируемые параметры"


# Параметры объекта, их верхняя и нижняя граница (например температура в помещении бассена)
class MlObjControlledParam(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    ml_obj_controlled_id = models.ForeignKey(MlObjControlledParamKey, on_delete=models.CASCADE)
    upper_value = models.DecimalField(max_digits=12, decimal_places=3)
    lower_value = models.DecimalField(max_digits=12, decimal_places=3)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")

    def __str__(self):
        return '{} {} {} {}'.format(self.ml_object_id, self.ml_obj_controlled_id, self.upper_value, self.lower_value)

    class Meta:
        # verbose_name = "object controlled parameter key"
        verbose_name = "параметр объекта (ключ)"
        # verbose_name_plural = "object controlled parameter keys"
        verbose_name_plural = "параметры объектов (ключи)"


# Периодически снимаемые показания датчиков, сведения об ошибке, если не в норме
class MlObjectControlledParamValues(models.Model):
    ml_obj_controlled_param_id = models.ForeignKey(MlObjControlledParam, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    value = models.DecimalField(max_digits=12, decimal_places=3)
    if_error = models.BooleanField(blank=True)
    error_code = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True,
                                   verbose_name="Описание ошибки")

    def __str__(self):
        return '{} {} {} {}'.format(self.date_time, self.value, self.if_error, self.error_code)

    class Meta:
        # verbose_name = "object controlled parameter value"
        verbose_name = "параметр объекта (значение)"
        # verbose_name_plural = "object controlled parameter values"
        verbose_name_plural = "параметры объектов (значения)"


# Группировка приборов учета (например учет эл. энергии, тепла, воды, газа)
class MlObjCounterParamKey(models.Model):
    name = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    upp_expense_cat = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")

    def __str__(self):
        return '{} {} {}'.format(self.name, self.units, self.upp_expense_cat)

    class Meta:
        # verbose_name = "common counter type"
        verbose_name = "тип счетчика по параметру учета"
        # verbose_name_plural = "common counter types"
        verbose_name_plural = "типы счетчиков по параметрам учета"


# Счетчик
class MlObjCounter(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    ml_obj_counter_param_key_id = models.ForeignKey(MlObjCounterParamKey, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        # verbose_name = "counter"
        verbose_name = "счетчик"
        # verbose_name_plural = "counters"
        verbose_name_plural = "счетчики"


# Периодически снимаемые показания счетчиков (всегда вводятся начальные и конечные, т.к. счетчик может быть заменен)
class MlObjCounterValues(models.Model):
    ml_obj_counter_id = models.ForeignKey(MlObjCounter, on_delete=models.CASCADE)
    old_date = models.DateTimeField()
    old_value = models.DecimalField(max_digits=12, decimal_places=3)
    new_date = models.DateTimeField()
    new_value = models.DecimalField(max_digits=12, decimal_places=3)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")

    def __str__(self):
        return '{} {} {} {}'.format(self.old_date, self.old_value, self.new_date, self.new_value)

    class Meta:
        # verbose_name = "counter value"
        verbose_name = "показания счетчика"
        # verbose_name_plural = "counter values"
        verbose_name_plural = "показания счетчиков"


# Документы, приложенные к объекту (чертежи, фото, схемы, ...)
class MlObjAddedDocs(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    obj_doc = models.FileField()
    doc_teg = models.CharField(max_length=255, blank=True)
    doc_description = models.TextField(blank=True,
                                       verbose_name="Описание документа")

    class Meta:
        # verbose_name = "added document"
        verbose_name = "приложенный документ"
        # verbose_name_plural = "added documents"
        verbose_name_plural = "приложенные документы"


# Стандартные группы сервисного обслуживания.
# Например Ежемесячное ТО, Ежеквартальное ТО, Ежегодное ТО, Консервация, Расконсервация, ...
class MlServiceGroup(models.Model):
    name = models.CharField(verbose_name="Наименование",
                            max_length=255,)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = "service group"
        verbose_name = "группа сервисного обслуживания"
        # verbose_name_plural = "added documents"
        verbose_name_plural = "группы сервисного обслуживания"


# Сгруппированный перечень стандартых операций по объекту
class MlObjServiceGroup(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    ml_service_group_id = models.ForeignKey(MlServiceGroup, on_delete=models.CASCADE)
    # Описание: например № и дата договора и компания, вып. работы
    description = models.TextField(blank=True,
                                   verbose_name="Описание")


# Полный перечень возможных сервисных операций
class MlServiceList(models.Model):
    name = models.CharField(max_length=255)
    # Код можно взять с стандартных таможенных кодировок
    job_code = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")


# Все что входит в конкретное ТО
# Все обслуживание объекта делится на ТО, а ТО состоит из оперций.
class MlObjServiceWork(models.Model):
    ml_obj_service_group_id = models.ForeignKey(MlServiceGroup, on_delete=models.CASCADE)
    ml_service_list_id = models.ForeignKey(MlServiceList, on_delete=models.CASCADE)
    # Полное описание операций: Например замена подшипников в кол-ве 30 штук
    description = models.TextField(blank=True,
                                   verbose_name="Описание")


# Способы определения даты обслуживания (в конкретоном квартале, в конкретном времени года,
# в конкретном месяце, раз в Х лет,  раз в Х месяцев, # раз в Х недель, раз в Х дней)
class MlServiceFreqType(models.Model):
    name = models.CharField(max_length=255)
    # используем, если дата ТО может быть сдвинута.
    # если дата сдвинута быть не может (например консервация на зиму) то False
    can_be_shifted_on = models.IntegerField(default=0)
    # используем, если ТО можеть быть проведено в любое время в году с периодичностью Х лет
    time_in_years_between_service = models.IntegerField(default=0)
    # используем, если ТО можеть быть проведено в любое время в квартале с периодичностью Х кварталов
    time_in_quarters_between_service = models.IntegerField(blank=True)
    # используем, если ТО можеть быть проведено в любое время в сезон с периодичностью Х сезонов
    time_in_seasons_between_service = models.IntegerField(blank=True)
    # используем, если ТО можеть быть проведено в любое время в месяце с периодичностью Х месяцев
    time_in_months_between_service = models.IntegerField(blank=True)
    # используем, если ТО можеть быть проведено в любое время в неделе с периодичностью Х недель
    time_in_weeks_between_service = models.IntegerField(blank=True)
    # используем, если ТО можеть быть проведено в любое время дня с периодичностью Х дней
    time_in_days_between_service = models.IntegerField(blank=True)
    # используем, если ТО можеть быть проведено в определенное время с периодичностью Х часов
    time_in_hours_between_service = models.IntegerField(blank=True)

    def __str__(self):
        return '{} shift:{} Y:{} Q:{} S:{} M:{} W:{} D:{} H:{}'\
            .format(self.name, self.can_be_shifted_on,
                    self.time_in_years_between_service,
                    self.time_in_quarters_between_service,
                    self.time_in_seasons_between_service,
                    self.time_in_months_between_service,
                    self.time_in_weeks_between_service,
                    self.time_in_days_between_service,
                    self.time_in_hours_between_service)


# Регламент бслуживания объекта (частота проведения разных видов ТО по объекту)
class MlObjReglament(models.Model):
    ml_obj_service_work_id = models.ForeignKey(MlObjServiceWork, on_delete=models.CASCADE)
    freq_type_id = models.ForeignKey(MlServiceFreqType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")


# Событийная система - срабатывает при определенном событии
# (потеплело, похолодало, открылся ТРЦ, закрылся ТРЦ, ...)
class MlTriggeredEventBook(models.Model):
    event_name = models.CharField(max_length=255)
    event_description = models.TextField(blank=True,
                                         verbose_name="Описпние события")
    # ToDo: Список ниже должен при срабатывании генерировать перечень задач в журнале задач
    list_of_triggered_service_works = models.ManyToManyField(MlObjServiceWork)

# ToDo:
# Объектная локальная событийная система. Срабатывает по показаниям датчиков объекта. Вызывает каскад действий
# Комп, обслуживающий датчик может послать Post на определенный УРЛ. Это является тригером.
# Подумать над интеграцией с консолью систем умных домов

# ToDo:
# Журнал аварий

# ToDo:
# Журнал внеплановых ремонтов

# ToDo:
# Журнал предписаний, устранения жалоб,  ручного планирования ремонтов

# ToDo:
# Перечень списываемых по умолчанию материалов на одну операцию по объекту (если конечно это нужно)

# ToDo:
# Журналы учета потребления энергоносителей (как ТРЦ так и арендаторов), автоматический прогноз потребления

# ToDo:
# ? Сметы по ремонту, Акты вып. работ, Приход-расход материалов,

# ToDo:
# Таблица приоритетов задач

# ToDo:
# ? Пути прохождения задач

# ToDo:
# Статус задачи: запланирована, отложена, в процессе исполнения, выполнена, отменена, черновик


# Журнал задач (задачи на день висят списком на главной странице.
# При считывании QR кода, появляются ближайшие задачи
# по объекту. При вызове задачи можно "выполнить задачу", "отменить задачу", "вернуться".
# При выполнении задачи или отмене, задача уходит с меню,
# в лог объекта пишется что задача выполнена или отменена
class MlObjTaskBook(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255)
    # дерево задач сворачивается на группы (они же ТО)
    # те задачи, которые не выполнены по прошлым ТО, попадают в верх списка в группу "Просрочено"
    service_group = models.CharField(max_length=255)
    date_of_issue = models.DateTimeField()
    should_be_done_before = models.DateTimeField()
    # у ежегодных задач: 0, у ежеквартальных: 1, у сезонных:2, у ежемесячных:3, у
    priority = models.SmallIntegerField(default=0)
    # описание работ, которые необходимо провести
    description = models.TextField(blank=True,
                                   verbose_name="Описание")
    # источник задачи (плановый журнал, аварийный журнал, событийный журнал, прочее)
    task_creator = models.CharField(max_length=255, blank=True)
    accept_task_trigger = models.DateTimeField()
    start_task_trigger = models.DateTimeField()
    # ToDo: Выяснить как дописать к задаче исполнителя, из залогиненных в системе
    task_person = models.CharField(max_length=255)


# Журнал Обслуживания объекта (автоматический лог)
# Is written by logic
class MlObjServiceBook(models.Model):
    ml_object_id = models.ForeignKey(MlObject, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255)
    service_group = models.CharField(max_length=255)
    time_of_completion_or_cancellation: datetime = models.DateTimeField()
    date_of_issue = models.DateTimeField()
    should_be_done_before = models.DateTimeField()
    priority = models.SmallIntegerField(default=0)
    description = models.TextField(blank=True,
                                   verbose_name="Описание")
    # источник задачи (плановый журнал, аварийный журнал, событийный журнал, прочее)
    task_creator = models.CharField(max_length=255, blank=True)
    # поле заполняет человек, если нужно описание проведенных работ
    operational_description = models.TextField(blank=True,
                                               verbose_name="Описание")
    # если задача отменена, то False
    is_completed = models.BooleanField(default=True)
    accept_task_trigger = models.DateTimeField()
    start_task_trigger = models.DateTimeField()
    task_person = models.CharField(max_length=255)
"""

# ToDo Журнал пресетов, таблица с БИМ структурой, журнал запчастей, собранный лог счетчиков
