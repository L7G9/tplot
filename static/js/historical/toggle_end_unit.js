function displayEndTimeUnits(show) {
    let endBCADDiv = document.getElementById('div_id_end_bc_ad');
    let endYearDiv = document.getElementById('div_id_end_year');
    if (show) {
        endBCADDiv.style.display = "block";
        endYearDiv.style.display = "block";
    }
    else
    {
        endBCADDiv.style.display = "none";
        endYearDiv.style.display = "none";
    }
}

var hasEndCheck = document.getElementById('id_has_end');

displayEndTimeUnits(hasEndCheck.checked)

hasEndCheck.onchange = function() {
    displayEndTimeUnits(hasEndCheck.checked)
};
