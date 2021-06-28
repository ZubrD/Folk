$('.tasks-img').click(function () {
    let agree_status = $(this).attr('agree')
    let task_id = $(this).attr('task-id')
    let username = $(this).attr('username')
    let deputy_name = $(this).attr('deputy-name')
    let rating_count = parseInt($(this).next('.span-task-rating').text())

    if (agree_status == 'yes'){
        rating_count -= 1
        $(this).next('.span-task-rating').text(rating_count)
        $(this).attr({agree: 'no'}).removeClass('task-agree').addClass('task-default')
        $.ajax({
            type: 'GET',
            url: '/delete_agree',
            data: {
                task_id: task_id,
                username: username,
                deputy_name: deputy_name
            },
            success: function () {

            }
        })
    }
    if (agree_status == 'no') {
        rating_count += 1
        $(this).next('.span-task-rating').text(rating_count)
        $(this).attr({agree: 'yes'}).removeClass('task-default').addClass('task-agree')
        $.ajax({
            type: 'GET',
            url: '/add_agree',
            data: {
                task_id: task_id,
                username: username,
                deputy_name: deputy_name
            },
            success: function () {

            }
        })
    }
})
