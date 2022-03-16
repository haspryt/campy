# campy
A Cambridge Pseudocode to Python transpiler, written in Python 3
# Usage
```
git clone git@github.com:haspryt/campy && cd campy
python main.py <input_filename> <output_filename>
```
# Current state
This project is still relatively early in development but most basic features should already work. THe official Cambridge pseudocode guide can be found [here](https://www.cambridgeinternational.org/Images/639920-2021-pseudocode-guide-for-teachers.pdf).
## Feature matrix
| Feature | Status | Notes |
| Variables | Done | |
| Types | Done | |
| Constants | Not started | |
| Functions, procedures | Not started | |
| File handling | Not started | |
| `IF`, `ELSE` | Done | |
| `WHILE` | Done | |
| `REPEAT ... UNTIL` | Done | |
| `FOR` | Done | |
| `CASE` | Not started | |
| `+`, `-`, `*`, `/`, `DIV`, `MOD` | Partly done | `DIV` and `MOD` not yet implemented, order of operations not taken into account (use parentheses) |
| `>`, `<`, `>=`, `<=`, `=`, `<>` | Done | |
| `&`, `,` (concatenation) | Done | |
| `OUTPUT` | Done | |
| `INPUT` | Done | |
| User-defined datatypes | Not started | |
| Syntax checking | Partly done | Requires testing |
| Indentation checking | Done | |
| Comments | Done | |
| Type checking | Not started | |
| Other checks | Not started | |