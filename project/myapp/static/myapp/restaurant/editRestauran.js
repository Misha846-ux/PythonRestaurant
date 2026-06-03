const form = document.getElementById("restaurantForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData();
    fd.append('name', document.getElementById('name').value);
    fd.append('adress', document.getElementById('adress').value);
    fd.append('phoneNumber', document.getElementById('phoneNumber').value);
    fd.append('website', document.getElementById('website').value);

    const selectedTypes = Array.from(document.getElementById('restaurantTypes').selectedOptions).map(o => o.value);
    selectedTypes.forEach(v => fd.append('restauranType', v));

    const photosInput = document.getElementById('photos');
    if (photosInput && photosInput.files.length) {
        Array.from(photosInput.files).forEach(f => fd.append('photos', f));
    }

    const response = await fetch('', {
        method: 'POST',
        body: fd
    });

    if (response.ok) {
        window.location.href = "/Restauran";
    }
});