
var diskLineChart = document.getElementById("diskLineChart");
var diskUsageChart = document.getElementById("diskUsageChart");

Chart.defaults.global.defaultFontFamily = "sans-serif";
Chart.defaults.global.defaultFontSize = 15;

// Disk Line Chart Data
// --------------------------------------------------
var diskLineChartData = {
    /* external */
    labels: lineLabelsData,
    datasets: [
        {
            /* external */
            label: lineDatasetName,
            backgroundColor: "rgba(151, 187, 205, 0.2)",
            borderColor: "rgba(151, 187, 205, 1)",

            pointBackgroundColor: "rgba(151, 187, 205, 1)",
            pointBorderColor: "#fff",

            pointHoverBackgroundColor: "rgba(151, 187, 205, 1)",
            pointHoverBorderColor: "#fff",

            borderWidth: 4,
            /* external */
            data: lineDatasetData
        }
    ]
};

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

// Disk Current Usage Chart Data
// --------------------------------------------------
var diskUsageChartData = {
    labels: diskUsageLabelsData,
    datasets: [
        {
            label: 'Current',

            backgroundColor: "rgba(38, 194, 129, 1)",
            borderColor: "rgba(38, 194, 129, 1)",

            data: diskUsageDatasetData
        },
        {
            label: 'Total',

            backgroundColor: "rgba(151, 187, 205, 0.2)",
            borderColor: "rgba(151, 187, 205, 1)",

            data: diskTotalDatasetData
        }
    ]
};

// Disk Current Usage Chart Options
// --------------------------------------------------
var diskUsageChartOptions = {
    responsive: false,
    title: {
        display: true,
        text: 'Disk Usage Chart'
    },
    scales: {
        xAxes: [{
            display: true,
            stacked: true,
            scaleLabel: {
                display: true,
                labelString: 'Disk Size (GB)'
            }
        }],
        yAxes: [{
            display: true,
            stacked: true,
            scaleLabel: {
                display: true,
                labelString: 'Total Disk Size (GB)'
            },
            ticks: {
                min: 0,
                /* external */
                max: maxDiskUsage,
                /* external */
                stepSize: Math.ceil( maxDiskUsage / diskUsageSteps ),
                steps: diskUsageSteps
            }
        }]
    }
};

// Disk Current Usage Chart Main Instance
// --------------------------------------------------
var usageChart = new Chart(diskUsageChart, {
    type: 'bar',
    data: diskUsageChartData,
    options: diskUsageChartOptions
});
