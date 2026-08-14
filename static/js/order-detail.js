document.addEventListener("DOMContentLoaded", () => {

    console.log("Order Detail JS Loaded");

    const cancelBtn = document.querySelector(".cancel-btn");

    if (!cancelBtn) return;

    // ==========================================
    // MODAL ELEMENTS
    // ==========================================

    const modal = document.getElementById("cancelModal");

    const closeBtn = document.getElementById("closeCancelModal");

    const keepBtn = document.getElementById("keepOrderBtn");

    const confirmBtn = document.getElementById("confirmCancelBtn");


    // ==========================================
    // TOAST ELEMENTS
    // ==========================================

    const toast = document.getElementById("toast");

    const toastTitle = document.getElementById("toastTitle");

    const toastMessage = document.getElementById("toastMessage");


    // ==========================================
    // SHOW TOAST
    // ==========================================

    function showToast(title, message) {

        toastTitle.textContent = title;

        toastMessage.textContent = message;

        toast.classList.add("show");

        setTimeout(() => {

            toast.classList.remove("show");

        }, 3000);

    }


    // ==========================================
    // OPEN MODAL
    // ==========================================

    cancelBtn.addEventListener("click", () => {

        modal.classList.add("active");

    });


    // ==========================================
    // CLOSE MODAL
    // ==========================================

    function closeModal() {

        modal.classList.remove("active");

    }

    closeBtn.addEventListener("click", closeModal);

    keepBtn.addEventListener("click", closeModal);

    modal.addEventListener("click", (e) => {

        if (e.target === modal) {

            closeModal();

        }

    });


    // ==========================================
    // CONFIRM CANCEL
    // ==========================================

    confirmBtn.addEventListener("click", async () => {

        confirmBtn.disabled = true;

        confirmBtn.textContent = "Cancelling...";

        try {

            const response = await fetch(
                CANCEL_ORDER_API,
                {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": CSRF_TOKEN,
                        "Content-Type": "application/json",
                    },
                }
            );

            const data = await response.json();

            if (data.success) {

                closeModal();

                showToast(
                    "Success",
                    data.message
                );

                // Give the user time to read the toast
                setTimeout(() => {

                    window.location.href =
                        window.location.pathname + "?refresh=" + Date.now();

                }, 1200);

            } else {

                showToast(
                    "Error",
                    data.message
                );

                confirmBtn.disabled = false;

                confirmBtn.textContent = "Yes, Cancel";

            }

        } catch (error) {

            console.error(error);

            showToast(
                "Error",
                "Something went wrong. Please try again."
            );

            confirmBtn.disabled = false;

            confirmBtn.textContent = "Yes, Cancel";

        }

    });

});