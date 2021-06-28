from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import PartyFraction, MandatBasis, Deputy, FederalRegion, Rules, Prefer, NotPrefer, \
    Comments, FinalTable, VoxPopuli, CheckRulesForVoting, HowManyRulesChecked, TaskForDeputy, TasksRating


@admin.register(FederalRegion)
class FederalRegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    ordering = ('name',)


@admin.register(PartyFraction)
class PartyFractionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MandatBasis)
class MandatBasisAdmin(admin.ModelAdmin):
    """Тип мандата"""
    list_display = ('basis',)


@admin.register(Deputy)
class DeputyAdmin(admin.ModelAdmin):
    """Депутаты"""
    list_display = ('name', 'party_fraction', 'get_image', )
    fields = ('name', 'short_name', 'mandat_basis', 'electoral_district', 'party_fraction', 'region',
              'birth', 'image', 'current_squad')
    readonly_fields = ('get_image',)
    ordering = ('name',)
    search_fields = ('party_fraction',)
    list_per_page = 500

    def get_image(self, obj):
        return mark_safe(f'<img src={ obj.image.url } width="60" height="60">')

    get_image.short_description = 'Изображение'


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    """Законы"""
    list_display = ('rule_number', 'initialization_date', 'title', 'voted', 'populated', 'populi_voted')
    fields = ('rule_number', 'title', 'description', 'author', 'branch', 'constitutional',
              'initialization_date', 'rejection', 'vote_yes', 'vote_no', 'vote_abstained', 'vote_not_vote',
              'voted', 'populated', 'rule_tags', 'populi_voted',
              )
    list_display_links = ('title', )
    list_filter = ('voted',)
    search_fields = ('rule_number',)
    list_per_page = 500


@admin.register(Prefer)
class PreferAdmin(admin.ModelAdmin):
    """Лайки"""
    list_display = ('person', 'rule')


@admin.register(NotPrefer)
class NotPreferAdmin(admin.ModelAdmin):
    """Дизлайки"""
    list_display = ('person', 'rule')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Комментарии"""
    list_display = ('rule', 'name', 'text', 'date1')


#######################################################################################
#                  ЗАПОЛНЕНИЕ ТАБЛИЦЫ ГОЛОСОВАНИЯ (FINALTABLE)
#######################################################################################

# @admin.register(RowVote)
# class RowVoteAdmin(admin.ModelAdmin):
#     list_display = ('rule_number_test',)


@admin.register(FinalTable)
class FinalTableAdmin(admin.ModelAdmin):
    list_display = ('rule_number_final', 'name', 'fraction', 'vote_result')
    list_filter = ('vote_result',)
    search_fields = ('rule_number_final',)
    ordering = ('rule_number_final',)
    list_per_page = 500

#######################################################################################################################
#                                               НАРОДНОЕ ГОЛОСОВАНИЕ
#######################################################################################################################


@admin.register(VoxPopuli)
class VoxPopuliAdmin(admin.ModelAdmin):
    """Проверка голосования"""
    list_display = ('name', 'rule_number', 'result')
    list_per_page = 500
    search_fields = ('rule_number',)

#######################################################################################################################
#                                   СПИСОК ЗАКОНОВ, ПО КОТОРЫМ НЕТ ДАННЫХ О ГОЛОСОВАНИИ
#######################################################################################################################


@admin.register(CheckRulesForVoting)
class ChekRulesForVotingAdmin(admin.ModelAdmin):
    list_display = ('rule_idd', 'rule_number', 'last_check')
    list_per_page = 500
    search_fields = ('rule_number',)
    ordering = ('last_check',)

#######################################################################################################################
#                          КОЛИЧЕСТВО ПРОВЕРОК ЗАКОНОВ НА ПРЕДМЕТ ПРОВЕДЕНИЯ ГОЛОСОВАНИЯ ПО НИМ
#######################################################################################################################


@admin.register(HowManyRulesChecked)
class HowManyRulesCheckedAdmin(admin.ModelAdmin):
    list_display = ('check_date',)
    list_per_page = 100
    search_fields = ('check_date',)
    ordering = ('check_date',)

#######################################################################################################################
#                                                 ПОРУЧЕНИЯ ДЕПУТАТАМ
#######################################################################################################################


@admin.register(TaskForDeputy)
class TaskForDeputyAdmin(admin.ModelAdmin):
    list_display = ('id', 'deputy_name', 'task_author', 'task_text', 'task_rating')

#######################################################################################################################
#                                                   РЕЙТИНГ ПОРУЧЕНИЙ
#######################################################################################################################


@admin.register(TasksRating)
class TasksRatingAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'name')