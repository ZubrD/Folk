from datetime import datetime, timedelta, date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
import random

from .forms import UserForm, CommentForm
from .models import Deputy, FederalRegion, Rules, Prefer, NotPrefer, Comments, FinalTable, \
    VoxPopuli, CheckRulesForVoting, HowManyRulesChecked, TaskForDeputy, TasksRating

# from .models import Post, Like
from .serializers import DeputySerializer, RuleSerializer, DeputyInstantSearchSerializer


#######################################################################################################################
#                                            ГЛАВНАЯ СТРАНИЦА
#######################################################################################################################


def get_index(request):
    items = Rules.objects.filter(populated=True, voted=True, populi_voted=True)    # случайный выбор закона,
    rule = random.choice(items)                 # за который проголосовал и народ, и депутаты
    startregdate = Rules.objects.order_by('initialization_date').last().initialization_date
    endregdate = startregdate - timedelta(days=6)
    registered_rules = Rules.objects.filter(initialization_date__range=[endregdate, startregdate], rejection=False).order_by('-initialization_date')
    startvotdate = Rules.objects.filter(voted=True, populated=True).order_by('voting_date').last().voting_date
    endvotdate = startvotdate - timedelta(days=30)
    voted_rules = Rules.objects.filter(voted=True, populated=True).filter(voting_date__range=[endvotdate, startvotdate]).order_by('-voting_date')
    regions = FederalRegion.objects.all()
    v_yes_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='За').count()
    v_no_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Против').count()
    v_abstained_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Воздержался').count()
    v_not_vote_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Не голосовал').count()
    v_total_count = FinalTable.objects.filter(rule_number_final=rule.rule_number).count()
    v_yes_pr = v_no_pr = v_abstained_pr = v_not_vote_pr = 0
    if v_total_count:   # Проверка деления на ноль
        v_yes_pr = round(v_yes_count/v_total_count*100, 1)
        v_no_pr = round(v_no_count/v_total_count*100, 1)
        v_abstained_pr = round(v_abstained_count/v_total_count*100, 1)
        v_not_vote_pr = round(100 - (v_yes_pr + v_no_pr + v_abstained_pr), 1)

    p_yes_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='За').count()
    p_no_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='Против').count()
    p_abstained_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='Воздержался').count()
    p_total_count = VoxPopuli.objects.filter(rule_number=rule.rule_number).count()
    p_yes_pr = p_no_pr = p_abstained_pr = 0
    if p_total_count:
        p_yes_pr = round(p_yes_count/p_total_count*100, 1)
        p_no_pr = round(p_no_count/p_total_count*100, 1)
        p_abstained_pr = round(100 - (p_yes_pr + p_no_pr), 1)

    quorum = 226
    if rule.constitutional:
        quorum = 296
    if (v_yes_count + v_no_count) < quorum:
        v_result_voting = 'Отклонён'
        v_result_voting_color = 'gray'
    else:
        if v_yes_count > v_no_count:
            v_result_voting = 'За'
            v_result_voting_color = 'green'
        else:
            v_result_voting = 'Против'
            v_result_voting_color = 'red'
    if p_yes_count > p_no_count:
        p_result_voting = 'За'
        p_result_voting_color = 'green'
    else:
        p_result_voting = 'Против'
        p_result_voting_color = 'red'

    rules_voted = Rules.objects.filter(populated=True, populi_voted=True)
    concurrence_count = 0       # Подсчёт совпадений мнений депутатов и народа при голосовании
    for rule_voted in rules_voted:
        if rule_voted.result_deputy_vote == rule_voted.result_populi_vote:
            concurrence_count += 1
    count_rules = Rules.objects.filter(populated=True, voted=True, populi_voted=True).count()
    concurrence_ratio = round((concurrence_count / count_rules) * 100)

    context = {'registered_rules': registered_rules,
               'endregdate': endregdate,
               'startregdate': startregdate,
               'voted_rules': voted_rules,
               'endvotdate': endvotdate,
               'startvotdate': startvotdate,
               'rule': rule,
               'regions': regions,
               'v_yes': v_yes_count,
               'v_no': v_no_count,
               'v_abstained': v_abstained_count,
               'v_not_vote': v_not_vote_count,
               'v_yes_pr': v_yes_pr,
               'v_no_pr': v_no_pr,
               'v_abstained_pr': v_abstained_pr,
               'v_not_vote_pr': v_not_vote_pr,
               'p_yes': p_yes_count,
               'p_no': p_no_count,
               'p_abstained': p_abstained_count,
               'p_total_count': p_total_count,
               'p_yes_pr': p_yes_pr,
               'p_no_pr': p_no_pr,
               'p_abstained_pr': p_abstained_pr,
               'v_result_voting': v_result_voting,
               'p_result_voting': p_result_voting,
               'v_result_voting_color': v_result_voting_color,
               'p_result_voting_color': p_result_voting_color,
               'total_voted_rules': count_rules,
               'concurrence_count': concurrence_count,
               'concurrence_ratio': concurrence_ratio,
               }
    return render(request, 'shabls/index.html', context)

