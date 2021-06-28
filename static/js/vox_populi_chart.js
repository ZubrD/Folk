let c_p = document.getElementById('VoxPopuliChart').getContext('2d');
let p_yes = parseInt($('#p-yes').attr('result'));
let p_no = parseInt($('#p-no').attr('result'));
let p_abstained = parseInt($('#p-abstained').attr('result'));
let p_total = p_yes + p_no + p_abstained;
let VoxPopuliChart = new Chart(c_p, {
    type: 'pie',
    data: {
        datasets: [{
            label: '# of Votes',
            data: [p_yes, p_no, p_abstained],
            fontSize: '300',
            backgroundColor: [
                'green',
                'red',
                'lightblue',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 10
        }]
    },
    options: {
        legend: {
            position: 'right',
            labels: {
              fontSize: 60,
              fontColor: ['green', 'red', 'blue']
          }
        },
        scales: {
                // Убрал оси YAxis
        }
    }
});