### Task: Create Test for Monthly Appointment Aggregation

**Related Requirement:** FR6, FR5, AC4, NFR1

**Description:**
Create a new test module for the `Reports` context. This test will verify that the data aggregation logic correctly counts appointments per month for the last 12 months. This is the first step in our TDD process for the backend logic, ensuring data accuracy before building any UI.

**Files to be Modified/Created:**
- `test/doctor_smart/reports_test.exs`

**Acceptance Criteria (for TDD):**
- AC-1: A new test file `test/doctor_smart/reports_test.exs` is created.
- AC-2: A test case seeds the database with `Appointment` records spanning multiple months (e.g., this month, last month, and a month older than 12 months).
- AC-3: The test asserts that `DoctorSmart.Reports.get_monthly_appointment_counts/0` returns a list of exactly 12 maps.
- AC-4: The test verifies that the `count` for recent months is correct and that the data from the appointment older than 12 months is excluded.
- AC-5: The returned data structure is a list of maps, with each map containing `:month` (as a "YYYY-MM" string) and `:count` (as an integer) keys.

**Technical Guidance:**
- Use your project's test data factory (e.g., ExMachina) to create `Appointment` records. You may need to manually set the `inserted_at` or other relevant timestamp fields to control which month they fall into.
- The test should not rely on the real system clock; control the dates of the test data precisely.