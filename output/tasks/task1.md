### Task: Add Chart.js Frontend Dependency

**Related Requirement:** FR4

**Description:**
Add the `chart.js` library to the frontend assets to enable chart rendering on the new reports page. This will be installed via npm and bundled with the application's JavaScript.

**Files to be Modified/Created:**
- `assets/package.json`

**Acceptance Criteria (for TDD):**
- AC-1: The `chart.js` library is added as a dependency in the `assets/package.json` file.
- AC-2: Running `npm install` from within the `assets` directory successfully installs the package and its dependencies into the `node_modules` folder.

**Technical Guidance:**
- Add a line for `chart.js` to the `dependencies` object in `package.json`. A recent stable version is recommended, for example: `"chart.js": "^4.4.0"`.