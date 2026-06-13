document.addEventListener("DOMContentLoaded", function () {

    const bookingForm =
        document.getElementById("bookingForm");

    if (!bookingForm) return;

    bookingForm.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();

            const booking = {
                city: document.getElementById("city").value,
                rooms: document.getElementById("rooms").value,
                adults: document.getElementById("adults").value,
                children: document.getElementById("children").value,
                checkin: document.getElementById("checkin").value,
                checkout: document.getElementById("checkout").value
            };

            if (booking.city === "") {
                alert("Please select a city");
                return;
            }

            try {

                const response = await fetch(
                    "http://127.0.0.1:5000/book",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                            "application/json"
                        },
                        body: JSON.stringify(booking)
                    }
                );

                const result =
                    await response.json();

                alert(result.message);

                bookingForm.reset();

            } catch (error) {

                console.error(error);

                alert(
                    "Unable to connect to server."
                );
            }
        }
    );
});
