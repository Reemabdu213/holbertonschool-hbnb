# HBnB Project — Comprehensive Technical Documentation

## 1. Introduction

### 1.1 Project Overview
HBnB is a booking and accommodation management application inspired by short-term rental platforms. It manages core entities such as **Users**, **Places**, **Reviews**, and **Amenities**.

### 1.2 Purpose of This Document
This document compiles the diagrams and explanatory notes produced in the previous tasks into a single technical reference. It serves as a blueprint for the HBnB project, guiding implementation phases and ensuring architectural consistency.

### 1.3 Scope
This document includes:
- High-Level Architecture (Package Diagram + rationale)
- Business Logic Layer (Detailed Class Diagram + explanations)
- API Interaction Flow (Sequence Diagrams + explanations)

---

## 2. High-Level Architecture

### 2.1 Layered Architecture
The HBnB application follows a **Three-Layer Architecture**:

1. **Presentation Layer (API)**
   - Exposes REST endpoints.
   - Handles HTTP requests/responses and validation at the boundary.
   - Delegates use-cases to the Facade.

2. **Business Logic Layer**
   - Contains core domain models and business rules.
   - Orchestrates workflows and validations.
   - Provides a Facade as a single entry point for the API.

3. **Persistence Layer**
   - Encapsulates data access and storage.
   - Exposes repositories/DAOs for CRUD operations.
   - Business logic interacts with persistence only via repositories.

### 2.2 Design Decision: Facade Pattern
The **Facade Pattern** is used to:
- Reduce coupling between the API and internal domain logic.
- Provide a single interface for application use-cases.
- Hide persistence/repository complexity from the Presentation layer.

### 2.3 High-Level Package Diagram (Mermaid)

