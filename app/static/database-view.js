// Database viewer state
let currentPage = 1;
let currentTable = null;
const PAGE_SIZE = 25;

// Table management functions
async function loadTableList() {
  try {
    const response = await fetch("/get-tables");
    const data = await response.json();

    const tableList = document.getElementById("table-list");
    tableList.innerHTML = "";

    if (!data.success) {
      throw new Error(data.error || "Failed to load tables");
    }

    data.tables.forEach((table) => {
      const div = document.createElement("div");
      div.className = "side-panel-item";
      div.textContent = table;
      div.dataset.table = table;
      div.onclick = () => showTable(table);
      tableList.appendChild(div);
    });
  } catch (err) {
    window.showMessage(err.message, "error");
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
  document.querySelectorAll(".side-panel-item").forEach((item) => {
    item.classList.remove("active");
    if (item.dataset.table === tableName) {
      item.classList.add("active");
    }
  });

  const response = await fetch(
    `/get-table-data?table=${tableName}&page=${page}&size=${PAGE_SIZE}`
  );
  const data = await response.json();
  renderTable(data);
}

function renderTable(data) {
  const table = document.getElementById("data-table");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");

  // Render headers
  thead.innerHTML = `<tr>${data.columns
    .map((col) => `<th>${col}</th>`)
    .join("")}</tr>`;

  // Render rows
  tbody.innerHTML = data.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`)
    .join("");
}

// SQL execution functions
async function executeSQL() {
  const query = document.getElementById("sql-input").value;
  const output = document.getElementById("sql-output");

  try {
    const response = await fetch("/execute-sql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.error) {
      output.innerHTML = `<div class="error">${data.error}</div>`;
    } else if (data.message) {
      output.innerHTML = `<div class="success">${data.message}</div>`;
    } else if (data.columns && data.rows) {
      output.innerHTML = `<table>${
        `<tr>${data.columns.map((col) => `<th>${col}</th>`).join("")}</tr>` +
        data.rows
          .map(
            (row) =>
              `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`
          )
          .join("")
      }</table>`;
    }
  } catch (err) {
    output.innerHTML = `<div class="error">Failed to execute query: ${err.message}</div>`;
  }
}

// Database reload functionality
async function reloadDatabase() {
  const button = document.getElementById("reload-db");
  const icon = button.querySelector("i");
  icon.classList.add("fa-spin");
  button.disabled = true;

  try {
    // Reload table list
    await loadTableList();

    // If we're in SQL view, clear the output
    if (
      document.getElementById("sql-editor-container").style.display !== "none"
    ) {
      document.getElementById("sql-output").innerHTML = "";
    }
    // If we're in table view, reload the current table
    else if (currentTable) {
      await showTable(currentTable, 1);
    }

    window.showMessage("Database reloaded successfully", "success");
  } catch (err) {
    window.showMessage("Failed to reload database: " + err.message, "error");
  } finally {
    icon.classList.remove("fa-spin");
    button.disabled = false;
  }
}

// Initialization function
function initializeDatabaseViewer() {
  // Set up SQL editor view as default
  document.querySelector('[data-view="sql"]').classList.add("active");

  // Set up SQL run button
  document.getElementById("run-sql").addEventListener("click", executeSQL);

  // Set up reload button
  document
    .getElementById("reload-db")
    .addEventListener("click", reloadDatabase);

  // Set up SQL view button
  document.querySelector('[data-view="sql"]').addEventListener("click", () => {
    document.getElementById("sql-editor-container").style.display = "flex";
    document.getElementById("table-viewer").style.display = "none";
    document
      .querySelectorAll(".side-panel-item")
      .forEach((item) => item.classList.remove("active"));
    document.querySelector('[data-view="sql"]').classList.add("active");
  });

  // Set up table search
  const searchInput = document.querySelector(".table-search");
  searchInput.addEventListener(
    "input",
    debounce(async (e) => {
      if (!currentTable) return;

      const response = await fetch(
        `/search-table?table=${currentTable}&search=${e.target.value}`
      );
      const data = await response.json();
      renderTable(data);
    }, 300)
  );

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
  tableContainer.addEventListener(
    "scroll",
    debounce(async () => {
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
            data.rows
              .map(
                (row) =>
                  `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`
              )
              .join("")
          );
        }
      }
    }, 100)
  );
}

// Utility functions
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

// Export functions
export { initializeDatabaseViewer, loadTableList };
