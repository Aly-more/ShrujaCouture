// ==========================================
// CSRF TOKEN
// ==========================================

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

const csrftoken = getCookie("csrftoken");


// ==========================================
// UPDATE QUANTITY
// ==========================================

function updateQuantity(itemKey, quantity) {

    const quantityElement = document.querySelector(
        `.quantity-value[data-item-key="${itemKey}"]`
    );

    if (quantityElement) {

        quantityElement.textContent = quantity;

    }

}


// ==========================================
// UPDATE ORDER SUMMARY
// ==========================================

function updateOrderSummary(cart) {

    document.getElementById("cart-subtotal").textContent =
        `₹${cart.subtotal}`;

    document.getElementById("cart-total").textContent =
        `₹${cart.total}`;

    document.getElementById("cart-shipping").textContent =
        cart.shipping === 0
            ? "Complimentary"
            : `₹${cart.shipping}`;

}

// ==========================================
// HANDLE CART ACTION
// ==========================================

async function handleCartAction(url, method, itemKey, onSuccess) {

    try {

        const response = await fetch(url, {

            method: method,

            headers: {

                "Content-Type": "application/json",

                "X-CSRFToken": csrftoken,

            },

            body: JSON.stringify({

                item_key: itemKey

            })

        });

        const data = await response.json();

        if (!response.ok || !data.success) {

            showToast(

                data.message || "Something went wrong.",

                "",

                ""

            );

            return;

        }

        onSuccess(data);

    }

    catch (error) {

        console.error(error);

        showToast(

            "Something went wrong.",

            "",

            ""

        );

    }

}

// ==========================================
// INCREASE QUANTITY
// ==========================================

document.querySelectorAll(".increase-btn").forEach(button => {

    button.addEventListener("click", function () {

        const itemKey = this.dataset.itemKey;

        handleCartAction(

            "/api/cart/increase/",

            "PATCH",

            itemKey,

            function (data) {

                const item = data.cart.items.find(

                    cartItem => cartItem.item_key === itemKey

                );

                if (!item) return;

                updateQuantity(itemKey, item.quantity);

                updateOrderSummary(data.cart);

                updateCartBadge();

            }

        );

    });

});


// ==========================================
// DECREASE QUANTITY
// ==========================================

document.querySelectorAll(".decrease-btn").forEach(button => {

    button.addEventListener("click", function () {

        const itemKey = this.dataset.itemKey;

        handleCartAction(

            "/api/cart/decrease/",

            "PATCH",

            itemKey,

            function (data) {

                const item = data.cart.items.find(

                    cartItem => cartItem.item_key === itemKey

                );

                if (item) {

                    updateQuantity(itemKey, item.quantity);

                    updateOrderSummary(data.cart);

                    updateCartBadge();

                }

                else {

                    location.reload();

                }

            }

        );

    });

});


// ==========================================
// REMOVE ITEM
// ==========================================

document.querySelectorAll(".cart-remove-btn").forEach(button => {

    button.addEventListener("click", function () {

        const itemKey = this.dataset.itemKey;

        handleCartAction(

            "/api/cart/remove/",

            "DELETE",

            itemKey,

            function (data) {

                const card = document.querySelector(

                    `.cart-product[data-item-key="${itemKey}"]`

                );

                if (!card) return;

                card.classList.add("removing");

                setTimeout(() => {

                    card.remove();

                    updateOrderSummary(data.cart);

                    updateCartBadge();

                    if (data.cart.items.length === 0) {

                        location.reload();

                    }

                }, 350);

            }

        );

    });

});


// ==========================================
// MOVE TO WISHLIST
// ==========================================

document.querySelectorAll(".cart-wishlist-btn").forEach(button => {

    button.addEventListener("click", function () {

        const productId = Number(

            this.dataset.product

        );

        const itemKey = this.dataset.itemKey;

        const card = this.closest(".cart-product");

        fetch(

            "/api/wishlist/move-from-cart/",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "X-CSRFToken": csrftoken

                },

                body: JSON.stringify({

                    product_id: productId,

                    item_key: itemKey

                })

            }

        )

        .then(response => response.json())

        .then(async data => {

            if (!data.success) {

                showToast(

                    data.message || "Unable to move item.",

                    "",

                    ""

                );

                return;

            }

            card.classList.add("removing");

            setTimeout(() => {

                card.remove();

            }, 350);

            updateWishlistCount(

                    data.wishlist.wishlist_count

                );

                await syncWishlist();

                await updateCartBadge();

                location.reload();

        })

        .catch(error => {

            console.error(error);

            showToast(

                "Something went wrong.",

                "",

                ""

            );

        });

    });

});

// ==========================================
// LOAD CUSTOM SIZE DROPDOWNS
// ==========================================

