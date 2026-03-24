# Project Conventions

## Naming

- Ticket IDs must use the `TKT-1001` pattern.
- Knowledge files must use `kebab-case`.
- Delivery artifacts must use literal, descriptive names.

## Directory intent

- `backend/` stores the FastAPI backend code.
- `knowledge/` stores the source files uploaded to the Dify knowledge base.
- `docs/` stores project documentation and delivery notes.
- `artifacts/` stores exported Studio assets and final delivery artifacts.
- `private/` stores internal reference material and is not versioned.

## Artifact names

- Studio exports should live under `artifacts/studio/`.
- The first Chatflow export should use a name such as `chatflow-v1`.
- Documentation files should use short, literal names.
