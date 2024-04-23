document.addEventListener("DOMContentLoaded", function() {
    const select = document.getElementById('select-competition');
    const tableRows = document.querySelectorAll('tbody tr');

    select.addEventListener('change', function() {
        const selectedValue = this.value;

        tableRows.forEach(function(row) {
            const competitionValue = row.querySelector('td:nth-child(5)').textContent.trim();

            if (selectedValue === '' || competitionValue === selectedValue) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
