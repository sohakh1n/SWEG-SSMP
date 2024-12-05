const uploadForm = document.getElementById('uploadForm');
const postForm = document.getElementById('postForm');
const searchForm = document.getElementById('searchForm');
const uploadResult = document.getElementById('uploadResult');
const recentPostsDiv = document.getElementById('recentPosts');
const searchResultsDiv = document.getElementById('searchResults');

// Upload an image
uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    const imageInput = document.getElementById('image');
    formData.append('file', imageInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/image', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        uploadResult.innerHTML = `<p><strong>${result.message}</strong></p><p>File Path: ${result.file_path}</p>`;
        document.getElementById('imagePath').value = result.file_path; // Autofill Image Path
    } catch (error) {
        uploadResult.innerHTML = `<p>Error uploading image: ${error.message}</p>`;
    }
});

// Create a post
postForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const imagePath = document.getElementById('imagePath').value;
    const username = document.getElementById('username').value;
    const comment = document.getElementById('comment').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imagePath, user: username, text: comment })
        });
        if (response.ok) {
            alert('Post created successfully!');
            loadRecentPosts(); // Refresh posts
        } else {
            alert('Failed to create post.');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Search posts
searchForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const query = document.getElementById('searchQuery').value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/post/search/${query}`);
        const results = await response.json();

        if (results.length === 0) {
            searchResultsDiv.innerHTML = `<p>No posts found for query: "${query}".</p>`;
            return;
        }

        const postsHTML = results.map(post => `
            <div class="post">
                <img src="http://127.0.0.1:8000/${post.image_path}" alt="Uploaded Image">
                <h3>Username: ${post.username}</h3>
                <p>Comment: ${post.comment}</p>
                <p><small>${post.created_at}</small></p>
            </div>
        `).join('');

        searchResultsDiv.innerHTML = postsHTML;
    } catch (error) {
        searchResultsDiv.innerHTML = `<p>Error searching posts: ${error.message}</p>`;
    }
});

// Load recent posts
async function loadRecentPosts() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/post/latest');
        const post = await response.json();

        if (!post || !post.image_path || !post.username || !post.comment) {
            recentPostsDiv.innerHTML = `<p>No recent posts found.</p>`;
            return;
        }

        const postHTML = `
            <div class="post">
                <img src="http://127.0.0.1:8000/${post.image_path}" alt="Uploaded Image">
                <h3>Username: ${post.username}</h3>
                <p>Comment: ${post.comment}</p>
                <p><small>${post.created_at}</small></p>
            </div>
        `;

        recentPostsDiv.innerHTML = postHTML;
    } catch (error) {
        recentPostsDiv.innerHTML = `<p>Error loading posts: ${error.message}</p>`;
    }
}

// Load posts on page load
loadRecentPosts();
