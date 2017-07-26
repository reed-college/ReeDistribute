$(document).ready(function() {
  var amount = $('amount').value * 100;
  $(':submit').on('click', function(event) {
    event.preventDefault();
    var $button = $(this),
      $form = $button.parents('form');
    var opts = $.extend({}, $button.data(), {
      token: function(result) {
        $form.append($('<input>').attr({
          type: 'hidden',
          name: 'stripeToken',
          value: result.id,
          amount: amount,
          stripeEmail: result.card.name
        })).submit();
      }
    });
    StripeCheckout.open(opts);
  });
});
