/**
 * create_events.js
 *
 * JS handles the creating of an event
 */

const getUserCountryCode = () => {
	return "UG";
};

document.addEventListener("DOMContentLoaded", function () {
	// check user's country
	const userCountryCode = getUserCountryCode();

	// location input
	const locationInput = document.getElementById("location");
	if (locationInput) {
		locationInput.addEventListener("focus", function () {
			const locationOptions = {
				componentRestrictions: { country: userCountryCode },
				fields: [
					"place_id",
					"name",
					"formatted_address",
					"geometry",
					"url",
				],
				types: ["point_of_interest"],
			};
			const autocomplete = new google.maps.places.Autocomplete(
				locationInput,
				locationOptions
			);
		});
	}

	// get user's timezone
	const timezoneInput = document.getElementById("event-timezone");
	if (timezoneInput) {
		const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
		timezoneInput.value = timezone;
	}

	// event-location-type & online-event-links
	const locationTypeSelect = document.getElementById("event-location-type");
	const onlineEventLink = document.getElementById("online-event-link");

	if (locationTypeSelect?.value === "ONLINE" && locationInput) {
		locationInput.disabled = true;
	}

	if (onlineEventLink && locationTypeSelect?.value === "IN_PERSON") {
		onlineEventLink.disabled = true;
	}

	if (locationTypeSelect && onlineEventLink) {
		locationTypeSelect.addEventListener("change", function () {
			if (locationTypeSelect.value === "IN_PERSON") {
				onlineEventLink.disabled = true;
			} else {
				onlineEventLink.disabled = false;
			}

			if (locationTypeSelect.value === "ONLINE") {
				locationInput.disabled = true;
			} else {
				locationInput.disabled = false;
			}
		});
	}
});
