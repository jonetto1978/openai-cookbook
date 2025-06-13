# Global Cursor AI Rules Setup

## 🌐 **Active Across ALL Your Projects - Latest Configuration**

Your comprehensive AI rules are now optimally configured through a **hybrid approach** combining User Rules and global files for maximum effectiveness across all Cursor projects.

## 📂 **Current Configuration:**

### 1. **User Rules (Highest Priority)**
```
Cursor Settings > User Rules
```
- **Purpose**: Advanced execution rules with Colppy/SaaS-specific workflows
- **Scope**: Applies to ALL Cursor instances and projects globally
- **Content**: Enhanced rules including Mixpanel integration, Argentina formatting, automation

### 2. **Global Fallback Rules**
```
~/.cursorrules
```
- **Purpose**: Backup/fallback rules file that Cursor automatically discovers
- **Scope**: Applies when User Rules aren't fully loaded or as supplementary
- **Priority**: Secondary to User Rules, higher than defaults

### 3. **Reference File**
```
~/.cursor/airulesgeenerated.mdc
```
- **Purpose**: Historical backup and reference documentation
- **Content**: Complete copy of all rules for troubleshooting

## 🔄 **Optimized Rule Priority Hierarchy:**

1. **User Rules in Cursor Settings** (highest priority) ← **Your primary setup**
2. **Global** `~/.cursorrules` (fallback/supplementary)
3. **Project-specific** `.cursorrules` (when present - now removed from this project)
4. **Cursor defaults** (lowest priority)

### **When Global Rules Apply:**
- ✅ **ALL projects** - User Rules apply universally
- ✅ **New projects** - Full rule set automatically active
- ✅ **Existing projects** - No local overrides needed
- ✅ **This project** - Local `.cursorrules` removed for clean global application

## 🎯 **Enhanced Benefits for You:**

### **Universal Application:**
- **User Rules** ensure consistent AI behavior across ALL projects
- **Advanced SaaS workflows** with Mixpanel integration and Colppy-specific patterns
- **Argentina formatting** (comma decimals, metric system, $ currency) applied everywhere
- **Never assume data** principle enforced globally with explicit clarification requests

### **Advanced Features:**
- **No hard-coded parameters** - always use {{placeholders}} for dates, plans, etc.
- **Automatic metadata attachment** to all metric exports (date range, source, record count)
- **Mixpanel Lexicon checking** before adding new tracking events
- **Unit tests first** for finance/billing logic
- **Automation suggestions** for repetitive reports (3+ times in 30 days)

### **Clean Configuration:**
- **No local rule conflicts** - removed `.cursorrules` from this project
- **Streamlined rule hierarchy** with User Rules taking priority
- **Maximum 300-line files** with automatic refactoring suggestions

## 🔧 **Verification:**

To confirm the optimized setup:

1. **Check User Rules** in Cursor Settings - should show comprehensive execution rules
2. **Open any project** in Cursor
3. **Request data analysis** - should get detailed step-by-step explanations
4. **Ask for currency formatting** - should use Argentina standards (1.234,56)
5. **Request a report** - should include metadata and use {{placeholders}}

## ⚠️ **Configuration Notes:**

- **User Rules take precedence** over all file-based rules
- **Global ~/.cursorrules** serves as backup/supplementary
- **No project-specific overrides** needed - clean global application
- **Restart Cursor** if rules don't seem to be applying correctly

## 🎉 **Optimized Success!**

Your professional AI standards are now **consistently applied** across all Cursor projects with enhanced SaaS/analytics-specific workflows! 