#######################################################################################################################
#                                             СТРАНИЦА ОДНОГО ЗАКОНА
#######################################################################################################################


class RulesView(ListView):
    model = Rules
    queryset = Rules.objects.all()
    template_name = 'shabls/rule.html'


def get_rule(request, rule_123):
    rule = get_object_or_404(Rules, rule_number=rule_123)
    deputies = Deputy.objects.values_list('short_name', flat=True)  # Создаю массив
    array_deputies = list(deputies)                                 # имён депутатов
    deputies_query = Deputy.objects.all()
    authors_without_comma = rule.author.replace(',', '')    # Удаляю запятыие из списка авторов
    authors_without_comma = authors_without_comma.replace(';', '')    # Удаляю точку с запятой из списка авторов
    array_authors = authors_without_comma.split()       # Список авторов помещаю пословно в массив
    visits = rule.visits    # Извлекаю количесво просмотров
    visits += 1             # Увеличиваю количество просмотров
    rule.visits = visits    # Записываю новое значение
    rule.save()             # Сохраняю новое значение в БД    liked_or_not = 'no'
    current_user = request.user.username
    comments = Comments.objects.filter(rule=rule.id).order_by('date1')

    l_count = Prefer.objects.filter(rule=rule.rule_number).count()       # Подсчёт лайков
    dl_count = NotPrefer.objects.filter(rule=rule.rule_number).count()   # Подсчёт дизлайков

    liked_or_not = 'not-liked'
    disliked_or_not = 'not-disliked'
    l = Prefer.objects.filter(rule=rule.rule_number, person=current_user)
    dl = NotPrefer.objects.filter(rule=rule.rule_number, person=current_user)
    if l:
        liked_or_not = 'liked'
    if dl:
        disliked_or_not = 'disliked'

    usefulness = 0
    usefulness_color = ''
    if l_count or dl_count:
        usefulness = round((l_count/(l_count+dl_count))*100, 1)
        if usefulness > 50:
            usefulness_color = 'green'
        if usefulness < 50:
            usefulness_color = 'red'
    if l_count == 0 and dl_count == 0:
        usefulness = l

    v_yes_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='За').count()
    v_no_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Против').count()
    v_abstained_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Воздержался').count()
    v_not_vote_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Не голосовал').count()
    v_total_count = FinalTable.objects.filter(rule_number_final=rule.rule_number).count()
    v_yes_pr = v_no_pr = v_abstained_pr = v_not_vote_pr = 0
    if v_total_count:   # Проверка деления на ноль
        v_yes_pr = round(v_yes_count/v_total_count*100, 1)
        v_no_pr = round(v_no_count/v_total_count*100, 1)
        v_abstained_pr = round(v_abstained_count/v_total_count*100, 1)
        v_not_vote_pr = round(100 - (v_yes_pr + v_no_pr + v_abstained_pr), 1)

    p_yes_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='За').count()
    p_no_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='Против').count()
    p_abstained_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='Воздержался').count()
    p_total_count = VoxPopuli.objects.filter(rule_number=rule.rule_number).count()
    p_yes_pr = p_no_pr = p_abstained_pr = 0
    if p_total_count:
        p_yes_pr = round(p_yes_count/p_total_count*100, 1)
        p_no_pr = round(p_no_count/p_total_count*100, 1)
        p_abstained_pr = round(100 - (p_yes_pr + p_no_pr), 1)

    quorum = 226
    if rule.constitutional:
        quorum = 296
    if (v_yes_count + v_no_count) < quorum:
        v_result_voting = 'Отклонён'
        v_result_voting_color = 'gray'
    else:
        if v_yes_count > v_no_count:
            v_result_voting = 'За'
            v_result_voting_color = 'green'
        else:
            v_result_voting = 'Против'
            v_result_voting_color = 'red'
    if p_yes_count > p_no_count:
        p_result_voting = 'За'
        p_result_voting_color = 'green'
    else:
        p_result_voting = 'Против'
        p_result_voting_color = 'red'
    this_user_result_voting = VoxPopuli.objects.filter(rule_number=rule.rule_number, name=current_user)
    rule_voted_or_not = FinalTable.objects.filter(rule_number_final=rule)

    context = {'rule': rule,
               'array_authors': array_authors,
               'array_deputies': array_deputies,
               'deputies_query': deputies_query,
               'current_user': current_user,
               'liked_or_not': liked_or_not,
               'likes_count': l_count,
               'disliked_or_not': disliked_or_not,
               'dislikes_count': dl_count,
               'usefulness': usefulness,
               'usefulness_color': usefulness_color,
               'comments': comments,
               'v_yes': v_yes_count,
               'v_no': v_no_count,
               'v_abstained': v_abstained_count,
               'v_not_vote': v_not_vote_count,
               'v_yes_pr': v_yes_pr,
               'v_no_pr': v_no_pr,
               'v_abstained_pr': v_abstained_pr,
               'v_not_vote_pr': v_not_vote_pr,
               'p_yes': p_yes_count,
               'p_no': p_no_count,
               'p_abstained': p_abstained_count,
               'p_total_count': p_total_count,
               'p_yes_pr': p_yes_pr,
               'p_no_pr': p_no_pr,
               'p_abstained_pr': p_abstained_pr,
               'v_result_voting': v_result_voting,
               'p_result_voting': p_result_voting,
               'v_result_voting_color': v_result_voting_color,
               'p_result_voting_color': p_result_voting_color,
               'this_user_result_voting': this_user_result_voting,
               'rule_voted_or_not': rule_voted_or_not,
               'quorum': quorum
               }
    return render(request, 'shabls/one_rule.html', context)

