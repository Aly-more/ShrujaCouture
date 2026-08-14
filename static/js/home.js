const modal = document.getElementById("quickAddModal");
const modalTitle = document.getElementById("modalProductName");
const modalSizes = document.getElementById("modalSizes");
const modalAddBtn = document.getElementById("modalAddBtn");

const closeBtn = document.querySelector(".close-modal");
const buttons = document.querySelectorAll(".quick-add-btn");

let selectedProduct = null;
let selectedSize = null;


// ==========================================
// GET CSRF TOKEN
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

// ==========================================
// OPEN QUICK ADD MODAL
// ==========================================

buttons.forEach(button => {

    button.addEventListener("click", async function () {

        selectedProduct = this.dataset.productId;
        selectedSize = null;

        modal.classList.add("active");

        modalTitle.innerText = this.dataset.productName;

        modalSizes.innerHTML = "Loading sizes...";

        modalAddBtn.disabled = false;
        modalAddBtn.classList.remove("success");
        modalAddBtn.innerHTML = "Add to Bag";

        try {

            const response = await fetch(
                `/api/products/${selectedProduct}/sizes/`
            );

            const sizes = await response.json();

            modalSizes.innerHTML = "";

            if (sizes.length === 0) {

                modalSizes.innerHTML =
                    "<p>No sizes available.</p>";

                modalAddBtn.disabled = true;
                modalAddBtn.innerHTML = "Out of Stock";

                return;

            }

            let availableSizeFound = false;

            sizes.forEach(size => {

                const btn = document.createElement("button");

                btn.type = "button";

                btn.className = "modal-size";

                btn.innerText = size.size;

                const stock =
                    size.remaining_stock !== undefined
                        ? size.remaining_stock
                        : size.stock;

                if (stock <= 0) {

                    btn.disabled = true;

                    btn.classList.add("disabled-size");

                }

                else {

                    availableSizeFound = true;

                }

                btn.addEventListener("click", function () {

                    document
                        .querySelectorAll(".modal-size")
                        .forEach(b => {

                            b.classList.remove("selected-size");

                        });

                    btn.classList.add("selected-size");

                    selectedSize = size.size;

                    modalAddBtn.disabled = false;

                    modalAddBtn.innerHTML = "Add to Bag";

                });

                modalSizes.appendChild(btn);

            });

            // ==========================================
            // ALL SIZES SOLD OUT
            // ==========================================

            if (!availableSizeFound) {

                modalAddBtn.disabled = true;

                modalAddBtn.innerHTML = "Out of Stock";

            }

        }

        catch (error) {

            console.error(error);

            modalSizes.innerHTML =
                "<p>Unable to load sizes.</p>";

            modalAddBtn.disabled = true;

            modalAddBtn.innerHTML = "Out of Stock";

        }

    });

});

// ==========================================
// ADD TO CART
// ==========================================

modalAddBtn.addEventListener("click", async function () {

    if (!selectedSize) {

        showToast(
            "Select Size",
            "Please select a size first."
        );

        return;

    }

    modalAddBtn.disabled = true;

    modalAddBtn.innerHTML = "Adding...";

    try {

        const response = await fetch("/cart/quick-add/", {

            method: "POST",

            headers: {

                "X-CSRFToken": getCookie("csrftoken"),

                "Content-Type":
                    "application/x-www-form-urlencoded",

            },

            body: new URLSearchParams({

                product_id: selectedProduct,

                selected_size: selectedSize

            })

        });

        const data = await response.json();

        if (data.success) {

            // ==========================================
            // UPDATE GLOBAL CART BADGE
            // ==========================================

            if (typeof updateCartBadge === "function") {

                await updateCartBadge();

            }

            modalAddBtn.classList.add("success");

            modalAddBtn.innerHTML = `
                <i data-lucide="check"></i>
                Added
            `;

            if (window.lucide) {

                lucide.createIcons();

            }

            setTimeout(() => {

                modal.classList.remove("active");

                showToast(
                    "Added to Bag",
                    modalTitle.innerText,
                    selectedSize
                );

                modalAddBtn.disabled = false;

                modalAddBtn.classList.remove("success");

                modalAddBtn.innerHTML = "Add to Bag";

            }, 700);

        }

        else {

            showToast(
                "Unable to Add",
                data.message
            );

            const availableSizes = document.querySelectorAll(
                ".modal-size:not(.disabled-size)"
            );

            if (availableSizes.length > 0) {

                modalAddBtn.disabled = false;

                modalAddBtn.innerHTML = "Add to Bag";

            }

            else {

                modalAddBtn.disabled = true;

                modalAddBtn.innerHTML = "Out of Stock";

            }

        }

    }

    catch (error) {

        console.error(error);

        showToast(
            "Error",
            "Something went wrong."
        );

        const availableSizes = document.querySelectorAll(
            ".modal-size:not(.disabled-size)"
        );

        if (availableSizes.length > 0) {

            modalAddBtn.disabled = false;

            modalAddBtn.innerHTML = "Add to Bag";

        }

        else {

            modalAddBtn.disabled = true;

            modalAddBtn.innerHTML = "Out of Stock";

        }

    }

});


// ==========================================
// CLOSE MODAL
// ==========================================

closeBtn.onclick = function () {

    modal.classList.remove("active");

};

window.onclick = function (event) {

    if (event.target === modal) {

        modal.classList.remove("active");

    }

};