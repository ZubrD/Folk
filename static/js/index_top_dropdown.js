
$('#drop1').click(function (){
    $('#dropdownMenuLink').text('Новые законопроекты')
    $('#drop1-new-rule').removeAttr('hidden').show()
    $('#drop2-new-voted').hide()
    $('#drop3-deputy-task').hide()
    $('#drop4-deputy-answer').hide()
    $('#drop5-popular').hide()
    $('#drop6-useful').hide()
    $('#drop7-needless').hide()
})

$('#drop2').click(function (){
    $('#dropdownMenuLink').text('Недавно проголосовали')
    $('#drop1-new-rule').hide()
    $('#drop2-new-voted').removeAttr('hidden').show()
    $('#drop3-deputy-task').hide()
    $('#drop4-deputy-answer').hide()
    $('#drop5-popular').hide()
    $('#drop6-useful').hide()
    $('#drop7-needless').hide()
})

$('#drop3').click(function (){
    $('#dropdownMenuLink').text('Поручения депутатам')
    $('#drop1-new-rule').hide()
    $('#drop2-new-voted').hide()
    $('#drop3-deputy-task').removeAttr('hidden').show()
    $('#drop4-deputy-answer').hide()
    $('#drop5-popular').hide()
    $('#drop6-useful').hide()
    $('#drop7-needless').hide()
})

$('#drop4').click(function (){
    $('#dropdownMenuLink').text('Ответы депутатов')
    $('#drop1-new-rule').hide()
    $('#drop2-new-voted').hide()
    $('#drop3-deputy-task').hide()
    $('#drop4-deputy-answer').removeAttr('hidden').show()
    $('#drop5-popular').hide()
    $('#drop6-useful').hide()
    $('#drop7-needless').hide()
})

$('#drop5').click(function (){
    $('#dropdownMenuLink').text('Самые популярные законы')
    $('#drop1-new-rule').hide()
    $('#drop2-new-voted').hide()
    $('#drop3-deputy-task').hide()
    $('#drop4-deputy-answer').hide()
    $('#drop5-popular').removeAttr('hidden').show()
    $('#drop6-useful').hide()
    $('#drop7-needless').hide()
})

$('#drop6').click(function (){
    $('#dropdownMenuLink').text('Самые полезные законы')
    $('#drop1-new-rule').hide()
    $('#drop2-new-voted').hide()
    $('#drop3-deputy-task').hide()
    $('#drop4-deputy-answer').hide()
    $('#drop5-popular').hide()
    $('#drop6-useful').removeAttr('hidden').show()
    $('#drop7-needless').hide()
})

$('#drop7').click(function (){
    $('#dropdownMenuLink').text('Самые ненужные законы')
    $('#drop1-new-rule').hide()
    $('#drop2-new-voted').hide()
    $('#drop3-deputy-task').hide()
    $('#drop4-deputy-answer').hide()
    $('#drop5-popular').hide()
    $('#drop6-useful').hide()
    $('#drop7-needless').removeAttr('hidden').show()
})