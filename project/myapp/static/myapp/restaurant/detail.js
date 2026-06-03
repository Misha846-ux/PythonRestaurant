document.getElementById("reviewForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const reviewText = document.getElementById("review").value.trim();

    if (!reviewText) {
        return;
    }

    const response = await fetch(
        window.location.pathname + "add_review",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                review: reviewText
            })
        }
    );

    if (response.ok) {
        document.getElementById("review").value = "";
        location.reload();
    }
});