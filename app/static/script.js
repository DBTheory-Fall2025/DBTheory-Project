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

// Database Viewer Functions
let currentPage = 1;
let currentTable = null;
const PAGE_SIZE = 25;

async function loadTableList() {
  try {
    const response = await fetch("/get-tables");
    const data = await response.json();
    
    const tableList = document.getElementById("table-list");
    tableList.innerHTML = "";
    
    if (!data.success) {
      throw new Error(data.error || "Failed to load tables");
    }
    
    data.tables.forEach(table => {
      const div = document.createElement("div");
      div.className = "side-panel-item";
      div.textContent = table;
      div.dataset.table = table;
      div.onclick = () => showTable(table);
      tableList.appendChild(div);
    });
  } catch (err) {
    showMessage(err.message, "error");
  }
}

async function reloadDatabase() {
  const button = document.getElementById("reload-db");
  const icon = button.querySelector("i");
  icon.classList.add("fa-spin");
  button.disabled = true;
  
  try {
    // Reload table list
    await loadTableList();
    
    // If we're in SQL view, clear the output
    if (document.getElementById("sql-editor-container").style.display !== "none") {
      document.getElementById("sql-output").innerHTML = "";
    }
    // If we're in table view, reload the current table
    else if (currentTable) {
      await showTable(currentTable, 1);
    }
    
    showMessage("Database reloaded successfully", "success");
  } catch (err) {
    showMessage("Failed to reload database: " + err.message, "error");
  } finally {
    icon.classList.remove("fa-spin");
    button.disabled = false;
  }
}

async function showTable(tableName, page = 1) {
  currentTable = tableName;
  currentPage = page;
  
  const tableViewer = document.getElementById("table-viewer");
  const sqlEditor = document.getElementById("sql-editor-container");
  
  tableViewer.style.display = "flex";
  sqlEditor.style.display = "none";
  
  // Update active state in side panel
  document.querySelectorAll(".side-panel-item").forEach(item => {
    item.classList.remove("active");
    if (item.dataset.table === tableName) {
      item.classList.add("active");
    }
  });
  
  const response = await fetch(`/get-table-data?table=${tableName}&page=${page}&size=${PAGE_SIZE}`);
  const data = await response.json();
  
  renderTable(data);
  
  // Update active state in side panel
  document.querySelectorAll(".side-panel-item").forEach(item => {
    item.classList.remove("active");
    if (item.dataset.table === tableName) {
      item.classList.add("active");
    }
  });
}

function renderTable(data) {
  const table = document.getElementById("data-table");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  
  // Render headers
  thead.innerHTML = `<tr>${data.columns.map(col => `<th>${col}</th>`).join("")}</tr>`;
  
  // Render rows
  tbody.innerHTML = data.rows.map(row => 
    `<tr>${row.map(cell => `<td>${cell}</td>`).join("")}</tr>`
  ).join("");
}

async function executeSQL() {
  const query = document.getElementById("sql-input").value;
  const output = document.getElementById("sql-output");
  
  try {
    const response = await fetch("/execute-sql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    
    const data = await response.json();
    
    if (data.error) {
      output.innerHTML = `<div class="error">${data.error}</div>`;
    } else if (data.message) {
      output.innerHTML = `<div class="success">${data.message}</div>`;
    } else if (data.columns && data.rows) {
      output.innerHTML = `<table>${
        `<tr>${data.columns.map(col => `<th>${col}</th>`).join("")}</tr>` +
        data.rows.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join("")}</tr>`).join("")
      }</table>`;
    }
  } catch (err) {
    output.innerHTML = `<div class="error">Failed to execute query: ${err.message}</div>`;
  }
}

function initializeDatabaseViewer() {
  // Set up SQL editor view as default
  document.querySelector('[data-view="sql"]').classList.add("active");
  
  // Set up SQL run button
  document.getElementById("run-sql").addEventListener("click", executeSQL);
  
  // Set up reload button
  document.getElementById("reload-db").addEventListener("click", reloadDatabase);
  
  // Set up SQL view button
  document.querySelector('[data-view="sql"]').addEventListener("click", () => {
    document.getElementById("sql-editor-container").style.display = "flex";
    document.getElementById("table-viewer").style.display = "none";
    document.querySelectorAll(".side-panel-item").forEach(item => item.classList.remove("active"));
    document.querySelector('[data-view="sql"]').classList.add("active");
  });
  
  // Set up table search
  const searchInput = document.querySelector(".table-search");
  searchInput.addEventListener("input", debounce(async (e) => {
    if (!currentTable) return;
    
    const response = await fetch(`/search-table?table=${currentTable}&search=${e.target.value}`);
    const data = await response.json();
    renderTable(data);
  }, 300));
  
  // Set up resizable divider
  const divider = document.getElementById("sql-divider");
  let isResizing = false;
  
  divider.addEventListener("mousedown", (e) => {
    isResizing = true;
    document.body.style.cursor = "row-resize";
  });
  
  document.addEventListener("mousemove", (e) => {
    if (!isResizing) return;
    
    const container = document.getElementById("sql-editor-container");
    const editor = document.querySelector(".sql-editor");
    const results = document.querySelector(".sql-results");
    const containerRect = container.getBoundingClientRect();
    
    const newEditorHeight = e.clientY - containerRect.top;
    const totalHeight = container.offsetHeight;
    
    if (newEditorHeight > 100 && newEditorHeight < totalHeight - 100) {
      editor.style.height = `${newEditorHeight}px`;
      results.style.height = `${totalHeight - newEditorHeight - 5}px`;
    }
  });
  
  document.addEventListener("mouseup", () => {
    isResizing = false;
    document.body.style.cursor = "";
  });
  
  // Initialize infinite scroll for table viewer
  const tableContainer = document.querySelector(".table-container");
  tableContainer.addEventListener("scroll", debounce(async () => {
    if (!currentTable) return;
    
    const { scrollTop, scrollHeight, clientHeight } = tableContainer;
    if (scrollTop + clientHeight >= scrollHeight - 100) {
      currentPage++;
      const response = await fetch(
        `/get-table-data?table=${currentTable}&page=${currentPage}&size=${PAGE_SIZE}`
      );
      const data = await response.json();
      
      if (data.rows.length > 0) {
        const tbody = document.querySelector("#data-table tbody");
        tbody.insertAdjacentHTML(
          "beforeend",
          data.rows.map(row => 
            `<tr>${row.map(cell => `<td>${cell}</td>`).join("")}</tr>`
          ).join("")
        );
      }
    }
  }, 100));
}

// Utility function for debouncing
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Initial setup
document.addEventListener("DOMContentLoaded", () => {
  loadDatabases();
  renderMermaidDiagram();
  initializeDatabaseViewer();
});