#######################################################################################################################
#                                     ПОИСК ДЕПУТАТОВ ИЗ ВЫПАДАЮЩЕГО СПИСКА
#######################################################################################################################


class SearchDeputyInRegion(APIView):
    """Поиск депутатов по региону (из выпадающего списка) из ajax-запроса """

    def get(self, request):
        if request.method == 'GET':
            searched_region = request.GET['search_region']
            deputies = Deputy.objects.filter(region__search=searched_region).filter(current_squad=True)
            serializer = DeputySerializer(deputies, many=True)
            return Response(serializer.data)

#######################################################################################################################
#                                            ПОИСК ДЕПУТАТА В СТРОКЕ ПОИСКА
#######################################################################################################################


class SearchDeputy(APIView):      # моментальный вывод результатов поиска депутата
    # get - в названии должно быть обязательно
    # https://stackoverflow.com/questions/57302570/detail-method-get-not-allowed-django-rest-framework

    def get(self, request):
        searched = request.GET['searched_val']
        query = Deputy.objects.filter(name__icontains=searched).filter(current_squad=True)
        serializer = DeputyInstantSearchSerializer(query, many=True)
        return Response(serializer.data)

#######################################################################################################################
#                                                    ДЕПУТАТ
#######################################################################################################################


def get_deputy(request, deputy_name):   # Имя аргумента deputy_name должно совпадать с тем, что в urls.py
    deputy = get_object_or_404(Deputy, name=deputy_name)
    rules = Rules.objects.filter(author__icontains=deputy.short_name)
    rules_count = Rules.objects.filter(author__icontains=deputy.short_name).count()

    d_yes = Rules.objects.filter(vote_yes__icontains=deputy_name)
    d_no = Rules.objects.filter(vote_no__icontains=deputy_name)
    d_abstained = Rules.objects.filter(vote_abstained__icontains=deputy_name)
    d_not_vote = Rules.objects.filter(vote_not_vote__icontains=deputy_name)
    d_total_count = d_yes.count() + d_no.count() + d_abstained.count() + d_not_vote.count()

    concurrences_yes = Rules.objects.filter(Q(vote_yes__icontains=deputy_name) & Q(result_populi_vote='За'))
    concurrences_no = Rules.objects.filter(Q(vote_no__icontains=deputy_name) & Q(result_populi_vote='Против'))
    concurrences = concurrences_yes | concurrences_no
    concurrences_count = concurrences.count()

    count_yes = concurrences_yes.count()
    count_no = concurrences_no.count()

    concurrence_ratio = round(((count_yes + count_no)/d_total_count)*100, 1)    # Совпадение с мнением народа

    tasks = TaskForDeputy.objects.filter(deputy_name=deputy_name).order_by('-task_rating')
    current_user = request.user.username
    tasks_rating = TasksRating.objects.filter(name=current_user).values_list('task_id', flat=True)
    id_list = list(tasks_rating)

    context = {'deputy': deputy,
               'rules': rules,
               'rules_count': rules_count,
               'concurrences': concurrences,
               'concurrences_yes': count_yes,
               'concurrences_no': count_no,
               'concurrences_count': concurrences_count,
               'concurrence_ratio': concurrence_ratio,
               'd_not_vote': d_not_vote.count(),
               'd_total_count': d_total_count,
               'tasks': tasks,
               'id_list': id_list,
               }
    print(id_list)
    return render(request, 'shabls/deputy.html', context)

