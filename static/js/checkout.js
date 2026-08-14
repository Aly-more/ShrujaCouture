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
// PROCEED TO PAYMENT
// ==========================================

const paymentButton = document.getElementById(
    "proceed-payment-btn"
);

if (paymentButton) {

    paymentButton.addEventListener("click", function () {

        const selectedAddress = document.querySelector(
            'input[name="address"]:checked'
        );

        if (!selectedAddress) {

            showToast(

                "Address Required",

                "Please select a delivery address before proceeding.",

                "error"

            );

            return;

        }

        paymentButton.disabled = true;
        paymentButton.innerText = "Processing...";

        placeOrder(selectedAddress.value);

    });

}


// ==========================================
// PLACE ORDER
// ==========================================

function placeOrder(addressId) {

    fetch("/api/orders/place/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "X-CSRFToken": csrftoken

        },

        body: JSON.stringify({

            address_id: Number(addressId)

        })

    })

    .then(response => response.json())

    .then(data => {

        if (!data.success) {

            paymentButton.disabled = false;

            paymentButton.innerText = "Proceed to Payment";

            showToast(

                "Order Failed",

                data.message,

                "error"

            );

            return;

        }

        console.log("Order Created:", data);

        createPayment(data.order.id);

    })

    .catch(error => {

        console.error(error);

        paymentButton.disabled = false;
        paymentButton.innerText = "Proceed to Payment";

    });

}


// ==========================================
// CREATE PAYMENT
// ==========================================

function createPayment(orderId) {

    fetch("/api/payments/create/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "X-CSRFToken": csrftoken

        },

        body: JSON.stringify({

            order_id: orderId

        })

    })

    .then(response => response.json())

    .then(data => {

        if (!data.success) {

            paymentButton.disabled = false;

            paymentButton.innerText = "Proceed to Payment";

            showToast(

                "Payment Error",

                data.message,

                "error"

            );

            return;

        }

        console.log("Payment Created:", data);

        openRazorpay(data.payment);

    })

    .catch(error => {

        console.error(error);

        paymentButton.disabled = false;
        paymentButton.innerText = "Proceed to Payment";

    });

}


// ==========================================
// OPEN RAZORPAY
// ==========================================

function openRazorpay(payment) {

    const options = {

        key: payment.key,

        amount: payment.amount,

        currency: payment.currency,

        name: "Shruja Couture",

        description: "Order Payment",

        image: "/static/images/logo4.png",

        order_id: payment.razorpay_order_id,

        handler: function (response) {

            verifyPayment(

                response.razorpay_order_id,

                response.razorpay_payment_id,

                response.razorpay_signature

            );

        },

        modal: {

            ondismiss: function () {

                paymentButton.disabled = false;
                paymentButton.innerText = "Proceed to Payment";

                console.log("Payment popup closed.");

            }

        },

        theme: {

            color: "#A65E3B"

        }

    };

    const rzp = new Razorpay(options);

    // ==========================================
    // PAYMENT FAILED
    // ==========================================

    rzp.on("payment.failed", function (response) {

        console.log("Payment Failed:", response.error);

        paymentButton.disabled = false;
        paymentButton.innerText = "Proceed to Payment";

        alert("❌ Payment Failed. Please try again.");

    });

    rzp.open();

}

// ==========================================
// VERIFY PAYMENT
// ==========================================

async function verifyPayment(orderId, paymentId, signature) {

    try {

        const response = await fetch("/api/payments/verify/", {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "X-CSRFToken": csrftoken

            },

            body: JSON.stringify({

                razorpay_order_id: orderId,

                razorpay_payment_id: paymentId,

                razorpay_signature: signature

            })

        });

        const data = await response.json();

        console.log("Payment Verification:", data);

        paymentButton.disabled = false;
        paymentButton.innerText = "Proceed to Payment";

        if (!data.success) {

            alert(data.message);

            return;

        }

        alert("🎉 Payment Successful!");

        // ==========================================
        // UPDATE GLOBAL CART BADGE
        // ==========================================

        if (typeof updateCartBadge === "function") {

            await updateCartBadge();

        }

        window.location.href = ORDER_SUCCESS_URL;

    }

    catch (error) {

        console.error(error);

        paymentButton.disabled = false;
        paymentButton.innerText = "Proceed to Payment";

        alert("Payment verification failed.");

    }

}

