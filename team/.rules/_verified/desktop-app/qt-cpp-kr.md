# Qt (C++) Coding Rules

> Auto-generated: 2026-03-13 00:00:00
> Framework version: Qt 6.x (latest)
> Status: 🤖 Auto-generated

---

## 1. Project Structure

```
project-root/
├── CMakeLists.txt              # Main build configuration
├── .gitignore                  # Version control exclusions
├── README.md                   # Project documentation
├── src/                        # Source code
│   ├── main.cpp               # Application entry point
│   ├── models/                # Data models (M in MVC/MVVM)
│   │   ├── CMakeLists.txt
│   │   └── *.h, *.cpp
│   ├── views/                 # UI components (V in MVC/MVVM)
│   │   ├── CMakeLists.txt
│   │   ├── *.h, *.cpp
│   │   └── *.ui               # Qt Designer forms
│   ├── controllers/           # Business logic (C in MVC)
│   │   ├── CMakeLists.txt
│   │   └── *.h, *.cpp
│   ├── delegates/             # Custom item delegates
│   │   └── *.h, *.cpp
│   ├── utils/                 # Utility classes
│   │   └── *.h, *.cpp
│   └── resources/             # Qt resources
│       ├── qml/              # QML files (when using Qt Quick)
│       ├── images/           # Image assets
│       └── resources.qrc     # Qt resource file
├── include/                   # Public headers (for libraries)
│   └── projectname/
│       └── *.h
├── tests/                     # Test code
│   ├── CMakeLists.txt
│   ├── unit/                 # Unit tests
│   │   └── tst_*.cpp
│   └── integration/          # Integration tests
│       └── tst_*.cpp
├── docs/                      # Documentation
│   └── *.md
└── build/                     # Build output (git-ignored)
```

### Directory Roles

