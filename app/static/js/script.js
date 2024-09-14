document.addEventListener("DOMContentLoaded", function() {
    const eventsList = document.getElementById("events-list");

    function loadEventsFromStorage() {
        const storedEvents = JSON.parse(localStorage.getItem('events')) || [];
        storedEvents.forEach(event => {
            const li = document.createElement('li');
            li.textContent = event;
            eventsList.appendChild(li);
        });
    }

    async function fetchLatestEvents() {
        try {
            const response = await fetch('/webhook/get-latest-events');
            const data = await response.json();
            const storedEvents = JSON.parse(localStorage.getItem('events')) || [];
            const newEvents = data.filter(event => !storedEvents.includes(event));
            const updatedEvents = [...newEvents, ...storedEvents];
            localStorage.setItem('events', JSON.stringify(updatedEvents));

            eventsList.innerHTML = '';
            updatedEvents.forEach(event => {
                const li = document.createElement('li');
                li.textContent = event;
                eventsList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    }

    loadEventsFromStorage();
    setInterval(fetchLatestEvents, 15000);
    fetchLatestEvents();
});
