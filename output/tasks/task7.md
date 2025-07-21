### Task: Add "Monthly Reports" to Admin Navigation

**Related Requirement:** FR1, NFR2

**Description:**
Modify the shared admin layout template to include the new navigation link to the monthly reports page. This makes the feature discoverable for admin users.

**Files to be Modified/Created:**
- `lib/doctor_smart_web/components/layouts/admin.html.heex` (path may vary based on project structure)

**Acceptance Criteria (for TDD):**
- AC-1: The "Monthly Reports" link is visible in the admin sidebar or navigation menu on all admin pages.
- AC-2: Clicking the link correctly navigates the user to the `/admin/reports/monthly` page.
- AC-3: The new link's visual style is consistent with other navigation links in the admin portal, adhering to `admin.css`.

**Technical Guidance:**
- Locate the list of navigation items in the admin layout template.
- Add a new Phoenix component link, for example: `<.link navigate={~p"/admin/reports/monthly"}> <.icon name="hero-chart-bar" /> Monthly Reports </.link>`.
- Ensure the structure and CSS classes match the other existing navigation items.