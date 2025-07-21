### Task: Implement Monthly Appointment Aggregation Logic

**Related Requirement:** FR6, FR5, NFR1, NFR4

**Description:**
Create the `Reports` context and implement the `get_monthly_appointment_counts/0` function. This function will query the database using Ecto and return the total number of appointments per month for the last 12 months. This task makes the test from the previous step pass.

**Files to be Modified/Created:**
- `lib/doctor_smart/reports.ex`

**Acceptance Criteria (for TDD):**
- AC-1: The `DoctorSmart.Reports.get_monthly_appointment_counts/0` function is implemented.
- AC-2: The function returns a list of 12 maps, each containing a `:month` (formatted as "YYYY-MM") and a `:count`.
- AC-3: The Ecto query correctly filters appointments to include only those from the last 12 full months.
- AC-4: The query groups appointments by month and correctly counts the records in each group.
- AC-5: The function correctly handles months within the range that have zero appointments, returning a map with `count: 0` for those months.

**Technical Guidance:**
- Use the `Timex` library to robustly calculate the start date of the 12-month period (e.g., `Timex.now() |> Timex.beginning_of_month() |> Timex.shift(months: -11)`).
- Use Ecto's `fragment/1` for database-specific date truncation to group by month. For PostgreSQL, this would be `fragment("TO_CHAR(?, 'YYYY-MM')", a.inserted_at)`.
- To ensure all 12 months are present, you can generate the list of the last 12 month-strings in Elixir and merge the Ecto query results into it.