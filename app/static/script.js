let selectedItems = [];
let allItems = [];

async function loadDatabases() {
  const response = await fetch("/get-databases");
  const data = await response.json();

  const availableContainer = document.querySelector(".available-items");
  if (!data.success) {
    showMessage(data.error || "An unknown error occurred.", "error");
    availableContainer.innerHTML = `<div class="item">Could not load databases.</div>`;
    return;
  }

  allItems = data.databases;
  if (allItems.length === 0) {
    availableContainer.innerHTML = `<div class="item">No databases found in config file.</div>`;
  } else {
    updateAvailableItems();
  }
}

function updateSelectedItems() {
  const container = document.querySelector(".selected-items");
  container.innerHTML = "";

  selectedItems.forEach((item) => {
    const div = document.createElement("div");
    div.className = "selected-item";
    div.innerHTML = `
      <span>${item}</span>
      <i class="fas fa-times remove-icon" onclick="deselectItem('${item}')"></i>
    `;
    container.appendChild(div);
  });
}

function updateAvailableItems() {
  const searchBox = document.querySelector(".search-box");
  const filter = searchBox.value.toLowerCase();
  const availableContainer = document.querySelector(".available-items");

  const filteredItems = allItems.filter(
    (item) =>
      !selectedItems.includes(item) && item.toLowerCase().includes(filter)
  );

  availableContainer.innerHTML = "";
  filteredItems.forEach((item) => {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <i class="fas fa-plus add-icon"></i>
      <span>${item}</span>
    `;
    div.onclick = () => selectItem(item);
    availableContainer.appendChild(div);
  });
}

function selectItem(item) {
  if (!selectedItems.includes(item)) {
    selectedItems.push(item);
    updateSelectedItems();
    updateAvailableItems();
  }
}

function deselectItem(item) {
  selectedItems = selectedItems.filter((i) => i !== item);
  updateSelectedItems();
  updateAvailableItems();
}

function showMessage(message, type = "success") {
  const statusDiv = document.getElementById("status-message");
  statusDiv.textContent = message;
  statusDiv.className = `status-message ${type}`;
}

async function combineDatabases() {
  const newDbName = document.getElementById("new-db-name").value;

  const resultsContainer = document.getElementById("results-container");
  const databaseViewer = document.getElementById("database-viewer");
  if (resultsContainer) {
    resultsContainer.style.display = "block";
  }
  if (databaseViewer) {
    databaseViewer.style.display = "block";
  }

  // Add a divider to all log tabs
  const logContainer = document.getElementById("agent-logs");
  const allLogTabs = logContainer.querySelectorAll(".tab-content");

  allLogTabs.forEach((tab) => {
    const divider = document.createElement("div");
    divider.className = "log-divider";
    divider.textContent = `New Combination: ${newDbName}`;
    tab.appendChild(divider);
  });

  // Start listening for real-time updates
  listenForUpdates();

  const response = await fetch("/combine-databases", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      selected_dbs: selectedItems,
      new_db_name: newDbName,
    }),
  });

  const data = await response.json();
  showMessage(
    data.error || "Database combination process started.",
    data.success ? "success" : "error"
  );
}

// Event listeners
document
  .querySelector(".search-box")
  .addEventListener("input", updateAvailableItems);

document.querySelectorAll(".tab-link").forEach((tab) => {
  tab.addEventListener("click", (event) => {
    openTab(event, event.currentTarget.dataset.tab);
  });
});

// Make functions available to other modules and global scope
window.showMessage = showMessage;
window.combineDatabases = combineDatabases;
window.deselectItem = deselectItem;
window.selectItem = selectItem;
window.openTab = openTab;

// Import database viewer
import { initializeDatabaseViewer } from "./database-view.js";

// Initial setup
document.addEventListener("DOMContentLoaded", () => {
  loadDatabases();
  renderMermaidDiagram();
  initializeDatabaseViewer();
});
