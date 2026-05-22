// MoodLens Dashboard JavaScript
// Purpose: Renders mood trend chart and mood breakdown chart
// Chart.js Reference: Chart.js Contributors (2023) Chart.js Documentation.
// Available at: https://www.chartjs.org/docs/ (Accessed: 16 May 2026)

function renderMoodChart(labels, scores) {
    const canvas = document.getElementById('moodChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mood Score',
                data: scores,
                borderColor: '#4a90d9',
                backgroundColor: 'rgba(74, 144, 217, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#4a90d9',
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: 'top' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let score = context.parsed.y;
                            let label = score >= 0.05 ? 'Positive' :
                                        score <= -0.05 ? 'Negative' : 'Neutral';
                            return 'Score: ' + score + ' (' + label + ')';
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: -1,
                    max: 1,
                    title: { display: true, text: 'Sentiment Score' },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: { grid: { color: 'rgba(0,0,0,0.05)' } }
            }
        }
    });
}

function renderBreakdownChart(positive, negative, neutral) {
    const canvas = document.getElementById('breakdownChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [positive, negative, neutral],
                backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let total = context.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = total > 0 ? Math.round((context.parsed / total) * 100) : 0;
                            return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

// Date filter function
function filterEntries() {
    const fromDate = document.getElementById('fromDate').value;
    const toDate = document.getElementById('toDate').value;
    const rows = document.querySelectorAll('.entry-row');

    rows.forEach(function(row) {
        const rowDate = row.getAttribute('data-date');
        let show = true;
        if (fromDate && rowDate < fromDate) show = false;
        if (toDate && rowDate > toDate) show = false;
        row.style.display = show ? '' : 'none';
    });
}

function clearFilter() {
    document.getElementById('fromDate').value = '';
    document.getElementById('toDate').value = '';
    document.querySelectorAll('.entry-row').forEach(function(row) {
        row.style.display = '';
    });
}

// Auto dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() { alert.remove(); }, 500);
        });
    }, 4000);
});