function filterPlayers() {
    const nameInput = document.getElementById('nameSearch').value.toLowerCase();
    const teamFilter = document.getElementById('teamFilter').value;
    const roleFilter = document.getElementById('roleFilter').value;

    const cards = document.querySelectorAll('.player-card');

    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const team = card.getAttribute('data-team');
        const role = card.getAttribute('data-role');

        const nameMatch = name.includes(nameInput);
        const teamMatch = !teamFilter || team === teamFilter;
        const roleMatch = !roleFilter || role === roleFilter;

        if (nameMatch && teamMatch && roleMatch) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function sortPlayers() {
    const sortField = document.getElementById('sortField').value;
    const grid = document.getElementById('playerGrid');
    const cards = Array.from(grid.querySelectorAll('.player-card'));

    if (sortField === 'default') {
        location.reload(); // Simplest way to return to original DB order
        return;
    }

    cards.sort((a, b) => {
        const valA = parseFloat(a.getAttribute(`data-${sortField.replace('_', '-')}`));
        const valB = parseFloat(b.getAttribute(`data-${sortField.replace('_', '-')}`));
        return valB - valA; // Descending order for stats
    });

    // Re-append to grid in new order
    cards.forEach(card => grid.appendChild(card));
}
