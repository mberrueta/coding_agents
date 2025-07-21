### Task: Implement Frontend Chart Rendering with Chart.js

**Related Requirement:** FR4, FR7, AC3, NFR3

**Description:**
Implement the JavaScript Phoenix Hook to render the monthly appointments chart using Chart.js. This hook will read the report data from the DOM element's `data-` attribute, parse it, and initialize a responsive bar chart.

**Files to be Modified/Created:**
- `assets/js/app.js`

**Acceptance Criteria (for TDD):**
- AC-1: A `MonthlyReportChart` hook is defined in `assets/js/app.js` and registered with the `LiveSocket` instance.
- AC-2: In the hook's `mounted()` callback, it successfully reads and parses the JSON data from the `data-report-data` attribute of its element.
- AC-3: A new `Chart.js` bar chart instance is created and rendered on the associated `<canvas>` element.
- AC-4: The chart's X-axis is correctly labeled with the months from the parsed data.
- AC-5: The chart's Y-axis dataset is correctly populated with the appointment counts.
- AC-6: The chart displays the title "Appointments per Month" and has clearly labeled axes.
- AC-7: The chart is configured to be responsive and resizes correctly with the browser window.

**Technical Guidance:**
- At the top of `app.js`, import and register Chart.js components: `import { Chart, registerables } from 'chart.js'; Chart.register(...registerables);`.
- Define the hook: `let Hooks = {}; Hooks.MonthlyReportChart = { mounted() { ... } };`.
- Inside `mounted()`, parse the data: `const data = JSON.parse(this.el.dataset.reportData);`.
- Prepare data for Chart.js: `const labels = data.map(d => d.month); const counts = data.map(d => d.count);`.
- Initialize the chart: `new Chart(this.el, { type: 'bar', data: { labels: labels, datasets: [{ label: 'Appointments', data: counts }] }, options: { responsive: true, plugins: { title: { display: true, text: 'Appointments per Month' } } } });`.
- Pass the `Hooks` object to the `LiveSocket` constructor: `let liveSocket = new LiveSocket("/live", Socket, {..., hooks: Hooks})`.