from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class FederalRegion(models.Model):
    """Регионы Российской федерации"""
    name = models.CharField('Субъект РФ', max_length=100)

    class Meta:
        verbose_name = 'Регионы'
        verbose_name_plural = 'Регионы'


class PartyFraction(models.Model):
    """Фракции"""
    name = models.CharField(max_length=30, default='')

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракции'

    def __str__(self):
        return self.name


class MandatBasis(models.Model):
    """Мандат"""
    # Избран по одномандатному или по партийным спискам
    basis = models.CharField('Тип мандата', max_length=30, default='')

    class Meta:
        verbose_name = 'Мандат'
        verbose_name_plural = 'Мандат'

    def __str__(self):
        return self.basis

#####################################################################################################################
#                                                     ДЕПУТАТЫ
#####################################################################################################################


class Deputy(models.Model):
    """Депутаты"""
    CHOICES = (
        ('Единая Россия', 'Единая Россия'),
        ('КПРФ', 'КПРФ'),
        ('Справедливая Россия', 'Справедливая Россия'),
        ('ЛДПР', 'ЛДПР'),
        ('Вне фракций', 'Вне фракций'),
    )
    name = models.CharField('ФИО', max_length=150, default='', unique=True)
    short_name = models.CharField('ФИО с инициалами', max_length=150, default='')
    party_fraction = models.CharField('Фракция', choices=CHOICES, max_length=50, default='')
    region = models.CharField('Регион', max_length=400, default='', blank=True)
    birth = models.DateField('Дата рождения', )
    image = models.ImageField('Изображение', upload_to='deputy/')
    mandat_basis = models.ForeignKey(MandatBasis, verbose_name='мандат', on_delete=models.SET_NULL, null=True,
                                     blank=True)
    electoral_district = models.CharField('Избирательный округ', max_length=20, default='', blank=True)
    current_squad = models.BooleanField('Действующий состав', default=True)

    def get_absolute_url(self):
        return reverse('deputy', kwargs={'deputy_name': self.name})

    class Meta:
        verbose_name = 'Депутат'
        verbose_name_plural = 'Депутаты'
        ordering = ['name']

    def __str__(self):
        return self.name


def get_all_deputy():
    all_deputy = Deputy.objects.all()
    return all_deputy

######################################################################################################################
#                                                      ЗАКОНЫ
######################################################################################################################


class Rules(models.Model):
    """Законы"""
    rule_number = models.CharField('Номер закона', unique=True, max_length=20, default='')    # Номер законопроекта
    title = models.TextField('Заголовок', max_length=700)
    description = models.TextField('Описание', max_length=50000, default='')
    constitutional = models.BooleanField('Поправка в Конституцию?', default=False)
    author = models.CharField('Авторы', max_length=400, default='')
    consumer = models.CharField('Заказчик', max_length=400, default='Неизвестен')
    branch = models.CharField('Отрасль законодательства', max_length=300, default='', blank=True)
    rule_link = models.CharField('Ссылка на страницу на сайте ГД', max_length=100, default='', blank=True)
    initialization_date = models.DateField('На рассмотрении с', default=None)
    yet_voted = models.BooleanField('Уже проголосовали?', default=False)
    rejection = models.BooleanField('Отклонён', default=False)
    vote_yes = models.TextField('За', max_length=15000, default='', blank=True)
    vote_no = models.TextField('Против', max_length=15000, default='', blank=True)
    vote_abstained = models.TextField('Воздержались', max_length=10000, default='', blank=True)
    vote_not_vote = models.TextField('Не голосовали', max_length=15000, default='', blank=True)
    voted = models.BooleanField('Депутаты', default=False)  # Депутаты проголосовали
    populi_voted = models.BooleanField('Н зап', default=False)  # Народ проголосовал
    voting_date = models.DateField('Дата голосования', default=date.today)
    result_deputy_vote = models.CharField('Рез депутатов', max_length=10, default='')
    result_populi_vote = models.CharField('Рез народа', max_length=10, default='')
    rule_tags = models.CharField('Теги', max_length=200, blank=True)
    visits = models.IntegerField('Просмотры', default=0)
    populated = models.BooleanField('Д зап', default=False) # Заполнена таблица депутатского голосования
    set_start_period = models.BooleanField('Добавлен закон в таблицу CheckRulesForVoting?', default=False)

    class Meta:
        verbose_name = 'Закон'
        verbose_name_plural = 'Законы'

    def __str__(self):
        return self.rule_number

    def get_absolute_url(self):
        return reverse('rule', kwargs={'rule_123': self.rule_number})

