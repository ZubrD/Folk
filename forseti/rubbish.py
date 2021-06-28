#############################################################################################
#############################################################################################
# Лайки - надо удалить

# def set_likes(request):
#     if request.method == 'GET':
#         rule_id = request.GET['rule_id']
#         rule = Rules.objects.get(id=int(rule_id))
#         if rule:
#             likes = rule.likes + 1
#             rule.likes = likes
#             rule.save()
#     return HttpResponse(likes)
#
#
# def set_dislikes(request):
#     if request.method == 'GET':
#         rule_id = request.GET['rule_id']
#         rule = Rules.objects.get(id=int(rule_id))
#         if rule:
#             dislikes = rule.dislikes + 1
#             rule.dislikes = dislikes
#             rule.save()
#     return HttpResponse(dislikes)

# $('#likes').click(function()
# {
#     ruleid = $(this).attr('rule-id')
# $.get('/url_likes', {rule_id: ruleid}, function(data)
# {
# $('#span-likes').html(data)
# })
# })
#
# $('#dislikes').click(function()
# {
#     ruleid = $(this).attr('rule-id')
# $.get('/url_dislikes', {rule_id: ruleid}, function(data)
# {
# $('#span-dislikes').html(data)
# })
# })

#######################################################################################################
#                                           ИЗ МОДЕЛИ RULES
#######################################################################################################


# vote_yes = models.ManyToManyField(Deputy, limit_choices_to={'current_squad': True}, related_name='v_yes')
# vote_no = models.ManyToManyField(Deputy, limit_choices_to={'current_squad': True}, related_name='v_no',
#                                  default=get_all_deputy)  # По умолчанию выбираю всех депутатов
# abstained = models.ManyToManyField(Deputy, limit_choices_to={'current_squad': True}, related_name='v_abstained')

########################################################################################################
#                                           ИЗ urlpatterns (urls.py)
########################################################################################################


# path('deputy/', views.DeputyView.as_view(), name='deputy'),
# path('post/', views.post_index, name='post_index'),  # index view at /
# path('likepost/', views.likePost, name='likepost'),  # likepost view at /likepost/1
# path('url_likes/', views.set_likes, name='url_likes'),
# path('url_dislikes/', views.set_dislikes, name='url_dislikes'),
# path('chart/', views.test_chart, name='test_chart'),


##################################################################################################
#                                           РЕГИСТРАЦИЯ
##################################################################################################
#
#
# def register(request):
#     # Булево значение для описания шаблона была ли регистрация успешной.
#     # Сначала установите False. Код меняет значение на True, когда регистрация прошла успешно
#     registered = False
#
#     # Если это HTTP POST, обрабатываю данные формы.
#     if request.method == 'POST':
#         # Попытка получить информацию из необработанной информации формы.
#         # Обратите внимание, что мы используем как UserForm, так и UserProfileForm.
#         user_form = UserForm(data=request.POST)
#
#         # Если форма действительна ...
#         if user_form.is_valid() :
#             # Сохранить данные формы пользователя в базу данных.
#             user = user_form.save()
#
#             # Теперь хэширую пароль с помощью метода set_password,
#             # после хеширования можно обновить объект user.
#             user.set_password(user.password)
#             user.save()
#
#             # Теперь экземпляр UserProfile.
#             # Так как нужно самому установить атрибут пользователя, устанавливаем commit = False.
#             # Это задерживает сохранение модели до тех пор (проверка целостности)
#
#             # Обновляю переменную, чтобы указать, что регистрация шаблона прошла успешно.
#             registered = True
#         else:
#             # Неправильная форма или формы - ошибки или что-то еще?
#             # Проблемы с печатью в терминале.
#             print(user_form.errors,)
#     else:
#         # Не HTTP POST, поэтому визуализирую форму, используя два экземпляра ModelForm.
#         # Эти формы будут пустыми, готовыми для ввода пользователем.
#         user_form = UserForm()
#
#     # Визуализировать шаблон в зависимости от контекста.
#     return render(request,
#                   'shabls/register.html',
#                   {'user_form': user_form,
#                    'registered': registered})

#############################################################################################
#                                       ПРИМЕР ЛАЙКОВ
#############################################################################################
# Пример лайков


# def post_index(request):
#     posts = Post.objects.all()
#     return render(request, 'post/post_index.html', {'posts': posts})
#
#
# def likePost(request):
#     if request.method == 'GET':
#         post_id = request.GET['post_id']
#         likedpost = Post.objects.get(pk=post_id)
#         m = Like(post=likedpost)
#         m.save()
#         return HttpResponse("Success!")
#     else:
#         return HttpResponse("Request method is not a GET")

##############################################################################################
#                                   ЗАПОЛНЕНИЕ ТАБЛИЦЫ ГОЛОСОВАНИЯ ДЕПУТАТОВ
##############################################################################################


# def populate_vote_1(request):
#     deputies = DeputyTest.objects.all()
#     row_vote = RowVote.objects.get(rule_number_test='1039149-6')
#     number = row_vote.rule_number_test
#     if not row_vote.populated:
#         for deputy in deputies:
#             if deputy.name in row_vote.yes_test:
#                 b = FinalTable.objects.create(rule_number_final=number,
#                                           name=deputy.name,
#                                           vote_result='За')
#                 b.save()
#             elif deputy.name in row_vote.no_test:
#                 b = FinalTable.objects.create(rule_number_final=number,
#                                           name=deputy.name,
#                                           vote_result='Против')
#                 b.save()
#             elif deputy.name in row_vote.abstained_test:
#                 b = FinalTable.objects.create(rule_number_final=number,
#                                           name=deputy.name,
#                                           vote_result='Воздержался')
#                 b.save()
#             elif deputy.name in row_vote.not_vote_test:
#                 b = FinalTable.objects.create(rule_number_final=number,
#                                           name=deputy.name,
#                                           vote_result='Не голосовал')
#                 b.save()
#         context = {'stroka': 'Success'}
#     else:
#         context = {'stroka': 'Нет законов для заполнения'}
#     row_vote.populated = True
#     row_vote.save()
#
#     return render(request, 'shabls/populate_vote.html', context)

