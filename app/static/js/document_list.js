document.getElementById('createDocumentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('title', document.getElementById('title').value);
    formData.append('content', document.getElementById('content').value);
    
    // Handle image file if present
    const imageFile = document.getElementById('img_content').files[0];
    if (imageFile) {
        formData.append('img_content', imageFile);
    }

    try {
        const response = await fetch('/api/documents/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error:', errorData);
            throw new Error('Network response was not ok');
        }

        // Refresh the page or update the UI
        window.location.reload();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to create document');
    }
});