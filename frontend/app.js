document.getElementById("postForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const imagePath = document.getElementById("imagePath").value;
    const username = document.getElementById("username").value;
    const comment = document.getElementById("comment").value;

    const response = await fetch("http://localhost:8000/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_path: imagePath, username, comment }),
    });

    if (response.ok) {
        alert("Post created successfully!");
    } else {
        alert("Failed to create post.");
    }
});