#####################################################################################################################
#                                           ЛАЙКИ (НУЖНЫЙ ЗАКОН)
#####################################################################################################################


class Prefer(models.Model):
    person = models.CharField('Имя', max_length=50)
    rule = models.CharField('Закон', max_length=15)

    class Meta:
        verbose_name = 'Нужность'
        verbose_name_plural = 'Нужность'

#####################################################################################################################
#                                       ДИЗЛАЙКИ (НЕНУЖНЫЙ ЗАКОН)
#####################################################################################################################


class NotPrefer(models.Model):
    person = models.CharField('Имя', max_length=50)
    rule = models.CharField('Закон', max_length=15)

    class Meta:
        verbose_name = 'Бесполезность'
        verbose_name_plural = 'Бесполезность'


#####################################################################################################################
#                                                    КОММЕНТАРИИ
#####################################################################################################################


class Comments(models.Model):
    """Комментарии"""
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    date1 = models.DateTimeField(auto_now=True)
    rule = models.ForeignKey(Rules, verbose_name='Закон', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.rule}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


#####################################################################################################################
#                                       ТАБЛИЦА ГОЛОСОВАНИЯ ДЕПУТАТОВ
#####################################################################################################################


class FinalTable(models.Model):
    rule_number_final = models.CharField('Номер закона', max_length=20)
    name = models.CharField('Имя депутата', max_length=50)
    fraction = models.CharField('Фракция', max_length=30, blank=True)
    vote_result = models.CharField('Результат голосования', max_length=20)

    class Meta:
        verbose_name = 'Голосования'
        verbose_name_plural ='Голосования'

#####################################################################################################################
#                                                 НАРОДНОЕ ГОЛОСОВАНИЕ
#####################################################################################################################


class VoxPopuli(models.Model):
    name = models.CharField('Кто проголосовал', max_length=50, default='')
    rule_number = models.CharField('Номер закона', max_length=20, default='')
    result = models.CharField('Как проголосовал', max_length=15)

    class Meta:
        verbose_name = 'Народное голосование'
        verbose_name_plural = 'Народное голосование'

#######################################################################################################################
#                                   ПРОВЕРКА БЫЛО ЛИ ПРОВЕДЕНО ГОЛОСОВАНИЕ ПО ЗАКОНУ
#######################################################################################################################


class CheckRulesForVoting(models.Model):
    rule_number = models.CharField('Номер закона', max_length=20, default='')
    rule_idd = models.CharField('ID закона', max_length=10, default='')
    last_check = models.DateField('Дата последней проверки', default=date.today)

    class Meta:
        verbose_name = 'Проверка голосования'
        verbose_name_plural = 'Проверка голосования'

#######################################################################################################################
#                           СКОЛЬКО ПРОВЕРИЛ ЗА ДЕНЬ ЗАКОНОВ (ПРОВЕРКА ГОЛОСОВАНИЯ)
#######################################################################################################################


class HowManyRulesChecked (models.Model):
    check_date = models.DateField('Дата проверки', default='')

    class Meta:
        verbose_name ='Количество проверок'
        verbose_name_plural = 'Количество проверок'


#######################################################################################################################
#                                                     ПОРУЧЕНИЯ
#######################################################################################################################


class TaskForDeputy(models.Model):
    task_author = models.CharField('Автор', max_length=50)
    task_text = models.CharField('Поручение', max_length=10000)
    task_date = models.DateField('Дата регистрации поручения', default='')
    task_rating = models.IntegerField('Рейтинг поручения', default=0)
    deputy_name = models.CharField('Для депутата', max_length=50)

    class Meta:
        verbose_name = 'Поручения'
        verbose_name_plural = 'Поручения'

#######################################################################################################################
#                                               РЕЙТИНГ ПОРУЧЕНИЙ
#######################################################################################################################


class TasksRating(models.Model):
    task_id = models.IntegerField('Id поручения', default=0)
    name = models.CharField('Пользователь', max_length=50)

    class Meta:
        verbose_name = 'Рейтинг поручений'
        verbose_name_plural = 'Рейтинг поручений'

#######################################################################################################################
#                                               ОТЗЫВЫ И ПОЖЕЛАНИЯ
#######################################################################################################################


class Suggestions(models.Model):
    suggestion_text = models.CharField('Текст', max_length=1000, default='')
    suggestion_date = models.DateTimeField('Дата', auto_now=True)
    suggestion_published = models.BooleanField('Опубликовано', default=False)
    suggestion_proved = models.BooleanField('Проверено', default=False)
    suggestion_author = models.CharField('Автор', max_length=100, default='')

    class Meta:
        verbose_name = 'Отзывы и пожелания'
