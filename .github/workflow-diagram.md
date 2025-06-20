Developer (You or Collaborator)
    |
    └──> git checkout dev
              |
              └──> git pull origin dev
                      |
                      └──> git checkout -b feature/<short-description>
                                |
                                └──> Code locally (frontend/backend or both)
                                          |
                                          └──> git add . && git commit -m "describe change"
                                                    |
                                                    └──> git push -u origin feature/<short-description>
                                                              |
                                                              └──> Open Pull Request (PR) on GitHub:
                                                                          - Base: dev
                                                                          - Compare: feature/<short-description>
                                                                          |
                                                                          └──> PR runs GitHub Actions CI:
                                                                                  - Lint Flask with flake8
                                                                                  - Test Flask with pytest
                                                                                  - Lint React with ESLint
                                                                                  - Test React with npm test
                                                                                  |
                                                                                  ├──> ✅ All checks pass
                                                                                  │       └──> Code review by CODEOWNER or assigned reviewer
                                                                                  │               └──> Reviewer approves
                                                                                  │                       └──> PR is squash/rebase merged into dev
                                                                                  │
                                                                                  └──> ❌ Any check fails or review rejected
                                                                                          └──> Developer updates code and force-push changes
                                                                                                  └──> PR re-triggers checks and review
                                                                                                          └──> Repeats until approved and clean

Merged to `dev` branch
    |
    └──> dev accumulates integrated, tested features
            |
            └──> When stable, open PR: dev → main
                    - Triggers same review and CI process
                    - Only you (or designated lead) can approve `main` merges
                    - This PR = release candidate for production

Merged to `main` branch
    |
    └──> (Optional) Trigger deployment
            - Production build & deployment (e.g., via GitHub Actions, Vercel, Netlify, or VPS)

