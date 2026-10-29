# 1. System Requirements — Doctor Appointment Booking System

## 1.1 Functional Requirements

| ID | Requirement |
|---|---|
| R1 | A patient can view the days and times when a doctor is available. |
| R2 | A patient can book an appointment during an available time slot. |
| R3 | A doctor can accept or decline an appointment request. |
| R4 | A patient can have at most N upcoming appointments at any given time. |

## 1.2 Non-Functional Requirements

| ID | Requirement |
|---|---|
| R5 | Patient medical data shall be accessible only to authorized staff. |
| R6 | Available appointment times shall be displayed within 2 seconds. |
| R7 | The application shall be usable on mobile phone screens. |

## 1.3 Appointment Limit

The selected value is **N = 3**.

A patient may have at most three upcoming appointments in Pending or Accepted status at any given time.

The following appointments do not count toward the limit:
- Declined appointments.
- Cancelled appointments.
- Past appointments.

## 1.4 Implementation Scope

- **R1:** Display doctors' available days and time slots.
- **R2:** Allow patients to book available time slots.
- **R3:** Allow doctors to accept or decline appointment requests.
- **R4:** Enforce the maximum of three upcoming Pending and Accepted appointments per patient.
- **R5:** Explain how access to medical data can be restricted to authorized staff.
- **R6:** Explain how available appointment times can be displayed within two seconds.
- **R7:** Explain how the interface can support mobile phone screens.

R1–R4 must be implemented as a working flow. R5–R7 must be addressed in the design or README; their implementation and testing are not required for this assignment.
