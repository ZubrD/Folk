let ctx = document.getElementById('DeputyChart').getContext('2d');
let v_yes = parseInt($('#for-deputy-chart').attr('vyes'));
let v_no = parseInt($('#for-deputy-chart').attr('vno'));
let v_abstained = parseInt($('#for-deputy-chart').attr('vabstained'));
let v_not_vote = parseInt($('#for-deputy-chart').attr('vnotvote'));
let data = [v_yes, v_no, v_abstained, v_not_vote];
let labels = ['За', 'Против', 'Воздержались', 'Не голосовали'];

let DeputyChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: data,
            label: 'Votes',
            backgroundColor: [
                'green',
                'red',
                'lightblue',
                'gray',
            ],
            borderColor: [
                'white',
                'white',
                'white',
                'white',
            ],
            borderWidth: 2
        }]
    },
    options: {
        tooltips: {
            backgroundColor: 'white',
            bodyFontColor: 'black',
            bodyFontSize: 18,
        },
        legend: {
            display: false,
        },
        scales: {
                //Убрал оси YAxis
        },
    }
});
