// Styles colors
const styles = {
    color: {
        solids: ['rgba(116, 72, 194, 1)', 'rgba(33, 192, 215, 1)', 'rgba(217, 158, 43, 1)', 'rgba(205, 58, 129, 1)', 'rgba(156, 153, 204, 1)', 'rgba(225, 78, 202, 1)'],

        alphas: ['rgba(116, 72, 194, .2)', 'rgba(33, 192, 215, .2)', 'rgba(217, 158, 43, .2)', 'rgba(205, 58, 129, .2)', 'rgba(156, 153, 204, .2)', 'rgba(225, 78, 202, .2)']
    }             ,                                                                                  
}

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

// TODO Create n chars replace (INDEX)
// let (CHART_ID) = new Chart(document.getElementById((CHART_CANVA)), { type: 'bar', data, options });
let charts = []

async function loadData(){
    //TODO update address
    const response = await fetch('http://192.168.0.3:8001/cpu_status')
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
        // create fetched_data.length charts in array
        if (first_time) {
            for (let index = 0; index < fetched_data.length; index++) {
                let chartID = 'chart_'+String(index);
                let ip_id = 'worker_'+String(index);
                let canva_id = '<canvas id= '+chartID+'></canvas>'
                let canva_space = '<figure> <h4>Usage percentage per thread</h4><h3 id = '+ip_id+'>IP: </h3>'+canva_id+'</figure>'
                const elemH1 = document.createElement("H4")
                elemH1.innerHTML = canva_space
                const $container = document.getElementById("chart_section")
                $container.append(elemH1)
                let cpu_usage = fetched_data[index].value
                let alphas = [];
                let alpha_index = 0;
                for (var i = 0; i < cpu_usage.length; i++) {
                    if (alpha_index == styles.color.alphas.length) {
                        alpha_index = 0;
                    }
                    color = styles.color.alphas[alpha_index]
                    alphas.push(color);
                    alpha_index += 1;
                }
                // data.datasets.backgroundColor = alphas;

                let solids = [];
                let solid_index = 0;
                for (var j = 0; j < cpu_usage.length; j++) {
                    if (solid_index == styles.color.solids.length) {
                        solid_index = 0;
                    }
                    color = styles.color.solids[solid_index]
                    solids.push(color);
                    solid_index += 1;
                }
                // data.datasets.borderColor = solids;

                let data = {
                    labels: [],
                    datasets: [{
                        data: [],
                        backgroundColor: alphas,
                        borderColor: solids
                    }]
                }
                
            
                let new_chart = new Chart(document.getElementById(chartID), { type: 'bar', data, options });
                charts.push(new_chart);
            }
            first_time = false
        }

        // TODO update chart ip
        document.body.classList.add('running');
        // update charts with data
        for (let index = 0; index < fetched_data.length; index++) {
            let ip_id = 'worker_'+String(index)
            document.getElementById(ip_id).innerHTML = fetched_data[index].ip
            updateChart(charts[index], fetched_data[index].value);
        }
    }
});

function updateChart(chart, cpu_usage) {
    console.log(chart)
    let tags = [];
    for (var index = 0; index < cpu_usage.length; index++) {
        tags.push("Thread "+index);
    }

    for (let index = 0; index < tags.length; index++) {
        const element = tags[index];
        chart.config.data.labels[index] = element;
        chart.update();
    }
    for (let index = 0; index < cpu_usage.length; index++) {
        const element = cpu_usage[index];
        chart.config.data.datasets[0].data[index] = element;
        chart.update();
    }
};