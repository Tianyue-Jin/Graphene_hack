document.addEventListener('DOMContentLoaded', function () {
    console.log('load js');

    // Function to update the chart with new data
    function updateChart(chart, data1, data2) {
        chart.data.datasets[0].data = data1;
        chart.data.datasets[1].data = data2;

        chart.update();
    }

    // Function to simulate receiving data
    function receiveData() {
        const newData1 = generateRandomData(10);
        const newData2 = generateRandomData(10);

        updateChart(lineChart, newData1, newData2);
    }

    // Function to generate an array of random numbers
    function generateRandomData(length) {
        return Array.from({ length }, () => Math.floor(Math.random() * 100));
    }

    // Create the initial chart
    const lineChart = new Chart(document.getElementById("line-chart"), {
        type: 'line',
        data: {
            labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            datasets: [
                {
                    data: generateRandomData(10),
                    label: "Test fabric_1",
                    borderColor: "#3e95cd",
                    fill: false
                },
                {
                    data: generateRandomData(10),
                    label: "Test_fabric_2",
                    borderColor: "#8e5ea2",
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                },
                y: {
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        display: true,
                        labelString: 'Voltage'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Real Time data'
                }
            }
        }
    });

    // Set up an interval to simulate receiving data every second
    setInterval(() => {
        receiveData();
    }, 1000);
});
