document.addEventListener("DOMContentLoaded", function() {
    const settingsContainer = document.getElementById("settings-container");
    const searchInput = document.getElementById("search-input");
    const categorySelect = document.getElementById("category-select");

    let settingsData = [];

    // Fetch settings data from the server
    async function fetchSettings() {
        const response = await fetch('/api/settings');
        settingsData = await response.json();
        displaySettings(settingsData);
    }

    // Display settings in the container
    function displaySettings(settings) {
        settingsContainer.innerHTML = '';
        settings.forEach(setting => {
            const settingDiv = document.createElement("div");
            settingDiv.classList.add("setting");
            settingDiv.innerHTML = `
                <h3>${setting.name}</h3>
                <p>${setting.description}</p>
                <p><strong>Value:</strong> ${setting.value}</p>
            `;
            settingsContainer.appendChild(settingDiv);
        });
    }

    // Filter settings based on search input and selected category
    function filterSettings() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategory = categorySelect.value;

        const filteredSettings = settingsData.filter(setting => {
            const matchesSearch = setting.name.toLowerCase().includes(searchTerm) || 
                                  setting.description.toLowerCase().includes(searchTerm);
            const matchesCategory = selectedCategory === "all" || setting.category === selectedCategory;
            return matchesSearch && matchesCategory;
        });

        displaySettings(filteredSettings);
    }

    // Event listeners for search input and category select
    searchInput.addEventListener("input", filterSettings);
    categorySelect.addEventListener("change", filterSettings);

    // Initialize the app
    fetchSettings();
});