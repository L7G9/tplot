function displayEndTimeUnits(show) {
    let endYearDiv = document.getElementById('div_id_end_year');
    let endMonthDiv = document.getElementById('div_id_end_month');
    if (show) {
        endYearDiv.style.display = "block";
        endMonthDiv.style.display = "block";
    }
    else
    {
        endYearDiv.style.display = "none";
        endMonthDiv.style.display = "none";
    }
}

var hasEndCheck = document.getElementById('id_has_end');

displayEndTimeUnits(hasEndCheck.checked)

hasEndCheck.onchange = function() {
    displayEndTimeUnits(hasEndCheck.checked)
};
