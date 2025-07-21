### Task: Implement Monthly Report Route and LiveView Shell

**Related Requirement:** FR2, FR3, FR7

**Description:**
Add the new route to the router and create the basic structure for the `Admin.MonthlyReportLive` LiveView and its HEEx template. This task will make the tests from the previous step pass by setting up the necessary server-side components.

**Files to be Modified/Created:**
- `lib/doctor_smart_web/router.ex`
- `lib/doctor_smart_web/live/admin/monthly_report_live.ex`
- `lib/doctor_smart_web/live/admin/monthly_report_live.html.heex`

**Acceptance Criteria (for TDD):**
- AC-1: A `live "/admin/reports/monthly", Admin.MonthlyReportLive` route is added inside the appropriate admin-only scope in `router.ex`.
- AC-2: The `DoctorSmartWeb.Admin.MonthlyReportLive` module is created. Its `mount/3` function calls `Reports.get_monthly_appointment_counts/0` and assigns the result to `@report_data`.
- AC-3: The `monthly_report_live.html.heex` template is created and displays a title, e.g., `<h1>Appointments per Month</h1>`.
- AC-4: The template includes a `<canvas>` element with a unique `id`, a `phx-hook="MonthlyReportChart"`, and a `data-report-data` attribute that is populated with JSON-encoded data.

**Technical Guidance:**
- In `router.ex`, place the new route within the `scope "/admin", DoctorSmartWeb do` block that uses your admin authentication plug (e.g., `pipe_through [:browser, :require_admin]`).
- In `monthly_report_live.ex`, the `mount/3` function should assign the data: `{:ok, assign(socket, :report_data, Reports.get_monthly_appointment_counts())}`.
- In the HEEx template, use `Jason.encode!/1` to pass the data to the frontend hook: `<canvas id="monthly-appointments-chart" phx-hook="MonthlyReportChart" data-report-data={Jason.encode!(@report_data)}></canvas>`.