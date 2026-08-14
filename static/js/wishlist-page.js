/*Remember when I told you

"I don't know if DRF is necessary."

😂

Now we're at the point where it absolutely is.

This cart...

Wishlist...

Checkout...

Orders...

Addresses...

Payments...

These are all API-driven features.*/ 

/* ==========================================
        WISHLIST PAGE
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initialiseWishlist();

});


/* ==========================================
        INITIALISE
========================================== */

function initialiseWishlist() {

    initialiseWishlistDelete();

    initialiseWishlistCart();

}


/* ==========================================
        ADD TO BAG
========================================== */

function initialiseWishlistCart() {

    const buttons = document.querySelectorAll(".wishlist-cart-btn");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            if (button.disabled) return;

            const card = button.closest(".wishlist-card");

            const picker = card.querySelector(".hidden-size-picker");

            /* ================================
                    CLOSE OTHER PICKERS
            ================================ */

            document.querySelectorAll(".hidden-size-picker.open")
                .forEach(section => {

                    if (section !== picker) {

                        section.classList.remove("open");

                    }

                });

            /* ================================
                    TOGGLE CURRENT PICKER
            ================================ */

            picker.classList.toggle("open");

        });

    });


    /* ======================================
            SIZE BUTTONS
    ====================================== */

    document.querySelectorAll(".wishlist-size-btn")
        .forEach(sizeButton => {

            sizeButton.addEventListener("click", async () => {

                if (sizeButton.disabled) return;

                const card =
                    sizeButton.closest(".wishlist-card");

                const addButton =
                    card.querySelector(".wishlist-cart-btn");

                const picker =
                    card.querySelector(".hidden-size-picker");

                const productId =
                    addButton.dataset.product;

                const size =
                    sizeButton.dataset.size;

                const text =
                    addButton.querySelector("span");

                /* ============================
                        ACTIVE SIZE
                ============================ */

                card.querySelectorAll(".wishlist-size-btn")
                    .forEach(btn => {

                        btn.classList.remove("active");

                    });

                sizeButton.classList.add("active");

                addButton.disabled = true;

                text.textContent = "Adding to Bag...";

                const formData = new FormData();

                formData.append("product_id", productId);

                formData.append(
                    "selected_size",
                    size
                );

                try {

                    const response = await fetch(

                        "/cart/quick-add/",

                        {

                            method: "POST",

                            headers: {

                                "X-CSRFToken":
                                    getCookie("csrftoken")

                            },

                            body: formData

                        }

                    );

                    const data =
                        await response.json();

                    if (data.success) {

                        updateCartCount(
                            data.cart_count
                        );

                        const productName=

                        card.querySelector("h3").innerText;

                        showLuxuryToast(

                            productName,

                            size

                        );

                        picker.classList.remove("open");

                        text.textContent = "Added to Bag";

                        addButton.classList.add("added");

                        addButton.animate(

                            [

                                {
                                    transform: "scale(1)"
                                },

                                {
                                    transform: "scale(1.05)"
                                },

                                {
                                    transform: "scale(1)"
                                }

                            ],

                            {

                                duration: 280,

                                easing: "ease-out"

                            }

                        );
                        setTimeout(() => {

                            card.animate(

                                [

                                    {

                                        opacity: 1,

                                        transform: "translateY(0) scale(1)"

                                    },

                                    {

                                        opacity: 0,

                                        transform: "translateY(-24px) scale(.94)"

                                    }

                                ],

                                {

                                    duration: 350,

                                    easing: "ease"

                                }

                            );

                            setTimeout(() => {

                                card.remove();

                                updateWishlistCount(

                                    data.wishlist_count

                                );

                                updateCartCount(

                                    data.cart_count

                                );

                                if (

                                    document.querySelectorAll(".wishlist-card").length === 0

                                ) {

                                    location.reload();

                                }

                            }, 330);

                        }, 1200);

                    }

                    else {

                        text.textContent =
                            "Sold Out";

                        addButton.classList.add("sold");

                        addButton.disabled = false;

                    }

                }

                catch (error) {

                    console.error(error);

                    text.textContent = "Error";

                    addButton.disabled = false;

                }

            });

        });

}

/* ==========================================
        DELETE FROM WISHLIST
========================================== */

function initialiseWishlistDelete() {

    const buttons = document.querySelectorAll(".wishlist-delete");

    buttons.forEach(button => {

        button.addEventListener("click", async () => {

            if (button.disabled) return;

            button.disabled = true;

            const productId = button.dataset.product;

            const card = button.closest(".wishlist-card");

            button.animate(

                [

                    { transform: "scale(1)" },

                    { transform: "scale(.82)" },

                    { transform: "scale(1)" }

                ],

                {

                    duration: 180,

                    easing: "ease-out"

                }

            );

            try {

                const response = await fetch(

                    "/api/wishlist/remove/",

                    {

                        method: "DELETE",

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

                if (data.success) {

                    card.animate(

                        [

                            {

                                opacity: 1,

                                transform: "translateY(0) scale(1)"

                            },

                            {

                                opacity: 0,

                                transform: "translateY(-24px) scale(.94)"

                            }

                        ],

                        {

                            duration: 350,

                            easing: "ease"

                        }

                    );

                    setTimeout(() => {

                        card.remove();

                        updateWishlistCount(

                            data.wishlist.wishlist_count

                        );

                        if (

                            document.querySelectorAll(".wishlist-card").length === 0

                        ) {

                            location.reload();

                        }

                    }, 330);

                }

                else {

                    button.disabled = false;

                }

            }

            catch (error) {

                console.error(error);

                button.disabled = false;

            }

        });

    });

}



/* ==========================================
        UPDATE CART BADGE
========================================== */

function updateCartCount(count) {

    const badge = document.querySelector(".cart-count");

    if (!badge) return;

    badge.textContent = count;

    badge.style.display = "flex";

    badge.animate(

        [

            { transform: "scale(.7)" },

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
        UPDATE WISHLIST BADGE
========================================== */

function updateWishlistCount(count) {

    const badge = document.getElementById("wishlist-count");

    if (!badge) return;

    badge.textContent = count;

    if (count <= 0) {

        badge.style.display = "none";

        return;

    }

    badge.style.display = "flex";

    badge.animate(

        [

            { transform: "scale(.7)" },

            { transform: "scale(1.25)" },

            { transform: "scale(.92)" },

            { transform: "scale(1)" }

        ],

        {

            duration: 300,

            easing: "ease-out"

        }

    );

}

/* ==========================================
        LUXURY TOAST
========================================== */

function showLuxuryToast(productName,size){

    const toast=document.getElementById("luxury-toast");

    if(!toast) return;

    document.getElementById("toast-product").textContent=productName;

    document.getElementById("toast-size").textContent="Size • "+size;

    toast.classList.add("show");

    setTimeout(()=>{

        toast.classList.remove("show");

    },3000);

}



/* ==========================================
        CSRF TOKEN
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