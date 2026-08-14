// ==========================================
// MY ORDERS
// ==========================================

const container = document.getElementById("orders-container");


// ==========================================
// FORMAT DATE
// ==========================================

function formatOrderDate(dateString) {

    const date = new Date(dateString);

    return date.toLocaleDateString("en-IN", {

        day: "2-digit",
        month: "short",
        year: "numeric"

    });

}


// ==========================================
// FETCH ORDERS
// ==========================================

fetch("/api/orders/")

.then(response => response.json())

.then(data => {

    if (!data.success) {

        container.innerHTML = `

            <div class="empty-orders">

                <h2>Unable to Load Orders</h2>

                <p>Please try again in a moment.</p>

            </div>

        `;

        return;

    }


    // ==========================================
    // NO ORDERS
    // ==========================================

    if (data.orders.length === 0) {

        container.innerHTML = `

            <div class="empty-orders">

                <span class="empty-orders-tag">
                    YOUR ORDERS
                </span>

                <h2>No Orders Yet</h2>

                <p>
                    Your shopping journey starts here.
                </p>

                <a href="/shop/" class="start-shopping-btn">

                    Start Shopping

                </a>

            </div>

        `;

        return;

    }


    // ==========================================
    // BUILD ORDER CARDS
    // ==========================================

    let html = "";


    data.orders.forEach(order => {

        const statusClass =
            order.status.toLowerCase();

        const firstItem =
            order.items && order.items.length > 0
                ? order.items[0]
                : null;

        const totalItems = order.items.reduce(

            (total, item) => {

                return total + item.quantity;

            },

            0

        );

        const additionalProducts =
            order.items.length - 1;


        // ==========================================
        // PRODUCT INFORMATION
        // ==========================================

        let productHTML = "";


        if (firstItem) {

            productHTML = `

                <div class="order-product">

                    <div class="order-product-image">

                        <img
                            src="${firstItem.image}"
                            alt="${firstItem.product_name}"
                        >

                    </div>


                    <div class="order-product-info">

                        <h3>
                            ${firstItem.product_name}
                        </h3>

                        <p>

                            Size: ${firstItem.size}

                            <span class="product-divider">
                                ·
                            </span>

                            Qty: ${firstItem.quantity}

                        </p>


                        ${
                            additionalProducts > 0

                            ? `

                                <span class="more-items">

                                    +${additionalProducts}
                                    more
                                    ${
                                        additionalProducts === 1
                                            ? "product"
                                            : "products"
                                    }

                                </span>

                              `

                            : ""
                        }

                    </div>

                </div>

            `;

        }


        // ==========================================
        // ORDER CARD
        // ==========================================

        html += `

            <article class="order-card">


                <!-- ORDER TOP -->

                <div class="order-card-top">

                    <div class="order-number">

                        <span class="order-label">
                            ORDER
                        </span>

                        <h2>
                           ${order.order_number}
                        </h2>

                        <p>
                            Placed on
                            ${formatOrderDate(order.created_at)}
                        </p>

                    </div>


                    <div class="order-status">

                        <span class="badge ${statusClass}">

                            ${order.status}

                        </span>

                    </div>

                </div>


                <!-- PRODUCT -->

                <div class="order-card-body">

                    ${productHTML}


                    <!-- ORDER SUMMARY -->

                    <div class="order-summary">

                        <div class="order-meta">

                            <span>
                                ${totalItems}
                                ${
                                    totalItems === 1
                                        ? "item"
                                        : "items"
                                }
                            </span>

                            <span class="meta-divider">
                                ·
                            </span>

                            <span>
                                Payment: ${order.payment_status}
                            </span>

                        </div>


                        <div class="order-total">

                            <span>
                                Total
                            </span>

                            <strong>
                                ₹${order.total}
                            </strong>

                        </div>


                        <a
                            href="/orders/${order.id}/"
                            class="view-order-btn"
                        >

                            View Details

                            <span aria-hidden="true">
                                →
                            </span>

                        </a>

                    </div>

                </div>

            </article>

        `;

    });


    container.innerHTML = html;

})

.catch(error => {

    console.error(
        "Unable to load orders:",
        error
    );

    container.innerHTML = `

        <div class="empty-orders">

            <h2>Something Went Wrong</h2>

            <p>
                We couldn't load your orders.
                Please try again.
            </p>

        </div>

    `;

});