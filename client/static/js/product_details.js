function incrementValue()
{
    var value = parseInt(document.getElementById('quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('quantity').value = value;
}

function decrementValue()
{
    var value = parseInt(document.getElementById('quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    if(value <= 0)value = 0;
    else value--;
    document.getElementById('quantity').value = value;
}
    