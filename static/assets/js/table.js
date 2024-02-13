function hover_function() {
    if (window.matchMedia("(max-width: 767px)").matches) {
        // Código para tablets y teléfonos
        // Por ejemplo, puedes cambiar la funcionalidad de la tabla o mostrar un diseño diferente
    } else {
        // Código para ordenadores
        // Oculta los botones y etiquetas a.
        let tr = $('tr')
        tr.off('mouseover')
        tr.off('mouseout')
        tr.find('button, a').hide()
        // Muesra los botones y etiquetas a cuando pasas el puntero por encima de la fila de la tabla
        tr.hover(
            function () {
                $(this).find('button, a').off('mouseover')
                $(this).find('button, a').off('mouseout')
                $(this).find('button, a').toggle();
                this.stopImmediatePropagation()
            }
        );
    }
}

