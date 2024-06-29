document.addEventListener('DOMContentLoaded', (event) => {
    console.log(tiposCancer); // Verificar se os dados foram recebidos corretamente
    console.log(contagens); // Verificar se as contagens foram recebidas corretamente

    // Criando o gráfico com Chart.js
    const ctx = document.getElementById('myChart').getContext('2d');

    const myChart = new Chart(ctx, {
        type: 'bar', // ou 'line', 'pie', etc.
        data: {
            labels: tiposCancer,
            datasets: [{
                label: 'Tipos de câncer mais atendidos',
                data: contagens,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
