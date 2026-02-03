# Vision: How to be a better library

The ultimate purpose of DepDigest is to **make complex libraries feel lightweight**. 

## To better serve this purpose, DepDigest should:

1.  **Be Invisible**: The best infrastructure is the one you don't notice. Automatic configuration discovery and intuitive decorators are the path to this.
2.  **Be Defensive**: It should protect the user's environment. If a missing dependency is detected, it should provide the exact command to fix it, reducing friction.
3.  **Encourage Good Architecture**: By providing the `audit` tools, it actively discourages "lazy" (not the good kind) development practices that lead to bloated imports.
4.  **Promote UIBCDF Ecosystem Symmetry**: Together with `ArgDigest` and `PyUnitWizard`, it should form a "Triad of Reliability" for scientific Python code.

## How to measure success?
Success for DepDigest means a user can `import molsysmt` in under 1 second, regardless of whether they have 0 or 20 optional libraries installed.
