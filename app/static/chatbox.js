/**
 * Chatbox Management Module
 * Handles all chatbox UI rendering, streaming, and thinking pane logic
 */

class ChatboxManager {
  constructor() {
    this.currentStreamingElement = null;
    this.currentThinkingElement = null;
    this.currentStreamBuffer = "";
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

    // Reset buffer for new stream
    this.currentStreamBuffer = "";

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
      // For regular text, handle streaming formatting
      this.currentStreamBuffer += chunk;
      const text = this.currentStreamBuffer.trim();

      // Check if it looks like the start of a JSON object/array
      if (text.startsWith("{") || text.startsWith("[")) {
        const formatted = this.formatPartialJSON(this.currentStreamBuffer);
        this.currentStreamingElement.textContent = formatted;
        this.currentStreamingElement.style.whiteSpace = "pre-wrap";
        this.currentStreamingElement.style.fontFamily = "monospace";
      } else {
        this.currentStreamingElement.textContent = this.currentStreamBuffer;
      }
    }

    // Auto-scroll to bottom
    const logContainer = this.currentStreamingElement.parentElement;
    if (logContainer) {
      logContainer.scrollTop = logContainer.scrollHeight;
    }
  }

  formatPartialJSON(text) {
    let indent = 0;
    let inString = false;
    let result = "";
    let lastChar = "";

    for (let i = 0; i < text.length; i++) {
      const char = text[i];

      if (char === '"' && lastChar !== "\\") {
        inString = !inString;
      }

      if (!inString) {
        if (char === "{" || char === "[") {
          result += char + "\n" + "  ".repeat(indent + 1);
          indent++;
        } else if (char === "}" || char === "]") {
          indent = Math.max(0, indent - 1);
          result += "\n" + "  ".repeat(indent) + char;
        } else if (char === ",") {
          result += char + "\n" + "  ".repeat(indent);
        } else if (char === ":") {
          result += ": ";
        } else {
          // Keep non-whitespace chars
          if (char.trim() !== "") {
            result += char;
          }
        }
      } else {
        result += char;
      }
      lastChar = char;
    }
    return result;
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
    // Attempt to format the completed log entry
    if (this.currentStreamingElement) {
      this.formatLogEntry(this.currentStreamingElement);
    }

    this.currentStreamingElement = null;
    this.currentThinkingElement = null;
  }

  /**
   * Format a log entry (markdown, json, html, mermaid)
   * @param {HTMLElement} element - The log entry element
   */
  formatLogEntry(element) {
    if (!element) return;

    // Check if it's a code block (isCode=true was used)
    const codeBlock = element.querySelector("pre.code-block code");
    if (codeBlock) {
      this.formatJSONInElement(codeBlock);
      return;
    }

    // Text entry - process markdown blocks
    const text = element.textContent;
    const parts = text.split(/(```(?:json|mermaid|html)?\s*[\s\S]*?```)/g);

    if (parts.length > 1) {
      element.innerHTML = ""; // Clear content
      element.style.whiteSpace = "normal"; // Reset style from streaming
      element.style.fontFamily = "inherit";

      parts.forEach((part) => {
        const codeMatch = part.match(
          /^```(json|mermaid|html)?\s*([\s\S]*?)```$/
        );
        if (codeMatch) {
          const lang = codeMatch[1];
          const codeContent = codeMatch[2];

          if (lang === "mermaid") {
            const mermaidDiv = document.createElement("div");
            mermaidDiv.className = "mermaid";
            mermaidDiv.textContent = codeContent.trim();
            element.appendChild(mermaidDiv);
            try {
              window.mermaid.init(undefined, mermaidDiv);
            } catch (e) {
              console.error("Mermaid render error:", e);
            }
            return;
          }

          if (lang === "html") {
            const htmlDiv = document.createElement("div");
            htmlDiv.innerHTML = codeContent; // Allow HTML rendering
            element.appendChild(htmlDiv);
            return;
          }

          // Handle JSON or generic code
          let formattedCode = codeContent;
          if (!lang || lang === "json") {
            try {
              const json = JSON.parse(codeContent.trim());
              formattedCode = JSON.stringify(json, null, 2);
            } catch (e) {
              // Not JSON, keep as is
            }
          }

          const pre = document.createElement("pre");
          pre.className = "code-block";
          const code = document.createElement("code");
          code.textContent = formattedCode;
          pre.appendChild(code);
          element.appendChild(pre);
        } else {
          // Regular text part - Render Markdown
          if (part.trim() !== "") {
            const p = document.createElement("div");
            if (window.marked && window.marked.parse) {
              p.innerHTML = window.marked.parse(part);
            } else {
              p.textContent = part;
            }
            element.appendChild(p);
          }
        }
      });
      return;
    }

    // If no markdown blocks, check if the whole content looks like JSON
    if (
      (text.trim().startsWith("{") && text.trim().endsWith("}")) ||
      (text.trim().startsWith("[") && text.trim().endsWith("]"))
    ) {
      try {
        JSON.parse(text); // Validate
        this.formatJSONInElement(element);
        return;
      } catch (e) {
        // Not valid JSON, fall through
      }
    }

    // Fallback: Render whole text as Markdown
    if (window.marked && window.marked.parse) {
      element.innerHTML = window.marked.parse(text);
      element.style.whiteSpace = "normal";
      element.style.fontFamily = "inherit";
    }
  }

  /**
   * Try to parse and pretty-print JSON inside an element
   * @param {HTMLElement} element
   */
  formatJSONInElement(element) {
    try {
      // Remove potential markdown fences if they exist in the text content
      let text = element.textContent.trim();
      text = text.replace(/^```(?:json)?/, "").replace(/```$/, "");

      const json = JSON.parse(text);
      element.textContent = JSON.stringify(json, null, 2);

      // If the parent is not a pre block, wrap it (for the non-isCode case)
      if (element.tagName !== "CODE" && element.tagName !== "PRE") {
        const pre = document.createElement("pre");
        pre.className = "code-block";
        const code = document.createElement("code");
        code.textContent = element.textContent;
        pre.appendChild(code);
        element.innerHTML = "";
        element.appendChild(pre);
      }
    } catch (e) {
      // Not valid JSON, leave as is
    }
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
      } else {
        // Non-streaming complete message (e.g., status update)
        const entry = chatboxManager.addLogEntry(
          data.agentId,
          data.message,
          data.isCode,
          false
        );
        chatboxManager.formatLogEntry(entry);
        // Reset currentStreamingElement so next message starts a new entry
        chatboxManager.currentStreamingElement = null;
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
