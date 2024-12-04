const uploadForm = document.getElementById('uploadForm');
const postForm = document.getElementById('postForm');
const postsContainer = document.getElementById('postsContainer');

// Handle image upload
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const imageInput = document.getElementById('image');
    formData.append('file', imageInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/image', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        document.getElementById('uploadResult').innerHTML = `<p>${result.message}</p><p><strong>File Path:</strong> ${result.file_path}</p>`;
    } catch (error) {
        document.getElementById('uploadResult').innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

// Handle post creation
postForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const imagePath = document.getElementById('imagePath').value;
    const username = document.getElementById('username').value;
    const comment = document.getElementById('comment').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imagePath, user: username, text: comment }),
        });

        if (response.ok) {
            alert('Post created successfully!');
            loadPosts();
        } else {
            alert('Failed to create post.');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Load posts from the API
async function loadPosts() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/post/latest');
        const post = await response.json();

        postsContainer.innerHTML = `
            <div class="post">
                <img src="${post.image_path}" alt="Post Image">
                <p><strong>${post.username}</strong></p>
                <p>${post.comment}</p>
                <p><small>${post.created_at}</small></p>
            </div>`;
    } catch (error) {
        postsContainer.innerHTML = `<p>Error loading posts: ${error.message}</p>`;
    }
}

// Initial load
loadPosts();

