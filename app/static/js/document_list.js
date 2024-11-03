document
    .getElementById("createDocumentForm")
    .addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append("content", document.getElementById("content").value);

        formData.append("title", document.getElementById("title").value);

        // Handle image file if present
        const imageFile = document.getElementById("img_content").files[0];
        if (imageFile) {
            formData.append("img_content", imageFile);
        }

        try {
            const response = await fetch("/api/documents/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector(
                        "[name=csrfmiddlewaretoken]"
                    ).value,
                },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("Error:", errorData);
                throw new Error("Network response was not ok");
            }

            // Refresh the page or update the UI
            window.location.reload();
        } catch (error) {
            console.error("Error:", error);
            alert("Failed to create document");
        }
    });


// Function to open the modal
function openModal() {
    document.getElementById("createDocumentModal").style.display = "block";
}

// Function to close the modal
function closeModal() {
    document.getElementById("createDocumentModal").style.display = "none";
}

// Close the modal if user clicks outside of it
window.onclick = function(event) {
    const modal = document.getElementById("createDocumentModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
