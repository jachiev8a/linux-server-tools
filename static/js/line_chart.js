
var diskChart = document.getElementById("diskChart");

Chart.defaults.global.defaultFontFamily = "sans-serif";
Chart.defaults.global.defaultFontSize = 15;

// Disk Chart Data
// --------------------------------------------------
var diskChartData = {
    labels: [
        {% for item in labels %}
            "{{ item }}",
        {% endfor %}
    ],
    datasets: [
        {
            label: "{{ dataset_name }}",
            backgroundColor: "rgba(151, 187, 205, 0.2)",
            borderColor: "rgba(151, 187, 205, 1)",

            pointBackgroundColor: "rgba(151, 187, 205, 1)",
            pointBorderColor: "#fff",

            pointHoverBackgroundColor: "rgba(151, 187, 205, 1)",
            pointHoverBorderColor: "#fff",

            borderWidth: 4,
            data: [
                {% for item in values %}
                    {{ item }},
                {% endfor %}
            ]
        }
    ]
};

var maxYAxisValue = {{ max }}
var steps = 11

// Disk Chart Options
// --------------------------------------------------
var diskChartOptions = {
    responsive: false,
    title: {
        display: true,
        text: 'Disk Space Line Chart'
    },
    tooltips: {
        mode: 'index',
        intersect: false,
    },
    hover: {
        mode: 'nearest',
        intersect: true
    },
    scales: {
        xAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: 'Current Data Size (GB)'
            }
        }],
        yAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: 'Total Size (GB)'
            },
            ticks: {
                min: 0,
                max: maxYAxisValue,
                stepSize: Math.ceil( maxYAxisValue / steps ),
                steps: steps
            }
        }]
    }
};

var lineChart = new Chart(diskChart, {
    type: 'line',
    data: diskChartData,
    options: diskChartOptions
});
