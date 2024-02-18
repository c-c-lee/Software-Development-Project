function populateDropdown() {
    var populationType = document.getElementById("population_type").value;
    var dropdown = document.getElementById("selected_population");
    dropdown.innerHTML = ""; // Clear existing options

    if (populationType === "superpopulation") {
        // Populate superpopulation options
        var superpopulations = ["East Asian", "Europe", "Ad Mixed American", "African", "South Asian"];
        for (var i = 0; i < superpopulations.length; i++) {
            var option = document.createElement("option");
            option.text = superpopulations[i];
            option.value = superpopulations[i];
            dropdown.add(option);
        }
    } else if (populationType === "population") {
        // Populate population options
        var populations = ["Siberian", "British in England and Scotland", "Finnish in Finland", "Southern Han Chinese", "Puerto Rican from Puerto Rico", "Chinese Dai in Xishuangbanna, China", "Colombian from Medellin, Colombia", "Iberian population in Spain", "Peruvian from Lima, Peru", "Punjabi from Lahore, Pakistan", "Kinh in Ho Chi Minh City, Vietnam", "African Caribbean in Barbados", "Gambian in Western Division, Gambia", "Esan in Nigeria", "Bengali from Bangladesh", "Mende in Sierra, Leone", "Sri Lankan Tamil from the UK", "Indian Telugu from the UK", "Utah Residents (CEPH) with Northern and Western European ancestry", "Yoruba in Ibadan, Nigeria", "Han Chinese in Beijing, China", "Japanese in Tokyo, Japan", "Luhya in Webuye, Kenya", "American's of African Ancestry in SW, USA", "Mexican Ancestry from Los Angeles, USA", "Toscani in Italia", "Gujarati Indian from Houston, Texas"];
        for (var j = 0; j < populations.length; j++) {
            var option = document.createElement("option");
            option.text = populations[j];
            option.value = populations[j];
            dropdown.add(option);
        }
    }
}

document.getElementById("selected_population").addEventListener("change", handleSelection);

function handleSelection() {
    var selectedPopulationsContainer = document.getElementById("selectedPopulationsContainer");
    selectedPopulationsContainer.innerHTML = ""; // Clear existing selections

    var selectedPopulations = document.getElementById("selected_population").selectedOptions;

    for (var i = 0; i < selectedPopulations.length; i++) {
        var selectedPopulation = selectedPopulations[i].value;
        var selectedPopulationBox = document.createElement("div");
        selectedPopulationBox.className = "selected-population";
        
        var populationText = document.createElement("span");
        populationText.innerText = selectedPopulation;

        var closeIcon = document.createElement("span");
        closeIcon.innerText = "×";
        closeIcon.addEventListener("click", function () {
            // Deselect the population when the close icon is clicked
            document.getElementById("selected_population").querySelector('option[value="' + selectedPopulation + '"]').selected = false;
            handleSelection();
        });

        selectedPopulationBox.appendChild(populationText);
        selectedPopulationBox.appendChild(closeIcon);
        selectedPopulationsContainer.appendChild(selectedPopulationBox);
    }
}
