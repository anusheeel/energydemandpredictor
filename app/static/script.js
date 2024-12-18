// Get references to the file input and file list container
const fileInput = document.getElementById('file');
const fileListContainer = document.getElementById('file-list');

// Listen for changes in the file input
fileInput.addEventListener('change', () => {
    // Clear the current file list
    fileListContainer.innerHTML = '';

    // Get the selected files
    const files = fileInput.files;

    // Display the list of selected files
    if (files.length > 0) {
        Array.from(files).forEach(file => {
            const listItem = document.createElement('li');
            listItem.textContent = file.name;
            fileListContainer.appendChild(listItem);
        });
    } else {
        const emptyMessage = document.createElement('li');
        emptyMessage.textContent = "No files selected.";
        fileListContainer.appendChild(emptyMessage);
    }
});
