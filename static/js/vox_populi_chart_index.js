let c_p = document.getElementById('VoxPopuliChart').getContext('2d');
let p_yes = parseInt($('#for-populi-chart').attr('pyes'));
let p_no = parseInt($('#for-populi-chart').attr('pno'));
let p_abstained = parseInt($('#for-populi-chart').attr('pabstained'));
let p_data = [p_yes, p_no, p_abstained]
let p_labels = ['За', 'Против', 'Воздержались'];

let VoxPopuliChart = new Chart(c_p, {
    type: 'pie',
    data: {
        labels: p_labels,
        datasets: [{
            label: '# of Votes',
            data: p_data,
            backgroundColor: [
                'green',
                'red',
                'lightblue',
            ],
            borderColor: [
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
                // Убрал оси YAxis
        }
    }
});