$(function(){
    $('.mask-date').mask('00/00/0000');
    $('.mask-fracao').mask('0.00000000');
    $('.mask-cpf').mask('000.000.000-00', {reverse: true});
    $('.mask-money').mask('000.000.000.000.000,00', {reverse: true});
    $('.mask-phone-ddd').mask('(00) 00000-0000');

    // Mask cell phone 8 ou 9 dígitos
    var behavior = function (val) {
        return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    options = {
        onKeyPress: function (val, e, field, options) {
            field.mask(behavior.apply({}, arguments), options);
        }
    };
    $('.mask-cell-phone').mask(behavior, options);
});

