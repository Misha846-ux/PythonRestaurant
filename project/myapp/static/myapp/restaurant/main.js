document.querySelectorAll(".deleteForm").forEach(form => {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const id = Number(form.elements["id"].value);

        console.log("Удаляем:", id);

        const response = await fetch("/Restauran", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id })
        });

        console.log(await response.text());

        if (response.ok) {
            location.reload();
        }
    });
});