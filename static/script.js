// ============================================================
//  Spice Delight — Frontend JavaScript (Updated for Flask)
//  Main changes from original:
//   1. Menu is now rendered by Flask (no menuItems array needed)
//   2. addToCart() now takes id, name, price as arguments
//   3. confirmOrder() now sends data to Flask via fetch()
// ============================================================

let cart = [];

// ============================================================
// Filter menu cards by veg / non-veg
// (Cards are rendered by Flask, we just show/hide them)
// ============================================================
function filterMenu(filter) {
    const cards = document.querySelectorAll('.menu-card');
    cards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================================
// Show ingredients popup
// ============================================================
function showIngredients(name, ingredients) {
    document.getElementById('ing-title').innerText = name;
    document.getElementById('ing-text').innerText  = ingredients;
    const modal = new bootstrap.Modal(document.getElementById('ingredientsModal'));
    modal.show();
}

// ============================================================
// Add item to cart
// Called from menu.html buttons: addToCart(id, name, price)
// ============================================================
function addToCart(id, name, price) {
    let found = false;
    for (let i = 0; i < cart.length; i++) {
        if (cart[i].id === id) {
            cart[i].qty++;
            found = true;
            break;
        }
    }
    if (!found) {
        cart.push({ id: id, name: name, price: price, qty: 1 });
    }
    updateCartCount();
}

// ============================================================
// Update the cart badge number on the navbar
// ============================================================
function updateCartCount() {
    let total = 0;
    cart.forEach(item => total += item.qty);
    document.getElementById('cart-count').innerText = total;
}

// ============================================================
// Show cart modal with all items
// ============================================================
function showCart() {
    updateCartDisplay();
    const modal = new bootstrap.Modal(document.getElementById('cartModal'));
    modal.show();
}

// ============================================================
// Render cart items inside the modal
// ============================================================
function updateCartDisplay() {
    const cartList  = document.getElementById('cart-items');
    const totalSpan = document.getElementById('cart-total');
    cartList.innerHTML = '';
    let total = 0;

    cart.forEach((item, i) => {
        let itemTotal = item.price * item.qty;
        total += itemTotal;
        cartList.innerHTML += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>${item.name}</strong><br>
                    <small>₹${item.price} x ${item.qty} = ₹${itemTotal}</small>
                </div>
                <div>
                    <button class="btn btn-sm btn-secondary" onclick="changeQty(${i}, -1)">−</button>
                    <span class="mx-2">${item.qty}</span>
                    <button class="btn btn-sm btn-secondary" onclick="changeQty(${i}, 1)">+</button>
                </div>
            </li>
        `;
    });

    totalSpan.innerText = total;
}

// ============================================================
// Change quantity of cart item (+1 or -1)
// ============================================================
function changeQty(index, change) {
    cart[index].qty += change;
    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }
    updateCartCount();
    updateCartDisplay();
}

// ============================================================
// Open checkout modal
// ============================================================
function openCheckout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    const cartModal = bootstrap.Modal.getInstance(document.getElementById('cartModal'));
    cartModal.hide();
    const checkoutModal = new bootstrap.Modal(document.getElementById('checkoutModal'));
    checkoutModal.show();
}

// ============================================================
// Confirm order — sends data to Flask backend using fetch()
// This is the BIG change from the original (no more just alert!)
// ============================================================
function confirmOrder() {
    const name    = document.getElementById('customer-name').value.trim();
    const address = document.getElementById('customer-address').value.trim();

    if (!name || !address) {
        alert('Please fill in your name and address!');
        return;
    }

    // Calculate total
    let total = 0;
    cart.forEach(item => total += item.price * item.qty);

    // Send order data to Flask backend at /place_order
    fetch('/place_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name:    name,
            address: address,
            cart:    cart,
            total:   total
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Order saved to database successfully!
            alert(`✅ Thank you ${name}! Your order #${data.order_id} has been placed.\nFood will be delivered to: ${address}`);
            cart = [];
            updateCartCount();
            // Close the modal
            const checkoutModal = bootstrap.Modal.getInstance(document.getElementById('checkoutModal'));
            checkoutModal.hide();
        } else {
            alert('Something went wrong. Please try again.');
        }
    })
    .catch(err => {
        console.error('Error placing order:', err);
        alert('Network error. Please try again.');
    });
}
