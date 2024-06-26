document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".post").forEach(post => {
        const postId = post.dataset.postId;

        post.querySelectorAll(".post-ratings-container").forEach((ratingsContainer, containerIndex) => {
            const ratings = ratingsContainer.querySelectorAll(".post-rating");

            ratings.forEach((rating, ratingIndex) => {
                const button = rating.querySelector(".post-rating-button");
                const count = rating.querySelector(".post-rating-count");

                // Add checks to ensure elements are found
                if (!button) {
                    console.error(`Button not found for post ${postId}, container ${containerIndex}, rating ${ratingIndex}`);
                    return;
                }
                if (!count) {
                    console.error(`Count not found for post ${postId}, container ${containerIndex}, rating ${ratingIndex}`);
                    return;
                }

                button.addEventListener("click", async () => {
                    const isSelected = rating.classList.contains("post-rating-selected");

                    // Toggle the count and class based on selection state
                    if (isSelected) {
                        count.textContent = Math.max(0, Number(count.textContent) - 1);
                        rating.classList.remove("post-rating-selected");
                        button.classList.remove("selected");
                    } else {
                        count.textContent = Number(count.textContent) + 1;

                        // Deselect other ratings
                        ratings.forEach(innerRating => {
                            const innerButton = innerRating.querySelector(".post-rating-button");
                            if (innerRating.classList.contains("post-rating-selected")) {
                                const innerCount = innerRating.querySelector(".post-rating-count");
                                innerCount.textContent = Math.max(0, Number(innerCount.textContent) - 1);
                                innerRating.classList.remove("post-rating-selected");
                                innerButton.classList.remove("selected");
                            }
                        });

                        rating.classList.add("post-rating-selected");
                        button.classList.add("selected");
                    }

                    // Send the appropriate request to the server
                    const action = isSelected ? "unlike" : (ratings[0] === rating ? "like" : "dislike");
                    console.log(`Sending ${action} request for post ${postId}, container ${containerIndex}, rating ${ratingIndex}`);
                    const response = await fetch(`/posts/${postId}/${action}`);
                    const body = await response.json();
                    console.log(`Response for post ${postId}, container ${containerIndex}, rating ${ratingIndex}:`, body);
                });
            });
        });
    });
});