##################################################################################################
#                                           РЕГИСТРАЦИЯ
##################################################################################################


def register(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('get_index'))
        else:
            print(user_form.errors.as_text(),)
    else:
        user_form = UserForm()

    return render(request,
                  'shabls/register.html',
                  {'user_form': user_form})

#############################################################################################
#                                    ВХОД И ВЫХОД
#############################################################################################


def user_login(request):
    if request.method == 'POST':
        # Соберите имя пользователя и пароль, предоставленные пользователем.
        # Эта информация получена из формы авторизации.
        # Мы используем request.POST.get ('<variable>')
        # в отличие от request.POST ['<variable>'],
        # потому что request.POST.get ('<variable>')
        # возвращает None, если значение не существует,
        # а request.POST ['<variable>'] вызовет исключение KeyError.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Используйте механизм Django,
        # чтобы попытаться проверить, является ли комбинация
        # имя пользователя / пароль действительной - объект User возвращается, если он есть.
        user = authenticate(username=username, password=password)

        # Если у нас есть объект User, детали верны.
        # Если None (способ представления отсутствия в Python),
        # пользователь с соответствующими учетными данными не найден.
        if user:
            # Активен ли аккаунт? Он мог быть отключен.
            if user.is_active:
                # Если учетная запись действительна и активна,
                # мы можем войти в систему пользователя.
                # Мы отправим пользователя обратно на домашнюю страницу.
                login(request, user)
                return HttpResponseRedirect(reverse('get_index'))
            else:
                # Использован неактивный аккаунт - не входить!
                return HttpResponse('Your Rango account is disabled.')
        else:
            # Указаны неверные данные для входа.
            # Поэтому мы не можем войти в систему.
            print('Invalid login details: {0}, {1}'.format(username, password))
            return HttpResponse('Неправильный логин или пароль.')

    # Запрос не является HTTP POST, поэтому отобразите форму входа.
    # Этот сценарий, скорее всего, будет HTTP GET.
    else:
        # Нет переменных контекста для передачи в систему шаблонов,
        # следовательно, пустой объект словаря ...
        return render(request, 'shabls/login.html', {})


