// ==========================================
// SHRUJA COUTURE TOAST
// ==========================================

function showToast(title, product = "", size = "") {

    const toast = document.getElementById("luxury-toast");

    if (!toast) return;

    const titleElement = document.getElementById("toast-title");
    const productElement = document.getElementById("toast-product");
    const sizeElement = document.getElementById("toast-size");

    // ==========================================
    // TITLE
    // ==========================================

    titleElement.textContent = title;

    // ==========================================
    // PRODUCT
    // ==========================================

    if (product) {

        productElement.textContent = product;

        productElement.style.display = "block";

    }

    else {

        productElement.textContent = "";

        productElement.style.display = "none";

    }

    // ==========================================
    // SIZE
    // ==========================================

    if (size) {

        sizeElement.textContent = size;

        sizeElement.style.display = "block";

    }

    else {

        sizeElement.textContent = "";

        sizeElement.style.display = "none";

    }

    // ==========================================
    // SHOW TOAST
    // ==========================================

    toast.classList.add("show");

    if (window.lucide) {

        lucide.createIcons();

    }

    clearTimeout(window.toastTimer);

    window.toastTimer = setTimeout(() => {

        toast.classList.remove("show");

    }, 3500);

}