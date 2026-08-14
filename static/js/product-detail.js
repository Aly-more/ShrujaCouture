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
// PRODUCT IMAGE GALLERY
// ==========================================

const thumbnails = document.querySelectorAll(".thumbnail");

const mainImage = document.getElementById("mainProductImage");

const imageContainer = document.querySelector(".main-image");

thumbnails.forEach((thumbnail) => {

    thumbnail.addEventListener("click", () => {

        thumbnails.forEach((img) => {

            img.classList.remove("active");

        });

        thumbnail.classList.add("active");

        mainImage.style.opacity = "0";

        setTimeout(() => {

            mainImage.src = thumbnail.src;

            mainImage.style.opacity = "1";

        }, 180);

    });

});


// ==========================================
// LUXURY IMAGE ZOOM
// ==========================================

if (imageContainer && mainImage) {

    imageContainer.addEventListener("mousemove", (e) => {

        const rect = imageContainer.getBoundingClientRect();

        const x = ((e.clientX - rect.left) / rect.width) * 100;

        const y = ((e.clientY - rect.top) / rect.height) * 100;

        mainImage.style.transformOrigin = `${x}% ${y}%`;

        mainImage.style.transform = "scale(2)";

    });

    imageContainer.addEventListener("mouseleave", () => {

        mainImage.style.transformOrigin = "center";

        mainImage.style.transform = "scale(1)";

    });

}


// ==========================================
// GLOBAL ELEMENTS
// ==========================================

const sizeButtons = document.querySelectorAll(".size-btn");

const selectedSize = document.getElementById("selected-size");

const minusBtn = document.getElementById("minusQty");

const plusBtn = document.getElementById("plusQty");

const quantityInput = document.getElementById("quantity");

const cartForm = document.getElementById("addToCartForm");

const addToCartBtn = document.getElementById("addToCartBtn");

const stockText = document.getElementById("stockText");

const stockIcon = document.getElementById("stockIcon");

if (stockIcon && stockText.textContent.trim() === "Select a size") {

    stockIcon.style.display = "none";

}

/* ==========================================
        SIZE SELECTION
========================================== */

sizeButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const stock = Number(button.dataset.stock);

        // ==========================================
        // REMOVE ACTIVE STATE
        // ==========================================

        sizeButtons.forEach((btn) => {

            btn.classList.remove("active");

        });

        // ==========================================
        // ACTIVATE SELECTED SIZE
        // ==========================================

        button.classList.add("active");

        selectedSize.value = button.dataset.size;

        // ==========================================
        // SOLD OUT
        // ==========================================

        if (stock <= 0) {

            quantityInput.value = 0;

            quantityInput.disabled = true;

            plusBtn.disabled = true;

            minusBtn.disabled = true;

            plusBtn.classList.add("disabled");

            minusBtn.classList.add("disabled");

            stockText.textContent = "Out of Stock";

            stockText.style.color = "#D74C4C";

            addToCartBtn.disabled = true;

            addToCartBtn.textContent = "Out of Stock";

            return;

        }

        // ==========================================
        // ENABLE QUANTITY
        // ==========================================

        quantityInput.value = 1;

        quantityInput.disabled = false;

        plusBtn.disabled = false;

        minusBtn.disabled = false;

        plusBtn.classList.remove("disabled");

        minusBtn.classList.remove("disabled");

        // ==========================================
        // LOW STOCK MESSAGE
        // ==========================================

        if (stock === 1) {

            stockText.textContent = "Only 1 piece left";

            stockText.style.color = "#169B62";

        }

        else if (stock <= 5) {

            stockText.textContent = `Only ${stock} pieces left`;

            stockText.style.color = "#169B62";

        }

        else {

            stockText.textContent = "";

        }

        // ==========================================
        // ENABLE BUTTON
        // ==========================================

        addToCartBtn.disabled = false;

        addToCartBtn.textContent = "Add to Bag";

    });

});

/* ==========================================
        UPDATE REMAINING STOCK
========================================== */

async function updateRemainingStock() {

    if (!cartForm) return;

    try {

        const response = await fetch(

            `/api/products/${cartForm.dataset.productId}/sizes/`

        );

        if (!response.ok) return;

        const variants = await response.json();

        variants.forEach((variant) => {

            const button = document.querySelector(

                `.size-btn[data-size="${variant.size}"]`

            );

            if (!button) return;

            // ==========================================
            // UPDATE REMAINING STOCK
            // ==========================================

            button.dataset.stock = variant.remaining_stock;

            // ==========================================
            // SIZE LABEL
            // ==========================================

            button.textContent = variant.size;

            const stockLabel = button.parentElement.querySelector(".size-stock");

            stockLabel.className = "size-stock";

            if (variant.remaining_stock <= 0) {

                stockLabel.textContent = "Sold Out";

                stockLabel.classList.add("sold-out");

            }

            else if (variant.remaining_stock === 1) {

                stockLabel.textContent = "Last Piece";

                stockLabel.classList.add("last-piece");

            }

            else if (variant.remaining_stock <= 3) {

                stockLabel.textContent = `Only ${variant.remaining_stock} left`;

                stockLabel.classList.add("low-stock");

            }

            else {

                stockLabel.textContent = "";

            }

            // ==========================================
            // ENABLE / DISABLE BUTTON ONLY
            // ==========================================
            if (variant.remaining_stock === 0) {

                // Keep it clickable
                button.disabled = false;

                button.classList.add("disabled");

            }

            else {

                button.disabled = false;

                button.classList.remove("disabled");

            }

        });

        // ==========================================
        // REFRESH CURRENTLY SELECTED SIZE
        // ==========================================

        const activeButton = document.querySelector(".size-btn.active");

        if (activeButton) {

            activeButton.click();

        }

    }

    catch (error) {

        console.error(error);

    }

}

