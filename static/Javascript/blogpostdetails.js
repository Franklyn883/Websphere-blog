"USE STRICT";
const moreOptionBtn = document.querySelector(".more-option-btn");
const moreOptionDisplay = document.querySelector(".post-option-more-content");

const displayMoreOption = () => {
    moreOptionDisplay.classList.toggle("hidden");
};

moreOptionBtn.addEventListener("click", displayMoreOption);
document.addEventListener("DOMContentLoaded", function () {
    // Get all reveal more buttons
    const revealButtons = document.querySelectorAll(".comment-action-btn");

    // Add click event listener to each reveal more button
    revealButtons.forEach((button) => {
        button.addEventListener("click", function (event) {
            // Prevent the click event from propagating to the parent containers
            event.stopPropagation();

            // Find the corresponding extra options panel for the clicked button
            const extraOptionsPanel = this.nextElementSibling;

            // Close all other extra options panels
            closeAllExtraOptionsPanels(extraOptionsPanel);

            // Toggle the visibility of the clicked extra options panel
            extraOptionsPanel.classList.toggle("hidden");
        });
    });

    // Close the extra options panels when clicking outside of them
    document.addEventListener("click", function () {
        closeAllExtraOptionsPanels();
    });

    function closeAllExtraOptionsPanels(excludePanel = null) {
        // Get all extra options panels
        const extraOptionsPanels = document.querySelectorAll(
            ".blog-post__comment-action-options"
        );

        // Close each extra options panel except the one to exclude
        extraOptionsPanels.forEach((panel) => {
            if (panel !== excludePanel) {
                panel.classList.add("hidden");
            }
        });
    }
});
