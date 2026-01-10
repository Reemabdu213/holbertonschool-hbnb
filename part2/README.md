# HBnB Project – Part 2: Business Logic and API Implementation

## Overview

This part of the **HBnB Project** focuses on implementing the **Business Logic** and **Presentation** layers of the application based on the system design completed in Part 1. The goal is to transform the documented architecture into a working Flask-based RESTful API.

At this stage, the application provides core functionalities such as managing **Users**, **Places**, **Reviews**, and **Amenities**. Authentication and authorization mechanisms (JWT, role-based access control) are intentionally excluded and will be implemented in the next phase.

---

## Project Scope

This implementation focuses on building a **scalable foundation** for the HBnB application.
* Core entity models:

  * User
  * Place
  * Review
  * Amenity
* CRUD operations for all entities.
* API documentation using `flask-restx`.
* In-memory or simple data handling for development purposes.

---

## Architecture Overview

The application follows a layered architecture:

### Presentation Layer

* Implemented using **Flask** and **flask-restx**.
* Defines RESTful API endpoints.
* Handles HTTP requests and responses.
* Serializes data returned to the client.

### Business Logic Layer

* Contains core models and rules of the application.
* Manages relationships between entities.
* Validates and processes incoming data.
* Exposes functionality through a Facade interface.

---

## Design Pattern

### Facade Pattern

The Facade pattern is used to provide a **single entry point** for the Presentation layer to interact with the Business Logic layer. This reduces coupling and improves maintainability.

---

## API Functionality

The API supports the following operations:

* Create, retrieve, update, and list Users
* Create, retrieve, update, and list Places
* Create, retrieve, update, and list Reviews
* Create, retrieve, update, and list Amenities

Responses include **extended attributes** where applicable. For example, retrieving a Place returns owner details and related amenities.

---

## Technologies Used

* Python 3
* Flask
* flask-restx
* UUID
* datetime

---

## Conclusion

Part 2 of the HBnB Project establishes a solid and maintainable backend foundation. The implemented architecture and APIs are designed to be easily extended in Part 3, where authentication, authorization, and persistence will be introduced.

