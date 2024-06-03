const bar=document.getElementById('bar');
const close=document.getElementById('close');
const nav=document.getElementById('navbar');



if(bar){
    bar.addEventListener('click', ()=> {
        nav.classList.add('active');
    })
}

if(close){
    close.addEventListener('click', ()=> {
        nav.classList.remove('active');
    })
}


// Assuming you have a way to store cart items (e.g., localStorage)
const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

// Function to display cart items in the cart page
function displayCartItems() {
  const cartItemsContainer = document.getElementById("cart-items");
  cartItemsContainer.innerHTML = ""; // Clear existing content

  if (cartItems.length === 0) {
    cartItemsContainer.innerHTML = "<p>Your cart is empty!</p>";
    return;
  }

  for (const item of cartItems) {
    const cartItem = document.createElement("div");
    cartItem.classList.add("cart-item");

    cartItem.innerHTML = `
      <img src="<span class="math-inline">\{item\.image\}" alt\="</span>{item.name}">
      <div class="details">
        <h3><span class="math-inline">\{item\.name\}</h3\>
<p\></span><span class="math-inline">\{item\.price\.toFixed\(2\)\}</p\>
<button data\-id\="</span>{item.id}">Remove</button>
      </div>
    `;

    cartItemsContainer.appendChild(cartItem);

    // Add event listener to remove button
    const removeBtn = cartItem.querySelector("button");
    removeBtn.addEventListener("click", handleRemoveItem);
  }

  // Update total price
  calculateTotalPrice();
}

// Function to calculate and display total price
function calculateTotalPrice() {
  const totalPrice = cartItems.reduce((acc, item) => acc + item.price, 0);
  document.getElementById("total-num").textContent = totalPrice.toFixed(2);
}

// Function to handle removing an item from the cart
function handleRemoveItem(event) {
  const itemId = event.target.dataset.id;
  const newCartItems = cartItems.filter((item) => item.id !== itemId);

  localStorage.setItem("cartItems", JSON.stringify(newCartItems));
  //cartItems = newCartItems
}
