const uploadForm = document.getElementById('uploadForm');
const postForm = document.getElementById('postForm');
const searchForm = document.getElementById('searchForm');
const uploadResult = document.getElementById('uploadResult');
const recentPostsDiv = document.getElementById('recentPosts');
const searchResultsDiv = document.getElementById('searchResults');


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
        console.log("API Response:", result); // Debug-Log der API Response

        if (result.full_size_path) {
            uploadResult.innerHTML = `<p><strong>${result.message}</strong></p>
                                      <p>Full-Size Path:
                                      <a href="${result.full_size_path}" target="_blank">View Full Image</a></p>`;
            document.getElementById('imagePath').value = result.full_size_path;
        } else {
            throw new Error("full_size_path is missing in the response.");
        }
    } catch (error) {
        console.error("Upload Error:", error);
        uploadResult.innerHTML = `<p>Error uploading image: ${error.message}</p>`;
    }
});


// Post erstellen
postForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const imagePath = document.getElementById('imagePath').value;
    const username = document.getElementById('username').value;
    const comment = document.getElementById('comment').value;

    await fetch('http://127.0.0.1:8000/api/v1/post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imagePath, user: username, text: comment })
    });
    loadRecentPosts();
});

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
                <img src="${post.image_path}" alt="Uploaded Image"> <!-- Korrektur hier -->
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
<img src="${post.image_path}" alt="Uploaded Image">
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
