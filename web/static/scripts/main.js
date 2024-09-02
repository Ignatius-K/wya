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
});
