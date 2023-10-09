function getPrice() {
  const quantities = document.getElementsByClassName("quantity");
  const prices = document.getElementsByClassName("price");

  //Buttons
let sum = 0;
  for (let i = 0; i < quantities.length; i++) {
    // Get the current count value and increment it by 1
    let qty = parseInt(quantities[i].value);
    let price = parseInt(prices[i].innerText);

    sum += (qty*price);
  }

  document.getElementById('total-price-of-products').innerText = sum;

  
}

getPrice() ;