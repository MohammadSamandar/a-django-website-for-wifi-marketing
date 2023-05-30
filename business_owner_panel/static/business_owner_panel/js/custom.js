

function AddProductToOrder(productId){
    $.get('/dashboard/order/add-to-order?product_id=' + productId).then(res =>
        {
            if (res.status === 'success'){
                Swal.fire(
                'پلن، به سبد خرید افزوده شد!',
                'خوش به حالت که به آرزوت رسیدی! بیلخره',
                'success'
                    );
            }

            else if (res.status === 'error'){
                Swal.fire(
                'خطایی رخ داد!',
                'محصول مورد نظر یافت نشد',
                'error'
                    );
            }

        }
    );

}


function removeOrderDetail(detailId){
    $.get('/dashboard/order/remove-basket-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
    });

}