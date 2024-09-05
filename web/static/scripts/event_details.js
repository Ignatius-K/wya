/**
 * Event details script
 *
 * JS script for the event details page
 */

document.addEventListener("DOMContentLoaded", () => {
	// save event
	const saveEventBtns = document.getElementsByClassName("save-event-button");
	for (const btn of saveEventBtns) {
		console.log(btn.dataset);
		btn.addEventListener("click", () => {
			const eventId = btn.getAttribute("data-event-id");
			window.location.href = `/events/${eventId}/save`;
		});
	}

	// unsave event
	const unsaveEventBtns = document.getElementsByClassName(
		"unsave-event-button"
	);
	for (const btn of unsaveEventBtns) {
		const eventId = btn.getAttribute("data-event-id");
		console.log(eventId);
		btn.addEventListener("click", () => {
			window.location.href = `/events/${eventId}/unsave`;
		});
	}

	// edit event image
	const editEventImageBtn = document.getElementsByClassName(
		"edit-event-image-button"
	);
	for (const btn of editEventImageBtn) {
		const eventId = btn.getAttribute("data-event-id");
		btn.addEventListener("click", () => {
			window.location.href = `/events/${eventId}/edit`;
		});
	}
});
