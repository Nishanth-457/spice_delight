// ============================================================
//  Spice Delight — script.js
// ============================================================

let cart = [];
let _addressMode = 'new';   // 'saved' or 'new'
let _savedName   = '';
let _savedAddr   = '';

// ============================================================
// TOAST NOTIFICATION
// ============================================================
function showToast(message) {
  const existing = document.getElementById('sd-toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.id = 'sd-toast';
  toast.innerHTML = message;
  toast.style.cssText = `
    position:fixed; bottom:40px; right:40px; background:#1C1917; color:#fff;
    padding:16px 28px; font-family:'Jost',sans-serif; font-size:13px;
    font-weight:400; letter-spacing:.5px; z-index:99999; opacity:0;
    transform:translateY(16px); transition:all .35s cubic-bezier(.34,1.56,.64,1);
    border-left:3px solid #C4783C; max-width:320px;
    box-shadow:0 8px 32px rgba(0,0,0,.18); pointer-events:none;
  `;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity='1'; toast.style.transform='translateY(0)'; }, 10);
  setTimeout(() => {
    toast.style.opacity='0'; toast.style.transform='translateY(10px)';
    setTimeout(() => toast.remove(), 350);
  }, 2500);
}

// ============================================================
// Show ingredients popup
// ============================================================
function showIngredients(name, ingredients) {
  document.getElementById('ing-title').innerText = name;
  document.getElementById('ing-text').innerText  = ingredients;
  new bootstrap.Modal(document.getElementById('ingredientsModal')).show();
}

// ============================================================
// Add item to cart
// ============================================================
function addToCart(id, name, price) {
  let found = false;
  for (let i = 0; i < cart.length; i++) {
    if (cart[i].id === id) {
      cart[i].qty++;
      found = true;
      showToast(`✓ &nbsp;<strong>${name}</strong> &nbsp;+1`);
      break;
    }
  }
  if (!found) {
    cart.push({ id, name, price, qty: 1 });
    showToast(`✓ &nbsp;<strong>${name}</strong> added to cart`);
  }
  updateCartCount();
}

// ============================================================
// Update cart badge
// ============================================================
function updateCartCount() {
  let total = 0;
  cart.forEach(item => total += item.qty);
  document.getElementById('cart-count').innerText = total;
}

// ============================================================
// Show cart modal
// ============================================================
function showCart() {
  updateCartDisplay();
  new bootstrap.Modal(document.getElementById('cartModal')).show();
}

// ============================================================
// Render cart items
// ============================================================
function updateCartDisplay() {
  const cartList  = document.getElementById('cart-items');
  const totalSpan = document.getElementById('cart-total');
  cartList.innerHTML = '';
  let total = 0;
  if (cart.length === 0) {
    cartList.innerHTML = `
      <div style="text-align:center;padding:40px;color:#78716C;">
        <div style="font-size:36px;margin-bottom:12px;">🛒</div>
        <p style="font-size:13px;font-weight:300;">Your cart is empty</p>
      </div>`;
    totalSpan.innerText = '0';
    return;
  }
  cart.forEach((item, i) => {
    let itemTotal = item.price * item.qty;
    total += itemTotal;
    cartList.innerHTML += `
      <div class="cart-item">
        <div>
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-price">₹${item.price} × ${item.qty} = ₹${itemTotal}</div>
        </div>
        <div class="qty-controls">
          <button class="qty-btn" onclick="changeQty(${i},-1)">−</button>
          <span style="font-size:14px;min-width:20px;text-align:center;">${item.qty}</span>
          <button class="qty-btn" onclick="changeQty(${i},1)">+</button>
        </div>
      </div>`;
  });
  totalSpan.innerText = total;
}

// ============================================================
// Change quantity in cart
// ============================================================
function changeQty(index, change) {
  cart[index].qty += change;
  if (cart[index].qty <= 0) cart.splice(index, 1);
  updateCartCount();
  updateCartDisplay();
}

// ============================================================
// SAVED ADDRESS — toggle UI between saved / new
// ============================================================
function selectAddressOption(mode) {
  _addressMode = mode;
  const savedBox  = document.getElementById('opt-saved-box');
  const newBox    = document.getElementById('opt-new-box');
  const savedCircle = document.getElementById('radio-saved-circle');
  const savedDot    = document.getElementById('radio-saved-dot');
  const newCircle   = document.getElementById('radio-new-circle');
  const newDot      = document.getElementById('radio-new-dot');
  const newInputs   = document.getElementById('new-address-inputs');

  if (mode === 'saved') {
    savedBox.classList.add('selected');
    newBox.classList.remove('selected');
    savedCircle.classList.add('selected');
    savedDot.classList.add('selected');
    newCircle.classList.remove('selected');
    newDot.classList.remove('selected');
    newInputs.style.display = 'none';
  } else {
    newBox.classList.add('selected');
    savedBox.classList.remove('selected');
    newCircle.classList.add('selected');
    newDot.classList.add('selected');
    savedCircle.classList.remove('selected');
    savedDot.classList.remove('selected');
    newInputs.style.display = 'block';
    // Clear inputs for fresh entry
    document.getElementById('customer-name').value    = '';
    document.getElementById('customer-address').value = '';
  }
}

// ============================================================
// Open checkout — fetch saved address first
// ============================================================
function openCheckout() {
  if (cart.length === 0) { showToast('Your cart is empty!'); return; }

  const cartModal = bootstrap.Modal.getInstance(document.getElementById('cartModal'));
  cartModal.hide();

  // Fetch saved address from Flask
  fetch('/get_saved_address')
    .then(r => r.json())
    .then(data => {
      if (data.saved) {
        // Show saved address options
        _savedName = data.name;
        _savedAddr = data.address;
        document.getElementById('saved-name-display').textContent = data.name;
        document.getElementById('saved-addr-display').textContent = data.address;
        document.getElementById('saved-address-block').style.display = 'block';
        document.getElementById('new-address-inputs').style.display  = 'none';
        _addressMode = 'saved';
        selectAddressOption('saved');
      } else {
        // No saved address — just show inputs
        document.getElementById('saved-address-block').style.display = 'none';
        document.getElementById('new-address-inputs').style.display  = 'block';
        _addressMode = 'new';
      }
    })
    .catch(() => {
      document.getElementById('saved-address-block').style.display = 'none';
      document.getElementById('new-address-inputs').style.display  = 'block';
      _addressMode = 'new';
    });

  setTimeout(() => {
    new bootstrap.Modal(document.getElementById('checkoutModal')).show();
  }, 300);
}

// ============================================================
// Confirm order — sends to Flask backend
// ============================================================
function confirmOrder() {
  let name, address;

  if (_addressMode === 'saved') {
    name    = _savedName;
    address = _savedAddr;
  } else {
    name    = document.getElementById('customer-name').value.trim();
    address = document.getElementById('customer-address').value.trim();
    if (!name || !address) {
      showToast('Please fill in your name and address!');
      return;
    }
  }

  let total = 0;
  cart.forEach(item => total += item.price * item.qty);

  fetch('/place_order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, address, cart, total })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const checkoutModal = bootstrap.Modal.getInstance(document.getElementById('checkoutModal'));
      checkoutModal.hide();
      cart = [];
      updateCartCount();
      showToast(`✓ &nbsp;Order #${data.order_id} placed successfully!`);
    } else {
      showToast('Something went wrong. Try again.');
    }
  })
  .catch(() => showToast('Network error. Please try again.'));
}
