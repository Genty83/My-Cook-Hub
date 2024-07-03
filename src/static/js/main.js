
// Variables
var closeBtn = document.querySelector(".close-btn");

/** Event listener for close button to remove flash container */
closeBtn.addEventListener("click", () => {
    var flashContainer = document.querySelector(".flash-container");

    flashContainer.remove();
})