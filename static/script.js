$(document).ready(function () {

  $('#donate-buttons').on('click', '.btn-blue', function (e) {
    e.preventDefault();
    $('.active').removeClass('active');
    $('#other-input').hide().siblings('#other').show();
    $(this).filter('.btn-blue').addClass("active");
    var value = $(this).data('impact');
    $(this).closest('div').find('p').text("" + value);
    $('#other-input').find('input').val('');
  });

  $('.btn-green').on('click', function () {
    var price;
    var input = $('#other-input').find('input').val();
    if (!input) {
      price = $('.active').data('tomans');
      if (!price) price = '0';
    } else if ($.trim(input) === '' || isNaN(input)) {
      price = '0';
    } else {
      price = input;
    }
    $('#price').text("" + price);
    $('.amount-input').val(price)
  });

  $('#other').on('click', function (e) {
    e.preventDefault();
    var buttons = $(this).parent('#donate-buttons');
    buttons.find('.active').removeClass('active');
    var other = $(this).hide().siblings('#other-input');
    other.show();
    other.find('input').focus();
    var pText = buttons.siblings('p');
    pText.text("ممنونم از سخاوت شما!");
    var oValue = other.find('input');
    oValue.keyup(function () {
      pText.text("ممنونم از سخاوت شما!");
    });
  });

});