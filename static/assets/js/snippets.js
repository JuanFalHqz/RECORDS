const myDateRangePickerCustomRanges = document.getElementById('myDateRangePickerCustomRanges')
if (myDateRangePickerCustomRanges) {
    const optionsCustomRanges = {
        locale: 'es',
        ranges: {
            'Día de hoy': [new Date(), new Date()],

            'Día de ayer': [
                new Date(new Date().setDate(new Date().getDate() - 1)),
                new Date(new Date().setDate(new Date().getDate() - 1))
            ],
            'Últimos 7 días': [
                new Date(new Date().setDate(new Date().getDate() - 6)),
                new Date(new Date())
            ],
            'Últimos 30 días': [
                new Date(new Date().setDate(new Date().getDate() - 29)),
                new Date(new Date())
            ],
            'Este mes': [
                new Date(new Date().setDate(1)),
                new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0)
            ],
            'Último mes': [
                new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1),
                new Date(new Date().getFullYear(), new Date().getMonth(), 0)
            ]
        }
    }

    new coreui.DateRangePicker(myDateRangePickerCustomRanges, optionsCustomRanges)
}

$("input[name = 'date-range-picker-start-date-myDateRangePickerCustomRanges']").attr('autocomplete', 'off')
$("input[name = 'date-range-picker-start-date-myDateRangePickerCustomRanges']").attr('placeholder', 'Fecha inicial (dd/mm/aaaa)')
$("input[name = 'date-range-picker-end-date-myDateRangePickerCustomRanges']").attr('autocomplete', 'off')
$("input[name = 'date-range-picker-end-date-myDateRangePickerCustomRanges']").attr('placeholder', 'Fecha final (dd/mm/aaaa)')