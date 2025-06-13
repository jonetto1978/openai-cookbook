# Cursor AI Rules Configuration

## Overview
This project now uses **global Cursor AI rules** managed through User Rules configuration and global files, ensuring consistent AI assistance across ALL development work, not just this project.

## Current Configuration

### 🌐 **Global Rules Setup**
- **User Rules**: Comprehensive execution rules defined in Cursor's User Rules (highest priority)
- **Global File**: `~/.cursorrules` - Applies to all projects without local rules
- **Backup File**: `~/.cursor/airulesgeenerated.mdc` - Reference copy

### 🚫 **Local Project Rules: REMOVED**
- No local `.cursorrules` file in this project
- This allows global rules to take effect
- Ensures consistency across all your projects

## Rule Categories

### 1. Communication Style
- Detailed explanations for non-senior developers
- Step-by-step breakdowns with clear examples
- Clear, jargon-free language with defined technical terms

### 2. Advanced Code Management
- No hard-coded dates/parameters (use {{placeholders}})
- Respect existing codebase structure
- Produce functions, not standalone scripts
- Centralize shared utilities in utils/services folders

### 3. Documentation Standards
- Always update README files
- Document all new functionality with examples
- Include purpose, inputs, outputs, side effects in docstrings

### 4. Data Handling & Analysis
- Never invent missing data - always request clarification
- Explicitly state assumptions about data interpretation
- Check Mixpanel Lexicon before adding tracking
- Attach metadata to every metric export

### 5. Development Practices
- Multi-environment compatibility (dev/test/prod)
- File size limits (300 lines with refactoring)
- Unit tests first for finance/billing logic
- No mocked data outside test suites

### 6. Argentina-Specific Standards
- Metric system measurements
- Comma decimal separator (1.234,56)
- $ currency with comma decimals
- Default output formatting to Argentina standards

## Best Practices Implemented

✅ **Global Consistency**: Rules apply to ALL Cursor projects
✅ **User Rules Priority**: Enhanced rules defined in Cursor's User Rules
✅ **No Local Overrides**: Clean global rule application
✅ **Advanced SaaS Workflows**: Mixpanel, automation, and analytics-focused rules

## Migration History

- **Phase 1**: Consolidated local rules from multiple sources
- **Phase 2**: Created global `~/.cursorrules` file
- **Phase 3**: Enhanced with advanced execution rules in User Rules
- **Phase 4**: Removed local `.cursorrules` for clean global application

## Usage

Cursor AI automatically applies these comprehensive rules to:
- ✅ This project (no local rules = global rules active)
- ✅ All new projects you create
- ✅ All existing projects without local `.cursorrules` files

**No additional configuration required** - rules are active globally! 