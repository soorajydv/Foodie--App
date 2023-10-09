// Get the element with the ID "count"
const countElement = document.getElementById('count');

const products = [];

// Get all elements with the class "add-to-cart"
const addToCartButtons = document.getElementsByClassName('add-to-cart');

// Add event listeners to all "add-to-cart" buttons
for (let i = 0; i < addToCartButtons.length; i++) {
  addToCartButtons[i].addEventListener('click', function() {
    // Get the current count value and increment it by 1
    let count = parseInt(countElement.innerText);
    products.push(parseInt(addToCartButtons[i].id));
    count += 1;

    // Update the count element with the new value
    countElement.innerText = count;
    console.log(products)
  });
}


// Go to cart Menu
document.getElementById('cart').addEventListener('click', function() {
  

    // Send the POST request using AJAX
    fetch('/go_to_cart/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if required
      },
      body: JSON.stringify({'products':products})
    })
    .then(response => response.json())
    .then(responseData => {
      // Handle the response data
      console.log(responseData);
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
  });

  // Helper function to get CSRF cookie value
  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }


