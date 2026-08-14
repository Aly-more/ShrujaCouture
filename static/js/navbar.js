// =====================================================
// SHRUJA COUTURE — NAVBAR
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    // =================================================
    // ELEMENTS
    // =================================================

    const siteHeader = document.getElementById("siteHeader");

    const menuToggle = document.getElementById("menuToggle");
    const mobileMenu = document.getElementById("mobileMenu");
    const closeMenu = document.getElementById("closeMenu");
    const menuOverlay = document.getElementById("menuOverlay");

    const accountBtn = document.getElementById("accountBtn");
    const accountMenu = document.getElementById("accountMenu");

    const searchBtn = document.getElementById("searchBtn");
    const searchOverlay = document.getElementById("searchOverlay");
    const closeSearch = document.getElementById("closeSearch");

    const searchForm = document.getElementById("productSearchForm");
    const searchInput = document.getElementById("productSearchInput");
    const searchResults = document.getElementById("searchResults");


    // =================================================
    // BODY SCROLL LOCK
    // =================================================

    function lockBody(){

        document.body.style.overflow = "hidden";

    }


    function unlockBody(){

        document.body.style.overflow = "";

    }


    // =================================================
    // MOBILE MENU
    // =================================================

    function openMobileMenu(){

        if (!mobileMenu || !menuOverlay) return;

        mobileMenu.classList.add("active");

        menuOverlay.classList.add("active");

        mobileMenu.setAttribute(
            "aria-hidden",
            "false"
        );

        if (menuToggle){

            menuToggle.setAttribute(
                "aria-expanded",
                "true"
            );

        }

        lockBody();

    }


    function closeMobileMenu(){

        if (!mobileMenu || !menuOverlay) return;

        mobileMenu.classList.remove("active");

        menuOverlay.classList.remove("active");

        mobileMenu.setAttribute(
            "aria-hidden",
            "true"
        );

        if (menuToggle){

            menuToggle.setAttribute(
                "aria-expanded",
                "false"
            );

        }

        unlockBody();

    }


    if (menuToggle){

        menuToggle.addEventListener(
            "click",
            openMobileMenu
        );

    }


    if (closeMenu){

        closeMenu.addEventListener(
            "click",
            closeMobileMenu
        );

    }


    if (menuOverlay){

        menuOverlay.addEventListener(
            "click",
            closeMobileMenu
        );

    }


    // Close drawer after selecting a mobile link

    if (mobileMenu){

        mobileMenu
            .querySelectorAll("a")
            .forEach(link => {

                link.addEventListener(
                    "click",
                    closeMobileMenu
                );

            });

    }


    // =================================================
    // ACCOUNT DROPDOWN
    // =================================================

    function closeAccountMenu(){

        if (!accountMenu) return;

        accountMenu.classList.remove("active");

        if (accountBtn){

            accountBtn.setAttribute(
                "aria-expanded",
                "false"
            );

        }

    }


    if (accountBtn && accountMenu){

        accountBtn.addEventListener(
            "click",
            event => {

                event.stopPropagation();

                const isOpen =
                    accountMenu.classList.contains(
                        "active"
                    );

                accountMenu.classList.toggle(
                    "active"
                );

                accountBtn.setAttribute(
                    "aria-expanded",
                    String(!isOpen)
                );

            }
        );


        accountMenu.addEventListener(
            "click",
            event => {

                event.stopPropagation();

            }
        );


        document.addEventListener(
            "click",
            closeAccountMenu
        );

    }


    // =================================================
    // SEARCH OVERLAY
    // =================================================

    function openSearch(){

        if (!searchOverlay) return;

        // Close other navbar UI first

        closeAccountMenu();
        closeMobileMenu();

        searchOverlay.classList.add("active");

        searchOverlay.setAttribute(
            "aria-hidden",
            "false"
        );

        lockBody();


        // Wait for overlay animation before focusing

        window.setTimeout(() => {

            if (searchInput){

                searchInput.focus();

            }

        }, 150);

    }


    function closeSearchOverlay(){

        if (!searchOverlay) return;

        searchOverlay.classList.remove("active");

        searchOverlay.setAttribute(
            "aria-hidden",
            "true"
        );

        unlockBody();

    }


    if (searchBtn){

        searchBtn.addEventListener(
            "click",
            openSearch
        );

    }


    if (closeSearch){

        closeSearch.addEventListener(
            "click",
            closeSearchOverlay
        );

    }

    // =================================================
// GLOBAL CART BADGE
// =================================================

async function updateCartBadge(){

    try{

        const response = await fetch("/api/cart/", {
            cache: "no-store"
        });

        if(!response.ok){

            return;

        }

        const data = await response.json();

        const badge = document.getElementById("cart-count");

        if(!badge){

            return;

        }

        if(data.cart_count > 0){

            badge.style.display = "flex";

            badge.textContent = data.cart_count;

        }

        else{

            badge.style.display = "none";

            badge.textContent = "";

        }

    }

    catch(error){

        console.error(
            "Unable to update cart badge.",
            error
        );

    }

}

