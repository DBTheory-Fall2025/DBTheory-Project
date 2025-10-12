let selectedItems = [];
let allItems = [];

// --- Agent Workflow ---
const agentWorkflow = `
graph TD
    A[Similarity Finder] --> B[New Schema Generator];
    B --> C[Conversion Generator];
    C --> D[SQL Generator];
    D --> E[SQL Executor];
    E --> F{SQL Error Handler};
    F --> D;
    C --> G[Conversion Executor];
    G --> H{Conversion Error Handler};
    H --> C;
    E --> I[Logic Checker];
    I -- Logic OK --> J[End];
    I -- Rerun --> B;
`;

async function renderMermaidDiagram(activeNodeId = null) {
  const container = document.getElementById("mermaid-diagram");
  container.innerHTML = ""; // Clear previous diagram

  let diagram = agentWorkflow;
  if (activeNodeId) {
    diagram += `\nstyle ${activeNodeId} fill:#f9f,stroke:#333,stroke-width:4px`;
  }

  const { svg } = await mermaid.render("mermaid-svg", diagram);
  container.innerHTML = svg;
}

function addLogEntry(agentId, message, isCode = false) {
  const logContainer = document.getElementById(agentId);
  if (!logContainer) return;

  const entry = document.createElement("div");
  entry.className = "log-entry";

  if (isCode) {
    entry.innerHTML = `<code>${message.replace(/\n/g, "<br>")}</code>`;
  } else {
    entry.textContent = message;
  }

  logContainer.appendChild(entry);
  logContainer.scrollTop = logContainer.scrollHeight; // Auto-scroll
}

function listenForUpdates() {
  const eventSource = new EventSource("/status");

  eventSource.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.agentId === "workflow-complete") {
      renderMermaidDiagram(); // Reset diagram
      eventSource.close();
      return;
    }

    if (data.agentId === "error") {
      showMessage(data.message, "error");
      eventSource.close();
      return;
    }

    renderMermaidDiagram(data.nodeId);
    openTab(null, data.agentId);
    addLogEntry(data.agentId, data.message, data.isCode);
  };

  eventSource.onerror = function (err) {
    console.error("EventSource failed:", err);
    showMessage("Connection to server lost.", "error");
    eventSource.close();
  };
}
// --- End Agent Workflow ---

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
  if (resultsContainer) {
    resultsContainer.style.display = "block";
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

function openTab(evt, tabName) {
  const tabcontent = document.getElementsByClassName("tab-content");
  for (let i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  const tablinks = document.getElementsByClassName("tab-link");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove("active");
  }

  const targetContent = document.getElementById(tabName);
  if (targetContent) {
    targetContent.style.display = "block";
  }

  const targetLink = document.querySelector(`.tab-link[data-tab="${tabName}"]`);
  if (targetLink) {
    targetLink.classList.add("active");
  }
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

// Initial setup
loadDatabases();
renderMermaidDiagram();
