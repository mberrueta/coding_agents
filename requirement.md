### Current Status
The application has an existing Admin Portal with a dashboard located at `/admin/dashboard`. This dashboard provides general administrative functions but lacks a dedicated view for aggregated, time-based reporting on key business metrics like appointment volume. Data analysis currently requires manual database queries or exporting raw data.

### Desired Status
A new dashboard page will be added to the Admin Portal, specifically for viewing monthly reports. This page will provide administrators with a clear, visual overview of key metrics over time. The initial implementation will focus on displaying the total number of appointments per month using a chart.

### Functional Requirements
- **FR1:** A new navigation link, labeled "Monthly Reports", shall be added to the Admin Portal's main navigation/sidebar.
- **FR2:** Clicking the "Monthly Reports" link shall navigate the admin to a new page, e.g., `/admin/reports/monthly`.
- **FR3:** Access to the `/admin/reports/monthly` page shall be restricted to users with the 'admin' role. Unauthorized users attempting to access the URL directly shall be redirected or shown an appropriate error.
- **FR4:** The monthly reports page shall display a chart visualizing the total number of appointments for each month.
- **FR5:** By default, the chart shall display data for the past 12 months.
- **FR6:** The data for the report shall be aggregated from the application's primary database.
- **FR7:** The chart shall be clearly labeled with a title (e.g., "Appointments per Month"), an X-axis for the months, and a Y-axis for the appointment count.

### Non-functional Requirements
- **NFR1:** The report page and its chart must load within 4 seconds. The data aggregation query should be optimized to handle a large volume of appointment records.
- **NFR2:** The visual design (colors, fonts, layout) of the new report page must be consistent with the existing Admin Portal stylesheet (`admin.css`).
- **NFR3:** The report page and chart must be responsive and render correctly on standard desktop and tablet screen sizes.
- **NFR4:** The data aggregation process should not introduce significant load on the database that could degrade the performance of other parts of the application.

### Acceptance Criteria
- **AC1:** An authenticated admin user can see and click the "Monthly Reports" link in the admin navigation.
- **AC2:** Upon clicking the link, the user is taken to the `/admin/reports/monthly` page, and the page loads successfully.
- **AC3:** A chart is visible on the page, displaying 12 data points corresponding to the last 12 months.
- **AC4:** The data shown in the chart for a given month accurately reflects the total number of appointments recorded in the database for that month.
- **AC5:** A non-admin user who tries to access the `/admin/reports/monthly` URL is denied access and redirected to their respective portal's home page.

### Out of Scope
- Reports for any user role other than Admin.
- Metrics other than the total number of appointments (e.g., revenue, patient sign-ups, doctor activity).
- The ability to export or download the report (e.g., as a PDF or CSV).
- Advanced filtering of the report data (e.g., by specific doctor, patient, or appointment status).
- Real-time, live updates to the chart.

### Questions to the user
- What is the precise definition of an "appointment" for this report? Should we count only completed appointments, or also include scheduled, canceled, or no-show appointments?
- What type of chart would you prefer for this data (e.g., a bar chart or a line chart)?
- Should users be able to select a different date range to view (e.g., a specific calendar year) or is the "last 12 months" view sufficient for now?
- Besides the chart, should any other summary statistics be displayed on the page (e.g., total appointments for the period, month-over-month growth percentage)?