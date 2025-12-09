// Overtime Analysis Platform - Frontend JavaScript

let monthChart = null;
let dailyChart = null;
let topEmployeesChart = null;

// Initialize upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#764ba2';
        uploadArea.style.background = '#f0f2ff';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = '#f8f9ff';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = '#f8f9ff';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileUpload(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
});

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.className = 'status-message';
    statusDiv.textContent = 'Uploading and processing file...';
    statusDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            statusDiv.className = 'status-message success';
            statusDiv.textContent = `File processed successfully! ${data.records} records loaded.`;
            
            // Load all data and visualizations
            await loadAllData();
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        statusDiv.className = 'status-message error';
        statusDiv.textContent = `Error: ${error.message}`;
    }
}

async function loadAllData() {
    try {
        // Load statistics
        await loadStats();
        
        // Load charts
        await loadCharts();
        
        // Load tables
        await loadTables();
        
        // Show all sections
        document.getElementById('statsSection').style.display = 'block';
        document.getElementById('chartsSection').style.display = 'block';
        document.getElementById('tablesSection').style.display = 'block';
        document.getElementById('exportSection').style.display = 'block';
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading data: ' + error.message);
    }
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const result = await response.json();
        
        if (result.success) {
            const stats = result.data;
            document.getElementById('totalOvertime').textContent = stats.total_overtime_hours.toLocaleString();
            document.getElementById('totalOvertimeHHMMSS').textContent = stats.total_overtime_hhmmss || formatHoursToHHMMSS(stats.total_overtime_hours);
            document.getElementById('totalOvertimeDDHHMMSS').textContent = stats.total_overtime_ddhhmmss || formatHoursToDDHHMMSS(stats.total_overtime_hours);
            document.getElementById('avgOvertime').textContent = stats.average_overtime_per_record.toLocaleString();
            document.getElementById('avgOvertimeHHMMSS').textContent = stats.average_overtime_hhmmss || formatHoursToHHMMSS(stats.average_overtime_per_record);
            document.getElementById('avgOvertimeDDHHMMSS').textContent = stats.average_overtime_ddhhmmss || formatHoursToDDHHMMSS(stats.average_overtime_per_record);
            document.getElementById('totalHours').textContent = stats.total_hours_worked.toLocaleString();
            document.getElementById('uniqueEmployees').textContent = stats.unique_employees.toLocaleString();
            document.getElementById('totalRecords').textContent = stats.total_records.toLocaleString();
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadCharts() {
    try {
        // Load month data
        const monthResponse = await fetch('/api/summary/month');
        const monthResult = await monthResponse.json();
        
        if (monthResult.success) {
            createMonthChart(monthResult.data);
        }
        
        // Load daily data
        const dailyResponse = await fetch('/api/summary/daily');
        const dailyResult = await dailyResponse.json();
        
        if (dailyResult.success) {
            createDailyChart(dailyResult.data);
        }
        
        // Load top employees
        const topResponse = await fetch('/api/top-employees?n=10');
        const topResult = await topResponse.json();
        
        if (topResult.success) {
            createTopEmployeesChart(topResult.data);
        }
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

function createMonthChart(data) {
    const ctx = document.getElementById('monthChart').getContext('2d');
    
    if (monthChart) {
        monthChart.destroy();
    }
    
    const labels = data.map(d => d.MONTH);
    const overtimeData = data.map(d => d.TOTAL_OVERTIME_HOURS);
    
    monthChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Overtime Hours',
                data: overtimeData,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createDailyChart(data) {
    const ctx = document.getElementById('dailyChart').getContext('2d');
    
    if (dailyChart) {
        dailyChart.destroy();
    }
    
    // Sort by date
    data.sort((a, b) => new Date(a.DATE) - new Date(b.DATE));
    
    const labels = data.map(d => {
        const date = new Date(d.DATE);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const overtimeData = data.map(d => d.TOTAL_OVERTIME_HOURS);
    
    dailyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Overtime Hours',
                data: overtimeData,
                borderColor: 'rgba(118, 75, 162, 1)',
                backgroundColor: 'rgba(118, 75, 162, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

function createTopEmployeesChart(data) {
    const ctx = document.getElementById('topEmployeesChart').getContext('2d');
    
    if (topEmployeesChart) {
        topEmployeesChart.destroy();
    }
    
    const labels = data.map(d => d.FULL_NAME.split(' ').slice(0, 2).join(' '));
    const overtimeData = data.map(d => d.TOTAL_OVERTIME_HOURS);
    
    topEmployeesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Overtime Hours',
                data: overtimeData,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

async function loadTables() {
    try {
        // Load employee summary
        const empResponse = await fetch('/api/summary/employees');
        const empResult = await empResponse.json();
        
        if (empResult.success) {
            populateEmployeeTable(empResult.data);
        }
        
        // Load month summary
        const monthResponse = await fetch('/api/summary/month');
        const monthResult = await monthResponse.json();
        
        if (monthResult.success) {
            populateMonthTable(monthResult.data);
        }
        
        // Load top employees
        const topResponse = await fetch('/api/top-employees?n=20');
        const topResult = await topResponse.json();
        
        if (topResult.success) {
            populateTopTable(topResult.data);
        }
    } catch (error) {
        console.error('Error loading tables:', error);
    }
}

function populateEmployeeTable(data) {
    const tbody = document.getElementById('employeeTableBody');
    tbody.innerHTML = '';
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.PIN_CODE}</td>
            <td>${row.FULL_NAME}</td>
            <td>${row.TOTAL_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.TOTAL_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.AVG_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.DAYS_WORKED}</td>
            <td>${row.TOTAL_HOURS_WORKED.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
    
    // Initialize filters and sorting after populating
    setTimeout(() => {
        initializeTableFilters();
        initializeTableSorting();
    }, 100);
}

function populateMonthTable(data) {
    const tbody = document.getElementById('monthTableBody');
    tbody.innerHTML = '';
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.MONTH}</td>
            <td>${row.TOTAL_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.TOTAL_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.AVG_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_HOURS_WORKED.toFixed(2)}</td>
            <td>${row.UNIQUE_EMPLOYEES}</td>
        `;
        tbody.appendChild(tr);
    });
    
    // Initialize filters and sorting after populating
    setTimeout(() => {
        initializeTableFilters();
        initializeTableSorting();
    }, 100);
}

function populateTopTable(data) {
    const tbody = document.getElementById('topTableBody');
    tbody.innerHTML = '';
    
    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${row.PIN_CODE}</td>
            <td>${row.FULL_NAME}</td>
            <td>${row.TOTAL_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.TOTAL_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.AVG_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.DAYS_WORKED}</td>
        `;
        tbody.appendChild(tr);
    });
    
    // Initialize filters and sorting after populating
    setTimeout(() => {
        initializeTableFilters();
        initializeTableSorting();
    }, 100);
}

function formatHoursToHHMMSS(hours) {
    if (!hours || hours === 0) return "00:00:00";
    const isNegative = hours < 0;
    hours = Math.abs(hours);
    const totalSeconds = Math.floor(hours * 3600);
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;
    const result = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return isNegative ? `-${result}` : result;
}

function formatHoursToDDHHMMSS(hours, hoursPerDay = 8) {
    if (!hours || hours === 0) return "00:00:00:00";
    const isNegative = hours < 0;
    hours = Math.abs(hours);
    const days = Math.floor(hours / hoursPerDay);
    const remainingHours = hours % hoursPerDay;
    const totalSeconds = Math.floor(remainingHours * 3600);
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;
    const result = `${days.toString().padStart(2, '0')}:${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return isNegative ? `-${result}` : result;
}

// Table filtering functionality
function initializeTableFilters() {
    const filterInputs = document.querySelectorAll('.table-filter');
    filterInputs.forEach(input => {
        // Remove existing listeners to avoid duplicates
        const newInput = input.cloneNode(true);
        input.parentNode.replaceChild(newInput, input);
        
        newInput.addEventListener('keyup', function() {
            const column = parseInt(this.getAttribute('data-column'));
            const table = this.closest('table');
            const filterValue = this.value.toLowerCase();
            
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const cell = row.cells[column];
                if (cell) {
                    const text = cell.textContent.toLowerCase();
                    if (text.includes(filterValue)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        });
    });
}

// Table sorting functionality
function initializeTableSorting() {
    const sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(header => {
        // Remove existing listeners to avoid duplicates
        const newHeader = header.cloneNode(true);
        header.parentNode.replaceChild(newHeader, header);
        
        newHeader.addEventListener('click', function() {
            const table = this.closest('table');
            const column = parseInt(this.getAttribute('data-column'));
            const type = this.getAttribute('data-type');
            const tbody = table.querySelector('tbody');
            
            // Get all rows (including hidden ones for proper sorting)
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            // Determine sort direction
            const isAscending = !this.classList.contains('sort-asc');
            
            // Remove sort classes from all headers in this table
            table.querySelectorAll('.sortable').forEach(h => {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add appropriate sort class
            this.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
            
            // Sort rows
            rows.sort((a, b) => {
                const aCell = a.cells[column];
                const bCell = b.cells[column];
                
                if (!aCell || !bCell) return 0;
                
                let aValue = aCell.textContent.trim();
                let bValue = bCell.textContent.trim();
                
                if (type === 'number') {
                    // Parse numbers, handling negative values
                    aValue = parseFloat(aValue) || 0;
                    bValue = parseFloat(bValue) || 0;
                } else {
                    // Text comparison (case-insensitive)
                    aValue = aValue.toLowerCase();
                    bValue = bValue.toLowerCase();
                }
                
                if (aValue < bValue) return isAscending ? -1 : 1;
                if (aValue > bValue) return isAscending ? 1 : -1;
                return 0;
            });
            
            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
            
            // Reapply filters after sorting
            applyFilters(table);
        });
    });
}

// Reapply filters after sorting
function applyFilters(table) {
    const filterInputs = table.querySelectorAll('.table-filter');
    filterInputs.forEach(input => {
        if (input.value) {
            const column = parseInt(input.getAttribute('data-column'));
            const filterValue = input.value.toLowerCase();
            
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const cell = row.cells[column];
                if (cell) {
                    const text = cell.textContent.toLowerCase();
                    if (text.includes(filterValue)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        }
    });
}

// Re-initialize filters after populating tables
function populateEmployeeTable(data) {
    const tbody = document.getElementById('employeeTableBody');
    tbody.innerHTML = '';
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.PIN_CODE}</td>
            <td>${row.FULL_NAME}</td>
            <td>${row.TOTAL_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.TOTAL_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.AVG_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.DAYS_WORKED}</td>
            <td>${row.TOTAL_HOURS_WORKED.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
    
    // Initialize filters and sorting after populating
    setTimeout(() => {
        initializeTableFilters();
        initializeTableSorting();
    }, 100);
}

function populateMonthTable(data) {
    const tbody = document.getElementById('monthTableBody');
    tbody.innerHTML = '';
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.MONTH}</td>
            <td>${row.TOTAL_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.TOTAL_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.AVG_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_HOURS_WORKED.toFixed(2)}</td>
            <td>${row.UNIQUE_EMPLOYEES}</td>
        `;
        tbody.appendChild(tr);
    });
    
    // Initialize filters and sorting after populating
    setTimeout(() => {
        initializeTableFilters();
        initializeTableSorting();
    }, 100);
}

function populateTopTable(data) {
    const tbody = document.getElementById('topTableBody');
    tbody.innerHTML = '';
    
    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${row.PIN_CODE}</td>
            <td>${row.FULL_NAME}</td>
            <td>${row.TOTAL_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.TOTAL_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.TOTAL_OVERTIME_DDHHMMSS || formatHoursToDDHHMMSS(row.TOTAL_OVERTIME_HOURS)}</td>
            <td>${row.AVG_OVERTIME_HOURS.toFixed(2)}</td>
            <td>${row.AVG_OVERTIME_HHMMSS || formatHoursToHHMMSS(row.AVG_OVERTIME_HOURS)}</td>
            <td>${row.DAYS_WORKED}</td>
        `;
        tbody.appendChild(tr);
    });
    
    // Initialize filters and sorting after populating
    setTimeout(() => {
        initializeTableFilters();
        initializeTableSorting();
    }, 100);
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

async function exportSummary() {
    try {
        const response = await fetch('/api/export');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'overtime_summary.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        alert('Error exporting file: ' + error.message);
    }
}