/* ==========================================
        QUANTITY
========================================== */

if (minusBtn && plusBtn && quantityInput) {

    minusBtn.addEventListener("click", () => {

        if (quantityInput.disabled) return;

        if (Number(quantityInput.value) > 1) {

            quantityInput.value--;

        }

    });

    plusBtn.addEventListener("click", () => {

        if (quantityInput.disabled) return;

        const activeSize = document.querySelector(".size-btn.active");

        if (!activeSize) {

            showToast(
                "Please select a size."
            );

            return;

        }

        const stock = Number(activeSize.dataset.stock);

        const quantity = Number(quantityInput.value);

        if (quantity >= stock) {

            showToast(
                `Only ${stock} piece${stock > 1 ? "s" : ""} available.`
            );

            return;

        }

        quantityInput.value++;

    });

}

/* ==========================================
        AJAX ADD TO CART
========================================== */

if (cartForm) {

    cartForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        if (selectedSize.value === "") {

            showToast(
                "Please select a size."
            );

            return;

        }

        addToCartBtn.disabled = true;

        addToCartBtn.textContent = "Adding...";

        try {

            const response = await fetch(

                "/api/cart/add/",

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json",

                        "X-CSRFToken": csrftoken

                    },

                    body: JSON.stringify({

                        product_id: Number(
                            cartForm.dataset.productId
                        ),

                        selected_size: selectedSize.value,

                        quantity: Number(
                            quantityInput.value
                        )

                    })

                }

            );

            const data = await response.json();

            if (!response.ok || !data.success) {

                showToast(

                    data.message || "Unable to add to bag."

                );

                addToCartBtn.disabled = false;

                addToCartBtn.textContent = "Add to Bag";

                return;

            }

            // ==========================
            // SUCCESS
            // ==========================

            showToast(

                "Added to Bag",

                document.querySelector("h1").textContent,

                `Size ${selectedSize.value}`

            );

            // ==========================================
            // UPDATE GLOBAL CART BADGE
            // ==========================================

            if (typeof updateCartBadge === "function") {

                await updateCartBadge();

            }

            // ==========================================
            // UPDATE WISHLIST BADGE
            // ==========================================

            const wishlistBadge = document.getElementById("wishlist-count");

            if (

                wishlistBadge &&

                data.wishlist_count !== undefined

            ) {

                if (data.wishlist_count > 0) {

                    wishlistBadge.style.display = "flex";

                    wishlistBadge.textContent = data.wishlist_count;

                }

                else {

                    wishlistBadge.style.display = "none";

                }

            }

            // ==========================================
            // REFRESH STOCK
            // ==========================================

            await updateRemainingStock();

            // ==========================================
            // RESET QUANTITY
            // ==========================================

            quantityInput.value =

                quantityInput.disabled ? 0 : 1;

            // ==========================================
            // RESTORE BUTTON ONLY IF AVAILABLE
            // ==========================================

            if (!addToCartBtn.disabled) {

                addToCartBtn.textContent = "Add to Bag";

            }

        }

        catch (error) {

            console.error(error);

            showToast(

                "Something went wrong."

            );

            if (!addToCartBtn.disabled) {

                addToCartBtn.textContent = "Add to Bag";

            }

            addToCartBtn.disabled = false;

        }

    });

}


/* ==========================================
        ACCORDION
========================================== */

const accordionHeaders = document.querySelectorAll(".accordion-header");

accordionHeaders.forEach((header) => {

    header.addEventListener("click", () => {

        const item = header.parentElement;

        item.classList.toggle("active");

        const icon = header.querySelector("span");

        icon.textContent = item.classList.contains("active")

            ? "−"

            : "+";

    });

});

/* ==========================================
        PAGE INITIALIZATION
========================================== */

window.addEventListener("DOMContentLoaded", async () => {

    // Sync stock with current cart
    await updateRemainingStock();

    // Restore stock when user comes back from Cart page
    window.addEventListener("focus", async () => {

        await updateRemainingStock();

    });

});

/* ==========================================
        PAGE RESTORED FROM BACK BUTTON
========================================== */
window.addEventListener("pageshow", async function () {

    await updateRemainingStock();

    if (typeof updateCartBadge === "function") {

        await updateCartBadge();

    }

});