const form = document.getElementById("restaurantForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const selectedTypes =
        Array.from(
            document.getElementById(
                "restaurantTypes"
            ).selectedOptions
        ).map(option => option.value);

    const data = {
        name: document.getElementById("name").value,
        adress: document.getElementById("adress").value,
        phoneNumber: document.getElementById("phoneNumber").value,
        website: document.getElementById("website").value,
        restauranType: selectedTypes
    };

    const response = await fetch("", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.href = "/Restauran";
    }
});