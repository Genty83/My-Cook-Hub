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

/** Function to toggle reviews board */
function toggleAlertWindow() {
    var alertWin = document.querySelector(".alert-window");

    if (alertWin.getBoundingClientRect().height == 0) {
        alertWin.style.display = 'flex';
    } else {
        alertWin.style.display = 'none';
    }
}

/** Function to toggle the side menu */
function toggleSideMenu() {

    var sideMenu = document.querySelector('.side-menu');

    if (sideMenu.getBoundingClientRect().width == 0) {
        sideMenu.style.width = '250px';
        sideMenu.style.padding = '0.5rem';
    } else {
        sideMenu.style.width = '0px';
        sideMenu.style.padding = '0';
    }
}