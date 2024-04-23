document.addEventListener("DOMContentLoaded", function() {
    const select = document.getElementById('select-competition');
    const table = document.getElementById('results-table');
    
    select.addEventListener('change', function() {
        const selectedValue = this.value;
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const competitionValue = row.getAttribute('data-competition');
            
            if (!competitionValue) continue; // Saltar si la fila no tiene un atributo de datos de competición
            
            if (selectedValue === '' || competitionValue === selectedValue) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
});
