# 6. AI Journal — Doctor Appointment Booking System

## Project decisions

- **Maximum upcoming appointments:** N = 3, matching `1_requirements.md`, `4_class_diagram.md`, and `5_sequence_diagram.md`.
- **Implementation:** One Python command-line demonstration in `main.py`, using the classes represented in the class diagram.
- **Docker:** Not required for this team because the team has 2–4 students.
- **Scope:** R1–R4 are implemented in the demonstration. As stated in the requirements document, R5–R7 are addressed as design/documentation considerations rather than fully implemented and tested features.

## AI-assisted work and checks

### Check 1 — Requirements classification

- **What was checked:** R1–R4 are functional requirements; R5–R7 are non-functional requirements. The value of N is 3.
- **Result:** The uploaded `1_requirements.md` uses this classification and records N = 3.
- **Issue found:** None confirmed during this check.

### Check 2 — Use cases and diagrams

- **What was checked:** The Patient can view availability and request a booking; the Doctor can review, accept, or decline a pending request. The alternative paths include reaching the appointment limit and selecting a slot that is no longer available.
- **Result:** These paths appear in the uploaded use-case and sequence-diagram files.
- **Review note:** The team should render the Mermaid diagrams on GitHub and verify that the final code and diagrams remain consistent after any edits.

### Check 3 — Candidate classes

- **What was checked:** The candidate-class analysis distinguishes explicit, inferred, and rejected classes.
- **Result:** The supplied analysis identifies Patient, Doctor, Appointment, TimeSlot, AppointmentStatus, Availability, MedicalRecord, and Notification, and rejects Admin and Payment for the current scope.
- **Action required:** Ensure the analysis is saved in the repository as `3_candidate_classes.md`.

### Check 4 — Python implementation

- **What was checked:** `main.py` was executed with `python main.py`. Its demonstration exercises viewing available slots, booking a slot, rejecting a duplicate booking, accepting and declining requests, releasing a declined slot, and enforcing the N = 3 limit.
- **Result:** The program completed successfully during this check.
- **Limitations checked:** The command-line demo does not implement medical-record authorization, a mobile interface, or a measured two-second response-time guarantee. Those requirements must be discussed in the project documentation, as allowed by the supplied `1_requirements.md`.

## AI mistakes and corrections

No confirmed AI mistake has been established in the checks recorded above, so none is invented here. Each team member must add any actual AI mistake they discover while reviewing or testing the work, including:

1. What the AI said or generated.
2. Why it was incorrect or inconsistent with the requirements/diagrams.
3. How the team noticed it.
4. What correction was made.

If the team discovers no AI mistakes, state that honestly rather than manufacturing one.

## Team verification still required

- [ ] Run `python main.py` on a team member's machine or GitHub Codespaces.
- [ ] Check the booking-limit rule with future Pending and Accepted appointments.
- [ ] Confirm that Declined, Cancelled, and past appointments do not count toward N.
- [ ] Confirm that a slot cannot be booked twice.
- [ ] Confirm a doctor cannot accept or decline a non-pending request.
- [ ] Render all Mermaid diagrams on GitHub.
- [ ] Update this journal with the team's real findings and any corrections.
- [ ] Confirm the required GitHub Actions check is green.

## Output of `python main.py`

```text
DOCTOR APPOINTMENT BOOKING SYSTEM
Maximum upcoming appointments per patient: N = 3

Available slots for Dr. Sara Hassan (General Practice):
  Slot 1: 2026-10-30 15:30 - 16:00
  Slot 2: 2026-10-31 15:30 - 16:00
  Slot 3: 2026-11-01 15:30 - 16:00
  Slot 4: 2026-11-02 15:30 - 16:00
  Slot 5: 2026-11-03 15:30 - 16:00

[Scenario 1] Patient books a free slot
Booking request created successfully. Status: Pending.
  Appointment #1: Ahmed Ali with Dr. Sara Hassan on 2026-10-30 15:30 [Pending]
Doctor accepts appointment: Success; status = Accepted

[Scenario 2] Another patient tries to book the same slot
Booking rejected: this time slot is no longer available.

[Scenario 3] Doctor declines a pending request; the slot is released
Booking request created successfully. Status: Pending.
  Appointment #2: Ahmed Ali with Dr. Sara Hassan on 2026-10-31 15:30 [Pending]
Doctor declines appointment: Success; status = Declined
Slot 2 available again: True

[Scenario 4] Patient reaches the N = 3 limit
Booking request created successfully. Status: Pending.
  Appointment #3: Ahmed Ali with Dr. Sara Hassan on 2026-10-31 15:30 [Pending]
Booking request created successfully. Status: Pending.
  Appointment #4: Ahmed Ali with Dr. Sara Hassan on 2026-11-01 15:30 [Pending]
Booking rejected: Ahmed Ali already has 3 upcoming appointments.
Current upcoming Pending/Accepted appointments: 3

Requirement notes:
- R1-R4 are demonstrated by this command-line program.
- R5 (medical-data authorization), R6 (2-second display target), and
  R7 (mobile-screen usability) are design/documentation considerations;
  this command-line demo does not implement a medical-record UI or mobile UI.
```
