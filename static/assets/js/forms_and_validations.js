$('#add-record').click((e) => {
    $('#errorMessages').hide()
})
//////////////////////////////////
// Validaciones mediante eventos//
//////////////////////////////////
$('#price').on('keydown', function (e) {
    if (e.key === "Backspace" || e.key === "Delete" || e.key === "ArrowLeft" || e.key === "ArrowRight" || e.key === "ArrowUp" || e.key === "ArrowDown" || e.key === ".") {
        // Permitir teclas de control
        if ((e.key === "." && this.value.includes(".")) || (e.key === "." && this.value == "")) {
            // Permite un solo punto y que no empiece con este
            $('#error_price').remove()
            $('#price').after("<span id='error_price' style='color: red; font-size: 14px'>El precio no puede tener dos (.), iniciar ni finalizar con un (.)</span>")
            e.preventDefault();
            return
        }
    } else if (e.key < "0" || e.key > "9") {
        $('#error_price').remove()
        $('#price').after("<span id='error_price' style='color: red; font-size: 14px'>El precio debe contener solo números.</span>")
        e.preventDefault();
        return;
    }
    $('#error_price').remove()
});
$('#customer-mobile').on('keydown', function (e) {
    if (e.key === "Backspace" || e.key === "Delete" || e.key === "ArrowLeft" || e.key === "ArrowRight" || e.key === "ArrowUp" || e.key === "ArrowDown") {

        // Permitir teclas de control
    } else if (this.value.length == 0 && e.key != "5") {
        $('#error_mobile').remove()
        $('#customer-mobile').after("<span id='error_mobile' style='color: red; font-size: 14px'>Debe respetar el formato. Comience con 5.</span>")
        e.preventDefault();
        return

    } else if (this.value.length > 7) {
        // Permite un máximo de 8 caractees
        $('#error_mobile').remove()
        $('#customer-mobile').after("<span id='error_mobile' style='color: red; font-size: 14px'>Debe respetar el formato. Son 8 números.</span>")
        e.preventDefault();
        return

    } else if (e.key < "0" || e.key > "9") {
        // Permite solo números
        $('#error_mobile').remove()
        $('#customer-mobile').after("<span id='error_mobile' style='color: red; font-size: 14px'>Debe respetar el formato. Solo números.</span>")
        e.preventDefault();
        return
    }
    $('#error_mobile').remove()
});
$('#customer-name').on('keydown', function (e) {
    $('#error_name').remove()
});
///////////////////////////////////////////////////////////
// Validaciones del formulario para crear una grabación  //
///////////////////////////////////////////////////////////
function validate_price() {
    let price = $('#price').val()
    $('#error_price').remove()
    //No permite estar en blanco
    if (price === "") {
        $('#price').after("<span id='error_price' style='color: red; font-size: 14px'>El precio no puede estar vacío</span>")
        return false;
    }
    if (price.length > 7) {
        $('#price').after("<span id='error_price' style='color: red; font-size: 14px'>El precio ha excedido el número de dígitos.</span>")
        return false;
    }
    if (price.endsWith(".") || price.startsWith(".")) {
        $('#price').after("<span id='error_price' style='color: red; font-size: 14px'>El precio no puede tener dos (.), iniciar ni finalizar con un (.)</span>")
        return false;
    }
    return true;
}

function validate_description() {
    let description = $('#description').val()
    $('#error_description').remove()
    //No permite estar en blanco
    if (description.length > 500) {
        $('#description').after("<span id='error_description' style='color: red; font-size: 14px'>La descripción debe poseer menos de 500 caracteres. Posee " + (description.length - 500) + " caracteres más.</span>")
        return false;
    }
    return true;
}

function validate_add_record_form() {
    let is_valid_price = validate_price();
    let is_valid_description = validate_description();
    if (is_valid_price && is_valid_description) {
        return true;
    } else {
        return false;
    }

}

///////////////////////////////////////////////////////
// Validaciones del formulario para crear un cliente //
///////////////////////////////////////////////////////
function validate_customer_name() {
    let name = $('#customer-name')
    if (name.val() == "") {
        $('#error_name').remove()
        name.after("<span id='error_name' style='color: red; font-size: 14px'>El nombre no debe estar vacío</span>")
        return false
    } else {
        $('#error_name').remove()
        return true
    }
}

function validate_customer_mobile() {
    let mobile = $('#customer-mobile')
    if (mobile.val().length > 0 && mobile.val().length < 8) {
        $('#error_mobile').remove()
        mobile.after("<span id='error_mobile' style='color: red; font-size: 14px'>Debe respetar el formato. Son 8 números.jjjj</span>")
        return false
    } else {
        $('#error_mobile').remove()
        return true
    }
}

function validate_add_customer_form() {
    if (validate_customer_name() && validate_customer_mobile()) {
        $("#errorMessages").hide();
        return true;
    } else {
        return false;
    }

}


/////////////////////////////////////
// Acciones generadas por eventos  //
/////////////////////////////////////

$('#customer-photo, #id_photo').on('change', function (e) {
    let file = e.target.files[0]; // Obtiene el archivo seleccionado.
    if (file) {
        $('#preview').remove()
        $('#img-content').append('<img id="preview" src="#" alt="Previsualización de imagen" width="100%" height="100%">')
        // Verifica si se seleccionó un archivo.
        let reader = new FileReader(); // Crea un nuevo objeto FileReader para leer el contenido del archivo.
        reader.onload = function (e) { // Define una función que se ejecutará cuando se complete la lectura del archivo.
            $('#preview').attr('src', e.target.result); // Establece el atributo src de la imagen de previsualización con la URL de la imagen seleccionada.
        }
        reader.readAsDataURL(file); //Lee el contenido del archivo como una URL de datos.
    }
});


////////////////////////////////////////////////////
// Validaciones del formulario buscar grabaciones //
////////////////////////////////////////////////////

$("input[name = 'date-range-picker-start-date-myDateRangePickerCustomRanges']").on('keydown', function (e) {
    if (e.key === "Backspace" || e.key === "Delete" || e.key === "ArrowLeft" || e.key === "ArrowRight" || e.key === "ArrowUp" || e.key === "ArrowDown" || e.key === "/") {
        // Permitir teclas de control
        // respete el formato
    } else if (e.key < "0" || e.key > "9") {
        e.preventDefault()
    }
});

$("input[name = 'date-range-picker-end-date-myDateRangePickerCustomRanges']").on('keydown', function (e) {
    if (e.key === "Backspace" || e.key === "Delete" || e.key === "ArrowLeft" || e.key === "ArrowRight" || e.key === "ArrowUp" || e.key === "ArrowDown" || e.key === "/") {
        // Permitir teclas de control
    } else if (e.key < "0" || e.key > "9") {
        e.preventDefault()
    }
});
