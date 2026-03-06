document.addEventListener('DOMContentLoaded', () => {
    console.log('IPL Auction Platform Initialized');

    // Quick search functionality or other global interactive elements
    const cards = document.querySelectorAll('.player-card');
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.tagName !== 'A') {
                const link = card.querySelector('.view-btn');
                if (link) window.location.href = link.href;
            }
        });
    });
});
