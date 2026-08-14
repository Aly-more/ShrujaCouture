/* ==========================================
        WISHLIST
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    syncWishlist();

    const wishlistButtons = document.querySelectorAll(
        ".wishlist-btn, .wishlist-detail-btn"
    );

    wishlistButtons.forEach(button => {

        button.addEventListener("click", async (e) => {

            e.preventDefault();

            const productId = Number(button.dataset.product);

            try {

                const response = await fetch(

                    "/api/wishlist/toggle/",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type": "application/json",

                            "X-CSRFToken": getCookie("csrftoken")

                        },

                        body: JSON.stringify({

                            product_id: productId

                        })

                    }

                );

                const data = await response.json();

                if (!data.success) return;

                if (data.wishlist.action === "added") {

                    updateWishlistButton(button, "added");

                    if (typeof flyHeartToWishlist === "function") {

                        flyHeartToWishlist(button, () => {

                            syncWishlist();

                        });

                    }

                    else {

                        syncWishlist();

                    }

                }

                else {

                    updateWishlistButton(button, "removed");

                    syncWishlist();

                }

            }

            catch (error) {

                console.error("Wishlist Error:", error);

            }

        });

    });

});


/* ==========================================
        UPDATE BUTTON
========================================== */

function updateWishlistButton(button, action) {

    const icon = button.querySelector("svg");

    if (!icon) return;

    if (action === "added") {

        button.classList.add("active");

        icon.style.fill = "#B66E4C";
        icon.style.stroke = "#B66E4C";

        button.animate(

            [

                { transform: "scale(1)" },
                { transform: "scale(1.15) rotate(-8deg)" },
                { transform: "scale(1.25) rotate(8deg)" },
                { transform: "scale(1)" }

            ],

            {

                duration: 420,

                easing: "cubic-bezier(.175,.885,.32,1.275)"

            }

        );

    }

    else {

        button.classList.remove("active");

        icon.style.fill = "none";
        icon.style.stroke = "";

    }

}


/* ==========================================
        NAVBAR COUNT
========================================== */

function updateWishlistCount(count) {

    const badge = document.getElementById("wishlist-count");

    if (!badge) return;

    if (count <= 0) {

        badge.textContent = "";

        badge.style.display = "none";

        return;

    }

    badge.textContent = count;

    badge.style.display = "flex";

    badge.animate(

        [

            { transform: "scale(.6)" },
            { transform: "scale(1.25)" },
            { transform: "scale(.92)" },
            { transform: "scale(1)" }

        ],

        {

            duration: 320,

            easing: "ease-out"

        }

    );

}


/* ==========================================
        SYNC WISHLIST
========================================== */

async function syncWishlist() {

    try {

        const response = await fetch(

            "/api/wishlist/status/"

        );

        const data = await response.json();

        if (!data.success) return;

        const wishlistIds = data.wishlist.wishlist_ids;

        const wishlistCount = data.wishlist.wishlist_count;

        document.querySelectorAll(

            ".wishlist-btn, .wishlist-detail-btn"

        ).forEach(button => {

            const id = Number(button.dataset.product);

            const icon = button.querySelector("svg");

            if (!icon) return;

            if (wishlistIds.includes(id)) {

                button.classList.add("active");

                icon.style.fill = "#B66E4C";

                icon.style.stroke = "#B66E4C";

            }

            else {

                button.classList.remove("active");

                icon.style.fill = "none";

                icon.style.stroke = "";

            }

        });

        updateWishlistCount(

            wishlistCount

        );

    }

    catch (error) {

        console.error(

            "Wishlist Sync Error:",

            error

        );

    }

}


/* ==========================================
        CSRF
========================================== */

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(

                    cookie.substring(name.length + 1)

                );

                break;

            }

        }

    }

    return cookieValue;

}


/* ==========================================
        BF CACHE FIX
========================================== */

window.addEventListener("pageshow", async () => {

    await syncWishlist();

    if (typeof updateCartBadge === "function") {

        await updateCartBadge();

    }

});