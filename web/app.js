document.addEventListener('DOMContentLoaded', () => {
  const runBtn = document.getElementById('run-btn');
  const resetBtn = document.getElementById('reset-btn');
  const terminalConsole = document.getElementById('terminal-console');

  // Load Initial Data
  fetchInventoryData();
  fetchAuditTrail();

  runBtn.addEventListener('click', async () => {
    runBtn.disabled = true;
    runBtn.innerHTML = '<span class="btn-icon">⏳</span> Executing CoCo Skills...';
    
    appendLog('comment', `# Triggering CoCo Agent Multi-Step Workflow [${new Date().toLocaleTimeString()}]`);
    
    // Animate DAG Step 1
    activateDagStep(1);
    appendLog('info', '[SKILL: data-anomaly-detector] Scanning Snowflake warehouse tables...');
    await sleep(600);

    // Animate DAG Step 2
    activateDagStep(2);
    appendLog('info', '[SKILL: cortex-reasoner] Performing Cortex AI multi-modal reasoning & log synthesis...');
    await sleep(800);

    // Animate DAG Step 3
    activateDagStep(3);
    appendLog('warning', '[BRANCH: policy-guardrails] Validating expenditure against $50,000 budget policy threshold...');
    await sleep(500);

    // Animate DAG Step 4
    activateDagStep(4);
    appendLog('success', '[SKILL: action-executor] Issued Emergency PO-F4D23D & updated database audit trail.');
    await sleep(600);

    try {
      const response = await fetch('/api/run-agent', { method: 'POST' });
      const data = await response.json();
      
      appendLog('success', `✔ Workflow Completed! Target: ${data.target_item} | Risk: ${data.risk_score}/100`);
      appendLog('comment', `Root Cause: ${data.root_cause}`);
      appendLog('info', `Action: ${data.action_executed.details.action_type} | PO: ${data.action_executed.details.po_number} ($${data.action_executed.details.cost_usd.toLocaleString()})`);

      // Refresh Tables & Stats
      fetchInventoryData();
      fetchAuditTrail();

      document.getElementById('metric-financial').textContent = `$${Math.round(data.action_executed.details.cost_usd * 8.3).toLocaleString()}`;
      document.getElementById('metric-risk').innerHTML = `${data.risk_score}<span class="unit">/100</span>`;

    } catch (err) {
      appendLog('error', `Execution error: ${err.message}`);
    } finally {
      runBtn.disabled = false;
      runBtn.innerHTML = '<span class="btn-icon">⚡</span> Run Autonomous Agent';
      clearDagHighlight();
    }
  });

  resetBtn.addEventListener('click', async () => {
    appendLog('comment', '# Resetting Snowflake enterprise tables & re-seeding mock data...');
    try {
      await fetch('/api/reset-data', { method: 'POST' });
      appendLog('success', '[OK] Database tables reset successfully.');
      fetchInventoryData();
      fetchAuditTrail();
    } catch (err) {
      appendLog('error', `Reset error: ${err.message}`);
    }
  });

  async function fetchInventoryData() {
    try {
      const res = await fetch('/api/inventory');
      const data = await res.json();
      const tbody = document.querySelector('#inventory-table tbody');
      tbody.innerHTML = '';

      data.forEach(item => {
        const days = (item.current_stock / Math.max(item.daily_burn_rate, 1)).toFixed(1);
        let badgeClass = 'stable';
        if (item.expected_arrival_delay_days > 5) badgeClass = 'critical';
        else if (item.expected_arrival_delay_days > 0) badgeClass = 'warning';

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-family: var(--font-mono); color: var(--cyan);">${item.item_id}</td>
          <td><strong>${item.item_name}</strong></td>
          <td>${item.current_stock} (${days}d left)</td>
          <td>${item.supplier_lead_time_days} days</td>
          <td style="color: ${item.expected_arrival_delay_days > 0 ? 'var(--red)' : 'var(--green)'};">+${item.expected_arrival_delay_days} days</td>
          <td><span class="badge ${badgeClass}">${item.status || 'ACTIVE'}</span></td>
        `;
        tbody.appendChild(tr);
      });
    } catch (err) {
      console.error(err);
    }
  }

  async function fetchAuditTrail() {
    try {
      const res = await fetch('/api/audit');
      const data = await res.json();
      const tbody = document.querySelector('#audit-table tbody');
      tbody.innerHTML = '';

      data.forEach(log => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-family: var(--font-mono); color: var(--green);">${log.action_id}</td>
          <td style="font-family: var(--font-mono);">${log.po_number || 'N/A'}</td>
          <td>${log.action_type}</td>
          <td>$${log.cost_usd.toLocaleString()}</td>
          <td><span class="badge ${log.policy_authorization === 'APPROVED_AUTO' ? 'stable' : 'warning'}">${log.policy_authorization}</span></td>
        `;
        tbody.appendChild(tr);
      });
    } catch (err) {
      console.error(err);
    }
  }

  function appendLog(type, text) {
    const div = document.createElement('div');
    div.className = `log-line ${type}`;
    div.textContent = text;
    terminalConsole.appendChild(div);
    terminalConsole.scrollTop = terminalConsole.scrollHeight;
  }

  function activateDagStep(stepNum) {
    clearDagHighlight();
    const el = document.getElementById(`dag-step-${stepNum}`);
    if (el) el.classList.add('active');
  }

  function clearDagHighlight() {
    document.querySelectorAll('.dag-step').forEach(s => s.classList.remove('active'));
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
});
