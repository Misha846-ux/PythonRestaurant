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
        const data = await response.json();
        document.getElementById("review").value = "";
        alert(data.message);
        location.reload();
    } else {
        const data = await response.json();
        alert(data.message || "Ошибка при отправке отзыва");
    }
});