// Chart for Expenses in Dashboard
var ctx = document.getElementById('expenseChart').getContext('2d');
var expenseChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Food', 'Transport', 'Utilities', 'Others'],
        datasets: [{
            label: 'Expense Categories',
            data: [200, 150, 100, 50], // Replace with actual data
            backgroundColor: ['#ff5733', '#33c1ff', '#33ff57', '#ff33ab']
        }]
    }
});

// Chart for Report Generation (can be monthly/yearly)
var ctxReport = document.getElementById('reportChart').getContext('2d');
var reportChart = new Chart(ctxReport, {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April'], // Replace with months or custom labels
        datasets: [{
            label: 'Monthly Expenses',
            data: [300, 500, 200, 400], // Replace with actual data
            backgroundColor: '#4caf50'
        }]
    }
});
