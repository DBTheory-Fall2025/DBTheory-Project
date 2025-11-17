/**
 * Chatbox Management Module
 * Handles all chatbox UI rendering, streaming, and thinking pane logic
 */

class ChatboxManager {
  constructor() {
    this.currentStreamingElement = null;
    this.currentThinkingElement = null;
  }

  /**
   * Add a log entry to the agent panel
   * @param {string} agentId - The ID of the agent
   * @param {string} message - The message to add
   * @param {boolean} isCode - Whether the message is code
   * @param {boolean} isThinking - Whether this is a thinking pane
   * @returns {HTMLElement} The created element
   */
  addLogEntry(agentId, message, isCode = false, isThinking = false) {
    const logContainer = document.getElementById(agentId);
    if (!logContainer) return null;

    const entry = document.createElement("div");

    if (isThinking) {
      entry.className = "thinking-bubble";
      entry.innerHTML = `<div class="thinking-bubble-content">💭 Thinking</div>`;

      const content = document.createElement("div");
      content.className = "thinking-detail";
      content.style.display = "none"; // Collapsed by default

      if (isCode) {
        const codeBlock = document.createElement("pre");
        codeBlock.className = "code-block";
        const codeEl = document.createElement("code");
        codeEl.textContent = message;
        codeBlock.appendChild(codeEl);
        content.appendChild(codeBlock);
      } else {
        content.textContent = message;
      }

      entry.appendChild(content);
      entry.onclick = () => this.toggleThinkingPane(entry);
      this.currentThinkingElement = content;
    } else {
      entry.className = "log-entry";

      if (isCode) {
        const codeBlock = document.createElement("pre");
        codeBlock.className = "code-block";
        const codeEl = document.createElement("code");
        codeEl.textContent = message;
        codeBlock.appendChild(codeEl);
        entry.appendChild(codeBlock);
        this.codeElement = codeEl; // Keep reference for appending
      } else {
        entry.textContent = message;
      }

      this.currentStreamingElement = entry;
    }

    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight; // Auto-scroll

    return entry;
  }

  /**
   * Append content to the current streaming element
   * @param {string} chunk - The chunk of text to append
   * @param {boolean} isCode - Whether the content is code
   */
  appendToCurrentStream(chunk, isCode = false) {
    if (!this.currentStreamingElement) return;

    if (isCode) {
      // For code blocks, append to the code element
      if (!this.codeElement) {
        const pre = this.currentStreamingElement.querySelector("pre");
        if (pre) {
          this.codeElement = pre.querySelector("code");
        }
      }
      if (this.codeElement) {
        this.codeElement.textContent += chunk;
      }
    } else {
      // For regular text, just append
      this.currentStreamingElement.textContent += chunk;
    }

    // Auto-scroll to bottom
    const logContainer = this.currentStreamingElement.parentElement;
    if (logContainer) {
      logContainer.scrollTop = logContainer.scrollHeight;
    }
  }

  /**
   * Append content to the current thinking pane
   * @param {string} chunk - The chunk of text to append
   * @param {boolean} isCode - Whether the content is code
   */
  appendToThinkingPane(chunk, isCode = false) {
    if (!this.currentThinkingElement) return;

    if (isCode) {
      const codeEl = this.currentThinkingElement.querySelector("code");
      if (codeEl) {
        codeEl.textContent += chunk;
      }
    } else {
      this.currentThinkingElement.textContent += chunk;
    }

    // Auto-scroll to bottom
    const logContainer = this.currentThinkingElement.closest(".tab-content");
    if (logContainer) {
      logContainer.scrollTop = logContainer.scrollHeight;
    }
  }

  /**
   * Toggle the visibility of a thinking pane
   * @param {HTMLElement} container - The thinking bubble element
   */
  toggleThinkingPane(container) {
    const content = container.querySelector(".thinking-detail");
    if (!content) return;

    if (content.style.display === "none") {
      content.style.display = "block";
    } else {
      content.style.display = "none";
    }
  }

  /**
   * Complete the current stream and reset
   */
  completeStream() {
    this.currentStreamingElement = null;
    this.currentThinkingElement = null;
  }

  /**
   * Add a retry message (for rate limit retries)
   * @param {string} agentId - The agent ID
   * @param {string} message - The retry message
   */
  addRetryMessage(agentId, message) {
    const logContainer = document.getElementById(agentId);
    if (!logContainer) return;

    const entry = document.createElement("div");
    entry.className = "retry-message";

    const icon = document.createElement("span");
    icon.className = "retry-icon";
    icon.textContent = "⏳ ";

    const text = document.createElement("span");
    text.className = "retry-text";
    text.textContent = message;

    entry.appendChild(icon);
    entry.appendChild(text);

    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight;
  }