```mermaid
flowchart TB

subgraph Presentation["Presentation Layer (API)"]
  API["REST API Endpoints"]
end

subgraph Business["Business Logic Layer"]
  Facade["Facade"]
  Services["Domain Services / Use-Cases"]
  Models["Domain Models (User, Place, Review, Amenity)"]
end

subgraph Persistence["Persistence Layer"]
  Repositories["Repositories / DAOs"]
  DB["Database"]
end

API --> Facade
Facade --> Services
Services --> Models
Services --> Repositories
Repositories --> DB

---

2.4 Diagram Notes

The only gateway from Presentation to Business is the Facade.

Database access happens only through Repositories/DAOs in the Persistence layer.

Services/Use-Cases coordinate workflows and enforce business rules

---

3. Business Logic Layer
3.1 Purpose

This class diagram describes:

Core entities (User, Place, Review, Amenity)

Key attributes (UUID4 + timestamps)

Core behaviors (methods)

Relationships and multiplicity (1.., 0.., many-to-many)

---

3.2 Detailed Class Diagram (Mermaid)
classDiagram
    class User {
        +UUID id
        +String email
        +String password_hash
        +String first_name
        +String last_name
        +DateTime created_at
        +DateTime updated_at
        +create_user()
        +update_user()
        +delete_user()
        +authenticate(password)
    }

    class Place {
        +UUID id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID owner_id
        +DateTime created_at
        +DateTime updated_at
        +create_place()
        +update_place()
        +delete_place()
        +add_amenity(amenity_id)
        +remove_amenity(amenity_id)
    }

    class Review {
        +UUID id
        +String text
        +Int rating
        +UUID place_id
        +UUID user_id
        +DateTime created_at
        +DateTime updated_at
        +create_review()
        +update_review()
        +delete_review()
        +validate_rating()
    }

    class Amenity {
        +UUID id
        +String name
        +String description
        +DateTime created_at
        +DateTime updated_at
        +create_amenity()
        +update_amenity()
        +delete_amenity()
    }

    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has

    Place "0..*" --> "0..*" Amenity : includes

---

3.3 Entity Explanations
3.3.1 User

Role: Represents registered users in the system.
Key Attributes: UUID4 id, timestamps, unique email, password_hash, name fields.
Key Methods: create/update/delete user, authenticate.

---

3.3.2 Place

Role: Represents a property/listing available on the platform.
Key Attributes: UUID4 id, timestamps, title, description, price, coordinates, owner reference.
Key Methods: create/update/delete place, add/remove amenities.

---

3.3.3 Review

Role: Represents user feedback for a specific place.
Key Attributes: UUID4 id, timestamps, text, rating, references to user and place.
Key Methods: create/update/delete review, validate rating (1–5).

---

3.3.4 Amenity

Role: Represents reusable features/services linked to places.
Key Attributes: UUID4 id, timestamps, name, description.
Key Methods: create/update/delete amenity.

---

3.4 Relationship Rationale

User → Place (1 to 0..*): a user can own zero or more places.

User → Review (1 to 0..*): a user can write zero or more reviews.

Place → Review (1 to 0..*): a place can have zero or more reviews.

Place ↔ Amenity (0.. to 0..)**: many-to-many association.

---

4. API Interaction Flow
4.1 Purpose

Sequence diagrams illustrate the request flow across layers:
Client → API → Facade → Business Logic → Repositories → Database, including validations and error paths

---

4.2 Create User — POST /users
sequenceDiagram
autonumber
actor Client
participant API as API Layer
participant Facade as Facade
participant UserLogic as User Service/Logic
participant UserRepo as User Repository
participant DB as Database

Client->>API: POST /users (email, password, first_name, last_name)
API->>Facade: create_user(payload)
Facade->>UserLogic: validate payload
UserLogic->>UserRepo: is_email_unique(email)
UserRepo->>DB: SELECT user WHERE email=email
DB-->>UserRepo: result

alt Email exists
  UserLogic-->>Facade: error "Email already exists"
  Facade-->>API: 409 Conflict
  API-->>Client: 409 Conflict
else Success
  UserLogic-->>UserLogic: hash password + set UUID4 + timestamps
  UserLogic->>UserRepo: save(user)
  UserRepo->>DB: INSERT user
  DB-->>UserRepo: inserted
  UserRepo-->>Facade: created user
  Facade-->>API: 201 Created + user
  API-->>Client: 201 Created
end

---

4.3 Create Place — POST /places
sequenceDiagram
autonumber
actor Client
participant API as API Layer
participant Facade as Facade
participant PlaceLogic as Place Service/Logic
participant UserRepo as User Repository
participant PlaceRepo as Place Repository
participant DB as Database

Client->>API: POST /places (title, price, lat, lon, owner_id, ...)
API->>Facade: create_place(payload)
Facade->>PlaceLogic: validate fields (price, coordinates, required)
PlaceLogic->>UserRepo: find(owner_id)
UserRepo->>DB: SELECT user WHERE id=owner_id
DB-->>UserRepo: result

alt Owner not found
  PlaceLogic-->>Facade: error "Owner not found"
  Facade-->>API: 404 Not Found
  API-->>Client: 404 Not Found
else Success
  PlaceLogic-->>PlaceLogic: set UUID4 + timestamps
  PlaceLogic->>PlaceRepo: save(place)
  PlaceRepo->>DB: INSERT place
  DB-->>PlaceRepo: inserted
  PlaceRepo-->>Facade: created place
  Facade-->>API: 201 Created + place
  API-->>Client: 201 Created
end

---

4.4 Add Review — POST /places/{place_id}/reviews
sequenceDiagram
autonumber
actor Client
participant API as API Layer
participant Facade as Facade
participant ReviewLogic as Review Service/Logic
participant PlaceRepo as Place Repository
participant UserRepo as User Repository
participant ReviewRepo as Review Repository
participant DB as Database

Client->>API: POST /places/{place_id}/reviews (user_id, rating, text)
API->>Facade: add_review(place_id, payload)
Facade->>ReviewLogic: validate rating/text (rating 1..5)

ReviewLogic->>PlaceRepo: find(place_id)
PlaceRepo->>DB: SELECT place WHERE id=place_id
DB-->>PlaceRepo: result

ReviewLogic->>UserRepo: find(user_id)
UserRepo->>DB: SELECT user WHERE id=user_id
DB-->>UserRepo: result

alt Place not found
  ReviewLogic-->>Facade: error "Place not found"
  Facade-->>API: 404 Not Found
  API-->>Client: 404 Not Found
else User not found
  ReviewLogic-->>Facade: error "User not found"
  Facade-->>API: 404 Not Found
  API-->>Client: 404 Not Found
else Success
  ReviewLogic-->>ReviewLogic: set UUID4 + timestamps
  ReviewLogic->>ReviewRepo: save(review)
  ReviewRepo->>DB: INSERT review
  DB-->>ReviewRepo: inserted
  ReviewRepo-->>Facade: created review
  Facade-->>API: 201 Created + review
  API-->>Client: 201 Created
end

---

4.5 Add Amenity to Place — POST /places/{place_id}/amenities/{amenity_id}
sequenceDiagram
autonumber
actor Client
participant API as API Layer
participant Facade as Facade
participant PlaceLogic as Place Service/Logic
participant PlaceRepo as Place Repository
participant AmenityRepo as Amenity Repository
participant LinkRepo as PlaceAmenity Repository
participant DB as Database

Client->>API: POST /places/{place_id}/amenities/{amenity_id}
API->>Facade: add_amenity_to_place(place_id, amenity_id)
Facade->>PlaceLogic: attach amenity

PlaceLogic->>PlaceRepo: find(place_id)
PlaceRepo->>DB: SELECT place WHERE id=place_id
DB-->>PlaceRepo: result

PlaceLogic->>AmenityRepo: find(amenity_id)
AmenityRepo->>DB: SELECT amenity WHERE id=amenity_id
DB-->>AmenityRepo: result

alt Place not found
  PlaceLogic-->>Facade: error "Place not found"
  Facade-->>API: 404 Not Found
  API-->>Client: 404 Not Found
else Amenity not found
  PlaceLogic-->>Facade: error "Amenity not found"
  Facade-->>API: 404 Not Found
  API-->>Client: 404 Not Found
else Success
  PlaceLogic->>LinkRepo: create_link(place_id, amenity_id)
  LinkRepo->>DB: INSERT place_amenity(place_id, amenity_id)
  DB-->>LinkRepo: inserted
  Facade-->>API: 204 No Content
  API-->>Client: 204 No Content
end

---

5. Conclusion

This document consolidates the HBnB system design into a single reference, including:

High-level architecture and design rationale (Facade + layering)

Business logic entities and relationships

API interaction flows across layers
