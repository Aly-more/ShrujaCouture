// ==========================================
// FAQ
// ==========================================

document.querySelectorAll(".faq-question").forEach(button => {

    button.addEventListener("click", () => {

        const currentItem = button.parentElement;

        document.querySelectorAll(".faq-item").forEach(item => {

            if(item !== currentItem){

                item.classList.remove("active");

            }

        });

        currentItem.classList.toggle("active");

    });

});


// ==========================================
// CONTACT FORM
// ==========================================

const contactForm = document.querySelector(".contact-form-card form");

if(contactForm){

    contactForm.addEventListener("submit", function(){

        const button = document.getElementById("contact-submit-btn");

        button.classList.add("loading");

        button.disabled = true;

    });

}

// ==========================================
// CONTACT SUCCESS TOAST
// ==========================================

const contactSuccess = document.querySelector(".contact-success");

if (contactSuccess) {

    showToast(
        "Message Sent",
        "Thank you for reaching out!",
        "We'll get back to you within 24 hours."
    );

}