window.updateCartBadge = updateCartBadge;


    // =================================================
    // SEARCH API
    // =================================================

    let searchTimer;


    async function searchProducts(query){

        if (!searchResults) return;


        // ---------------------------------------------
        // EMPTY SEARCH
        // ---------------------------------------------

        if (!query){

            searchResults.innerHTML = `

                <p class="search-hint">

                    Start typing to discover
                    Shruja Couture.

                </p>

            `;

            return;

        }


        // ---------------------------------------------
        // LOADING
        // ---------------------------------------------

        searchResults.innerHTML = `

            <p class="search-hint">

                Searching...

            </p>

        `;


        try{

            const response = await fetch(
                `/api/products/search/?q=${encodeURIComponent(query)}`
            );


            if (!response.ok){

                throw new Error(
                    "Search request failed."
                );

            }


            const data = await response.json();


            // -----------------------------------------
            // NO RESULTS
            // -----------------------------------------

            if (
                !data.success ||
                !data.products ||
                data.products.length === 0
            ){

                searchResults.innerHTML = `

                    <div class="search-no-results">

                        No products found for
                        "<strong>${escapeHTML(query)}</strong>".

                    </div>

                `;

                return;

            }


            // -----------------------------------------
            // BUILD RESULTS
            // -----------------------------------------

            searchResults.innerHTML =
                data.products
                    .map(product => {

                        const price =
                            product.discount_price
                                ? product.discount_price
                                : product.price;


                        return `

                            <a
                                href="${product.url}"
                                class="search-result-item"
                            >

                                ${
                                    product.image
                                        ? `
                                            <img
                                                src="${product.image}"
                                                alt="${escapeHTML(product.name)}"
                                            >
                                        `
                                        : ""
                                }

                                <div class="search-result-info">

                                    <h4>
                                        ${escapeHTML(product.name)}
                                    </h4>

                                    <p>
                                        ₹${price}
                                    </p>

                                </div>

                            </a>

                        `;

                    })
                    .join("");

        }

        catch(error){

            console.error(
                "Product search error:",
                error
            );

            searchResults.innerHTML = `

                <div class="search-no-results">

                    Something went wrong while searching.
                    Please try again.

                </div>

            `;

        }

    }


    // =================================================
    // LIVE SEARCH
    // =================================================

    if (searchInput){

        searchInput.addEventListener(
            "input",
            () => {

                clearTimeout(searchTimer);

                const query =
                    searchInput.value.trim();


                searchTimer = setTimeout(
                    () => {

                        searchProducts(query);

                    },
                    300
                );

            }
        );

    }


    // =================================================
    // SEARCH FORM SUBMIT
    // =================================================

    if (searchForm){

        searchForm.addEventListener(
            "submit",
            event => {

                event.preventDefault();

                const query =
                    searchInput
                        ? searchInput.value.trim()
                        : "";


                searchProducts(query);

            }
        );

    }


    // =================================================
    // ESCAPE KEY
    // =================================================

    document.addEventListener(
        "keydown",
        event => {

            if (event.key !== "Escape"){

                return;

            }


            if (
                searchOverlay &&
                searchOverlay.classList.contains(
                    "active"
                )
            ){

                closeSearchOverlay();

                return;

            }


            if (
                mobileMenu &&
                mobileMenu.classList.contains(
                    "active"
                )
            ){

                closeMobileMenu();

                return;

            }


            closeAccountMenu();

        }
    );

        // =================================================
    // NAVBAR SCROLL EFFECT
    // =================================================

    function updateNavbar(){

        if (!siteHeader) return;

        if (window.scrollY > 20){

            siteHeader.classList.add(
                "navbar-scrolled"
            );

        }

        else{

            siteHeader.classList.remove(
                "navbar-scrolled"
            );

        }

    }

    window.addEventListener(
        "scroll",
        updateNavbar,
        {
            passive: true
        }
    );

    updateNavbar();

    // ==========================================
    // INITIALIZE GLOBAL CART BADGE
    // ==========================================

    updateCartBadge();

    // =================================================
// REFRESH AFTER BACK/FORWARD NAVIGATION
// =================================================

        window.addEventListener("pageshow", function () {

            updateCartBadge();

            if (typeof syncWishlist === "function") {

                syncWishlist();

            }

        });

    // =================================================
    // WINDOW RESIZE
    // =================================================

    window.addEventListener(
        "resize",
        () => {

            /*
                If the browser moves from mobile/tablet
                back to desktop while the drawer is open,
                reset the drawer and body scroll.
            */

            if (window.innerWidth > 992){

                closeMobileMenu();

            }

        }
    );
    

    // =================================================
    // SAFE HTML OUTPUT
    // =================================================

    function escapeHTML(value){

        const div =
            document.createElement("div");

        div.textContent =
            value == null
                ? ""
                : String(value);

        return div.innerHTML;

    }

});