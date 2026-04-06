# Desktop App Workflow

> **Project Type**: desktop-app (e.g., Tauri + React, Electron, Qt)
>
> **Applicable When**: `project_type` in `.project-meta.json` is `"desktop-app"`

---

## 📂 Deliverable Structure

```
projects/{current_project}/planning/specs/
├── screens/
│   ├── PLAN-{number}-{slug}.md          # Screen requirements
│   └── PLAN-{number}-{slug}.html        # Wireframe
├── state/
│   └── PLAN-{number}-{slug}.md          # State management spec
├── ipc/
│   └── PLAN-{number}-{slug}.md          # IPC communication spec (if needed)
└── test-cases/
    ├── PLAN-{number}-unit.md            # Unit tests
    ├── PLAN-{number}-integration.md     # Integration tests
    └── PLAN-{number}-e2e.md             # E2E tests
```

---

## 🔨 Work Process

### Step 1: Ticket Analysis

Extract the following from ticket:
- [ ] Screens/Windows (main window, settings dialog, etc.)
- [ ] User interactions (button clicks, drag and drop, etc.)
- [ ] State management (global state, local state)
- [ ] Backend communication (IPC, File I/O, network)

---

### Step 2: Present Deliverable List

```
Project: {current_project} (desktop-app)
Ticket: PLAN-{number}-{slug}

Files to be created:
- specs/screens/PLAN-{number}-{slug}.md
- specs/screens/PLAN-{number}-{slug}.html
- specs/state/PLAN-{number}-{slug}.md
- specs/ipc/PLAN-{number}-{slug}.md (if needed)
- specs/test-cases/PLAN-{number}-unit.md
- specs/test-cases/PLAN-{number}-integration.md
- specs/test-cases/PLAN-{number}-e2e.md

Main screens: Main window, Settings dialog
Main state: File list, Current selection
IPC communication: Open file, Save file

Continue? (yes/no)
```

---

### Step 3-1: Screen Requirements

**File**: `specs/screens/PLAN-{number}-{slug}.md`

```markdown
# {Screen Name} Requirements

## Screen Information
- **Type**: Main window / Dialog / Modal
- **Size**: 800x600 (minimum), Resizable / Fixed
- **Position**: Center / Restore previous position

## Layout Structure
- Header: Title, Minimize/Maximize/Close buttons
- Sidebar: File list
- Main area: Editor
- Footer: Status bar

## Component List

### File List (Sidebar)
- File tree view
- Context menu (right-click)
- Drag and drop support

### Editor (Main Area)
- Text input
- Syntax highlighting
- Auto-save indicator

## Keyboard Shortcuts
| Shortcut | Action |
|--------|------|
| Ctrl+O | Open file |
| Ctrl+S | Save file |
| Ctrl+W | Close window |

## Window Events
| Event | Action |
|--------|------|
| Window close | Check unsaved changes → Ask to save |
| Resize | Adjust layout, save size |
| Focus loss | Auto-save (if enabled in settings) |
```

---

### Step 3-2: Wireframe

**File**: `specs/screens/PLAN-{number}-{slug}.html`

Desktop App also uses vanilla HTML like Web-Fullstack:
- No external libraries
- Structure only
- State transition simulation

---

### Step 3-3: State Management Spec

**File**: `specs/state/PLAN-{number}-{slug}.md`

```markdown
# {Feature Name} State Management

## State Structure

\`\`\`typescript
interface AppState {
  files: FileItem[];
  selectedFile: FileItem | null;
  editorContent: string;
  isDirty: boolean;  // Unsaved changes
}
\`\`\`

## State Change Scenarios

### Open File
1. Initial state: `selectedFile = null`
2. User action: Click in file list
3. IPC call: `readFile(filePath)`
4. State update: `selectedFile = file, editorContent = content, isDirty = false`

### Edit Content
1. User action: Type in editor
2. State update: `editorContent = newContent, isDirty = true`
3. UI reflection: Display "*" in title

## State Persistence
| State | Storage Location | When |
|------|----------|------|
| Window size/position | Local config file | On window close |
| Recently opened files | Local config file | On file open |
| Editor settings | Local config file | On change |
```

---

### Step 3-4: IPC Communication Spec (If Needed)

**File**: `specs/ipc/PLAN-{number}-{slug}.md`

```markdown
# {Feature Name} IPC Communication

## IPC Method List

### readFile
- **Direction**: Frontend → Backend
- **Input**: `{ filePath: string }`
- **Output**: `{ content: string, encoding: string }`
- **Errors**: `FileNotFoundError`, `PermissionError`

### writeFile
- **Direction**: Frontend → Backend
- **Input**: `{ filePath: string, content: string }`
- **Output**: `{ success: boolean }`
- **Errors**: `WriteError`, `DiskFullError`

### watchFile
- **Direction**: Frontend ← Backend (event)
- **Trigger**: File system change detection
- **Data**: `{ filePath: string, changeType: 'modified' | 'deleted' }`
```

---

### Step 3-5: Test Cases

**Create 3 files**:
- `test-cases/PLAN-{number}-unit.md` - Component unit tests
- `test-cases/PLAN-{number}-integration.md` - IPC communication, state management integration tests
- `test-cases/PLAN-{number}-e2e.md` - User scenario E2E tests

---

## ✅ Completion Checklist

- [ ] Screen requirements created (layout, components)
- [ ] Wireframe created (HTML)
- [ ] State management spec created
- [ ] IPC spec created (if backend communication exists)
- [ ] 3 types of test cases created
- [ ] Keyboard shortcuts defined
- [ ] Window event handling defined
- [ ] Log file created

---

**Related Documents**:
- [gotchas.md](../gotchas.md)
- [CLAUDE.md](../CLAUDE.md)
