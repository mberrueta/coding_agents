### Task: Create Tests for Monthly Report LiveView

**Related Requirement:** FR2, FR3, FR4, AC2, AC5

**Description:**
Create a test file for the `Admin.MonthlyReportLive` LiveView. This will include tests for authorization (only admins can access) and for verifying the initial page content and data assignment when an authorized admin visits the page.

**Files to be Modified/Created:**
- `test/doctor_smart_web/live/admin/monthly_report_live_test.exs`

**Acceptance Criteria (for TDD):**
- AC-1: **(Authorization)** A test confirms that a logged-in, non-admin user is redirected when attempting to access `/admin/reports/monthly`.
- AC-2: **(Admin Access)** A test confirms that a logged-in admin user receives a `200 OK` response when navigating to `/admin/reports/monthly`.
- AC-3: **(Content)** The admin access test asserts that the rendered page contains the title "Appointments per Month".
- AC-4: **(Chart Element)** The admin access test asserts that the rendered page contains a `<canvas>` element with a `phx-hook="MonthlyReportChart"` attribute.
- AC-5: **(Data Assignment)** The test verifies that `mount/3` calls `Reports.get_monthly_appointment_counts/0` and that the result is assigned to the socket.

**Technical Guidance:**
- Use `Phoenix.LiveViewTest` helpers like `live/2` and `render/1`.
- For the authorization test, ensure you can simulate logging in as a non-admin user.
- For the content test, you can mock the `Reports.get_monthly_appointment_counts/0` call to return predictable data, which isolates the LiveView test from the database logic. Example: `Mox.expect(DoctorSmart.ReportsMock, :get_monthly_appointment_counts, fn -> [%{month: "2023-10", count: 10}] end)`.