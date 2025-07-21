### Task: Create Test for Admin Navigation Link

**Related Requirement:** FR1, AC1

**Description:**
Add a test to an existing admin-related test file (e.g., the admin dashboard test) to ensure that a "Monthly Reports" link is present in the navigation for admin users.

**Files to be Modified/Created:**
- `test/doctor_smart_web/live/admin/dashboard_live_test.exs` (or a similar existing test file)

**Acceptance Criteria (for TDD):**
- AC-1: A test case renders a page that uses the main admin layout (e.g., the admin dashboard).
- AC-2: The test is run in the context of a logged-in admin user.
- AC-3: The test asserts that the rendered HTML contains a link (`<a>` tag) with the text "Monthly Reports".
- AC-4: The test asserts that this link's `href` attribute is `/admin/reports/monthly`.

**Technical Guidance:**
- Find the most appropriate existing test file that covers the shared admin layout. Add a new `test "shows monthly reports link for admins" ...` block.
- Use `Phoenix.LiveViewTest` helpers to render the view and then assert on the resulting HTML content.