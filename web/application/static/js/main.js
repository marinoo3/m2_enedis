const updateContainer = document.querySelector('header .update');
const updateButton = updateContainer.querySelector('.action #update');
const updateProgress = updateContainer.querySelector('.collecting .progress');





// Update dataset when update requested
updateButton.addEventListener('click', () => {
    
    updateContainer.classList.add('loading');

    const eventSource = new EventSource('api/update_data');
    eventSource.onmessage = async function(event) {
        if (event.data === 'complete') {
            eventSource.close();
            location.reload();
        } else {
            console.log(event);
            const progress = parseInt(event.data);
            updateProgress.style.width = progress + "%";
        }
    }
});