#####################################################################################################
#                                   ПРЕЖНЯЯ ГЛАВНАЯ СТРАНИЦА
#####################################################################################################
#
#
# def get_old_index(request):
#     response = render(request, 'shabls/old_index.html')
#     # visits_templ = visitor_cookie_handler(request, response)    # получаю количество просмотров
#     visitor_cookie_handler(request)
#     visits_templ = request.session['visits']    # получаю количество просмотров
#
#     context = {'visits': visits_templ}
#     response = render(request, 'shabls/old_index.html', context)
#     # visitor_cookie_handler(request, response)
#
#     return response
#
#
# def get_regions(request):
#     regions = FederalRegion.objects.all()
#     context = {'regions': regions}
#     return render(request, 'shabls/regions.html', context)
#
#
# def excluded_deputy(request):
#     """Список экс-депутатов"""
#     excluded = Deputy.objects.filter(current_squad=False)
#     context = {'exdeputy': excluded}
#     return render(request, 'shabls/exdeputy.html', context)
#
#
# def searchDeputy(request):
#     searched_region = 'Курская'
#     deputy = Deputy.objects.filter(region__search=searched_region)
#     context = {'deputy_name': deputy, 'searched_region': searched_region}
#     return render(request, 'shabls/s_dep.html', context)
#


###################################################################################################
#                          ЗАПОЛНЕНИЕ ПОЛЯ ФАМИЛИИ С ИНИЦИАЛАМА
###################################################################################################


# def populate_short_name(request):
#     authors = Deputy.objects.filter(short_name='')
#     for author in authors:
#         author_array = author.name.split()
#         famil = author_array[0]
#         first_letter = author_array[1][:1]
#         second_letter = author_array[2][:1]
#         short_name = first_letter + '.' +second_letter + '.' + famil
#         Deputy.objects.filter(name=author.name).update(short_name=short_name)
#     return render(request, 'shabls/short_name_service.html')

#######################################################################################################################
#                             ДОПОЛНИТЬ РЕЗУЛЬТАТАМИ ГОЛОСОВАНИЯ ДЕПУТАТОВ ТАБЛИЦУ RULES
#######################################################################################################################
#
#
# def add_deputy_result(request):
#     rules = Rules.objects.filter(populated=True)
#     quorum = 226
#     for rule in rules:
#         yes_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='За').count()
#         no_count = FinalTable.objects.filter(rule_number_final=rule.rule_number, vote_result='Против').count()
#         if (yes_count + no_count) < quorum:
#             Rules.objects.filter(rule_number=rule.rule_number).update(result_deputy_vote='Отклонён')
#         else:
#             if yes_count > no_count:
#                 Rules.objects.filter(rule_number=rule.rule_number).update(result_deputy_vote='За')
#             else:
#                 Rules.objects.filter(rule_number=rule.rule_number).update(result_deputy_vote='Против')
#     return HttpResponseRedirect(reverse('get_index'))

#######################################################################################################################
#                           ДОПОЛНИТЬ РЕЗУЛЬТАТАМИ ГОЛОСОВАНИЯ НАРОДА ТАБЛИЦУ RULES
#######################################################################################################################


# def add_populi_result(request):
#     rules = Rules.objects.filter(populi_voted=True)
#     for rule in rules:
#         yes_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='За').count()
#         no_count = VoxPopuli.objects.filter(rule_number=rule.rule_number, result='Против').count()
#         if yes_count > no_count:
#             Rules.objects.filter(rule_number=rule.rule_number).update(result_populi_vote='За')
#         else:
#             Rules.objects.filter(rule_number=rule.rule_number).update(result_populi_vote='Против')
#     return HttpResponseRedirect(reverse('get_index'))

################################################################################################
#                                       КОЛИЧЕСТВО ПРОСМОТРОВ
################################################################################################


# def get_server_side_cookie(request, cookie, default_val=None):
#     val = request.session.get(cookie)
#     if not val:
#         val = default_val
#     return val
#
#
# def visitor_cookie_handler(request):
#     # visits = int(request.COOKIES.get('visits', '1'))
#     visits = int(get_server_side_cookie(request, 'visits', '1'))
#     # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#     last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
#
#     if (datetime.now() - last_visit_time).seconds > 0:
#         visits = visits + 1
#         # response.set_cookie('last_visit', str(datetime.now()))
#         request.session['last_visit'] = str(datetime.now())
#     else:
#         # response.set_cookie('last_visit', last_visit_cookie)
#         # response.set_cookie('visits', visits)
#         request.session['last_visit'] = last_visit_cookie
#     # response.set_cookie('visits', visits)
#     request.session['visits'] = visits
#     return visits

##################################################################
#           ЗАПОЛНИТЬ ПРОВЕРКУ ГОЛОСОВАНИЯ И УДАЛИТЬ ЭТОТ СКРИПТ
##################################################################

# def c12(request):
#     rules_not_checked = Rules.objects.all().filter(rejection=True)
#     for rule in rules_not_checked:
#         new_record = CheckRulesForVoting(rule_number=rule.rule_number,
#                                          rule_idd=rule.id,
#                                          last_check=date.today(),
#                                         )
#         new_record.save()
#     return render(request, 'shabls/for_add_voting.html')