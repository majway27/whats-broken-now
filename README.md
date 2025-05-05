# WBN - "What's Broken Now ?!!" (game)

## Design Goals

### Functional

- Highly entwined Generative AI via LLM
- Highly oriented to AI agent architecture
- Who-what-when-where-why dynamic, JIT templating of prompts, rather than library of static, pre considered ones.

### Technology

- Highly portable.  
  - Little to no external components (ie standalone db server).  
  - Exception - BYO LLM flexiblity (ex as a player I want to plumb in openAI w/ API key vs stock LLM py lib)

## Modules

### Main

- Runtime
- Start

### Menu

- Py Rich
- UI
- Interactive
- Views

### Hardware

- Ficticious game content

### Tickets

- Player Tasks

### Mailbox

- Overly, this is a functional surface for notifications.
    - Enables async chat with game NPCs (non customer / ticket submitters)

### HR

- Employee handbook
    - Employee handbook is the rules list that AI NPCs are supposed to follow.

## Data Architecture

### Models vs Utils

- The models.py should focus on data structures, while utils.py is better for business logic (ie setup and validation).

### Models vs Repositories

- Separation of Concerns
  - models.py contains the data structures (like the Player class) that represent your domain objects
  - repository.py handles all database interactions and data persistence
- This separation makes the code more maintainable and easier to test
- Single Responsibility Principle
  - The Player class in models.py is a simple data container with basic validation
  - The PlayerRepository class handles all database operations (CRUD)
  - This makes each class focused on one specific task
- Dependency Management
  - The Player model doesn't need to know about database connections or SQL
  - The repository layer abstracts away all database-specific code
  - This makes it easier to change the database implementation if needed
- Testing
  - You can test the Player model without needing a database
  - You can mock the repository layer when testing business logic
  - This separation makes unit testing much easier
- Code Organization
  - All database-related code is in one place (repository)
  - All domain models are in another place (models)
  - This makes the codebase more organized and easier to navigate

## ?Next?

- ?TODO?
