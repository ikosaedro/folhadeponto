function PlotarGraficoDeBarras(grafico, eixoX, eixoY) {
    const ctx = obterElemento(grafico).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: eixoX,
            datasets: [{
                label: 'Servidores por Setor',
                data: eixoY,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                    '#9966FF', '#FF9F40', '#E7E9ED'
                ],
                borderColor: '#fff',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'x',
            scales: {
                y: {
                    ticks: {
                        display: false
                    },
                    grid: {
                        display: false
                    },
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantidade de Servidores'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                datalabels: {
                    anchor: 'end',
                    align: 'start',
                    color: '#000',
                    font: {
                        weight: 'bold'
                    },
                    formatter: function (value) {
                        return value;
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    })
}

const graficos = {};

function PlotarGraficoDePizza(grafico, rotulos, valores) {

    const ctx = obterElemento(grafico).getContext('2d');

    if (graficos[grafico]) {
        graficos[grafico].destroy();
    }

   graficos[grafico] = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: rotulos,
            datasets: [{
                label: 'Servidores por Setor',
                data: valores,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#E7E9ED'
                ],
                borderColor: '#fff',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            size: 8
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw;
                            return `${label}: ${value} servidores`;
                        }
                    }
                },
                datalabels: {
                    color: 'white',
                    font: {
                        weight: 'bold',
                        size: 12
                    },
                    formatter: function (value, context) {
                        return value;
                    }
                }
            }
        },
        plugins: [ChartDataLabels] // Ativa o plugin
    });
}