  /**
   * Add an error message with retry button
   * @param {string} agentId - The agent ID
   * @param {string} message - The error message
   */
  addErrorMessage(agentId, message) {
    const logContainer = document.getElementById(agentId);
    if (!logContainer) return;

    const entry = document.createElement("div");
    entry.className = "error-message";

    const icon = document.createElement("span");
    icon.className = "error-icon";
    icon.textContent = "⚠️ ";

    const text = document.createElement("span");
    text.className = "error-text";
    text.textContent = message;

    const button = document.createElement("button");
    button.className = "retry-button";
    button.textContent = "Retry Workflow";
    button.onclick = () => {
      showMessage("Retrying workflow...", "info");
      combineDatabases();
    };

    entry.appendChild(icon);
    entry.appendChild(text);
    entry.appendChild(button);

    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight;
  }
}

// Create a global instance
const chatboxManager = new ChatboxManager();

/**
 * Listen for streaming updates from the server via Server-Sent Events (SSE)
 */
function listenForUpdates() {
  const eventSource = new EventSource("/status");

  eventSource.onmessage = function (event) {
    const data = JSON.parse(event.data);

    // Handle workflow completion
    if (data.agentId === "workflow-complete") {
      renderMermaidDiagram();
      chatboxManager.completeStream();
      eventSource.close();
      return;
    }

    // Handle errors
    if (data.agentId === "error") {
      showMessage(data.message, "error");
      chatboxManager.completeStream();
      eventSource.close();
      return;
    }

    // Render diagram with active node
    renderMermaidDiagram(data.nodeId);

    // Open the tab for this agent
    openTab(null, data.agentId);

    // Handle retry messages
    if (data.isRetry) {
      chatboxManager.addRetryMessage(data.agentId, data.message);
      return;
    }

    // Handle error with retry prompt
    if (data.retryPrompt) {
      chatboxManager.addErrorMessage(data.agentId, data.message);
      return;
    }

    // Handle different message types
    if (data.type === "thinking") {
      // This is a thinking pane message
      if (data.isStreaming && !data.streamComplete) {
        // Streaming chunk
        if (!chatboxManager.currentThinkingElement) {
          // Create new thinking pane
          chatboxManager.addLogEntry(data.agentId, "", false, true);
        }
        chatboxManager.appendToThinkingPane(data.message, false);
      }
    } else {
      // Regular message
      if (data.isStreaming && !data.streamComplete) {
        // Streaming chunk
        if (!chatboxManager.currentStreamingElement) {
          // Create new log entry for this stream
          chatboxManager.addLogEntry(data.agentId, "", data.isCode, false);
        }
        chatboxManager.appendToCurrentStream(data.message, data.isCode);
      } else if (data.streamComplete) {
        // Stream finished
        chatboxManager.completeStream();
      }
    }
  };

  eventSource.onerror = function (err) {
    console.error("EventSource failed:", err);
    showMessage("Connection to server lost.", "error");
    chatboxManager.completeStream();
    eventSource.close();
  };
}

/**
 * Render the workflow diagram, optionally highlighting an active node
 * @param {string|null} activeNodeId - The node to highlight, or null for no highlight
 */
async function renderMermaidDiagram(activeNodeId = null) {
  const container = document.getElementById("mermaid-diagram");
  if (!container) return;

  container.innerHTML = ""; // Clear previous diagram

  const agentWorkflow = `
graph TD
    A[Similarity Finder] --> B[New Schema Generator];
    B --> C[Conversion Generator];
    C --> D[SQL Generator];
    D --> E[SQL Executor];
    E --> F[SQL Error Handler];
    F --> D;
    C --> G[Conversion Executor];
    G --> H[Conversion Error Handler];
    H --> C;
    D --> I[Logic Checker];
    I --> B;
    I --> C;
    I --> D;
`;

  let diagram = agentWorkflow;
  if (activeNodeId) {
    diagram += `\nstyle ${activeNodeId} fill:#f9f,stroke:#333,stroke-width:4px`;
  }

  try {
    const { svg } = await window.mermaid.render("mermaid-svg", diagram);
    container.innerHTML = svg;
  } catch (err) {
    console.error("Failed to render mermaid diagram:", err);
  }
}

/**
 * Open a specific tab
 * @param {Event|null} evt - The click event, or null if called programmatically
 * @param {string} tabName - The name of the tab to open
 */
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