- **src/models/**: QAbstractItemModel, QAbstractListModel, QAbstractTableModel implementations for complex data
- **src/views/**: QWidget, QMainWindow, QDialog subclasses and .ui files
- **src/controllers/**: Business logic that coordinates models and views
- **src/delegates/**: QStyledItemDelegate subclasses for custom rendering/editing
- **src/utils/**: Helper classes, constants, type definitions
- **tests/**: QTest-based test cases with tst_ prefix

---

## 2. Architecture Patterns

### Model/View/Delegate (Qt's MVC Variant)

Qt uses a modified Model-View-Controller pattern that separates data management from presentation:

**Model**: Manages data through the QAbstractItemModel interface. Does not store data directly but provides access to the underlying source (database, file, memory). Use QAbstractListModel or QAbstractTableModel for simpler structures.

**View**: Displays model data using QListView, QTableView, QTreeView, or custom views. Multiple views can display the same model simultaneously.

**Delegate**: Handles item rendering and editing through QStyledItemDelegate. Customizes appearance and user interaction.

### When to Use Model/View vs. Convenience Classes

- **Model/View**: Use for complex data, multiple views, custom rendering, large datasets, database-backed data
- **Convenience Classes** (QListWidget, QTableWidget, QTreeWidget): Use for simple, static lists where flexibility is less critical

### MVVM Pattern (When Using Qt Quick/QML)

For QML applications, use Model-View-ViewModel:
- **Model**: C++ data models (QAbstractItemModel)
- **View**: QML visual components
- **ViewModel**: C++ classes exposed to QML via Q_PROPERTY and signals

---

## 3. Naming Conventions

### File Names

- **C++ source/header**: lowercase + underscores (e.g., `main_window.cpp`, `main_window.h`)
- **UI files**: Match corresponding class (e.g., `main_window.ui`)
- **QML files**: UpperCamelCase (e.g., `MainWindow.qml`)
- **Test files**: `tst_` prefix (e.g., `tst_main_window.cpp`)

### Classes

- Classes start with uppercase: `MainWindow`, `UserModel`
- Public Qt classes use `Q` prefix: `QRgb`, `QString` (Qt framework classes only)
- Abbreviations are camel-cased: `QXmlStreamReader` (not `QXMLStreamReader`)

### Variables and Functions

- Start with lowercase, subsequent words uppercase: `userName`, `calculateTotal()`
- Avoid abbreviations except widely known terms (`id`, `url`)
- Avoid single-character names except loop counters (`i`, `j`, `k`)
- Declare each variable on a separate line

### Member Variables

- Private members can use prefix convention (project-specific): `m_userName` or `_userName`
- Qt style doesn't require special prefix, but consistency is important

### Constants and Enums

- Constants: All uppercase + underscores: `MAX_BUFFER_SIZE`
- Enum names: UpperCamelCase: `enum ConnectionState { ... }`
- Enum values: UpperCamelCase: `Connected`, `Disconnected`

---

## 4. Coding Style

### Language-Specific Style Guides

- **C++ Standard**: Modern C++ (C++17 or later recommended for Qt 6)
- **Qt Style Guide**: [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- **Qt Coding Conventions**: [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)

### Indentation and Formatting

- **Indentation**: 4 spaces (not tabs)
- **Line length**: Maximum 100 characters; comments under 80 characters
- **Blank lines**: Use only one line for separation

### Braces

- Control structures have opening brace on same line:
  ```cpp
  if (condition) {
      // code
  }
  ```
- Functions and classes have opening brace on new line:
  ```cpp
  void MyClass::myFunction()
  {
      // code
  }
  ```
- Use braces for empty bodies: `while (a) {}`
- Single-line bodies can omit braces unless part of multi-branch structure

### Whitespace

- One space after flow control keywords: `if (`, `while (`, `for (`
- One space before opening brace
- Pointers/references: `Type *variable` or `Type &variable` (space after type)
- Binary operators: Surround with spaces: `a + b`, `x == y`
- No space after cast operators

### Headers

- Include guards: Use `#pragma once` or traditional guards
- Include order:
  1. Corresponding header (for .cpp files)
  2. Qt headers: `#include <QtCore/qstring.h>` or `#include <QString>`
  3. Other library headers
  4. Project headers
- Use full format in public headers: `#include <QtCore/qobject.h>`

### Qt-Specific Best Practices

- All QObject subclasses require `Q_OBJECT` macro
- Prefer Qt containers for Qt-compatible types over STL
- Use Qt signal/slot mechanism instead of direct callbacks
- Use Qt's meta-object system: `Q_PROPERTY`, `Q_ENUM`, `Q_INVOKABLE`
- Avoid RTTI (dynamic_cast); use qobject_cast

---

## 5. Dependency Management

### Package Managers

- **vcpkg**: Cross-platform C++ package manager (recommended)
- **Conan**: Alternative C++ package manager
- **System package managers**: apt, brew, pacman (for development)

### CMake Configuration

**CMakeLists.txt** (Qt 6's primary build system):

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt configuration
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui)

# Add executable
add_executable(${PROJECT_NAME}
    src/main.cpp
    # ... other sources
)

target_link_libraries(${PROJECT_NAME}
    Qt6::Core
    Qt6::Widgets
    Qt6::Gui
)
```

### Qt Modules

Common Qt modules:
- **Core**: Foundation (QObject, QString, containers)
- **Gui**: GUI components (QImage, QFont, events)
- **Widgets**: Traditional desktop widgets
- **Quick**: QML/Qt Quick for modern UI
- **Network**: Networking (QNetworkAccessManager)
- **Sql**: Database access
- **Test**: Testing framework

Add only needed modules to minimize dependencies.

---

## 6. Environment Configuration

### Environment Variables

- **Qt installation**: Set `Qt6_DIR` or add to `CMAKE_PREFIX_PATH`
- **Application settings**: Use QSettings for persistent configuration
- **Development**: Use `.env` or CMake cache variables for build settings

### Configuration Files

```cpp
// Reading settings
QSettings settings("MyCompany", "MyApp");
QString dbPath = settings.value("database/path", "default.db").toString();

// Writing settings
settings.setValue("database/path", "/path/to/db");
```

### Platform-Specific Configuration

- **Windows**: Registry (`HKEY_CURRENT_USER\Software\MyCompany\MyApp`)
- **macOS**: plist file (`~/Library/Preferences/com.mycompany.myapp.plist`)
- **Linux**: INI file (`~/.config/MyCompany/MyApp.conf`)

---

## 7. Security Guidelines

### Input Validation

- **User input**: Always validate and sanitize
  ```cpp
  QString sanitized = userInput.simplified(); // Remove extra whitespace
  if (!validateInput(sanitized)) {
      qWarning() << "Invalid input received";
      return;
  }
  ```
- **File paths**: Use QFileInfo to canonicalize and validate
- **Network data**: Validate all data from network sources

### Preventing SQL Injection

Use parameterized queries in Qt SQL:

```cpp
// Correct: Parameterized query
QSqlQuery query;
query.prepare("SELECT * FROM users WHERE username = :username");
query.bindValue(":username", userName);
query.exec();

// Wrong: String concatenation
// query.exec("SELECT * FROM users WHERE username = '" + userName + "'");
```

### Memory Safety

- **RAII**: Use smart pointers or Qt parent-child ownership
  ```cpp
  QWidget *widget = new QWidget(parent); // Automatically deleted when parent is destroyed
  ```
- **Buffer overflow**: Avoid raw C strings; use QString and QByteArray
- **Array access**: Qt containers perform bounds checking in debug mode

### Secret Management

- **Passwords**: Never store plain-text passwords
- **API keys**: Use encrypted QSettings or platform keychain
  - macOS: Keychain Services
  - Windows: Credential Manager (DPAPI)
  - Linux: libsecret/KWallet
- **Encryption**: Use QCryptographicHash for hashing, OpenSSL for encryption

### Code Signing (Distribution)

- **macOS**: Sign code with Apple Developer ID
- **Windows**: Sign with authenticode certificate
- **Linux**: Package signing varies by distribution

### Security Standards Compliance

- **OWASP Secure Coding Practices**: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- **MISRA C++**: For safety-critical applications
- **SEI CERT C++ Coding Standard**: https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682

---

## 8. Error Handling

### Exception Handling

Qt generally **avoids exceptions**:
- Qt classes do not throw exceptions
- Return error codes or use signals to indicate errors
- If using exceptions in your code, ensure proper RAII cleanup

### Error Reporting

```cpp
// Check return values
QFile file("data.txt");
if (!file.open(QIODevice::ReadOnly)) {
    qWarning() << "Failed to open file:" << file.errorString();
    return false;
}

// Use QMessageBox for user-facing errors
QMessageBox::critical(this, "Error", "Failed to save file");
```

### Logging

**Qt Logging Categories**:

```cpp
// Define logging category
Q_LOGGING_CATEGORY(lcMyApp, "myapp.main")

// Use in code
qCDebug(lcMyApp) << "Debug message";
qCInfo(lcMyApp) << "Info message";
qCWarning(lcMyApp) << "Warning message";
qCCritical(lcMyApp) << "Critical error";
```

**Log Levels**:
- **qDebug()**: Debug information (removed in release builds by default)
- **qInfo()**: Informational messages
- **qWarning()**: Warnings that don't interrupt execution
- **qCritical()**: Critical errors
- **qFatal()**: Fatal errors (terminates application)

**Configuration**:
Create `qtlogging.ini` to control logging:
```ini
[Rules]
myapp.*.debug=true
qt.*.debug=false
```

---

## 9. Testing Strategy

### Testing Framework

**QTest**: Qt's official unit testing framework

### Test Structure

```
tests/
├── CMakeLists.txt
├── unit/
│   ├── tst_mymodel.cpp
│   └── tst_mycontroller.cpp
└── integration/
    └── tst_database.cpp
```

### Unit Test Example

```cpp
#include <QtTest/QtTest>
#include "mymodel.h"

class TestMyModel : public QObject
{
    Q_OBJECT

private slots:
    void initTestCase();    // Called before first test
    void cleanupTestCase(); // Called after last test
    void init();            // Called before each test
    void cleanup();         // Called after each test

    void testAddItem();
    void testRemoveItem();
};

void TestMyModel::testAddItem()
{
    MyModel model;
    model.addItem("Test");
    QCOMPARE(model.rowCount(), 1);
    QVERIFY(model.data(model.index(0, 0)).toString() == "Test");
}

QTEST_MAIN(TestMyModel)
#include "tst_mymodel.moc"
```

### Testing Best Practices

- **Avoid hardcoded timeouts**: Use `QTRY_VERIFY()`, `QTRY_COMPARE()`, `QSignalSpy` instead of `QTest::qWait()`
- **Use QVERIFY2**: Provide error messages: `QVERIFY2(condition, "Error message")`
- **Restore state**: Prevent tests from affecting each other; use cleanup() or RAII
- **Headless testing**: Use `-platform offscreen` for GUI tests in CI/CD
- **Stack allocation**: Instantiate test objects on stack for automatic cleanup

### GUI Testing

```cpp
void TestMainWindow::testButtonClick()
{
    MainWindow window;
    QTest::mouseClick(window.submitButton(), Qt::LeftButton);
    QCOMPARE(window.status(), MainWindow::Submitted);
}
```

### Signal/Slot Testing

```cpp
void TestMyClass::testSignalEmitted()
{
    MyClass obj;
    QSignalSpy spy(&obj, &MyClass::dataChanged);

    obj.updateData();

    QCOMPARE(spy.count(), 1);
    QList<QVariant> arguments = spy.takeFirst();
    QVERIFY(arguments.at(0).toInt() == 42);
}
```

### Coverage Goals

- **Goal**: 70-80% code coverage for business logic
- **Critical paths**: 100% coverage for security-critical code
- **UI code**: Focus on logic testing; visual testing may require manual QA

### Running Tests

```bash
# Run all tests
ctest --output-on-failure

# Run specific test
./tests/unit/tst_mymodel

# Verbose output
./tests/unit/tst_mymodel -v2
```

---

## 10. Performance Optimization

### Qt-Specific Optimizations

**Implicit sharing**: Qt containers use copy-on-write
```cpp
QString a = "Hello";
QString b = a;  // Data shared, no deep copy until modified
```

**Reserve capacity**: Pre-allocate for known sizes
```cpp
QVector<int> vec;
vec.reserve(1000);  // Prevent reallocation
```

**Const correctness**: Use const iterators and references
```cpp
for (const QString &str : stringList) {  // Prevents detachment
    // Read-only access
}
```

**Model/View optimization**:
- Implement `canFetchMore()` and `fetchMore()` for lazy loading
- Use `QAbstractItemModel::dataChanged()` for minimal updates
- Override `rowCount()` and `columnCount()` efficiently

**Signal/Slot**:
- Use `Qt::QueuedConnection` to avoid blocking
- Use `Qt::UniqueConnection` to prevent duplicate connections
- Disconnect slots when no longer needed

**QString operations**:
- Use `QString::arg()` instead of multiple concatenations
- Use `QStringBuilder` (define `QT_USE_QSTRINGBUILDER`)

**Database**:
- Use prepared statements (faster + secure)
- Batch operations with transactions
- Use appropriate fetch size for queries

---

## 11. Documentation

### Code Comments

**Header documentation**:
```cpp
/**
 * @brief Manages user data and authentication
 *
 * UserModel provides access to user information and
 * handles authentication logic. It implements
 * QAbstractTableModel for display in table views.
 *
 * @see QAbstractTableModel
 */
