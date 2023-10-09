const removeItemButtons = document.getElementsByClassName('remove-item');

function subElemCount() {
   const elem =  document.getElementById('item-count');

    let count = parseInt(elem.innerText);
    count -= 1;
    elem.innerText = count;
}

for (let i = 0; i < removeItemButtons.length; i++) {
    let btn = removeItemButtons[i];
  btn.addEventListener('click', function() {
    console.log('Hello: ',btn);
    
    let btn_id = btn.id;
    let product_id = 'product'+btn_id;
    
    let product = document.getElementById(product_id);
    product.remove();
    subElemCount();
  });
}