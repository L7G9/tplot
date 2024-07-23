function displayEndTimeUnits(show) {
    let endFractionDiv = document.getElementById('div_id_end_year_fraction');
    let endMultiplierDiv = document.getElementById('div_id_end_multiplier');
    if (show) {
        endFractionDiv.style.display = "block";
        endMultiplierDiv.style.display = "block";
    }
    else
    {
        endFractionDiv.style.display = "none";
        endMultiplierDiv.style.display = "none";
    }
}

var hasEndCheck = document.getElementById('id_has_end');

displayEndTimeUnits(hasEndCheck.checked)

hasEndCheck.onchange = function() {
    displayEndTimeUnits(hasEndCheck.checked)
};
