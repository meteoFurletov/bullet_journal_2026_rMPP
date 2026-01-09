# 0. Project Abstract: The "Tactical Unit" Planner

**Project Goal:** To generate a specialized, hyperlinked PDF template tailored for the reMarkable Paper Pro, designed specifically for high-intensity, technical project management (e.g., Software Architecture, Data Engineering, ML Pipelines).

**The Philosophy:**
Unlike standard planners that force a "one size fits all" approach for an entire year, this tool treats **one notebook as one project**. It is a disposable, focused "container" for a single sprint, feature build, or architectural design. It is built to manage the three stages of technical work:

1. **Definition** (The Hub)
2. **Architecture & Execution** (The Map)
3. **Deep Work & Solving** (The Lab)

**Target Device:** reMarkable Paper Pro (E-Ink).
**Output Format:** PDF (Generated via Python).

---

## 1. Functional Specifications & Structure

### 1.1 Global Parameters

* **Total Page Count:** 10 Pages fixed.
* **Page Dimensions:** A4 or reMarkable native resolution (approx. 1620 x 2160 px).
* **Grid System:** 5mm Dot Grid (standard engineering precision).
* **Navigation Logic:** "Always-on" visibility. Every page must be accessible from every other page without returning to a central index.

### 1.2 Global Navigation (The "Right Rail")

* **Location:** A fixed vertical strip on the right-most edge of *every* page.
* **Components:** A vertical stack of 10 distinct touch zones (buttons).
* **Button 1:** Labeled `HUB` (Links to Page 1).
* **Button 2:** Labeled `MAP` (Links to Page 2).
* **Buttons 3–10:** Labeled `3` through `10` (Links to respective Note Pages).

* **User Experience:** This simulates an app-like sidebar, allowing instant context switching (e.g., jumping from a sketch on Page 7 directly to the Task List on Page 2) with zero friction.

---

### 1.3 Page Layouts

#### **Page 1: The HUB (Definition & Context)**

* **Purpose:** The project's anchor. Used to define the "North Star" and verify completion.
* **Zone A: The Header (Top 25%)**
* *Left Column:* **"Core Concept"** – A blank text field for the Project Name and the primary hypothesis/logic.
* *Right Column:* **"Definition of Done"** – A rigid, static checklist (5-6 items) to define exit criteria.

* **Zone B: The Scratchpad (Bottom 75%)**
* *Content:* Standard Dot Grid.
* *Usage:* Unstructured space for quick calculations, temporary notes, or rough logic flows that do not require preservation.

#### **Page 2: The MAP (Architecture & Execution)**

* **Purpose:** The primary workspace. Combines system design (Visual) with task tracking (Linear).
* **Zone A: Architecture Canvas (Top 60%)**
* *Content:* Faint/Subtle Dot Grid (to aid drawing straight lines/boxes).
* *Layout:* Full-width, open horizontal space.
* *Usage:* Flowcharts, System Architecture diagrams, Data Pipelines (Source  Transform  Sink).

* **Zone B: Task Console (Bottom 40%)**
* *Divider:* A solid horizontal line separating Zone A and B.
* *Layout:* Two-Column list format.
* *Col 1 (Left, Narrow):* Checkbox.
* *Col 2 (Right, Wide):* Task Description.

* *Capacity:* Approx. 10–15 high-priority items.

#### **Pages 3–10: The LAB (Deep Work)**

* **Purpose:** Pure, distraction-free space for solving specific problems identified in The MAP.
* **Layout:** Full-page Dot Grid.
* **Header:** Minimalist top corner indicator for "Date/Topic" (optional, kept blank for flexibility).
* **Interaction:** These pages are the "RAM" of the project—used for detailed database schemas, mathematical proofs, or debugging logs.

---

### 1.4 User Flow (The "Happy Path")

1. **Initialization:** User opens a new "Tactical Unit" PDF file on the device.
2. **Setup (Page 1):** User writes the Project Name and defines the "Definition of Done" criteria.
3. **Planning (Page 2):** User sketches the system architecture in the top canvas and lists the necessary build steps in the bottom task list.
4. **Execution (Pages 3–10):** When a specific task requires complex thought (e.g., "Design API Schema"), the user taps `3` on the Right Rail, solves the problem on Page 3, then taps `MAP` to return to Page 2 and check off the task.
5. **Completion:** User returns to `HUB`, verifies all "Definition of Done" items are checked, and archives the notebook.

### 1.5 Success Metrics

The project is successful if the generated PDF:

1. Has accurate, clickable hyperlinks on the reMarkable Paper Pro (finger-touch accuracy).
2. Visually separates the "Thinking" (Hub), "Planning" (Map), and "Doing" (Lab) phases.
3. Eliminates the need for multiple templates/files for a single project.
