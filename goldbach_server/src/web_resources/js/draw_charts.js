// Default chart conf
Chart.defaults.global.defaultFontColor = '#fff'
Chart.defaults.global.elements.line.borderWidth = 1
Chart.defaults.global.elements.rectangle.borderWidth = 1
Chart.defaults.scale.gridLines.color = '#444'
Chart.defaults.scale.ticks.display = false

const options = {
    legend: {
        display: false
    },
    scales: {
        yAxes: [{
            gridLines: {
                display: false
            },
            ticks: {
                min: 0,
                max: 100,
                stepSize: 10,
                display: true,
            }
        }]
    }
}
let charts = []
// Default chart conf

async function loadData(){
    //TODO update address
    const response = await fetch('http://172.30.56.252:8001/cpu_status')
    const data = await response.json();
    return data
}

document.addEventListener("DOMContentLoaded", async () => {
    let fetched_data = new Map();
    let first_time = true;
    while (true) {
        try {
            fetched_data = await loadData();
        } catch (error) {
            alert("Error fetching from api")
            break; 
        }
        first_time = initChartSection(first_time, fetched_data);
        document.body.classList.add('running');
        for (let index = 0; index < fetched_data.length; index++) {
            let ip_id = 'worker_'+String(index)
            document.getElementById(ip_id).innerHTML = fetched_data[index].ip
            updateChart(charts[index], fetched_data[index].value);
        }
    }
});

function createChartSection(index, chart_id){
    let ip_id = 'worker_'+String(index);
    let canva_id = '<canvas id= '+chart_id+'></canvas>'
    let canva_space = '<figure> <h4>Usage percentage per thread</h4><h3 id = '+ip_id+'>IP: </h3>'+canva_id+'</figure>'
    const elemH1 = document.createElement("H4")
    elemH1.innerHTML = canva_space
    const $container = document.getElementById("chart_section")
    $container.append(elemH1)
};

function getNewChartData(cpu_usage){
    const styles = {
        color: {
            solids: ['rgba(116, 72, 194, 1)', 'rgba(33, 192, 215, 1)', 'rgba(217, 158, 43, 1)', 'rgba(205, 58, 129, 1)', 'rgba(156, 153, 204, 1)', 'rgba(225, 78, 202, 1)'],

            alphas: ['rgba(116, 72, 194, .2)', 'rgba(33, 192, 215, .2)', 'rgba(217, 158, 43, .2)', 'rgba(205, 58, 129, .2)', 'rgba(156, 153, 204, .2)', 'rgba(225, 78, 202, .2)']
        }             ,              
    }
    let alphas = getColorsArray(cpu_usage, styles.color.alphas);
    let solids = getColorsArray(cpu_usage, styles.color.solids);

    let data = {
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: alphas,
            borderColor: solids
        }]
    }
    return data;
};

function getColorsArray(cpu_usage, colors){
    let result = [];
    let result_index = 0;
    for (var j = 0; j < cpu_usage.length; j++) {
        if (result_index == colors.length) {
            result_index = 0;
        }
        let color = colors[result_index]
        result.push(color);
        result_index += 1;
    }
    return result;
};

function initChartSection(first_time, fetched_data) {
    let flag = false;
    if (first_time) {
        for (let index = 0; index < fetched_data.length; index++) {
            let chart_id = 'chart_'+String(index);
            createChartSection(index, chart_id);
            let cpu_usage = fetched_data[index].value;
            let data = getNewChartData(cpu_usage);
            let new_chart = new Chart(document.getElementById(chart_id), { type: 'bar', data, options });
            charts.push(new_chart);
        }
    }
    return flag;
};

function updateChart(chart, cpu_usage) {
    for (let index = 0; index < cpu_usage.length; index++) {
        const tag = "Thread "+index;
        chart.config.data.labels[index] = tag;
        const cpu_info = cpu_usage[index];
        chart.config.data.datasets[0].data[index] = cpu_info;
        chart.update();
    }
};