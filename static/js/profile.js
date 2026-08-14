/* =====================================================
        SHRUJA COUTURE — PROFILE
===================================================== */

document.addEventListener("DOMContentLoaded", function () {


    /* =====================================================
            EDIT PROFILE MODAL — ELEMENTS
    ===================================================== */

    const profileModal =
        document.getElementById("editProfileModal");

    const openProfileButton =
        document.getElementById("openEditProfile");

    const closeProfileButton =
        document.getElementById("closeEditProfile");

    const profileCloseElements =
        document.querySelectorAll(
            "[data-close-profile-modal]"
        );


    /* =====================================================
            ADDRESS MODAL — ELEMENTS
    ===================================================== */

    const addressModal =
        document.getElementById("addAddressModal");

    const openAddressButton =
        document.getElementById("openAddAddress");

    const openFirstAddressButton =
        document.getElementById("openFirstAddress");

    const closeAddressButton =
        document.getElementById("closeAddAddress");

    const addressCloseElements =
        document.querySelectorAll(
            "[data-close-address-modal]"
        );

    const addressForm =
        document.getElementById("addAddressForm");

    const addressFormAction =
        document.getElementById("addressFormAction");

    const addressIdInput =
        document.getElementById("address_id");

    const addressModalTitle =
        document.getElementById("addAddressTitle");

    const addressModalDescription =
        document.getElementById(
            "addressModalDescription"
        );

    const addressSubmitText =
        document.getElementById(
            "addressSubmitText"
        );

    const editAddressButtons =
        document.querySelectorAll(
            ".edit-address-btn"
        );


    /* =====================================================
            REMOVE ADDRESS MODAL — ELEMENTS
    ===================================================== */

    const removeAddressModal =
        document.getElementById(
            "removeAddressModal"
        );

    const removeAddressButtons =
        document.querySelectorAll(
            ".remove-address-btn"
        );

    const closeRemoveAddressButton =
        document.getElementById(
            "closeRemoveAddress"
        );

    const removeAddressCloseElements =
        document.querySelectorAll(
            "[data-close-remove-address-modal]"
        );

    const removeAddressIdInput =
        document.getElementById(
            "removeAddressId"
        );

    const removeAddressName =
        document.getElementById(
            "removeAddressName"
        );


    /* =====================================================
            ADDRESS OPTIONS MENU — ELEMENTS
    ===================================================== */

    const addressMenuTriggers =
        document.querySelectorAll(
            ".address-menu-trigger"
        );


    /* =====================================================
            CHANGE PASSWORD MODAL — ELEMENTS
    ===================================================== */

    const changePasswordModal =
        document.getElementById(
            "changePasswordModal"
        );

    const openChangePasswordButton =
        document.getElementById(
            "openChangePassword"
        );

    const closeChangePasswordButton =
        document.getElementById(
            "closeChangePassword"
        );

    const passwordCloseElements =
        document.querySelectorAll(
            "[data-close-password-modal]"
        );

    const changePasswordForm =
        document.getElementById(
            "changePasswordForm"
        );

    const passwordToggleButtons =
        document.querySelectorAll(
            "[data-password-toggle]"
        );

    const passwordModalReopen =
        document.querySelector(
            '[data-password-modal-reopen="true"]'
        );


    /* =====================================================
            BODY SCROLL
    ===================================================== */

    function updateBodyScroll() {

        const profileOpen =
            profileModal &&
            profileModal.classList.contains(
                "active"
            );

        const addressOpen =
            addressModal &&
            addressModal.classList.contains(
                "active"
            );

        const removeAddressOpen =
            removeAddressModal &&
            removeAddressModal.classList.contains(
                "active"
            );

        const changePasswordOpen =
            changePasswordModal &&
            changePasswordModal.classList.contains(
                "active"
            );


        if (
            profileOpen ||
            addressOpen ||
            removeAddressOpen ||
            changePasswordOpen
        ) {

            document.body.classList.add(
                "profile-modal-open"
            );

        } else {

            document.body.classList.remove(
                "profile-modal-open"
            );

        }

    }


    /* =====================================================
            OPEN EDIT PROFILE MODAL
    ===================================================== */

    function openProfileModal() {

        if (!profileModal) return;


        profileModal.classList.add(
            "active"
        );

        profileModal.setAttribute(
            "aria-hidden",
            "false"
        );


        updateBodyScroll();

    }


    /* =====================================================
            CLOSE EDIT PROFILE MODAL
    ===================================================== */

    function closeProfileModal() {

        if (!profileModal) return;


        profileModal.classList.remove(
            "active"
        );

        profileModal.setAttribute(
            "aria-hidden",
            "true"
        );


        updateBodyScroll();

    }


    /* =====================================================
            OPEN CHANGE PASSWORD MODAL
    ===================================================== */

    function openChangePasswordModal() {

        if (!changePasswordModal) return;


        changePasswordModal.classList.add(
            "active"
        );

        changePasswordModal.setAttribute(
            "aria-hidden",
            "false"
        );


        updateBodyScroll();


        const currentPasswordInput =
            document.getElementById(
                "current_password"
            );


        if (currentPasswordInput) {

            setTimeout(
                function () {

                    currentPasswordInput.focus();

                },
                150
            );

        }


        refreshLucideIcons();

    }


    /* =====================================================
            RESET CHANGE PASSWORD FORM
    ===================================================== */

    function resetChangePasswordForm() {

        if (changePasswordForm) {

            changePasswordForm.reset();

        }


        passwordToggleButtons.forEach(
            function (button) {

                const targetId =
                    button.dataset.passwordToggle;

                const input =
                    document.getElementById(
                        targetId
                    );


                if (input) {

                    input.type =
                        "password";

                }


                button.setAttribute(
                    "aria-pressed",
                    "false"
                );

                button.setAttribute(
                    "aria-label",
                    "Show password"
                );

                button.innerHTML =
                    '<i data-lucide="eye"></i>';

            }
        );


        refreshLucideIcons();

    }


    /* =====================================================
            CLOSE CHANGE PASSWORD MODAL
    ===================================================== */

    function closeChangePasswordModal() {

        if (!changePasswordModal) return;


        changePasswordModal.classList.remove(
            "active"
        );

        changePasswordModal.setAttribute(
            "aria-hidden",
            "true"
        );


        resetChangePasswordForm();

        updateBodyScroll();

    }


    /* =====================================================
            RESET ADDRESS FORM — ADD MODE
    ===================================================== */

    function resetAddressFormForAdd() {

        if (!addressForm) return;


        addressForm.reset();


        /* =============================================
                ACTION
        ============================================= */

        if (addressFormAction) {

            addressFormAction.value =
                "add_address";

        }


        /* =============================================
                ADDRESS ID
        ============================================= */

        if (addressIdInput) {

            addressIdInput.value = "";

        }


        /* =============================================
                MODAL TEXT
        ============================================= */

        if (addressModalTitle) {

            addressModalTitle.textContent =
                "Add Address";

        }


        if (addressModalDescription) {

            addressModalDescription.textContent =
                "Save your delivery details for a faster checkout.";

        }


        if (addressSubmitText) {

            addressSubmitText.textContent =
                "Save Address";

        }


        /* =============================================
                DEFAULT DJANGO VALUES
        ============================================= */

        const fullName =
            document.getElementById(
                "address_full_name"
            );

        const phone =
            document.getElementById(
                "address_phone_number"
            );

        const country =
            document.getElementById(
                "address_country"
            );


        if (fullName) {

            fullName.value =
                fullName.defaultValue;

        }


        if (phone) {

            phone.value =
                phone.defaultValue;

        }


        if (country) {

            country.value =
                country.defaultValue ||
                "India";

        }


        /* =============================================
                DEFAULT ADDRESS TYPE
        ============================================= */

        const homeType =
            addressForm.querySelector(
                'input[name="address_type"][value="HOME"]'
            );


        if (homeType) {

            homeType.checked = true;

        }


        refreshLucideIcons();

    }


    /* =====================================================
            OPEN ADDRESS MODAL
            ADD MODE / EDIT MODE
    ===================================================== */

    function openAddressModal(
        editButton = null
    ) {

        if (!addressModal) return;


        /* =================================================
                EDIT MODE
        ================================================= */

        if (editButton) {


            /* =============================================
                    ACTION
            ============================================= */

            if (addressFormAction) {

                addressFormAction.value =
                    "update_address";

            }


            /* =============================================
                    ADDRESS ID
            ============================================= */

            if (addressIdInput) {

                addressIdInput.value =
                    editButton.dataset.addressId ||
                    "";

            }


            /* =============================================
                    MODAL TEXT
            ============================================= */

            if (addressModalTitle) {

                addressModalTitle.textContent =
                    "Edit Address";

            }


            if (addressModalDescription) {

                addressModalDescription.textContent =
                    "Update your saved delivery details.";

            }


            if (addressSubmitText) {

                addressSubmitText.textContent =
                    "Update Address";

            }


            /* =============================================
                    PRE-FILL FIELDS
            ============================================= */

            const fieldValues = {

                "address_full_name":
                    editButton.dataset.fullName ||
                    "",

                "address_phone_number":
                    editButton.dataset.phoneNumber ||
                    "",

                "address_line_1":
                    editButton.dataset.addressLine1 ||
                    "",

                "address_line_2":
                    editButton.dataset.addressLine2 ||
                    "",

                "address_city":
                    editButton.dataset.city ||
                    "",

                "address_state":
                    editButton.dataset.state ||
                    "",

                "address_postal_code":
                    editButton.dataset.postalCode ||
                    "",

                "address_country":
                    editButton.dataset.country ||
                    "India"

            };


            Object.entries(
                fieldValues
            ).forEach(
                function ([id, value]) {

                    const field =
                        document.getElementById(
                            id
                        );


                    if (field) {

                        field.value =
                            value;

                    }

                }
            );


            /* =============================================
                    ADDRESS TYPE
            ============================================= */

            const addressType =
                editButton.dataset.addressType ||
                "HOME";


            const typeInput =
                addressForm
                    ? addressForm.querySelector(
                        'input[name="address_type"][value="' +
                        addressType +
                        '"]'
                    )
                    : null;


            if (typeInput) {

                typeInput.checked =
                    true;

            }


            /* =============================================
                    DEFAULT ADDRESS
            ============================================= */

            const defaultInput =
                addressForm
                    ? addressForm.querySelector(
                        'input[name="is_default"]'
                    )
                    : null;


            if (defaultInput) {

                defaultInput.checked =
                    editButton.dataset.isDefault ===
                    "true";

            }

        }


        /* =================================================
                ADD MODE
        ================================================= */

        else {

            resetAddressFormForAdd();

        }


        /* =================================================
                SHOW MODAL
        ================================================= */

        addressModal.classList.add(
            "active"
        );

        addressModal.setAttribute(
            "aria-hidden",
            "false"
        );


        updateBodyScroll();


        /* =============================================
                FOCUS FIRST FIELD
        ============================================= */

        const firstField =
            document.getElementById(
                "address_full_name"
            );


        if (firstField) {

            setTimeout(
                function () {

                    firstField.focus();

                },
                150
            );

        }

    }


    /* =====================================================
            CLOSE ADDRESS MODAL
    ===================================================== */

    function closeAddressModal() {

        if (!addressModal) return;


        addressModal.classList.remove(
            "active"
        );

        addressModal.setAttribute(
            "aria-hidden",
            "true"
        );


        updateBodyScroll();

    }


    /* =====================================================
            OPEN REMOVE ADDRESS MODAL
    ===================================================== */

    function openRemoveAddressModal(
        button
    ) {

        if (!removeAddressModal) return;


        const addressId =
            button.dataset.addressId ||
            "";

        const addressName =
            button.dataset.addressName ||
            "Saved Address";


        /* =============================================
                ADDRESS ID
        ============================================= */

        if (removeAddressIdInput) {

            removeAddressIdInput.value =
                addressId;

        }


        /* =============================================
                ADDRESS NAME
        ============================================= */

        if (removeAddressName) {

            removeAddressName.textContent =
                addressName;

        }


        /* =============================================
                SHOW MODAL
        ============================================= */

        removeAddressModal.classList.add(
            "active"
        );

        removeAddressModal.setAttribute(
            "aria-hidden",
            "false"
        );


        updateBodyScroll();

        refreshLucideIcons();

    }


    /* =====================================================
            CLOSE REMOVE ADDRESS MODAL
    ===================================================== */

    function closeRemoveAddressModal() {

        if (!removeAddressModal) return;


        removeAddressModal.classList.remove(
            "active"
        );

        removeAddressModal.setAttribute(
            "aria-hidden",
            "true"
        );


        updateBodyScroll();

    }


    /* =====================================================
            CLOSE ALL ADDRESS MENUS
    ===================================================== */

    function closeAddressMenus() {

        document.querySelectorAll(
            ".address-menu.active"
        ).forEach(
            function (menu) {

                menu.classList.remove(
                    "active"
                );


                const trigger =
                    menu.querySelector(
                        ".address-menu-trigger"
                    );


                if (trigger) {

                    trigger.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }
        );

    }


    /* =====================================================
            EDIT PROFILE — OPEN
    ===================================================== */

    if (openProfileButton) {

        openProfileButton.addEventListener(
            "click",
            openProfileModal
        );

    }


    /* =====================================================
            EDIT PROFILE — CLOSE
    ===================================================== */

    if (closeProfileButton) {

        closeProfileButton.addEventListener(
            "click",
            closeProfileModal
        );

    }


    /* =====================================================
            EDIT PROFILE — BACKDROP / CANCEL
    ===================================================== */

    profileCloseElements.forEach(
        function (element) {

            element.addEventListener(
                "click",
                closeProfileModal
            );

        }
    );


    /* =====================================================
            CHANGE PASSWORD — OPEN
    ===================================================== */

    if (openChangePasswordButton) {

        openChangePasswordButton.addEventListener(
            "click",
            openChangePasswordModal
        );

    }


    /* =====================================================
            CHANGE PASSWORD — CLOSE BUTTON
    ===================================================== */

    if (closeChangePasswordButton) {

        closeChangePasswordButton.addEventListener(
            "click",
            closeChangePasswordModal
        );

    }


    /* =====================================================
            CHANGE PASSWORD — BACKDROP / CANCEL
    ===================================================== */

    passwordCloseElements.forEach(
        function (element) {

            element.addEventListener(
                "click",
                closeChangePasswordModal
            );

        }
    );


    /* =====================================================
            PASSWORD SHOW / HIDE
    ===================================================== */

    passwordToggleButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const targetId =
                        button.dataset.passwordToggle;

                    const input =
                        document.getElementById(
                            targetId
                        );


                    if (!input) return;


                    const showPassword =
                        input.type ===
                        "password";


                    input.type =
                        showPassword
                            ? "text"
                            : "password";


                    button.setAttribute(
                        "aria-pressed",
                        showPassword
                            ? "true"
                            : "false"
                    );

                    button.setAttribute(
                        "aria-label",
                        showPassword
                            ? "Hide password"
                            : "Show password"
                    );


                    button.innerHTML =
                        showPassword
                            ? '<i data-lucide="eye-off"></i>'
                            : '<i data-lucide="eye"></i>';


                    refreshLucideIcons();

                }
            );

        }
    );


    /* =====================================================
            ADD ADDRESS — OPEN
    ===================================================== */

    if (openAddressButton) {

        openAddressButton.addEventListener(
            "click",
            function () {

                closeAddressMenus();

                openAddressModal();

            }
        );

    }


    /* =====================================================
            FIRST ADDRESS — OPEN
    ===================================================== */

    if (openFirstAddressButton) {

        openFirstAddressButton.addEventListener(
            "click",
            function () {

                closeAddressMenus();

                openAddressModal();

            }
        );

    }


    /* =====================================================
            EDIT SAVED ADDRESS
    ===================================================== */

    editAddressButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    closeAddressMenus();

                    openAddressModal(
                        button
                    );

                }
            );

        }
    );


    /* =====================================================
            ADDRESS MODAL — CLOSE BUTTON
    ===================================================== */

    if (closeAddressButton) {

        closeAddressButton.addEventListener(
            "click",
            closeAddressModal
        );

    }


    /* =====================================================
            ADDRESS MODAL — BACKDROP / CANCEL
    ===================================================== */

    addressCloseElements.forEach(
        function (element) {

            element.addEventListener(
                "click",
                closeAddressModal
            );

        }
    );


    /* =====================================================
            REMOVE SAVED ADDRESS — OPEN
    ===================================================== */

    removeAddressButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    closeAddressMenus();

                    openRemoveAddressModal(
                        button
                    );

                }
            );

        }
    );


    /* =====================================================
            REMOVE ADDRESS — CLOSE BUTTON
    ===================================================== */

    if (closeRemoveAddressButton) {

        closeRemoveAddressButton.addEventListener(
            "click",
            closeRemoveAddressModal
        );

    }


    /* =====================================================
            REMOVE ADDRESS — BACKDROP / CANCEL
    ===================================================== */

    removeAddressCloseElements.forEach(
        function (element) {

            element.addEventListener(
                "click",
                closeRemoveAddressModal
            );

        }
    );


    /* =====================================================
            ADDRESS OPTIONS MENU
    ===================================================== */

    addressMenuTriggers.forEach(
        function (trigger) {

            trigger.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();


                    const menu =
                        trigger.closest(
                            ".address-menu"
                        );


                    if (!menu) {

                        return;

                    }


                    const willOpen =
                        !menu.classList.contains(
                            "active"
                        );


                    /*
                        Close any other open menu.
                    */

                    closeAddressMenus();


                    /*
                        Open selected menu.
                    */

                    if (willOpen) {

                        menu.classList.add(
                            "active"
                        );

                        trigger.setAttribute(
                            "aria-expanded",
                            "true"
                        );

                    }

                }
            );

        }
    );


    /* =====================================================
            CLOSE ADDRESS MENU WHEN CLICKING OUTSIDE
    ===================================================== */

    document.addEventListener(
        "click",
        function () {

            closeAddressMenus();

        }
    );


    /* =====================================================
            PREVENT MENU CLICK FROM CLOSING ITSELF
    ===================================================== */

    document.querySelectorAll(
        ".address-menu-dropdown"
    ).forEach(
        function (dropdown) {

            dropdown.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();

                }
            );

        }
    );


    /* =====================================================
            ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key !==
                "Escape"
            ) {

                return;

            }


            /* =============================================
                    ADDRESS OPTIONS MENU
            ============================================= */

            closeAddressMenus();


            /* =============================================
                    CHANGE PASSWORD MODAL
            ============================================= */

            if (
                changePasswordModal &&
                changePasswordModal.classList.contains(
                    "active"
                )
            ) {

                closeChangePasswordModal();

                return;

            }


            /* =============================================
                    REMOVE ADDRESS MODAL
            ============================================= */

            if (
                removeAddressModal &&
                removeAddressModal.classList.contains(
                    "active"
                )
            ) {

                closeRemoveAddressModal();

                return;

            }


            /* =============================================
                    ADD / EDIT ADDRESS MODAL
            ============================================= */

            if (
                addressModal &&
                addressModal.classList.contains(
                    "active"
                )
            ) {

                closeAddressModal();

                return;

            }


            /* =============================================
                    EDIT PROFILE MODAL
            ============================================= */

            if (
                profileModal &&
                profileModal.classList.contains(
                    "active"
                )
            ) {

                closeProfileModal();

            }

        }
    );


    /* =====================================================
            PROFILE IMAGE — ELEMENTS
    ===================================================== */

    const imageInput =
        document.getElementById(
            "profile_image"
        );

    const imagePreview =
        document.getElementById(
            "profileImagePreview"
        );

    const imageInitial =
        document.getElementById(
            "profileImageInitial"
        );

    const removePhotoButton =
        document.getElementById(
            "removeProfilePhoto"
        );

    const removeImageInput =
        document.getElementById(
            "remove_profile_image"
        );


    /* =====================================================
            REMOVE PROFILE PHOTO
    ===================================================== */

    if (
        removePhotoButton &&
        removeImageInput
    ) {

        removePhotoButton.addEventListener(
            "click",
            function () {


                /* ==========================================
                        MARK FOR REMOVAL
                ========================================== */

                removeImageInput.value =
                    "true";


                /* ==========================================
                        CLEAR NEW IMAGE
                ========================================== */

                if (imageInput) {

                    imageInput.value = "";

                }


                /* ==========================================
                        HIDE CURRENT IMAGE
                ========================================== */

                if (imagePreview) {

                    imagePreview.src = "";

                    imagePreview.hidden =
                        true;

                    imagePreview.style.display =
                        "none";

                }


                /* ==========================================
                        SHOW INITIAL
                ========================================== */

                if (imageInitial) {

                    imageInitial.style.display =
                        "flex";

                }


                /* ==========================================
                        BUTTON STATE
                ========================================== */

                removePhotoButton.classList.add(
                    "selected"
                );

                removePhotoButton.innerHTML = `
                    <i data-lucide="check"></i>
                    Photo will be removed
                `;


                refreshLucideIcons();

            }
        );

    }


    /* =====================================================
            PROFILE IMAGE PREVIEW
    ===================================================== */

    if (
        imageInput &&
        imagePreview
    ) {

        imageInput.addEventListener(
            "change",
            function () {

                const file =
                    imageInput.files[0];


                if (!file) {

                    return;

                }


                /* ==========================================
                        FILE TYPE VALIDATION
                ========================================== */

                const allowedTypes = [

                    "image/jpeg",

                    "image/png",

                    "image/webp"

                ];


                if (
                    !allowedTypes.includes(
                        file.type
                    )
                ) {

                    alert(
                        "Please choose a JPG, PNG or WEBP image."
                    );

                    imageInput.value =
                        "";

                    return;

                }


                /* ==========================================
                        FILE SIZE VALIDATION
                ========================================== */

                const maxSize =
                    5 * 1024 * 1024;


                if (
                    file.size >
                    maxSize
                ) {

                    alert(
                        "Please choose an image smaller than 5 MB."
                    );

                    imageInput.value =
                        "";

                    return;

                }


                /* ==========================================
                        CANCEL PHOTO REMOVAL
                ========================================== */

                if (removeImageInput) {

                    removeImageInput.value =
                        "false";

                }


                if (removePhotoButton) {

                    removePhotoButton.classList.remove(
                        "selected"
                    );

                    removePhotoButton.innerHTML = `
                        <i data-lucide="trash-2"></i>
                        Remove Photo
                    `;

                }


                /* ==========================================
                        IMAGE PREVIEW
                ========================================== */

                const reader =
                    new FileReader();


                reader.onload =
                    function (event) {

                        imagePreview.src =
                            event.target.result;

                        imagePreview.hidden =
                            false;

                        imagePreview.style.display =
                            "block";


                        if (imageInitial) {

                            imageInitial.style.display =
                                "none";

                        }


                        refreshLucideIcons();

                    };


                reader.readAsDataURL(
                    file
                );

            }
        );

    }


    /* =====================================================
            ADDRESS PIN CODE
    ===================================================== */

    const postalCodeInput =
        document.getElementById(
            "address_postal_code"
        );


    if (postalCodeInput) {

        postalCodeInput.addEventListener(
            "input",
            function () {

                postalCodeInput.value =
                    postalCodeInput.value
                        .replace(
                            /\D/g,
                            ""
                        )
                        .slice(
                            0,
                            6
                        );

            }
        );

    }


