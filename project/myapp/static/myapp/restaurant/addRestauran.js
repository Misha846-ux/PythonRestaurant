const restaurantForm = document.getElementById("restaurantForm")

restaurantForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = document.getElementById("restaurantForm");
    const fd = new FormData();
    fd.append('name', document.getElementById('name').value);
    fd.append('adress', document.getElementById('adress').value);
    fd.append('phoneNumber', document.getElementById('phoneNumber').value);
    fd.append('website', document.getElementById('website').value);

    const select = document.getElementById('restaurantTypes');
    const selectedTypes = Array.from(select.selectedOptions).map(o => o.value);
    selectedTypes.forEach(v => fd.append('restauranType', v));

    const photosInput = document.getElementById('photos');
    if (photosInput && photosInput.files.length) {
        Array.from(photosInput.files).forEach(f => fd.append('photos', f));
    }

    await fetch('', {
        method: 'POST',
        body: fd
    });
    window.location.href = '/Restauran';
})