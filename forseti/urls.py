from django.urls import path

from . import views

urlpatterns = [
    # path('', views.get_empty, name='get_empty'),
    path('', views.get_index, name='get_index'),
    # path('rules/', views.RulesView.as_view(), name='rules'),
    path('rule/<str:rule_123>/', views.get_rule, name='rule'),
    path('search_deputy_in_region/', views.SearchDeputyInRegion.as_view(), name='search_deputy_in_region'),
    path('deputy/<str:deputy_name>/', views.get_deputy, name='deputy'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('restricted/', views.restricted, name='restricted'),
    path('add_url_prefer/', views.add_prefer_rule, name='add_prefer_rule'),
    path('delete_url_prefer/', views.delete_prefer_rule, name='add_prefer_rule'),
    path('add_url_dislike/', views.add_dislike_rule, name='add_dislike_rule'),
    path('delete_url_dislike/', views.delete_dislike_rule, name='delete_dislike_rule'),
    path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('populate/', views.populate_vote, name='populate_deputy'),       # Заполнение таблицы Голосования
    path('folk/', views.populate_folk_vote, name='populate_folk_vote'),  # Заполнение таблицы народного Голосования
    path('vox/', views.vox_populi, name='vox_populi'),      # Народное голосование
    path('search/', views.search_rule, name='search_rule'),
    path('isearch/', views.SearchRule.as_view(), name='search_print'),
    path('isearch_deputy/', views.SearchDeputy.as_view(), name='instant_search_deputy'),
    path('add_voting/', views.list_for_add_voting, name='add_voting'),  # Добавить голосования депутатов
    path('extend_check_date/', views.extend_check_date, name='extend_check_date'),  # Продлить на 10 дней срок проверки голосования по закону
    path('extend_check_date_20/', views.extend_check_date_20, name='extend_check_date_20'),  # Продлить на 20 дней срок проверки голосования по закону
    path('extend_check_date_60/', views.extend_check_date_60, name='extend_check_date_60'),  # Продлить на 20 дней срок проверки голосования по закону
    path('delete_check_date/', views.delete_check_date, name='delete_check_date'),  # Проголосовали - удалить запись из списка проверки
    path('set_start_period/', views.set_start_period, name='set_start_period'),  # Установить стартовый период проверки голосования
    path('delete_vox_populi/', views.delete_vox_populi, name='delete_vox_populi'),  # Удалить ВСЕ результаты народного голосования
    path('delete_populi_voting/', views.delete_populi_voting, name='delete_populi_voting'),  # Удалить голосование
    path('usefulness_uselesness/', views.usefulness_uselesness, name='usefulness_uselesness'),  # Добавить нужность/бесполезность
    path('delete_usefulness/', views.delete_usefulness, name='delete_usefulness'),  # Удалить содержимое таблиц Prefer и NotPrefer
    path('input_protocols/', views.input_protocols, name='input_protocols'),  # Открытие формы учёта протоколов
    path('protocols/', views.protocols_view, name='protocols'),  # Проверка протоколов, пересмотр даты проверки закона
    path('add_task/', views.addTask, name='add_task'),
    path('add_agree/', views.add_agree, name='add_agree'),  # Добавить согласие с поручением депутату в TasksRating
    path('delete_agree/', views.delete_agree, name='delete_agree'),  # Удалить согласие с поручением депутату
    path('add_suggestion/', views.add_suggestion, name='add_suggestion'),  # Удалить согласие с поручением депутату
    # path('add_deputy_result/', views.add_deputy_result, name='add_deputy_result'),  # Дополнить Rules результатами, потом удалить
    # path('add_populi_result/', views.add_populi_result, name='add_populi_result'),  # Дополнить Rules результатами, потом удалить
    # path('c121212/', views.c12, name='121212'),   # УДАЛИТЬ заполнение таблицы проверки голосования
]