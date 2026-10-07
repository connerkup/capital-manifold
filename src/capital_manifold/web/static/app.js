/**
 * CAPITAL MANIFOLD: INSTITUTIONAL FINANCIAL ENGINEERING FRONTEND
 * Palantir / Bloomberg Terminal / Linear Aesthetic
 */

document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

const App = {
  // State
  activeTab: "tab-graph",
  cy: null,
  topologyData: null,
  scorecardData: null,
  poolsData: [],
  featuredCircuits: [],
  selectedNodeId: null,
  radarChart: null,
  
  // Ledger pagination state
  ledgerOffset: 0,
  ledgerLimit: 50,
  ledgerTotal: 0,

  init() {
    this.setupTabs();
    this.setupEventListeners();
    this.initCytoscape();
    this.loadHealthAndMetrics();
    this.loadTopology();
    this.loadScorecard();
    this.loadExplorer();
    this.loadGauntlet(1); // Pre-load Regime 1
    this.loadPrivateAssets();
    this.loadLedger();
  },

  // =========================================================================
  // Tab Management
  // =========================================================================
  setupTabs() {
    const tabButtons = document.querySelectorAll(".nav-tab");
    tabButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetTabId = btn.getAttribute("data-tab");
        if (targetTabId === this.activeTab) return;

        tabButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        document.querySelectorAll(".tab-panel").forEach(panel => {
          panel.classList.add("hidden");
        });
        const targetPanel = document.getElementById(targetTabId);
        if (targetPanel) {
          targetPanel.classList.remove("hidden");
        }

        this.activeTab = targetTabId;

        // Resize Cytoscape if switching to graph tab
        if (targetTabId === "tab-graph" && this.cy) {
          setTimeout(() => {
            this.cy.resize();
            this.cy.fit(undefined, 30);
          }, 50);
        }

        // Render radar chart if switching to scorecard tab
        if (targetTabId === "tab-scorecard" && !this.radarChart) {
          this.renderRadarChart();
        }
      });
    });
  },

  // =========================================================================
  // Global Event Listeners
  // =========================================================================
  setupEventListeners() {
    // Quick refresh
    document.getElementById("btn-quick-refresh")?.addEventListener("click", () => {
      this.loadHealthAndMetrics();
      this.loadTopology(true);
      this.loadLedger();
    });

    // Close Node Drawer
    document.getElementById("btn-close-drawer")?.addEventListener("click", () => this.closeDrawer());
    document.getElementById("btn-drawer-close")?.addEventListener("click", () => this.closeDrawer());
    document.getElementById("node-drawer-backdrop")?.addEventListener("click", () => this.closeDrawer());

    // Drawer focus node on canvas
    document.getElementById("btn-drawer-focus-canvas")?.addEventListener("click", () => {
      if (this.selectedNodeId && this.cy) {
        this.switchTab("tab-graph");
        this.closeDrawer();
        this.focusNodeOnCanvas(this.selectedNodeId);
      }
    });

    // Graph Controls
    document.getElementById("btn-zoom-in")?.addEventListener("click", () => {
      if (this.cy) this.cy.zoom(this.cy.zoom() * 1.25);
    });
    document.getElementById("btn-zoom-out")?.addEventListener("click", () => {
      if (this.cy) this.cy.zoom(this.cy.zoom() * 0.8);
    });
    document.getElementById("btn-fit-graph")?.addEventListener("click", () => {
      if (this.cy) this.cy.fit(undefined, 40);
    });

    // Graph Layout Switchers
    document.getElementById("layout-hierarchical")?.addEventListener("click", () => this.applyLayout("preset"));
    document.getElementById("layout-breadthfirst")?.addEventListener("click", () => this.applyLayout("breadthfirst"));
    document.getElementById("layout-concentric")?.addEventListener("click", () => this.applyLayout("concentric"));
    document.getElementById("layout-cose")?.addEventListener("click", () => this.applyLayout("cose"));

    // Graph Tier Filters
    document.querySelectorAll(".tier-filter-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".tier-filter-btn").forEach(b => {
          b.classList.remove("active-tier", "bg-cyan-950", "text-cyan-400", "border-cyan-800");
          b.classList.add("bg-slate-800", "text-slate-300", "border-slate-700");
        });
        btn.classList.add("active-tier", "bg-cyan-950", "text-cyan-400", "border-cyan-800");
        btn.classList.remove("bg-slate-800", "text-slate-300", "border-slate-700");

        const tierVal = btn.getAttribute("data-tier");
        this.filterGraphByTier(tierVal);
      });
    });

    // Graph Search Input
    document.getElementById("graph-search-input")?.addEventListener("input", (e) => {
      const q = e.target.value.trim().toLowerCase();
      this.searchNodeOnCanvas(q);
    });

    // Explorer: Path discovery
    document.getElementById("btn-run-path-discovery")?.addEventListener("click", () => this.runPathDiscovery());
    document.getElementById("btn-scroll-path-finder")?.addEventListener("click", () => {
      document.getElementById("path-finder-section")?.scrollIntoView({ behavior: "smooth" });
    });

    // Explorer: Pool browser filters
    document.getElementById("pool-filter-input")?.addEventListener("input", () => this.filterPoolsBrowser());
    document.getElementById("pool-tier-select")?.addEventListener("change", () => this.filterPoolsBrowser());

    // Gauntlet: Trigger buttons
    document.querySelectorAll(".btn-trigger-regime").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const regimeNum = parseInt(btn.getAttribute("data-regime"), 10);
        this.triggerGauntletRegime(regimeNum);
      });
    });

    // Gauntlet: Highlight bypasses on graph
    document.getElementById("btn-highlight-sim-bypasses")?.addEventListener("click", () => {
      this.highlightCurrentSimBypasses();
    });

    // Ledger: Search & Filter inputs
    document.getElementById("ledger-search-input")?.addEventListener("input", () => {
      this.ledgerOffset = 0;
      this.loadLedger();
    });
    document.getElementById("ledger-currency-filter")?.addEventListener("change", () => {
      this.ledgerOffset = 0;
      this.loadLedger();
    });
    document.getElementById("ledger-type-filter")?.addEventListener("change", () => {
      this.ledgerOffset = 0;
      this.loadLedger();
    });
    document.getElementById("btn-ledger-prev")?.addEventListener("click", () => {
      if (this.ledgerOffset > 0) {
        this.ledgerOffset = Math.max(0, this.ledgerOffset - this.ledgerLimit);
        this.loadLedger();
      }
    });
    document.getElementById("btn-ledger-next")?.addEventListener("click", () => {
      if (this.ledgerOffset + this.ledgerLimit < this.ledgerTotal) {
        this.ledgerOffset += this.ledgerLimit;
        this.loadLedger();
      }
    });
  },

  switchTab(tabId) {
    const btn = document.querySelector(`.nav-tab[data-tab="${tabId}"]`);
    if (btn) btn.click();
  },

  // =========================================================================
  // API Loaders & Metrics
  // =========================================================================
  async loadHealthAndMetrics() {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      if (data.database) {
        document.getElementById("header-flows").textContent = data.database.flow_events_count || 115;
      }
      if (data.topology) {
        document.getElementById("header-nodes").textContent = data.topology.node_count || 140;
        document.getElementById("header-edges").textContent = data.topology.edge_count || 317;
      }
    } catch (e) {
      console.warn("Could not load /api/health:", e);
    }
  },

  async loadScorecard() {
    try {
      const res = await fetch("/api/scorecard");
      const data = await res.json();
      this.scorecardData = data;

      // Update header
      document.getElementById("header-score").textContent = `${data.system_integrity_score} / 100`;
      document.getElementById("audit-overall-score").textContent = data.system_integrity_score;
      document.getElementById("audit-leak-sum").textContent = this.formatCurrency(data.total_leakage_usd || 0.0);
      document.getElementById("audit-coverage-ratio").textContent = `${(data.at_risk_coverage_ratio_pct || 100.0).toFixed(1)}%`;

      // Render anomalies
      const anomaliesContainer = document.getElementById("anomalies-list");
      if (anomaliesContainer && data.high_risk_anomalies) {
        document.getElementById("anomaly-count").textContent = data.high_risk_anomalies.length;
        anomaliesContainer.innerHTML = data.high_risk_anomalies.map(a => `
          <div class="bg-slate-900 border ${a.severity === 'CRITICAL' ? 'border-red-800/80 bg-red-950/20' : 'border-amber-800/80 bg-amber-950/20'} rounded-lg p-3.5 space-y-1.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold ${a.severity === 'CRITICAL' ? 'bg-red-900/60 text-red-300 border border-red-700' : 'bg-amber-900/60 text-amber-300 border border-amber-700'}">${a.severity}</span>
                <span class="text-xs font-mono font-bold text-slate-200">${a.dimension}</span>
              </div>
              <span class="text-[11px] font-mono text-slate-500">${a.id}</span>
            </div>
            <div class="text-xs font-mono text-cyan-300">${a.entity}</div>
            <p class="text-xs text-slate-300">${a.description}</p>
            <div class="text-[11px] text-slate-400 font-mono pt-1 border-t border-slate-800">
              <strong class="text-slate-300">Systemic Impact:</strong> ${a.impact}
            </div>
          </div>
        `).join("");
      }

      // Render remediations
      const remTbody = document.getElementById("remediation-table-body");
      if (remTbody && data.remediation_recommendations) {
        remTbody.innerHTML = data.remediation_recommendations.map(r => `
          <tr class="table-dark-row">
            <td class="py-2.5 px-4 font-bold text-cyan-400">${r.id}</td>
            <td class="py-2.5 px-4 text-purple-300">${r.area}</td>
            <td class="py-2.5 px-4 text-slate-200 font-bold">${r.action}</td>
            <td class="py-2.5 px-4 text-slate-400 font-sans text-xs">${r.details}</td>
          </tr>
        `).join("");
      }

      // Render radar chart if active
      if (this.activeTab === "tab-scorecard") {
        this.renderRadarChart();
      }
    } catch (e) {
      console.warn("Could not load /api/scorecard:", e);
    }
  },

  renderRadarChart() {
    const canvas = document.getElementById("audit-radar-chart");
    if (!canvas || !this.scorecardData) return;

    if (this.radarChart) {
      this.radarChart.destroy();
    }

    const cat = this.scorecardData.category_scores || {
      conservation: 20.0,
      dimensional: 20.0,
      temporal: 13.3,
      topology: 19.0,
      dark_matter: 18.5
    };

    this.radarChart = new Chart(canvas, {
      type: "radar",
      data: {
        labels: ["Conservation (20)", "Dimensional (20)", "Temporal (20)", "Topology (20)", "Dark Matter (20)"],
        datasets: [{
          label: "Audit Score",
          data: [cat.conservation, cat.dimensional, cat.temporal, cat.topology, cat.dark_matter],
          backgroundColor: "rgba(0, 240, 255, 0.2)",
          borderColor: "#00f0ff",
          borderWidth: 2,
          pointBackgroundColor: "#00f0ff",
          pointBorderColor: "#ffffff",
          pointRadius: 4,
        }, {
          label: "Ideal Target",
          data: [20, 20, 20, 20, 20],
          backgroundColor: "rgba(16, 185, 129, 0.05)",
          borderColor: "rgba(16, 185, 129, 0.4)",
          borderWidth: 1,
          borderDash: [4, 4],
          pointRadius: 0,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            min: 0,
            max: 20,
            ticks: { stepSize: 5, color: "#64748b", backdropColor: "transparent", font: { family: "JetBrains Mono", size: 9 } },
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            angleLines: { color: "rgba(255, 255, 255, 0.08)" },
            pointLabels: { color: "#94a3b8", font: { family: "JetBrains Mono", size: 10 } }
          }
        },
        plugins: {
          legend: {
            display: true,
            labels: { color: "#94a3b8", font: { family: "JetBrains Mono", size: 10 } }
          }
        }
      }
    });
  },

  // =========================================================================
  // Cytoscape.js Graph Engine
  // =========================================================================
  initCytoscape() {
    const container = document.getElementById("cy-container");
    if (!container) return;

    this.cy = cytoscape({
      container: container,
      boxSelectionEnabled: false,
      autounselectify: false,
      style: [
        // Default Node Style
        {
          selector: "node",
          style: {
            "label": "data(label)",
            "color": "#cbd5e1",
            "font-size": "10px",
            "font-family": "JetBrains Mono, monospace",
            "text-valign": "bottom",
            "text-margin-y": "6px",
            "text-max-width": "120px",
            "text-wrap": "ellipsis",
            "background-color": "#475569",
            "border-width": 2,
            "border-color": "#1e293b",
            "width": 28,
            "height": 28,
            "transition-property": "background-color, border-color, width, height, opacity",
            "transition-duration": "0.2s"
          }
        },
        // Tier 0 Genesis Nodes
        {
          selector: "node[tier = 0]",
          style: {
            "background-color": "#0284c7",
            "border-color": "#38bdf8",
            "width": 36,
            "height": 36,
            "color": "#38bdf8",
            "font-weight": "bold"
          }
        },
        // Tier 1 Transmission Nodes
        {
          selector: "node[tier = 1]",
          style: {
            "background-color": "#7c3aed",
            "border-color": "#c084fc",
            "width": 32,
            "height": 32,
            "color": "#e9d5ff"
          }
        },
        // Tier 2 Traversal Nodes
        {
          selector: "node[tier = 2]",
          style: {
            "background-color": "#d97706",
            "border-color": "#fbbf24",
            "width": 26,
            "height": 26,
            "color": "#fef3c7"
          }
        },
        // Tier 3 Sink Nodes
        {
          selector: "node[tier = 3]",
          style: {
            "background-color": "#059669",
            "border-color": "#34d399",
            "width": 34,
            "height": 34,
            "color": "#34d399",
            "font-weight": "bold"
          }
        },
        // Decoy / Distractor Nodes
        {
          selector: "node[is_decoy = true]",
          style: {
            "background-color": "#991b1b",
            "border-color": "#f87171",
            "border-style": "dashed",
            "color": "#fca5a5"
          }
        },
        // Selected / Focused Node
        {
          selector: "node:selected, node.highlighted",
          style: {
            "border-color": "#00f0ff",
            "border-width": 4,
            "width": 42,
            "height": 42,
            "font-size": "12px",
            "font-weight": "bold",
            "color": "#00f0ff",
            "z-index": 999
          }
        },
        // Default Edge Style
        {
          selector: "edge",
          style: {
            "width": 1.5,
            "line-color": "#1e293b",
            "target-arrow-color": "#334155",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "opacity": 0.55,
            "arrow-scale": 0.8,
            "transition-property": "line-color, width, opacity",
            "transition-duration": "0.2s"
          }
        },
        // Bypass Edges
        {
          selector: "edge[is_bypass = true]",
          style: {
            "line-color": "#059669",
            "target-arrow-color": "#10b981",
            "width": 2.5,
            "opacity": 0.85,
            "line-style": "dashed"
          }
        },
        // Active Corridor / Highlighted Edge
        {
          selector: "edge.highlighted",
          style: {
            "line-color": "#00f0ff",
            "target-arrow-color": "#00f0ff",
            "width": 3.5,
            "opacity": 1.0,
            "z-index": 999
          }
        },
        // Dimmed Non-Corridor Elements
        {
          selector: ".dimmed",
          style: {
            "opacity": 0.12
          }
        }
      ],
      layout: { name: "preset" }
    });

    // Node Click -> Open Drawer
    this.cy.on("tap", "node", (evt) => {
      const node = evt.target;
      const nodeId = node.id();
      this.inspectPool(nodeId);
    });

    // Canvas Background Click -> Reset highlights
    this.cy.on("tap", (evt) => {
      if (evt.target === this.cy) {
        this.resetGraphHighlights();
      }
    });
  },

  async loadTopology(forceReload = false) {
    try {
      const res = await fetch("/api/topology");
      const data = await res.json();
      this.topologyData = data;

      if (this.cy) {
        this.cy.elements().remove();
        this.cy.add(data.elements.nodes);
        this.cy.add(data.elements.edges);
        this.applyLayout("preset");
      }
    } catch (e) {
      console.warn("Could not load /api/topology:", e);
    }
  },

  applyLayout(layoutName) {
    if (!this.cy) return;

    let layoutOptions = { name: layoutName };
    if (layoutName === "preset") {
      layoutOptions = {
        name: "preset",
        fit: true,
        padding: 40,
        animate: true,
        animationDuration: 400
      };
    } else if (layoutName === "breadthfirst") {
      layoutOptions = {
        name: "breadthfirst",
        directed: true,
        spacingFactor: 1.25,
        animate: true,
        fit: true,
        padding: 40
      };
    } else if (layoutName === "concentric") {
      layoutOptions = {
        name: "concentric",
        concentric: (node) => 4 - node.data("tier"),
        levelWidth: () => 1,
        animate: true,
        fit: true,
        padding: 40
      };
    } else if (layoutName === "cose") {
      layoutOptions = {
        name: "cose",
        animate: false,
        fit: true,
        padding: 40,
        nodeOverlap: 20,
        componentSpacing: 100
      };
    }

    const layout = this.cy.layout(layoutOptions);
    layout.run();
  },

  filterGraphByTier(tierVal) {
    if (!this.cy) return;

    this.cy.batch(() => {
      if (tierVal === "all") {
        this.cy.nodes().show();
        this.cy.edges().show();
      } else {
        const t = parseInt(tierVal, 10);
        this.cy.nodes().forEach(node => {
          if (node.data("tier") === t) {
            node.show();
          } else {
            node.hide();
          }
        });
        this.cy.edges().forEach(edge => {
          if (edge.source().visible() && edge.target().visible()) {
            edge.show();
          } else {
            edge.hide();
          }
        });
      }
    });

    this.cy.fit(undefined, 30);
  },

  searchNodeOnCanvas(query) {
    if (!this.cy) return;
    if (!query) {
      this.resetGraphHighlights();
      return;
    }

    const matched = this.cy.nodes().filter(node => {
      const id = node.id().toLowerCase();
      const label = (node.data("label") || "").toLowerCase();
      return id.includes(query) || label.includes(query);
    });

    if (matched.length > 0) {
      this.cy.elements().addClass("dimmed");
      matched.removeClass("dimmed").addClass("highlighted");
      this.cy.animate({
        center: { eles: matched },
        zoom: 1.2,
        duration: 300
      });
    } else {
      this.resetGraphHighlights();
    }
  },

  focusNodeOnCanvas(nodeId) {
    if (!this.cy) return;
    const node = this.cy.getElementById(nodeId);
    if (node && node.length > 0) {
      this.resetGraphHighlights();
      this.cy.elements().addClass("dimmed");
      node.removeClass("dimmed").addClass("highlighted");
      node.neighborhood().removeClass("dimmed");
      node.connectedEdges().addClass("highlighted");

      this.cy.animate({
        center: { eles: node },
        zoom: 1.4,
        duration: 400
      });
    }
  },

  highlightCorridor(nodeIds) {
    if (!this.cy || !nodeIds || nodeIds.length === 0) return;

    this.cy.batch(() => {
      this.cy.elements().addClass("dimmed").removeClass("highlighted");
      const nodes = this.cy.nodes().filter(n => nodeIds.includes(n.id()));
      nodes.removeClass("dimmed").addClass("highlighted");

      // Highlight connecting edges
      for (let i = 0; i < nodeIds.length - 1; i++) {
        const u = nodeIds[i];
        const v = nodeIds[i + 1];
        const edge = this.cy.edges().filter(e => (e.source().id() === u && e.target().id() === v));
        edge.removeClass("dimmed").addClass("highlighted");
      }
    });

    const highlightEles = this.cy.elements(".highlighted");
    if (highlightEles.length > 0) {
      this.cy.animate({
        fit: { eles: highlightEles, padding: 60 },
        duration: 500
      });
    }
  },

  resetGraphHighlights() {
    if (!this.cy) return;
    this.cy.elements().removeClass("dimmed highlighted");
  },

  // =========================================================================
  // Tab 2: Flow & Pool Explorer
  // =========================================================================
  async loadExplorer() {
    // 1. Load featured circuits
    try {
      const res = await fetch("/api/circuits/featured");
      const circuits = await res.json();
      this.featuredCircuits = circuits;
      this.renderFeaturedCircuits(circuits);
    } catch (e) {
      console.warn("Could not load /api/circuits/featured:", e);
    }

    // 2. Load pools registry
    try {
      const res = await fetch("/api/pools");
      const pools = await res.json();
      this.poolsData = pools;
      document.getElementById("pool-count-label").textContent = pools.length;
      this.renderPoolsBrowser(pools);
      this.populatePathDropdowns(pools);
    } catch (e) {
      console.warn("Could not load /api/pools:", e);
    }
  },

  renderFeaturedCircuits(circuits) {
    const grid = document.getElementById("featured-circuits-grid");
    if (!grid) return;

    grid.innerHTML = circuits.map(c => `
      <div class="bg-manifold-card border border-manifold-border hover:border-cyan-500/50 rounded-lg p-4 transition flex flex-col justify-between space-y-3">
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyan-300 border border-slate-700 font-semibold">${c.id}</span>
            ${c.regime_link ? `<span class="text-[9px] font-mono px-1.5 rounded bg-purple-950 text-purple-300 border border-purple-800">Regime ${c.regime_link}</span>` : ''}
          </div>
          <h4 class="text-sm font-bold text-white leading-snug">${c.title}</h4>
          <p class="text-[11px] text-slate-400 leading-relaxed">${c.subtitle}</p>
        </div>

        <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-2">
          <button class="btn-trace-circuit flex-1 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 font-mono text-xs border border-slate-700 flex items-center justify-center gap-1.5 transition" data-circuit-id="${c.id}">
            <i class="fa-solid fa-play text-[10px]"></i> Animate Path
          </button>
          <button class="btn-inspect-circuit px-2.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs border border-slate-700 transition" data-source-id="${c.source_id}" title="Inspect Origin">
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
        </div>
      </div>
    `).join("");

    // Bind circuit click handlers
    grid.querySelectorAll(".btn-trace-circuit").forEach(btn => {
      btn.addEventListener("click", () => {
        const cid = btn.getAttribute("data-circuit-id");
        const circuit = this.featuredCircuits.find(c => c.id === cid);
        if (circuit) {
          this.switchTab("tab-graph");
          this.highlightCorridor(circuit.key_nodes);
        }
      });
    });

    grid.querySelectorAll(".btn-inspect-circuit").forEach(btn => {
      btn.addEventListener("click", () => {
        const sid = btn.getAttribute("data-source-id");
        this.inspectPool(sid);
      });
    });
  },

  populatePathDropdowns(pools) {
    const srcSelect = document.getElementById("path-source-select");
    const tgtSelect = document.getElementById("path-target-select");
    if (!srcSelect || !tgtSelect) return;

    const optionsHtml = pools.map(p => `
      <option value="${p.id}">${p.name} (${p.tier_label})</option>
    `).join("");

    srcSelect.innerHTML = `<option value="">Select Origin Pool...</option>` + optionsHtml;
    tgtSelect.innerHTML = `<option value="">Select Destination Pool...</option>` + optionsHtml;

    // Presets default
    srcSelect.value = "french_republic_tresor";
    tgtSelect.value = "bund_risk_free_anchor";
  },

  async runPathDiscovery() {
    const src = document.getElementById("path-source-select").value;
    const tgt = document.getElementById("path-target-select").value;
    const resultsContainer = document.getElementById("path-discovery-results");

    if (!src || !tgt) {
      alert("Please select both an Origin and a Destination pool.");
      return;
    }

    try {
      resultsContainer.classList.remove("hidden");
      resultsContainer.innerHTML = `<div class="p-3 text-xs font-mono text-cyan-400 animate-pulse">Executing Dual-Frontier A* Search...</div>`;

      const res = await fetch(`/api/paths?source_id=${src}&target_id=${tgt}`);
      const data = await res.json();

      if (!data.success) {
        resultsContainer.innerHTML = `
          <div class="bg-red-950/40 border border-red-800 rounded p-3 text-xs font-mono text-red-300">
            <strong>No Viable Clearing Corridor Discovered:</strong> Path between '${src}' and '${tgt}' is severed or blocked.
          </div>
        `;
        return;
      }

      resultsContainer.innerHTML = `
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-mono text-xs font-bold border border-emerald-800">CORRIDOR DISCOVERED</span>
              <span class="text-xs font-mono text-slate-400">${data.hops} Hops</span>
            </div>
            <div class="text-xs font-mono">
              <span class="text-slate-400">Total Impedance Cost:</span>
              <span class="text-cyan-400 font-bold ml-1">${data.total_cost}</span>
            </div>
          </div>

          <!-- Corridor Hop Steps -->
          <div class="space-y-1.5">
            ${data.hop_details.map((hop, i) => `
              <div class="flex items-center gap-3 p-2 rounded bg-slate-950/80 border border-slate-800/80 text-xs font-mono">
                <span class="w-5 h-5 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 font-bold text-[10px]">${i + 1}</span>
                <span class="tier-badge-${hop.tier} px-1.5 py-0.5 rounded text-[10px] font-bold">T${hop.tier}</span>
                <span class="text-slate-200 font-bold flex-1">${hop.name}</span>
                <span class="text-slate-400 text-[11px]">${hop.sector}</span>
                <span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">${hop.jurisdiction}</span>
                <button class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 text-[10px] btn-hop-inspect" data-hop-id="${hop.id}">Inspect</button>
              </div>
            `).join("")}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button id="btn-highlight-discovered-path" class="px-3 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-black font-semibold text-xs font-mono flex items-center gap-2">
              <i class="fa-solid fa-eye"></i> View & Animate on Graph
            </button>
          </div>
        </div>
      `;

      resultsContainer.querySelector("#btn-highlight-discovered-path")?.addEventListener("click", () => {
        this.switchTab("tab-graph");
        this.highlightCorridor(data.path_nodes);
      });

      resultsContainer.querySelectorAll(".btn-hop-inspect").forEach(b => {
        b.addEventListener("click", () => {
          this.inspectPool(b.getAttribute("data-hop-id"));
        });
      });

    } catch (e) {
      resultsContainer.innerHTML = `<div class="p-3 text-xs font-mono text-red-400">Error querying path: ${e}</div>`;
    }
  },

  renderPoolsBrowser(pools) {
    const container = document.getElementById("pools-cards-container");
    if (!container) return;

    container.innerHTML = pools.map(p => `
      <div class="bg-manifold-card border border-manifold-border hover:border-slate-700 rounded-lg p-4 transition flex flex-col justify-between space-y-3">
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="tier-badge-${p.tier} px-2 py-0.5 rounded text-[10px] font-mono font-bold">T${p.tier} ${p.tier_label.split(':')[0]}</span>
            <span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">${p.jurisdiction}</span>
          </div>
          <h4 class="text-sm font-bold text-white truncate" title="${p.name}">${p.name}</h4>
          <div class="text-[11px] font-mono text-slate-500 truncate">${p.id}</div>
          <div class="text-[11px] font-mono text-purple-300 truncate">${p.sector}</div>
        </div>

        <div class="pt-2.5 border-t border-slate-800 text-xs font-mono space-y-1">
          <div class="flex items-center justify-between">
            <span class="text-slate-500">Inflow:</span>
            <span class="text-emerald-400 font-bold">${this.formatCurrency(p.inflow_usd)}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-slate-500">Outflow:</span>
            <span class="text-amber-400 font-bold">${this.formatCurrency(p.outflow_usd)}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-slate-500">Net:</span>
            <span class="${p.net_flow_usd >= 0 ? 'text-cyan-400' : 'text-red-400'} font-bold">${this.formatCurrency(p.net_flow_usd)}</span>
          </div>
        </div>

        <div class="pt-1 flex items-center justify-between gap-2">
          <button class="w-full py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono border border-slate-700 transition flex items-center justify-center gap-1.5 btn-inspect-pool-card" data-pool-id="${p.id}">
            <i class="fa-solid fa-magnifying-glass text-[10px]"></i> Inspect Pool
          </button>
        </div>
      </div>
    `).join("");

    container.querySelectorAll(".btn-inspect-pool-card").forEach(btn => {
      btn.addEventListener("click", () => {
        this.inspectPool(btn.getAttribute("data-pool-id"));
      });
    });
  },

  filterPoolsBrowser() {
    const q = document.getElementById("pool-filter-input")?.value.trim().toLowerCase() || "";
    const tierVal = document.getElementById("pool-tier-select")?.value;

    const filtered = this.poolsData.filter(p => {
      const matchQ = !q || p.id.toLowerCase().includes(q) || p.name.toLowerCase().includes(q);
      const matchTier = tierVal === "" || p.tier === parseInt(tierVal, 10);
      return matchQ && matchTier;
    });

    document.getElementById("pool-count-label").textContent = filtered.length;
    this.renderPoolsBrowser(filtered);
  },

  // =========================================================================
  // Node Inspection Slide-Over Drawer
  // =========================================================================
  async inspectPool(poolId) {
    this.selectedNodeId = poolId;
    const drawer = document.getElementById("node-drawer");
    const backdrop = document.getElementById("node-drawer-backdrop");

    drawer.classList.remove("translate-x-full");
    backdrop.classList.remove("hidden");

    try {
      const res = await fetch(`/api/pools/${poolId}`);
      const data = await res.json();
      const p = data.pool;

      document.getElementById("drawer-node-name").textContent = p.name;
      document.getElementById("drawer-node-id").textContent = p.id;
      document.getElementById("drawer-sector").textContent = p.sector;
      document.getElementById("drawer-description").textContent = p.description || "Capital flow counterparty pool.";
      document.getElementById("drawer-jurisdiction-badge").textContent = p.jurisdiction;

      const tierBadge = document.getElementById("drawer-tier-badge");
      tierBadge.className = `tier-badge-${p.tier} px-2 py-0.5 rounded text-[10px] font-mono font-bold`;
      tierBadge.textContent = p.tier_label || `TIER ${p.tier}`;

      const decoyBadge = document.getElementById("drawer-decoy-badge");
      if (p.is_decoy) {
        decoyBadge.classList.remove("hidden");
      } else {
        decoyBadge.classList.add("hidden");
      }

      document.getElementById("drawer-conservation-status").textContent = data.conservation_status.replace(/_/g, " ").toUpperCase();
      document.getElementById("drawer-inflow-val").textContent = this.formatCurrency(data.totals.inflow_usd);
      document.getElementById("drawer-outflow-val").textContent = this.formatCurrency(data.totals.outflow_usd);
      document.getElementById("drawer-net-val").textContent = this.formatCurrency(data.totals.net_usd);

      // Metrics
      const metricsContainer = document.getElementById("drawer-metrics-container");
      if (p.metrics && Object.keys(p.metrics).length > 0) {
        metricsContainer.innerHTML = Object.entries(p.metrics).map(([k, v]) => `
          <div class="flex items-center justify-between text-[11px] font-mono py-1 px-2 rounded bg-slate-900/60 border border-slate-800">
            <span class="text-slate-400">${k.replace(/_/g, " ")}:</span>
            <span class="text-cyan-300 font-bold">${typeof v === 'number' ? v.toFixed(3) : v}</span>
          </div>
        `).join("");
      } else {
        metricsContainer.innerHTML = `<div class="text-[11px] text-slate-500 font-mono">Standard institutional cashflow node.</div>`;
      }

      // Upstream list
      const upList = document.getElementById("drawer-upstream-list");
      if (data.upstream_neighbors && data.upstream_neighbors.length > 0) {
        upList.innerHTML = data.upstream_neighbors.map(u => `
          <div class="truncate cursor-pointer hover:text-cyan-400" onclick="App.inspectPool('${u.source}')">
            &bull; ${u.source} <span class="text-slate-500 text-[10px]">(${u.relation})</span>
          </div>
        `).join("");
      } else {
        upList.innerHTML = `<div class="text-slate-500">None (Genesis Origin)</div>`;
      }

      // Downstream list
      const downList = document.getElementById("drawer-downstream-list");
      if (data.downstream_neighbors && data.downstream_neighbors.length > 0) {
        downList.innerHTML = data.downstream_neighbors.map(d => `
          <div class="truncate cursor-pointer hover:text-cyan-400" onclick="App.inspectPool('${d.target}')">
            &bull; ${d.target} <span class="text-slate-500 text-[10px]">(${d.relation})</span>
          </div>
        `).join("");
      } else {
        downList.innerHTML = `<div class="text-slate-500">None (Terminal Sink)</div>`;
      }

      // Associated flows
      const flowsList = document.getElementById("drawer-flows-list");
      const combinedFlows = [...data.inbound_flows, ...data.outbound_flows];
      if (combinedFlows.length > 0) {
        flowsList.innerHTML = combinedFlows.slice(0, 8).map(f => `
          <div class="bg-slate-900 border border-slate-800 rounded p-2 text-[11px] font-mono space-y-1">
            <div class="flex items-center justify-between">
              <span class="text-cyan-400 font-bold">${f.instrument}</span>
              <span class="text-emerald-400">${this.formatCurrency(f.amount_usd_normalized)}</span>
            </div>
            <div class="text-slate-400 text-[10px] flex items-center justify-between">
              <span>${f.source_entity} &rarr; ${f.target_entity}</span>
              <span class="badge-provenance badge-${(f.data_source || 'dtcc').toLowerCase().slice(0, 3)}">${f.data_source || 'LEDGER'}</span>
            </div>
          </div>
        `).join("");
      } else {
        flowsList.innerHTML = `<div class="text-slate-500 text-[11px] font-mono">No direct flow events recorded in DuckDB.</div>`;
      }

    } catch (e) {
      console.warn("Could not load pool details:", e);
    }
  },

  closeDrawer() {
    document.getElementById("node-drawer")?.classList.add("translate-x-full");
    document.getElementById("node-drawer-backdrop")?.classList.add("hidden");
  },

  // =========================================================================
  // Tab 4: Systemic Shock Gauntlet Control Room
  // =========================================================================
  async loadGauntlet(regimeNum) {
    await this.triggerGauntletRegime(regimeNum);
  },

  async triggerGauntletRegime(regimeNum) {
    const titleElem = document.getElementById("sim-active-regime-title");
    const descElem = document.getElementById("sim-active-regime-desc");
    const pillElem = document.getElementById("sim-active-regime-pill");

    titleElem.textContent = `Running Regime ${regimeNum} Simulation...`;

    try {
      const res = await fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ regime: regimeNum })
      });
      const data = await res.json();
      this.currentSimResult = data;

      pillElem.textContent = data.regime_id;
      titleElem.textContent = data.regime_name;
      descElem.textContent = data.description;
      document.getElementById("sim-bypass-pct").textContent = `${data.bypass_corridor_activation_pct.toFixed(1)}%`;
      document.getElementById("sim-cost-delta").textContent = `+${data.avg_pct_cost_delta.toFixed(2)}%`;
      document.getElementById("sim-latency").textContent = `${data.execution_time_ms.toFixed(2)} ms`;

      // Render routes
      const routesContainer = document.getElementById("sim-routes-container");
      routesContainer.innerHTML = Object.entries(data.routes).map(([k, r]) => `
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-3.5 space-y-2">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div class="text-xs font-mono font-bold text-white flex items-center gap-2">
              <span>${r.source_id}</span>
              <span class="text-slate-500">&rarr;</span>
              <span>${r.target_id}</span>
            </div>
            <div class="flex items-center gap-2 text-xs font-mono">
              ${r.is_severed_expected 
                ? '<span class="px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 font-bold">[SEVERED: 0 HALLUCINATIONS]</span>' 
                : `<span class="text-amber-400 font-bold">Delta C: +${r.pct_cost_delta}%</span>
                   <span class="text-slate-500">|</span>
                   <span class="text-slate-400">Shock Cost: ${r.shocked_cost}</span>`}
            </div>
          </div>

          <div class="text-[11px] font-mono space-y-1">
            <div class="text-slate-400 flex items-center gap-2">
              <span class="w-16 text-slate-500">Baseline:</span>
              <span class="text-slate-300">${r.baseline_path.join(" &rarr; ")}</span>
            </div>
            <div class="text-slate-400 flex items-center gap-2">
              <span class="w-16 text-slate-500">Shocked:</span>
              <span class="${r.is_severed_expected ? 'text-red-400' : 'text-emerald-300 font-bold'}">${r.shocked_path.length > 0 ? r.shocked_path.join(" &rarr; ") : "Interdicted Corridor (0 Edges)"}</span>
            </div>
          </div>

          ${r.bypasses_used && r.bypasses_used.length > 0 ? `
            <div class="pt-1.5 border-t border-slate-800 flex items-center gap-2 text-[10px] font-mono">
              <span class="text-slate-500">Active Bypass:</span>
              ${r.bypasses_used.map(b => `<span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-bold">${b}</span>`).join("")}
            </div>
          ` : ''}
        </div>
      `).join("");

      // Render bottlenecks
      const bottlenecksContainer = document.getElementById("sim-bottlenecks-list");
      bottlenecksContainer.innerHTML = (data.bottleneck_nodes || []).map(b => `
        <div class="flex items-center justify-between text-xs font-mono p-2 rounded bg-slate-950 border border-slate-800">
          <span class="text-amber-300 font-bold">${b}</span>
          <span class="text-slate-400">Congestion: ${(data.node_congestion_scores[b] || 0.5) * 100}%</span>
        </div>
      `).join("");

      // Render active bypasses
      const bypassesContainer = document.getElementById("sim-bypasses-list");
      bypassesContainer.innerHTML = (data.active_bypasses || []).map(b => `
        <div class="flex items-center justify-between text-xs font-mono p-2 rounded bg-slate-950 border border-slate-800">
          <span class="text-emerald-300 font-bold">${b}</span>
          <span class="text-emerald-400 font-bold">[ACTIVATED 100%]</span>
        </div>
      `).join("");

    } catch (e) {
      console.warn("Could not execute gauntlet regime:", e);
    }
  },

  highlightCurrentSimBypasses() {
    if (!this.currentSimResult) return;
    const bypassNodes = this.currentSimResult.active_bypasses || [];
    this.switchTab("tab-graph");
    this.highlightCorridor(bypassNodes);
  },

  // =========================================================================
  // Tab 5: Private Asset Downstream Waterfall
  // =========================================================================
  async loadPrivateAssets() {
    try {
      const res = await fetch("/api/private_assets");
      const data = await res.json();

      document.getElementById("priv-total-commitments").textContent = this.formatCurrency(data.aggregates.total_private_commitments_usd);

      // Render entities grid
      const grid = document.getElementById("private-entities-grid");
      if (grid && data.portfolio_entities) {
        grid.innerHTML = data.portfolio_entities.map(e => `
          <div class="bg-manifold-card border border-manifold-border rounded-lg p-5 space-y-3.5 flex flex-col justify-between">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 font-semibold">${e.domain}</span>
                <span class="text-sm font-bold font-mono text-cyan-400">${this.formatCurrency(e.allocation_usd)}</span>
              </div>
              <h4 class="text-base font-bold text-white">${e.name}</h4>
              <p class="text-xs text-slate-300">${e.role}</p>
            </div>

            <!-- Inbound & Outbound -->
            <div class="space-y-2 pt-2 border-t border-slate-800 text-xs font-mono">
              <div class="text-[10px] text-slate-400 uppercase font-bold">Inbound Macro Transmission:</div>
              ${e.inbound_flows.map(inf => `
                <div class="bg-slate-900 border border-slate-800/80 p-2 rounded flex items-center justify-between">
                  <span class="text-slate-300 text-[11px] truncate">${inf.instrument}</span>
                  <span class="text-emerald-400 font-bold ml-2">${this.formatCurrency(inf.amount_usd)}</span>
                </div>
              `).join("")}

              <div class="text-[10px] text-slate-400 uppercase font-bold pt-1">Downstream Allocations:</div>
              ${e.outbound_allocations.map(outf => `
                <div class="bg-slate-900 border border-slate-800/80 p-2 rounded flex items-center justify-between">
                  <span class="text-slate-300 text-[11px] truncate">${outf.purpose}</span>
                  <span class="text-amber-400 font-bold ml-2">${this.formatCurrency(outf.amount_usd)}</span>
                </div>
              `).join("")}
            </div>

            <div class="pt-2">
              <button class="w-full py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono border border-slate-700 transition btn-inspect-priv" data-pool-id="${e.id}">
                Inspect Ledger & Balance Sheet
              </button>
            </div>
          </div>
        `).join("");

        grid.querySelectorAll(".btn-inspect-priv").forEach(btn => {
          btn.addEventListener("click", () => {
            this.inspectPool(btn.getAttribute("data-pool-id"));
          });
        });
      }

      // Render Macro Links Table
      const linksTbody = document.getElementById("macro-links-table-body");
      if (linksTbody && data.macro_liquidity_links) {
        linksTbody.innerHTML = data.macro_liquidity_links.map(l => `
          <tr class="table-dark-row">
            <td class="py-2.5 px-4 font-bold text-cyan-400">${l.conduit}</td>
            <td class="py-2.5 px-4 text-purple-300">${l.instrument}</td>
            <td class="py-2.5 px-4 text-emerald-400 font-bold">${this.formatCurrency(l.volume_usd)}</td>
            <td class="py-2.5 px-4 text-slate-400">${l.direction}</td>
          </tr>
        `).join("");
      }

    } catch (e) {
      console.warn("Could not load /api/private_assets:", e);
    }
  },

  // =========================================================================
  // Tab 6: DuckDB Flow Ledger
  // =========================================================================
  async loadLedger() {
    const q = document.getElementById("ledger-search-input")?.value.trim() || "";
    const curr = document.getElementById("ledger-currency-filter")?.value || "";
    const type = document.getElementById("ledger-type-filter")?.value || "";

    const params = new URLSearchParams({
      limit: this.ledgerLimit,
      offset: this.ledgerOffset,
    });
    if (q) params.set("search", q);
    if (curr) params.set("currency", curr);
    if (type) params.set("flow_type", type);

    try {
      const res = await fetch(`/api/flows?${params.toString()}`);
      const data = await res.json();

      this.ledgerTotal = data.total;
      document.getElementById("ledger-showing-count").textContent = `${this.ledgerOffset + 1} - ${Math.min(this.ledgerTotal, this.ledgerOffset + data.flows.length)}`;
      document.getElementById("ledger-total-count").textContent = this.ledgerTotal;

      document.getElementById("btn-ledger-prev").disabled = this.ledgerOffset === 0;
      document.getElementById("btn-ledger-next").disabled = this.ledgerOffset + this.ledgerLimit >= this.ledgerTotal;

      const tbody = document.getElementById("ledger-table-body");
      if (tbody) {
        tbody.innerHTML = data.flows.map(f => `
          <tr class="table-dark-row">
            <td class="py-2.5 px-4">
              <div class="font-bold text-slate-200 truncate max-w-[140px]" title="${f.event_id}">${f.event_id}</div>
              <div class="text-[10px] text-slate-500">${f.period_label || f.timestamp.split('T')[0]}</div>
            </td>
            <td class="py-2.5 px-4">
              <div class="text-cyan-400 font-bold truncate max-w-[150px]" title="${f.source_entity}">${f.source_entity}</div>
              <span class="text-[10px] text-slate-500">${f.source_jurisdiction}</span>
            </td>
            <td class="py-2.5 px-4">
              <div class="text-purple-400 font-bold truncate max-w-[150px]" title="${f.target_entity}">${f.target_entity}</div>
              <span class="text-[10px] text-slate-500">${f.target_jurisdiction}</span>
            </td>
            <td class="py-2.5 px-4 text-slate-300 truncate max-w-[180px]" title="${f.instrument}">${f.instrument}</td>
            <td class="py-2.5 px-4 text-right font-bold text-slate-200">
              ${f.nominal_amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${f.currency}
            </td>
            <td class="py-2.5 px-4 text-right font-bold text-emerald-400">
              ${this.formatCurrency(f.amount_usd_normalized)}
            </td>
            <td class="py-2.5 px-4 text-right font-bold text-amber-400">
              ${this.formatCurrency(f.annualized_rate_usd)} / yr
            </td>
            <td class="py-2.5 px-4 text-center">
              <span class="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700">${f.flow_type}</span>
            </td>
            <td class="py-2.5 px-4 text-center">
              <span class="badge-provenance badge-${f.provenance_badge.toLowerCase()}">${f.provenance_badge}</span>
            </td>
          </tr>
        `).join("");
      }

    } catch (e) {
      console.warn("Could not load /api/flows:", e);
    }
  },

  // =========================================================================
  // Currency Formatter
  // =========================================================================
  formatCurrency(val) {
    if (val === null || val === undefined || isNaN(val)) return "$0.00";
    const abs = Math.abs(val);
    const sign = val < 0 ? "-" : "";
    if (abs >= 1e12) return `${sign}$${(abs / 1e12).toFixed(2)}T`;
    if (abs >= 1e9) return `${sign}$${(abs / 1e9).toFixed(2)}B`;
    if (abs >= 1e6) return `${sign}$${(abs / 1e6).toFixed(2)}M`;
    return `${sign}$${abs.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }
};
