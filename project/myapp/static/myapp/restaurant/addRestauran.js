const restaurantForm = document.getElementById("restaurantForm")

restaurantForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const adress = document.getElementById("adress").value;
    const phoneNumber = document.getElementById("phoneNumber").value;
    const website = document.getElementById("website").value;

    const select = document.getElementById("restaurantTypes");

    const selectedTypes = Array.from(select.selectedOptions)
        .map(option => option.value);

    const formData = {
      name: name,
      adress: adress,
       phoneNumber: phoneNumber,
       website: website,
       restauranType: selectedTypes
    };

    fetch("", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(formData)
    })
})