/* =====================================================
        LUCIDE ICON REFRESH
===================================================== */

function refreshLucideIcons() {

    if (window.lucide) {

        lucide.createIcons();

    }

}


/* =====================================================
        PASSWORD SUCCESS TOAST
===================================================== */

const passwordSuccessToast =
    document.getElementById(
        "passwordSuccessToast"
    );

const closePasswordSuccessToast =
    document.getElementById(
        "closePasswordSuccessToast"
    );


function hidePasswordSuccessToast() {

    if (!passwordSuccessToast) {

        return;

    }


    if (
        passwordSuccessToast.classList.contains(
            "toast-hide"
        )
    ) {

        return;

    }


    passwordSuccessToast.classList.add(
        "toast-hide"
    );


    setTimeout(
        function () {

            passwordSuccessToast.remove();

        },
        300
    );

}


if (passwordSuccessToast) {

    setTimeout(
        hidePasswordSuccessToast,
        4000
    );

}


if (closePasswordSuccessToast) {

    closePasswordSuccessToast.addEventListener(
        "click",
        hidePasswordSuccessToast
    );

}


/* =====================================================
        REOPEN CHANGE PASSWORD AFTER ERROR
===================================================== */

if (
    passwordModalReopen &&
    changePasswordModal
) {

    openChangePasswordModal();

}


/* =====================================================
        INITIAL ICON RENDER
===================================================== */

refreshLucideIcons();

});

   
    