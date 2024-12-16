// Initialize charts
function initializeCharts() {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'hour',
                    displayFormats: {
                        hour: 'HH:mm'
                    }
                }
            },
            y: {
                beginAtZero: true
            }
        }
    };

    // Line 1 Chart
    const line1Ctx = document.getElementById('line1-chart').getContext('2d');
    const line1Chart = new Chart(line1Ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Parts/Hour',
                    borderColor: 'rgb(54, 162, 235)',
                    data: []
                },
                {
                    label: 'Total Quantity',
                    borderColor: 'rgb(75, 192, 192)',
                    data: []
                }
            ]
        },
        options: commonOptions
    });

    // Line 2 Chart
    const line2Ctx = document.getElementById('line2-chart').getContext('2d');
    const line2Chart = new Chart(line2Ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Parts/Hour',
                    borderColor: 'rgb(54, 162, 235)',
                    data: []
                },
                {
                    label: 'Total Quantity',
                    borderColor: 'rgb(75, 192, 192)',
                    data: []
                }
            ]
        },
        options: commonOptions
    });

    return { line1Chart, line2Chart };
}

// Update production data
function updateProductionData() {
    fetch('/production_data')
        .then(response => response.json())
        .then(data => {
            // Update line 1 data
            document.getElementById('program-1').textContent = data.line1_part.program;
            document.getElementById('part-number-1').textContent = data.line1_part.number;
            document.getElementById('part-description-1').textContent = data.line1_part.description;
            document.getElementById('quantity-1').textContent = data.line1_production.quantity;
            document.getElementById('delta-1').textContent = data.line1_production.delta;
            document.getElementById('scrap-1').textContent = data.line1_scrap.total;
            document.getElementById('scrap-rate-1').textContent = data.line1_scrap.rate + '%';

            // Update line 2 data
            document.getElementById('program-2').textContent = data.line2_part.program;
            document.getElementById('part-number-2').textContent = data.line2_part.number;
            document.getElementById('part-description-2').textContent = data.line2_part.description;
            document.getElementById('quantity-2').textContent = data.line2_production.quantity;
            document.getElementById('delta-2').textContent = data.line2_production.delta;
            document.getElementById('scrap-2').textContent = data.line2_scrap.total;
            document.getElementById('scrap-rate-2').textContent = data.line2_scrap.rate + '%';

            // Update totals
            document.getElementById('total-quantity').textContent = data.total_quantity;
            document.getElementById('total-delta').textContent = data.total_delta;
            document.getElementById('total-scrap').textContent = data.total_scrap;
            document.getElementById('average-scrap-rate').textContent = data.average_scrap_rate + '%';

            // Update last refresh time
            document.getElementById('last-refresh').textContent = data.current_time;
        })
        .catch(error => {
            console.error('Error updating production data:', error);
        });
}

// Handle video upload
document.getElementById('video-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('video', file);

        fetch('/upload_video', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Video uploaded successfully');
            } else {
                console.error('Error uploading video:', data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

// Initialize application
const charts = initializeCharts();

// Update production data every second
setInterval(updateProductionData, 1000);

// Initial update
updateProductionData();