let ctx = document.getElementById('DeputyChart').getContext('2d');
let v_yes = parseInt($('#v-yes').attr('result'));
let v_no = parseInt($('#v-no').attr('result'));
let v_abstained = parseInt($('#v-abstained').attr('result'));
let v_not_vote = parseInt($('#v-not-vote').attr('result'));
let v_total = v_yes + v_no + v_abstained + v_not_vote;
let DeputyChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            label: '# of Votes',
            data: [v_yes, v_no, v_abstained, v_not_vote],
            fontSize: '300',
            backgroundColor: [
                'green',
                'red',
                'lightblue',
                'gray',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
            ],
            borderWidth: 10
        }]
    },
    options: {
        legend: {
            position: 'right',
            labels: {
              fontSize: 10,
              fontColor: ['green', 'red', 'blue', 'gray']
          }
        },
        scales: {
                //Убрал оси YAxis
        }
    },

});