# Используйте декоратор login_required (), чтобы обеспечить доступ
# к представлению только зарегистрированным пользователям.
@login_required
def restricted(request):
    context_dict = {'restricted_text': 'Это страница с ограниченным доступом'}
    return render(request, 'shabls/restricted.html', context_dict)


@login_required
def user_logout(request):
    # Так как мы знаем, что пользователь вошел в систему,
    # теперь мы можем просто вывести его из неё.
    logout(request)
    return HttpResponseRedirect(reverse('get_index'))




#######################################################################################################################
#                               ЛАЙКИ И ДИЗЛАЙКИ (НУЖНОСТЬ И БЕСПОЛЕЗНОСТЬ ЗАКОНА)
#######################################################################################################################


def add_prefer_rule(request):
    if request.method == 'GET':
        rule_number = request.GET['rule_number']
        person = request.GET['person']
        m = Prefer(person=person, rule=rule_number)
        m.save()
        m_count = Prefer.objects.filter(rule=rule_number).count()
        return HttpResponse(m_count)


def delete_prefer_rule(request):
    if request.method == 'GET':
        rule_number = request.GET['rule_number']
        person = request.GET['person']
        Prefer.objects.filter(person=person, rule=rule_number).delete()
        m_count = Prefer.objects.filter(rule=rule_number).count()
        return HttpResponse(m_count)


def add_dislike_rule(request):
    if request.method == 'GET':
        rule_number = request.GET['rule_number']
        person = request.GET['person']
        dl = NotPrefer(person=person, rule=rule_number)
        dl.save()
        dl_count = NotPrefer.objects.filter(rule=rule_number).count()
        return HttpResponse(dl_count)


def delete_dislike_rule(request):
    if request.method == 'GET':
        rule_number = request.GET['rule_number']
        person = request.GET['person']
        NotPrefer.objects.get(person=person, rule=rule_number).delete()
        dl_count = NotPrefer.objects.filter(rule=rule_number).count()
        return HttpResponse(dl_count)

#######################################################################################################################
#                                                       КОММЕНТАРИИ
#######################################################################################################################


class AddComment(View):
    """Комментарии"""
    def post(self, request, pk):
        form = CommentForm(request.POST)
        rule = Rules.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.rule = rule       # объяснение, что такое _id приведено
            form.save()             # в https://youtu.be/OdmeEBIRf_8 в 10.48
        return redirect(rule.get_absolute_url())

##############################################################################################
#                                   ЗАПОЛНЕНИЕ ТАБЛИЦЫ ГОЛОСОВАНИЯ ДЕПУТАТОВ
##############################################################################################


def populate_vote(request):
    deputies = Deputy.objects.all()
    stroka = 'Нет законов для заполнения'
    count_populated_rules = 0
    row_vote = Rules.objects.filter(populated=False, voted=True)    # Выборка, по которым уже
    for ob in row_vote:                                       # проголосовали, но которыми
        number = ob.rule_number                               # ещё не заполнили FinalTable
        for deputy in deputies:
            if deputy.name in ob.vote_yes:
                b = FinalTable.objects.create(rule_number_final=number,
                                              name=deputy.name,
                                              fraction=deputy.party_fraction,
                                              vote_result='За')
                b.save()
            elif deputy.name in ob.vote_no:
                b = FinalTable.objects.create(rule_number_final=number,
                                              name=deputy.name,
                                              fraction=deputy.party_fraction,
                                              vote_result='Против')
                b.save()
            elif deputy.name in ob.vote_abstained:
                b = FinalTable.objects.create(rule_number_final=number,
                                              name=deputy.name,
                                              fraction=deputy.party_fraction,
                                              vote_result='Воздержался')
                b.save()
            elif deputy.name in ob.vote_not_vote:
                b = FinalTable.objects.create(rule_number_final=number,
                                              name=deputy.name,
                                              fraction=deputy.party_fraction,
                                              vote_result='Не голосовал')
                b.save()
            stroka = 'Заполнение прошло успешно'
        ob.populated = True
        ob.save()
        count_populated_rules += 1

    rules = Rules.objects.filter(populated=True, result_deputy_vote='')
    quorum = 226
    for rule in rules:
        yes_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='За').count()
        no_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Против').count()
        if (yes_count + no_count) < quorum:
            Rules.objects.filter(rule_number=rule.rule_number).update(result_deputy_vote='Отклонён')
        else:
            if yes_count > no_count:
                Rules.objects.filter(rule_number=rule.rule_number).update(result_deputy_vote='За')
            else:
                Rules.objects.filter(rule_number=rule.rule_number).update(result_deputy_vote='Против')

    context = {'stroka': stroka, 'count_populated_rules': count_populated_rules}
    return render(request, 'shabls/populate_vote.html', context)

