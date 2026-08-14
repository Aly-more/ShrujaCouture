/* ==========================================
        HEART TO WISHLIST
========================================== */

function flyHeartToWishlist(button, callback) {

    const navbarHeart = document.getElementById("wishlistNav");

    if (!button || !navbarHeart) {

        if (callback) callback();
        return;

    }

    const icon = button.querySelector("svg");
    const navIcon = navbarHeart.querySelector("svg");

    if (!icon || !navIcon) {

        if (callback) callback();
        return;

    }

    const start = icon.getBoundingClientRect();
    const end = navIcon.getBoundingClientRect();

    /* ==========================================
            CLONE CLICKED HEART
    ========================================== */

    const heart = icon.cloneNode(true);

    heart.style.position = "fixed";
    heart.style.left = start.left + "px";
    heart.style.top = start.top + "px";

    heart.style.width = "42px";
    heart.style.height = "42px";

    heart.style.strokeWidth = "2.6";

    heart.style.transformOrigin = "center";

    heart.style.filter =
        "drop-shadow(0 12px 28px rgba(182,110,76,.45))";

    heart.style.fill = "#B66E4C";
    heart.style.stroke = "#B66E4C";

    heart.style.pointerEvents = "none";
    heart.style.zIndex = "999999";

    heart.style.filter =
        "drop-shadow(0 8px 18px rgba(182,110,76,.35))";

    heart.style.willChange = "transform, opacity";

    heart.style.transition =
        "transform .45s cubic-bezier(.22,.61,.36,1), opacity .45s ease";

    document.body.appendChild(heart);

    /* ==========================================
            STRAIGHT LINE
    ========================================== */

    const x =
        (end.left + end.width / 2) -
        (start.left + start.width / 2);

    const y =
        (end.top + end.height / 2) -
        (start.top + start.height / 2);

    requestAnimationFrame(() => {

        heart.style.transform =
            `translate(${x}px, ${y}px) scale(.4)`;

        heart.style.opacity = "0";

    });

    heart.addEventListener("transitionend", () => {

        heart.remove();

        /* ==========================================
                NAVBAR HEART PULSE
        ========================================== */

        navIcon.animate(

            [

                { transform: "scale(1)" },

                { transform: "scale(1.20)" },

                { transform: "scale(.92)" },

                { transform: "scale(1)" }

            ],

            {

                duration: 340,

                easing: "ease-out"

            }

        );

        navIcon.animate(

            [

                {
                    filter:
                        "drop-shadow(0 0 0 rgba(182,110,76,0))"
                },

                {
                    filter:
                        "drop-shadow(0 0 14px rgba(182,110,76,.55))"
                },

                {
                    filter:
                        "drop-shadow(0 0 0 rgba(182,110,76,0))"
                }

            ],

            {

                duration: 340

            }

        );

        if (callback) {

            callback();

        }

    });

}