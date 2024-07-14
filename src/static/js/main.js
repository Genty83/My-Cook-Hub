// Main js file containing all the main functions


/** Function to close flash window */
function closeFlashWindow() {
    var flashContainer = document.querySelector(".flash-container");
    flashContainer.remove();
}

/** Function to open review form */
function toggleReviewForm() {
    var reviewForm = document.querySelector(".review-form");

    if (reviewForm.getBoundingClientRect().height == 0) {
        reviewForm.style.display = "flex";
    } else {
        reviewForm.style.display = "none";
    }
    
}

/** Function to toggle reviews board */
function toggleReviewsBoard() {
    var reviewsBoard = document.querySelector(".reviews-board");

    if (reviewsBoard.getBoundingClientRect().height == 0) {
        reviewsBoard.style.display = 'flex';
    } else {
        reviewsBoard.style.display = 'none';
    }
}