class UserModel : public QAbstractTableModel
{
    // ...
};
```

**Function documentation**:
```cpp
/**
 * @brief Authenticates a user with username and password
 * @param username The user's username
 * @param password The user's password (hashed)
 * @return true if authentication succeeds, false otherwise
 */
bool authenticate(const QString &username, const QString &password);
```

**Inline comments**:
- Explain "why", not "what"
- Use `//` for single line, `/* */` for multiple lines
- Keep comments concise and up-to-date

### Qt Documentation Format

Qt uses **QDoc** for documentation generation. Use special commands:
- `\brief`: Short description
- `\param`: Parameter description
- `\return`: Return value description
- `\sa`: See also (cross-references)
- `\note`: Important notes
- `\warning`: Warnings

### README.md Required Sections

```markdown
# Project Name

## Description
Brief description of the application

## Features
- Feature 1
- Feature 2

## Requirements
- Qt 6.x
- CMake 3.16+
- C++17 compiler

## Build
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

## Run
```bash
./MyApp
```

## Testing
```bash
ctest --output-on-failure
```

## License
[License Type]

## Contributing
Guidelines for contributors
```

---

## 12. Prohibited Practices

### Framework Anti-Patterns

- **Do not use raw pointers without ownership tracking**: Use Qt parent-child or smart pointers
- **Do not omit Q_OBJECT macro**: Required for signals/slots in QObject subclasses
- **Do not use dynamic_cast on QObject**: Use `qobject_cast`
- **Do not manually delete objects with Qt parent**: Parent handles deletion
- **Do not block event loop**: Use `QThread` or `QtConcurrent` for heavy operations