document.querySelectorAll(".cart-size-dropdown").forEach(async (dropdown) => {

    const productId = dropdown.dataset.productId;

    const currentSize = dropdown.querySelector(".selected-size").textContent.trim();

    const trigger = dropdown.querySelector(".cart-size-trigger");

    const menu = dropdown.querySelector(".cart-size-menu");

    const status = dropdown.parentElement.querySelector(".cart-size-status");

    try {

        const response = await fetch(

            `/api/products/${productId}/sizes/`

        );

        if (!response.ok) return;

        const sizes = await response.json();

        menu.innerHTML = "";

        sizes.forEach(size => {

            const item = document.createElement("div");

            item.className = "cart-size-option";

            item.dataset.size = size.size;

            let badge = "";

            if (size.remaining_stock <= 0) {

                item.classList.add("sold-out");

                badge = "Sold Out";

            }

            else if (size.remaining_stock === 1) {

                item.classList.add("last-piece");

                badge = "Last Piece";

            }

            else if (size.remaining_stock <= 5) {

                item.classList.add("low-stock");

                badge = `Only ${size.remaining_stock} left`;

            }

            else {

                item.classList.add("normal");

            }

            if (size.size === currentSize) {

                item.classList.add("selected");

            }

            item.innerHTML = `

                <div class="cart-size-left">

                    <span class="size-name">${size.size}</span>

                </div>

                <small>${badge}</small>

            `;

            menu.appendChild(item);

        });

    }

    catch (error) {

        console.error(error);

    }

});

// ==========================================
// TOGGLE CUSTOM DROPDOWN
// ==========================================

document.addEventListener("click", function (event) {

    // Close all dropdowns first

    document.querySelectorAll(".cart-size-dropdown").forEach(dropdown => {

        if (!dropdown.contains(event.target)) {

            dropdown.classList.remove("open");

            dropdown.querySelector(".cart-size-trigger")
                .classList.remove("open");

        }

    });

    // Open clicked dropdown

    const trigger = event.target.closest(".cart-size-trigger");

    if (!trigger) return;

    const dropdown = trigger.closest(".cart-size-dropdown");

    dropdown.classList.toggle("open");

    trigger.classList.toggle("open");

});

// ==========================================
// SELECT SIZE
// ==========================================

document.addEventListener("click", async function (event) {

    const option = event.target.closest(".cart-size-option");

    if (!option) return;

    const dropdown = option.closest(".cart-size-dropdown");

    const trigger = dropdown.querySelector(".cart-size-trigger");

    const selectedText = trigger.querySelector(".selected-size");

    const itemKey = dropdown.dataset.itemKey;

    const newSize = option.dataset.size;

    // ==========================================
    // UPDATE UI IMMEDIATELY
    // ==========================================

    selectedText.innerHTML = `
        <span class="size-name">${newSize}</span>
    `;

    dropdown.querySelectorAll(".cart-size-option").forEach(item => {

        item.classList.remove("selected");

    });

    option.classList.add("selected");

    dropdown.classList.remove("open");

    trigger.classList.remove("open");

    try {

        const response = await fetch(

            "/cart/change-size/",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/x-www-form-urlencoded",

                    "X-CSRFToken": csrftoken,

                },

                body: new URLSearchParams({

                    item_key: itemKey,

                    size: newSize,

                }),

            }

        );

        const data = await response.json();

        if (!data.success) {

            showToast(

                "Unable to Change Size",

                data.message

            );

            location.reload();

            return;

        }

        // ==========================================
        // ITEM MERGED
        // ==========================================

        if (data.merged) {

            const removedCard = document.querySelector(

                `.cart-product[data-item-key="${data.removed_item_key}"]`

            );

            if (removedCard) {

                removedCard.classList.add("removing");

                setTimeout(() => {

                    removedCard.remove();

                }, 350);

            }

        }

        // ==========================================
        // UPDATE QUANTITY
        // ==========================================

        const quantityElement = document.querySelector(

            `.quantity-value[data-item-key="${data.updated_item_key}"]`

        );

        if (quantityElement) {

            quantityElement.textContent = data.adjusted_quantity;

        }

        // ==========================================
        // UPDATE ORDER SUMMARY
        // ==========================================

        updateOrderSummary(data.cart);

        updateCartBadge();

        // ==========================================
        // TOAST
        // ==========================================

        if (data.merged) {

            showToast(

                "Quantity Updated",

                `${newSize} size quantity is now ${data.adjusted_quantity}.`

            );

        }

        else if (data.quantity_adjusted) {

            showToast(

                "Quantity Adjusted",

                `Only ${data.adjusted_quantity} piece${data.adjusted_quantity > 1 ? "s" : ""} available.`

            );

        }

        else {

            showToast(

                "Size Updated",

                `Changed to ${newSize}`

            );

        }

    }

    catch (error) {

        console.error(error);

        showToast(

            "Error",

            "Unable to update size."

        );

    }

});
