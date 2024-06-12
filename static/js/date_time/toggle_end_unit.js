function displayEndTimeUnits(show) {
    let endDiv = document.getElementById('div_id_end_date_time');
    if (show) {
        endDiv.style.display = "block";
    }
    else
    {
        endDiv.style.display = "none";
    }
}

var hasEndCheck = document.getElementById('id_has_end');

displayEndTimeUnits(hasEndCheck.checked)

hasEndCheck.onchange = function() {
    displayEndTimeUnits(hasEndCheck.checked)
};
