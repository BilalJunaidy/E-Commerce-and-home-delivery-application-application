// document.querySelectorAll()
// document.querySelectorAll(".add-btn").forEach(function(btn) {

// })

// addEventListener("click", function() {
//     console.log('this js file is linked correctly');
// }) 


document.querySelectorAll('.add-btn').forEach(function(button) {
    button.addEventListener("click", function() {
        // Its important to notice here that I used the special term of "this" instead of using "button". 
        // This is because of the following reasons:
        // a - This is the Javascript convention
        // b - Since I am not passing in the "button" object upon which the event handler is being run, therefore, I can't access it below. 
        
        var product_id = this.dataset.product_id
        var button_type = this.dataset.button_type
        
        if (user == 'AnonymousUser') {
            // console.log('User is not logged in')
            addCookieItem(product_id, button_type)
        }
        else {
            UpdateCartItem(product_id, button_type);
        }
        // The following has now been commented out since this works and we are able to console log the following correctly. 
        // console.log("Product ID:", product_id);
        // console.log("Button Type:", button_type);
        // console.log('USER:', user)
    });
});


function addCookieItem(productId, action) {
    console.log('Not logged in.....')

    if(action == 'add') {
        if(cart[productId]== undefined) {
            cart[productId] = {'quantity':1}
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove') {
        cart[productId]['quantity'] -= 1

        if(cart[productId] <= 0) {
            console.log('[REMOVE ITEM]')
            delete cart[productId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}



document.querySelectorAll('.chg-quantity').forEach((button) => {
    button.addEventListener('click', function() {
        var product_id = this.dataset.product_id
        var button_type = this.dataset.button_type
        
        if (user == 'AnonymousUser') {
            console.log('User is not logged in')
        }
        else {
            UpdateCartItem(product_id, button_type);
        }


    })
})




function UpdateCartItem(product_id, button_type) {
        console.log('User is authenticated, sending data....');

        url = '/update_cart/'

        fetch(url, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }, 
            body: JSON.stringify({
                'productid': product_id, 
                'buttontype': button_type,
            })
        })

        .then((response) => {
            return response.json();
        })

        .then((data) => {
            // console.log(data);
            location.reload()
        });
        

}