###################################################################################################################
#                                   ЗАПОЛНЕНИЕ ТАБЛИЦЫ НАРОДНОГО ГОЛОСОВАНИЯ
###################################################################################################################


def populate_folk_vote(request):
    rules_1 = Rules.objects.filter(populated=True, populi_voted=False)
    spisok = rules_1
    count_rules = 0
    for rule in spisok:
        for i in range(444):
            b = VoxPopuli(name='bot',
                          rule_number=rule,
                          result=random.choice(['За', 'За', 'За', 'Против', 'Против', 'Против', 'Воздержался']))
            b.save()
        Rules.objects.filter(rule_number=rule.rule_number).update(populi_voted=True)
        count_rules += 1

    rules_2 = Rules.objects.filter(populi_voted=True, result_populi_vote='') # Добавить результат голосования народа в Rules
    for rule in rules_2:
        yes_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='За').count()
        no_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='Против').count()
        if yes_count > no_count:
            Rules.objects.filter(rule_number=rule.rule_number).update(result_populi_vote='За')
        else:
            Rules.objects.filter(rule_number=rule.rule_number).update(result_populi_vote='Против')
    context = {'count_rules': count_rules}
    return render(request, 'shabls/populate_folk_vote.html', context)

#######################################################################################################################
#             НАРОДНОЕ ГОЛОСОВАНИЕ (ПОЛУЧЕНИЕ ДАННЫХ ИЗ ФОРМЫ ГОЛОСОВАНИЯ НА СТРАНИЦЕ ЗАКОНА)
#######################################################################################################################