### Security Vulnerabilities

- **SQL injection**: Do not concatenate SQL queries with user input
- **Path traversal**: Validate file paths, use canonical paths
- **Buffer overflow**: Avoid raw C strings, use Qt containers
- **Hardcoded credentials**: Do not commit passwords or API keys
- **Unvalidated input**: Always sanitize user and network input

### Performance Issues

- **Detaching shared containers**: Avoid non-const operations on implicitly shared objects in loops
- **Excessive signal emission**: Batch updates, use blockSignals() judiciously
- **Synchronous network calls**: Use asynchronous Qt Network APIs
- **Frequent string concatenation**: Use `QString::arg()` or QStringBuilder

### Build/Deployment

- **Do not commit build artifacts**: Add `build/`, `*.o`, `*.exe`, `moc_*`, `ui_*` to .gitignore
- **Do not hardcode paths**: Use QStandardPaths for system directories
- **Do not skip testing**: Always run tests before release

---

## 13. References

### Official Documentation
- [Qt Documentation](https://doc.qt.io/)
- [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)
- [Qt Test Best Practices](https://doc.qt.io/qt-6/qttest-best-practices-qdoc.html)
- [Model/View Programming](https://doc.qt.io/qt-6/model-view-programming.html)
- [Qt Security](https://doc.qt.io/qt-6/security.html)

### Best Practices
- [Clean Qt Blog](https://cleanqt.io/)
- [How to Ensure High Cyber Security in Qt Apps](https://scythe-studio.com/en/blog/how-to-ensure-high-cyber-security-in-qt-apps)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Top 10 Secure C++ Coding Practices](https://www.incredibuild.com/blog/top-10-secure-c-coding-practices)

### Example Projects
- [Qt Examples and Tutorials](https://doc.qt.io/qt-6/qtexamplesandtutorials.html)
- [Qt Creator Source Code](https://code.qt.io/cgit/qt-creator/qt-creator.git/)

---

## 🔄 About This Document

This coding rule was auto-generated by the **Stack Initializer Agent**.

- **Verification needed**: Can be moved to `.rules/_verified/` after project-specific modifications
- **Expiration**: Option to regenerate provided after 24 hours
- **Contribution**: Improvement suggestions can be submitted as PRs on GitHub

---

## Sources

Research for this document was gathered from:
- [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- [Qt Coding Conventions](https://wiki.qt.io/Coding_Conventions)
- [Model/View Programming | Qt 6.10.2](https://doc.qt.io/qt-6/model-view-programming.html)
- [Qt Test Best Practices | Qt 6.10.2](https://doc.qt.io/qt-6/qttest-best-practices-qdoc.html)
- [Clean Qt Blog](https://cleanqt.io/)
- [How to Ensure High Cyber Security in Qt Apps](https://scythe-studio.com/en/blog/how-to-ensure-high-cyber-security-in-qt-apps)
- [Qt Security | Qt 6.10](https://doc.qt.io/qt-6/security.html)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