// ==========================================
// ADDRESS MODAL
// ==========================================

const addressModal = document.getElementById("addressModal");

const addAddressBtn = document.getElementById("checkout-add-address");

const addFirstAddressBtn = document.getElementById("checkout-add-first-address");

const closeAddressModal = document.querySelector(".address-modal-close");

const modalTitle = document.getElementById("addressModalTitle");

const submitAddressButton = document.getElementById("addressSubmitBtn");

const editingAddressId = document.getElementById("editingAddressId");

// ==========================================
// CONFIRM DELETE MODAL
// ==========================================

const confirmModal = document.getElementById(
    "confirmModal"
);

const confirmDeleteBtn = document.getElementById(
    "confirmDeleteBtn"
);

const confirmCancelBtn = document.getElementById(
    "confirmCancelBtn"
);

const confirmCloseBtn = document.querySelector(
    ".confirm-modal-close"
);

let addressToDelete = null;

// ==========================================
// TOAST NOTIFICATION
// ==========================================

const checkoutToast = document.getElementById(
    "checkoutToast"
);

const checkoutToastTitle = document.getElementById(
    "checkoutToastTitle"
);

const checkoutToastMessage = document.getElementById(
    "checkoutToastMessage"
);

const checkoutToastClose = document.getElementById(
    "checkoutToastClose"
);

let toastTimer;

// ==========================================
// SHOW TOAST
// ==========================================

function showToast(title, message, type = "success") {

    checkoutToastTitle.textContent = title;

    checkoutToastMessage.textContent = message;

    checkoutToast.classList.remove(

        "success",

        "error"

    );

    checkoutToast.classList.add(type);

    checkoutToast.classList.add("show");

    if (window.lucide) {

        lucide.createIcons();

    }

    clearTimeout(toastTimer);

    toastTimer = setTimeout(

        hideToast,

        2500

    );

}


// ==========================================
// HIDE TOAST
// ==========================================

function hideToast() {

    checkoutToast.classList.remove("show");

}

checkoutToastClose?.addEventListener(

    "click",

    hideToast

);

function openAddressModal(){

    if(!addressModal) return;

    addressModal.classList.add("show");

}

function closeModal(){

    if(!addressModal) return;

    addressModal.classList.remove("show");

}



// ==========================================
// CLOSE BUTTON
// ==========================================

if(closeAddressModal){

    closeAddressModal.addEventListener("click", closeModal);

}

// ==========================================
// CLICK OUTSIDE
// ==========================================

if(addressModal){

    addressModal.addEventListener("click", function(event){

        if(event.target === addressModal){

            closeModal();

        }

    });

}

// ==========================================
// ESC KEY
// ==========================================

document.addEventListener("keydown", function(event){

    if(event.key === "Escape"){

        closeModal();

    }

});

// ==========================================
// SAVE ADDRESS
// ==========================================

const addressForm = document.getElementById(
    "checkout-address-form"
);

if (addressForm) {

    addressForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const submitButton = addressForm.querySelector(
            'button[type="submit"]'
        );

        const isEditing = editingAddressId.value !== "";

        submitButton.disabled = true;

        submitButton.textContent = isEditing
            ? "Saving Changes..."
            : "Saving Address...";

        const formData = new FormData(addressForm);

        try {

            const url = isEditing
                ? `/api/checkout/address/${editingAddressId.value}/`
                : "/api/checkout/address/create/";

            const method = isEditing
                ? "PUT"
                : "POST";

            const response = await fetch(

                url,

                {

                    method,

                    headers: {

                        "X-CSRFToken": csrftoken,

                    },

                    body: formData,

                }

            );

            const data = await response.json();

            if (!response.ok) {

                console.log(data);

                submitButton.disabled = false;

                submitButton.textContent = isEditing
                    ? "Save Changes"
                    : "Save Address";

                return;

            }

            closeModal();

            addressForm.reset();

            editingAddressId.value = "";

            modalTitle.textContent = "Add New Address";

            submitAddressButton.textContent = "Save Address";

            submitButton.disabled = false;

            submitButton.textContent = "Save Address";

            await refreshAddresses();

            showToast(

                "Success",

                isEditing
                    ? "Address updated successfully."
                    : "Address saved successfully."

            );

        }

        catch (error) {

            console.error(error);

            submitButton.disabled = false;

            submitButton.textContent = isEditing
                ? "Save Changes"
                : "Save Address";

        }

    });

}


