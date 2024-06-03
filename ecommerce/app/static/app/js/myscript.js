$(".modify-cart").click(function() {
    let productID = $(this).attr("pid").toString();
    let action = $(this).attr("modify-action").toString();
    let productQuantity = this.parentNode.children[2];
    
    $.ajax({
        type: "GET",
        url: "/modify-cart",
        data: {
            productID: productID,
            action: action
        },
        success: function(data) {
            productQuantity.innerText = data.quantity;
            $("#amount").text("RM " + data.amount);
            $("#totalamount").text("RM " + data.totalamount);
        }
    })
})

$(".remove-cart").click(function() {
    let productID = $(this).attr("pid").toString();
    let action = "remove";
    let deleteProduct = this;
    
    $.ajax({
        type: "GET",
        url: "/modify-cart",
        data: {
            productID: productID,
            action: action
        },
        success: function(data) {
            $("#amount").text("RM " + data.amount);
            $("#totalamount").text("RM " + data.totalamount);
            deleteProduct.parentNode.parentNode.parentNode.parentNode.remove();
        }
    })
})

$(".modify-wishlist").click(function() {
    let productID = $(this).attr("pid").toString();
    
    $.ajax({
        type: "GET",
        url: "/modify-wishlist",
        data: {
            productID: productID
        },
        success: function(data) {
            window.location.href = "http://127.0.0.1:8000/product-detail/" + productID;
        }
    })
})