def vox_populi(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        rule = Rules.objects.get(rule_number=data['rule'])  # ссылка на текущий закон, чтобы перейти...
        new_vote = VoxPopuli(name=data['person'],
                             rule_number=data['rule'],
                             result=data['btnradio'])
        new_vote.save()
        Rules.objects.filter(rule_number=data['rule']).update(populi_voted=True)  # Ставлю флаг, что народ проголосовал
    return redirect(rule.get_absolute_url())        # после голосования обратно на страницу закона

#######################################################################################################################
#                                                   ПОИСК ЗАКОНА
#######################################################################################################################


def search_rule(request):       # вывод формы поиска
    if request.method == 'POST':
        searched = request.POST['searched']
        query = Rules.objects.filter(title__icontains=searched)
    else:
        return render(request, 'shabls/search.html')
    return render(request, 'shabls/search.html', {'search': query})


class SearchRule(APIView):      # моментальный вывод результатов поиска
    # get - в названии должно быть обязательно
    # https://stackoverflow.com/questions/57302570/detail-method-get-not-allowed-django-rest-framework

    def get(self, request):
        searched = request.GET['searched_val']
        query = Rules.objects.filter(Q(title__icontains=searched) | Q(rule_number__icontains=searched))
        serializer = RuleSerializer(query, many=True)
        return Response(serializer.data)

#######################################################################################################################
#                       ВЫВОД СПИСКА ЗАКОНОВ ДЛЯ ДОПОЛНЕНИЯ РЕЗУЛЬТАТАМИ ГОЛОСОВАНИЯ ДЕПУТАТАМИ
#######################################################################################################################

@login_required
def list_for_add_voting(request):
    rules = CheckRulesForVoting.objects.all().order_by('last_check')[:1]
    rules_count = CheckRulesForVoting.objects.all().order_by('last_check').count()
    rules_voted_not_populated_count = Rules.objects.filter(voted=True, populated=False).count()
    checks_per_day = HowManyRulesChecked.objects.filter(check_date=date.today()).count()
    context = {'rules': rules,
               'rules_count': rules_count,
               'rules_voted_not_populated_count': rules_voted_not_populated_count,
               'checks_per_day': checks_per_day,
               }
    return render(request, 'shabls/for_add_voting.html', context)

#######################################################################################################################
#               ПО ЗАКОНУ ПРОГОЛОСОВАЛИ - УДАЛИТЬ ЗАПИСЬ О ЗАКОНЕ ИЗ СПИСКА ПРОВЕРКИ (CheckRulesForVoting)
#######################################################################################################################


def delete_check_date(request):
    data = request.GET
    CheckRulesForVoting.objects.filter(rule_number=data['rule_number']).delete()
    b = HowManyRulesChecked.objects.create(check_date=date.today())     # Для подсчёта кол-ва просмотренных законов
    b.save()
    return HttpResponseRedirect(reverse('add_voting'))

#######################################################################################################################
#                               ПО ЗАКОНУ ЕЩЁ НЕ ГОЛОСОВАЛИ - ПРОДЛИТЬ СРОК ПРОВЕРКИ
#######################################################################################################################


def extend_check_date(request):                     # НА 10 ДНЕЙ
    data = request.GET
    new_date = date.today() + timedelta(days=10)
    CheckRulesForVoting.objects.filter(rule_number=data['rule_number']).update(last_check=new_date)
    b = HowManyRulesChecked.objects.create(check_date=date.today())     # Для подсчёта кол-ва просмотренных законов
    b.save()
    return HttpResponseRedirect(reverse('add_voting'))


def extend_check_date_20(request):                  # НА 20 ДНЕЙ
    data = request.GET
    new_date = date.today() + timedelta(days=20)
    CheckRulesForVoting.objects.filter(rule_number=data['rule_number']).update(last_check=new_date)
    b = HowManyRulesChecked.objects.create(check_date=date.today())     # Для подсчёта кол-ва просмотренных законов
    b.save()
    return HttpResponseRedirect(reverse('add_voting'))


def extend_check_date_60(request):                  # НА 60 ДНЕЙ
    data = request.GET
    new_date = date.today() + timedelta(days=60)
    CheckRulesForVoting.objects.filter(rule_number=data['rule_number']).update(last_check=new_date)
    b = HowManyRulesChecked.objects.create(check_date=date.today())     # Для подсчёта кол-ва просмотренных законов
    b.save()
    return HttpResponseRedirect(reverse('add_voting'))


#######################################################################################################################
#                              УСТАНОВИТЬ СТАРТОВЫЙ ПЕРИОД ПРОВЕРКИ ЗАКОНА ПОСЛЕ ЕГО РЕГИСТРАЦИИ
#######################################################################################################################


def set_start_period(request):  # Следует запускать после того, как будут добавлены новые законы в Rules
    not_set_rules = Rules.objects.filter(set_start_period=False, rejection=False)
    how_many = 0
    for rule in not_set_rules:
        set_period = rule.initialization_date + timedelta(days=20)
        b = CheckRulesForVoting(rule_number=rule.rule_number,
                                rule_idd=rule.id,
                                last_check=set_period)
        b.save()
        Rules.objects.filter(rule_number=rule.rule_number).update(set_start_period=True)
        how_many += 1
    context = {'how_many': how_many}
    return render(request, 'shabls/set_start_period_service.html', context)

#######################################################################################################################
#                           УДАЛИТЬ ВСЕ РЕЗУЛЬТАТЫ НАРОДНОГО ГОЛОСОВАНИЯ
#######################################################################################################################


def delete_vox_populi(request):
    VoxPopuli.objects.all().delete()
    return HttpResponseRedirect(reverse('get_index'))

#######################################################################################################################
#                                       ОТМЕНИТЬ ГОЛОСОВАНИЕ
#######################################################################################################################


def delete_populi_voting(request):
    if request.method == 'GET':
        name = request.GET['name']
        rule_number = request.GET['rule_number']
        VoxPopuli.objects.filter(name=name, rule_number=rule_number).delete()
    return HttpResponse()

#######################################################################################################################
#                                   ЗАПОЛНЕНИЕ ТАБЛИЦ НУЖНОСТЬ/БЕСПОЛЕЗНОСТЬ
#######################################################################################################################


def usefulness_uselesness(request):
    rules = Rules.objects.all()[:5]
    for rule in rules:
        usefulness = random.randint(1, 100)
        total = random.randint(10, 20)
        likes = int((usefulness / 100) * total)
        dislikes = total - likes
        for i in range(likes):
            m = Prefer(person='bot', rule=rule.rule_number)
            m.save()
        for i in range(dislikes):
            n = NotPrefer(person='bot', rule=rule.rule_number)
            n.save()
        print(rule.rule_number, usefulness)
    return HttpResponseRedirect(reverse('get_index'))

#######################################################################################################################
#                              УДАЛИТЬ ЛАЙКИ И ДИЗЛАЙКИ (ПОЛЕЗНОСТЬ И БЕСПОЛЕЗНОСТЬ)
#######################################################################################################################


def delete_usefulness(request):
    Prefer.objects.all().delete()
    NotPrefer.objects.all().delete()
    return HttpResponseRedirect(reverse('get_index'))

#######################################################################################################################
#               ЗАНЕСЕНИЕ ДАННЫХ ИЗ ПРОТОКОЛОВ И ИСПРАВЛЕНИЕ ДАННЫ ПРОВЕРКИ ЗАКОНА НА ТЕКУЩУЮ ДАТУ
#######################################################################################################################


def input_protocols(request):
    return render(request, 'shabls/input_protocols.html')


def protocols_view(request):
    got = request.POST['controlled']
    list_got = list(got.split(' '))
    count_rules = 0
    for i in list_got:
        if CheckRulesForVoting.objects.filter(rule_number=i):
            CheckRulesForVoting.objects.filter(rule_number=i).update(last_check='2021-05-01')
            count_rules += 1
    print('Изменено', count_rules)
    return HttpResponseRedirect(reverse('add_voting'))

#######################################################################################################################
#                                                 ДОБАВИТЬ ПОРУЧЕНИЕ
#######################################################################################################################


def addTask(request):
    if request.method == 'POST':
        deputy_name = request.POST['deputy_name']
        deputy = Deputy.objects.get(name=deputy_name)
        task_text = request.POST['task_text']
        task_author = request.POST['task_author']
        TaskForDeputy(task_author=task_author,
                      task_text=task_text,
                      task_date=date.today(),
                      deputy_name=deputy_name).save()
        return redirect(deputy.get_absolute_url())


#######################################################################################################################
#                                           ДОБАВИТЬ И УДАЛИТЬ СОГЛАСИЕ С ПОРУЧЕНИЕМ
#######################################################################################################################


def add_agree(request):
    if request.method == 'GET':
        task_id = request.GET['task_id']
        username = request.GET['username']
        TasksRating(
            task_id=task_id,
            name=username
        ).save()
        rating_count = TaskForDeputy.objects.get(id=task_id).task_rating
        rating_count += 1
        TaskForDeputy.objects.filter(id=task_id).update(task_rating=rating_count)
    return HttpResponse()


def delete_agree(request):
    if request.method == 'GET':
        task_id = request.GET['task_id']
        username = request.GET['username']
        TasksRating.objects.filter(task_id=task_id, name=username).delete()
        rating_count = TaskForDeputy.objects.get(id=task_id).task_rating
        rating_count -= 1
        TaskForDeputy.objects.filter(id=task_id).update(task_rating=rating_count)
    return HttpResponse()

#######################################################################################################################
#                                                   ПРОВЕРКА РАБОТЫ САЙТА НА VPS
#######################################################################################################################


def get_empty(request):
    return HttpResponse('привет локал')