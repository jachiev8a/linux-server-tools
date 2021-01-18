
var diskLineChart = document.getElementById("diskLineChart");
var diskUsageChart = document.getElementById("diskUsageChart");

Chart.defaults.global.defaultFontFamily = "sans-serif";
Chart.defaults.global.defaultFontSize = 15;

// Disk Line Chart Options
// --------------------------------------------------
var diskLineChartOptions = {
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
                /* external */
                max: maxYAxisValue,
                /* external */
                stepSize: Math.ceil( maxYAxisValue / lineChartSteps ),
                steps: lineChartSteps
            }
        }]
    }
};

// Disk Line Chart Main Instance
// --------------------------------------------------
var lineChart = new Chart(diskLineChart, {
    type: 'line',
    data: diskLineChartData,
    options: diskLineChartOptions
});
