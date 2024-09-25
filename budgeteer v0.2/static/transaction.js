// first row remove button
$(document).on('click', '.remove', function(event) {
    event.preventDefault();
    if(document.getElementsByClassName("product-name").length > 1) {
        $('#modalConfirm').data('targetRow', $(this).closest('tr'));
        openModal()

    }
});

function openModal() {
    var targetRow = $('#modalConfirm').data('targetRow');
    let check = false;
    targetRow.find('input[type="text"], input[type="number"], select').each(function() {
        if ($(this).val().trim() !== '') {
            check = true;
        }
    });
    if(check) {
        document.getElementById('customModal').style.display = 'flex';
    }
    else {
        confirmDelete();
    }
}

function closeModal() {
    var targetRow = $('#modalConfirm').data('targetRow');
    targetRow.css('transform', 'translateX(0)');
    document.getElementById('customModal').style.display = 'none';
}

function confirmDelete() {
    var targetRow = $('#modalConfirm').data('targetRow');
    targetRow.removeClass('slide-in');
    targetRow.css('transform', 'translateX(-100%)');
    setTimeout(() => {targetRow.remove(); updateTotal(); closeModal();}, 100)
}

function openModal2() {
    document.getElementById('customModal2').style.display = 'flex';
}

function closeModal2() {
    document.getElementById('customModal2').style.display = 'none';
}

// form validation
$('#transaction-form').submit(function(event) {
    let isValid = true;
    $(this).find('input[type="text"], input[type="number"], select').each(function() {

        if ($(this).val().trim() === '') {
            openModal2();
            isValid = false;
            return false;
        }
    });
    if (!isValid) {
        event.preventDefault();
    }
});

// add new merchant functionality
$('#merchant').on('change', function() {
    if ($(this).val() === 'new') {
        $('#new-merchant').css('visibility', 'visible');
    } else {
        $('#new-merchant').css('visibility', 'hidden');
    }
});

if ($('#merchant').val() === 'new') {
    $('#merchant').trigger('change');
}

// dynamically update totals
function updateTotal() {
    let total = 0;
    let count = 0
    $('.total-price').each(function() {
        const value = parseFloat($(this).val());
        if (!isNaN(value)) {
            total += value;
        }
        count += 1;
    });
    $('#total-amount').text(`${total.toFixed(2)}`);
    $('#total-items').text(`${count}`);
    $('#total-header').text(`${count} items - $${total.toFixed(2)}`);
}


// jump to next input on enter
$('#transaction-form').on('keydown', 'input', function (event) {
    if (event.which == 13) {
        var $allInputs = $('#transaction-form input')
        var $this = $(event.target);
        var index = $allInputs.index($this);
        if (index < $allInputs.length - 1) {
            event.preventDefault();
            $allInputs[index+1].focus()
        }
    }
});


//swipe functionality
var touchStartX = 0;
var touchCurrentX = 0;
var initialTransform = '';

$(document).on('touchstart', '.swipe', function (event) {
    if(document.getElementsByClassName("product-name").length > 1 && initialTransform === '') {
        touchStartX = event.touches[0].clientX;
        touchCurrentX = touchStartX;
        initialTransform = $(this).closest('tr').css('transform');
    }
});

$(document).on('touchmove', '.swipe', function (event) {
    touchCurrentX = event.touches[0].clientX;
    var distance = touchCurrentX - touchStartX;

    if (distance < 0) {
        $(this).closest('tr').css('transform', `translateX(${distance}px)`);
    }
});

$(document).on('touchend', '.swipe', function () {
    var distance = touchCurrentX - touchStartX;

    if (distance < 0 && Math.abs(distance) > $(this).closest('tr').width() / 3) {
        if(document.getElementsByClassName("product-name").length > 1) {
            initialTransform = '';
            $('#modalConfirm').data('targetRow', $(this).closest('tr'));
            openModal()
        }
    }
    else {
        $(this).closest('tr').css('transform', initialTransform);
        initialTransform = '';
    }
    touchStartX = 0;
    touchCurrentX = 0;
});


$(document).on('input', '.total-price', updateTotal);
$(document).on('input', '.quantity', updateTotal);