// ==========================================
// INITIALIZE ADDRESS EVENTS
// ==========================================

function initializeAddressEvents() {

    // ==========================================
    // ADD NEW ADDRESS
    // ==========================================

    document.querySelector("#checkout-add-address")?.addEventListener(

        "click",

        function () {

            editingAddressId.value = "";

            addressForm.reset();

            modalTitle.textContent = "Add New Address";

            submitAddressButton.textContent = "Save Address";

            openAddressModal();

            addressForm.full_name.focus();

        }

    );

    document.querySelector("#checkout-add-first-address")?.addEventListener(

        "click",

        function () {

            editingAddressId.value = "";

            addressForm.reset();

            modalTitle.textContent = "Add New Address";

            submitAddressButton.textContent = "Save Address";

            openAddressModal();

            addressForm.full_name.focus();

        }

    );

    // ==========================================
    // EDIT ADDRESS
    // ==========================================

    document.querySelectorAll(".address-edit-btn").forEach(button => {

        button.addEventListener("click", function () {

            editingAddressId.value = this.dataset.address;

            modalTitle.textContent = "Edit Address";

            submitAddressButton.textContent = "Save Changes";

            addressForm.reset();

            addressForm.full_name.value = this.dataset.fullName;

            addressForm.phone_number.value = this.dataset.phone;

            addressForm.address_line_1.value = this.dataset.address1;

            addressForm.address_line_2.value = this.dataset.address2 || "";

            addressForm.city.value = this.dataset.city;

            addressForm.state.value = this.dataset.state;

            addressForm.postal_code.value = this.dataset.postal;

            addressForm.is_default.checked = (

                this.dataset.default === "true"

            );

            openAddressModal();

            addressForm.full_name.focus();

        });

    });

    // ==========================================
    // DELETE ADDRESS
    // ==========================================

    document.querySelectorAll(".address-delete-btn").forEach(button => {

        button.addEventListener("click", function () {

            addressToDelete = this.dataset.address;

            confirmModal.classList.add("show");

        });

    });

}


// ==========================================
// REFRESH ADDRESSES
// ==========================================

async function refreshAddresses() {

    try {

        const response = await fetch(

            "/checkout/address-list/"

        );

        const data = await response.json();

        document.querySelector(

            ".checkout-form"

        ).innerHTML = data.html;

        initializeAddressEvents();

        if (window.lucide) {

            lucide.createIcons();

        }

    }

    catch (error) {

        console.error(error);

    }

}

initializeAddressEvents();


// ==========================================
// CONFIRM DELETE
// ==========================================

if (confirmDeleteBtn) {

    confirmDeleteBtn.addEventListener("click", async function () {

        if (!addressToDelete) {

            return;

        }

        try {

            const response = await fetch(

                `/api/checkout/address/${addressToDelete}/delete/`,

                {

                    method: "DELETE",

                    headers: {

                        "X-CSRFToken": csrftoken,

                    },

                }

            );

            const data = await response.json();

            if (!response.ok) {

                alert(data.message);

                return;

            }

            confirmModal.classList.remove("show");

            addressToDelete = null;

            await refreshAddresses();

            showToast(

                "Success",

                "Address deleted successfully."

            );

        }

        catch (error) {

            console.error(error);

        }

    });

}


// ==========================================
// CLOSE CONFIRM MODAL
// ==========================================

function closeConfirmModal() {

    confirmModal.classList.remove("show");

    addressToDelete = null;

}

confirmCancelBtn?.addEventListener(

    "click",

    closeConfirmModal

);

confirmCloseBtn?.addEventListener(

    "click",

    closeConfirmModal

);

confirmModal?.addEventListener(

    "click",

    function(event){

        if(event.target === confirmModal){

            closeConfirmModal();

        }

    }

);

document.addEventListener(

    "keydown",

    function(event){

        if(event.key === "Escape"){

            closeConfirmModal();

        }

    }

);