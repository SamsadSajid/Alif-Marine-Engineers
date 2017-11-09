function incrementValue()
{
    var value = parseInt(document.getElementById('product_quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('product_quantity').value = value;
}

function decrementValue()
{
    var value = parseInt(document.getElementById('product_quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    if(value <= 0)value = 0;
    else value--;
    document.getElementById('product_quantity').value = value;
}
    