const canvas = document.getElementById("drawCanvas");
const ctx = canvas.getContext("2d");
const max_hist = 10;

function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);

let isDrawing = false;
let lastX = 0;
let lastY = 0;
let drawingColor = "#c2a7ef";
let lineWidth = 2;
let history = [];
let historyIndex = -1;
let isEraser = false;

function getCoordinates(e) {
    const rect = canvas.getBoundingClientRect();
    if (e.type.includes("touch")) {
        return {
            x: e.touches[0].clientX - rect.left,
            y: e.touches[0].clientY - rect.top,
        };
    }
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
    };
}

function startDrawing(e) {
    e.preventDefault();
    isDrawing = true;
    const coords = getCoordinates(e);
    [lastX, lastY] = [coords.x, coords.y];
}

function draw(e) {
    e.preventDefault();
    if (!isDrawing) return;

    const coords = getCoordinates(e);

    if (isEraser) {
        // Clear pixels instead of drawing color
        ctx.clearRect(
            coords.x - lineWidth / 2,
            coords.y - lineWidth / 2,
            lineWidth,
            lineWidth
        );
    } else {
        ctx.strokeStyle = drawingColor;
        ctx.lineWidth = lineWidth;
        ctx.lineJoin = "round";
        ctx.lineCap = "round";

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(coords.x, coords.y);
        ctx.stroke();
    }

    [lastX, lastY] = [coords.x, coords.y];
}

function stopDrawing(e) {
    if (e) e.preventDefault();
    if (isDrawing) {
        isDrawing = false;
        saveState();
    }
}

function saveState() {
    if (historyIndex >= max_hist - 1) {
        history.shift();
    }
    history.push(canvas.toDataURL());
    historyIndex = history.length - 1;
}

function undo() {
    if (historyIndex > 0) {
        historyIndex--;
        restoreState(history[historyIndex]);
    }
}

function redo() {
    if (historyIndex < history.length - 1) {
        historyIndex++;
        restoreState(history[historyIndex]);
    }
    // saveCanvasAsPNG();
}

function saveCanvasAsPNG() {
    // Convert canvas to data URL
    const dataURL = canvas.toDataURL("image/png");

    // Create a temporary link element
    const link = document.createElement("a");
    link.download = "drawing.png"; // Set filename
    link.href = dataURL;

    // Get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie("csrftoken");

    // Create form data and append the blob
    const formData = new FormData();
    fetch(dataURL)
        .then((res) => res.blob())
        .then((blob) => {
            formData.append("image", blob, "drawing.png");

            // Send to server
            fetch("/render", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                body: formData,
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.blob();
                })
                .then(blob => {
                    // Create object URL from blob
                    const pdfUrl = URL.createObjectURL(blob);
                    
                    // Update the PDF viewer
                    const pdfViewer = document.querySelector('#main-render object');
                    pdfViewer.data = pdfUrl;
                    
                    // Show the preview if not already visible
                    document.getElementById('hidden-preview').style.display = 'block';
                    document.getElementById('view-canvas').style.display = 'none';
                    document.getElementById('main-toolbox').style.display = 'none';
                    document.getElementById('hidden-tools').style.display = 'block';
                    
                    // Update toggle state
                    const toggle = document.getElementById('preview-toggle');
                    toggle.classList.add('active');
                    toggle.style.backgroundColor = '#c2a7ef';
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });

    // Programmatically click the link to trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function restoreState(dataURL) {
    const img = new Image();
    img.src = dataURL;
    img.onload = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
    };
}

document.getElementById("penButton").addEventListener("click", function () {
    drawingColor = "#c2a7ef";
    lineWidth = 2;
    isEraser = false;
    toggleActive(this);
});

document.getElementById("eraserButton").addEventListener("click", function () {
    isEraser = true;
    lineWidth = 30;
    toggleActive(this);
});

document.getElementById("undoButton").addEventListener("click", undo);
document.getElementById("redoButton").addEventListener("click", redo);
document
    .getElementById("downloadButton")
    .addEventListener("click", saveCanvasAsPNG);

function toggleActive(button) {
    document
        .querySelectorAll(".button")
        .forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");
}

// Mouse events
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseout", stopDrawing);

// Touch events
canvas.addEventListener("touchstart", startDrawing, { passive: false });
canvas.addEventListener("touchmove", draw, { passive: false });
canvas.addEventListener("touchend", stopDrawing, { passive: false });
canvas.addEventListener("touchcancel", stopDrawing, { passive: false });

function toggleViewable(id) {
    elem = document.getElementById(id);
    if (elem.style.display == "none") {
        elem.style.display = "block";
    } else {
        elem.style.display = "none";
    }
}

function toggleSource() {
    toggleViewable("main-source");

    main_elem = document.getElementById("main-render");
    if (main_elem.classList.contains("split") && main_elem.classList.contains("right")) {
        // If they are present, switch to "full"
        main_elem.classList.remove("split", "right");
        main_elem.classList.add("full");
    } else {
        // Otherwise, switch back to "split" and "right"
        main_elem.classList.remove("full");
        main_elem.classList.add("split", "right");
    }

    button_elem = document.getElementById("split-view");
    if (button_elem.classList.contains("active")) {
        button_elem.classList.remove("active");
    }
    else {
        button_elem.classList.add("active");
    }
}

document.getElementById("split-view").addEventListener('click', toggleSource);

function toggleSwitch(element) {
    element.classList.toggle("active");
    toggle_elem = document.getElementById("preview-toggle");
    if (toggle_elem.style.backgroundColor === "rgb(255, 255, 255)") {
        toggle_elem.style.backgroundColor = "#c2a7ef";
    } else {
        toggle_elem.style.backgroundColor = "#ffffff";
    }

    toggleViewable("hidden-preview");
    toggleViewable("view-canvas");
    toggleViewable("main-toolbox");
    toggleViewable("hidden-tools");

    // print("Toggle View")
}

// Prevent scrolling on the entire page while touching the canvas
document.body.addEventListener(
    "touchstart",
    function (e) {
        if (e.target === canvas) {
            e.preventDefault();
        }
    },
    { passive: false }
);

document.body.addEventListener(
    "touchmove",
    function (e) {
        if (e.target === canvas) {
            e.preventDefault();
        }
    },
    { passive: false }
);

// Save initial state
saveState();

// Get the textarea and highlighted code elements
const editableCode = document.getElementById("editable-code");
const highlightedCode = document.getElementById("highlighted-code");

// Function to update syntax highlighting and render LaTeX
editableCode.addEventListener("input", () => {
    // Update the highlighted code content
    highlightedCode.textContent = editableCode.value;

    // Reapply syntax highlighting with Prism
    Prism.highlightElement(highlightedCode);

    // // Render LaTeX syntax with MathJax
    // MathJax.typesetPromise([highlightedCode]);
});

