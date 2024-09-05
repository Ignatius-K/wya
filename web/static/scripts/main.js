/**
 * main.js
 *
 * JS script handling the main user-interaction
 */

document.addEventListener("DOMContentLoaded", function () {
	// view all events button
	const viewAllEventsButton = document.querySelector(
		"button.view-all-events-button"
	);
	if (viewAllEventsButton) {
		viewAllEventsButton.addEventListener("click", () => {
			window.location.href = "/events";
		});
	}

	// create event button
	const createEventButton = document.querySelector(
		".user-events-header button"
	);
	if (createEventButton) {
		createEventButton.addEventListener("click", () => {
			window.location.href = "/events/create";
		});
	}

	// sign up button
	const signUpButtons = document.getElementsByClassName("sign-up");
	for (const button of signUpButtons) {
		button.addEventListener("click", () => {
			window.location.href = "/auth/register";
		});
	}

	// sign in button
	const signInButtons = document.getElementsByClassName("sign-in");
	for (const button of signInButtons) {
		button.addEventListener("click", () => {
			window.location.href = "/auth/login";
		});
	}

	// sign-out button
	const signOutButton = document.getElementsByClassName("sign-out");
	for (const button of signOutButton) {
		button.addEventListener("click", () => {
			window.location.href = "/auth/logout";
		});
	}

	// delete message button
	const deleteMessageButtons = document.getElementsByClassName("delete-icon");
	for (const button of deleteMessageButtons) {
		button.addEventListener("click", () => {
			button.parentElement.remove();
		});
	}

	// message disappear after 5 seconds
	const messages = document.getElementsByClassName("message");
	for (const message of messages) {
		message.classList.add("slide-in");
		setTimeout(() => {
			message.classList.add("slide-out");
			setTimeout(() => {
				message.remove();
			}, 500);
		}, 8000);
	}

	// click event-card
	const eventCards = document.getElementsByClassName("event-card");
	for (const eventCard of eventCards) {
		eventCard.addEventListener("click", () => {
			const eventId = eventCard.getAttribute("data-event-id");
			window.location.href = `/events/${eventId}`;
		});
	}
});
