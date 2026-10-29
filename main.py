"""Simple Doctor Appointment Booking System.

Run with:
    python main.py

Scope:
- Implements R1-R4 in a small command-line demonstration.
- R5-R7 are addressed as design considerations in the project documentation,
  as allowed by the supplied assignment requirements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional


MAX_UPCOMING_APPOINTMENTS = 3  # N = 3, as documented in 1_requirements.md


class AppointmentStatus(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    CANCELLED = "Cancelled"


@dataclass
class TimeSlot:
    slot_id: int
    start_datetime: datetime
    end_datetime: datetime
    is_booked: bool = False

    def check_availability(self) -> bool:
        return not self.is_booked and self.start_datetime > datetime.now()

    def reserve(self) -> bool:
        """Reserve this slot if it is still available."""
        if not self.check_availability():
            return False
        self.is_booked = True
        return True

    def release(self) -> None:
        self.is_booked = False


@dataclass
class Availability:
    day: str
    start_time: str
    end_time: str
    time_slots: List[TimeSlot] = field(default_factory=list)

    def is_available(self) -> bool:
        return any(slot.check_availability() for slot in self.time_slots)


@dataclass
class Doctor:
    doctor_id: int
    name: str
    specialization: str
    availability: List[Availability] = field(default_factory=list)

    def view_appointment_requests(self, appointments: List["Appointment"]) -> List["Appointment"]:
        return [
            appointment for appointment in appointments
            if appointment.doctor is self
            and appointment.status == AppointmentStatus.PENDING
        ]

    def accept_appointment(self, appointment: "Appointment") -> bool:
        if appointment.doctor is not self or appointment.status != AppointmentStatus.PENDING:
            return False
        appointment.status = AppointmentStatus.ACCEPTED
        return True

    def decline_appointment(self, appointment: "Appointment") -> bool:
        if appointment.doctor is not self or appointment.status != AppointmentStatus.PENDING:
            return False
        appointment.status = AppointmentStatus.DECLINED
        appointment.time_slot.release()
        return True


@dataclass
class Patient:
    patient_id: int
    name: str
    email: str

    def count_upcoming_appointments(
        self, appointments: List["Appointment"], now: Optional[datetime] = None
    ) -> int:
        now = now or datetime.now()
        counted_statuses = {AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED}
        return sum(
            1 for appointment in appointments
            if appointment.patient is self
            and appointment.appointment_datetime > now
            and appointment.status in counted_statuses
        )

    def book_appointment(
        self,
        doctor: Doctor,
        time_slot: TimeSlot,
        appointments: List["Appointment"],
        next_appointment_id: int,
    ) -> tuple[Optional["Appointment"], str]:
        """Request a booking, enforcing the appointment limit and unique slot."""
        if self.count_upcoming_appointments(appointments) >= MAX_UPCOMING_APPOINTMENTS:
            return None, f"Booking rejected: {self.name} already has {MAX_UPCOMING_APPOINTMENTS} upcoming appointments."

        if not time_slot.check_availability():
            return None, "Booking rejected: this time slot is no longer available."

        if not time_slot.reserve():
            return None, "Booking rejected: this time slot is no longer available."

        appointment = Appointment(
            appointment_id=next_appointment_id,
            patient=self,
            doctor=doctor,
            time_slot=time_slot,
            appointment_datetime=time_slot.start_datetime,
            status=AppointmentStatus.PENDING,
        )
        appointments.append(appointment)
        return appointment, "Booking request created successfully. Status: Pending."


@dataclass
class Appointment:
    appointment_id: int
    patient: Patient
    doctor: Doctor
    time_slot: TimeSlot
    appointment_datetime: datetime
    status: AppointmentStatus = AppointmentStatus.PENDING

    def cancel(self) -> bool:
        if self.status not in {AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED}:
            return False
        self.status = AppointmentStatus.CANCELLED
        self.time_slot.release()
        return True


def show_available_slots(doctor: Doctor) -> None:
    """Display future, unbooked slots for a doctor (R1)."""
    print(f"\nAvailable slots for Dr. {doctor.name} ({doctor.specialization}):")
    found = False
    for availability in doctor.availability:
        for slot in availability.time_slots:
            if slot.check_availability():
                found = True
                print(
                    f"  Slot {slot.slot_id}: "
                    f"{slot.start_datetime.strftime('%Y-%m-%d %H:%M')} - "
                    f"{slot.end_datetime.strftime('%H:%M')}"
                )
    if not found:
        print("  No available slots.")


def print_booking_result(appointment: Optional[Appointment], message: str) -> None:
    print(message)
    if appointment is not None:
        print(
            f"  Appointment #{appointment.appointment_id}: "
            f"{appointment.patient.name} with Dr. {appointment.doctor.name} "
            f"on {appointment.appointment_datetime.strftime('%Y-%m-%d %H:%M')} "
            f"[{appointment.status.value}]"
        )


def run_demo() -> None:
    """Run a repeatable workflow that demonstrates the main requirements."""
    now = datetime.now().replace(second=0, microsecond=0)
    start_times = [
        now + timedelta(days=1),
        now + timedelta(days=2),
        now + timedelta(days=3),
        now + timedelta(days=4),
        now + timedelta(days=5),
    ]
    slots = [
        TimeSlot(
            slot_id=index + 1,
            start_datetime=start,
            end_datetime=start + timedelta(minutes=30),
        )
        for index, start in enumerate(start_times)
    ]
    availability = Availability(
        day="Upcoming days",
        start_time="09:00",
        end_time="17:00",
        time_slots=slots,
    )
    doctor = Doctor(
        doctor_id=1,
        name="Sara Hassan",
        specialization="General Practice",
        availability=[availability],
    )
    patient = Patient(patient_id=1, name="Ahmed Ali", email="ahmed@example.com")
    other_patient = Patient(patient_id=2, name="Mona Samir", email="mona@example.com")
    appointments: List[Appointment] = []

    print("DOCTOR APPOINTMENT BOOKING SYSTEM")
    print(f"Maximum upcoming appointments per patient: N = {MAX_UPCOMING_APPOINTMENTS}")
    show_available_slots(doctor)

    print("\n[Scenario 1] Patient books a free slot")
    appointment, message = patient.book_appointment(doctor, slots[0], appointments, 1)
    print_booking_result(appointment, message)

    if appointment is not None:
        accepted = doctor.accept_appointment(appointment)
        print(f"Doctor accepts appointment: {'Success' if accepted else 'Rejected'}; status = {appointment.status.value}")

    print("\n[Scenario 2] Another patient tries to book the same slot")
    duplicate, message = other_patient.book_appointment(doctor, slots[0], appointments, 2)
    print_booking_result(duplicate, message)

    print("\n[Scenario 3] Doctor declines a pending request; the slot is released")
    declined_request, message = patient.book_appointment(doctor, slots[1], appointments, 2)
    print_booking_result(declined_request, message)
    if declined_request is not None:
        declined = doctor.decline_appointment(declined_request)
        print(f"Doctor declines appointment: {'Success' if declined else 'Rejected'}; status = {declined_request.status.value}")
        print(f"Slot {slots[1].slot_id} available again: {slots[1].check_availability()}")

    print("\n[Scenario 4] Patient reaches the N = 3 limit")
    second, message = patient.book_appointment(doctor, slots[1], appointments, 3)
    print_booking_result(second, message)
    if second is not None:
        doctor.accept_appointment(second)
    third, message = patient.book_appointment(doctor, slots[2], appointments, 4)
    print_booking_result(third, message)
    if third is not None:
        doctor.accept_appointment(third)

    fourth, message = patient.book_appointment(doctor, slots[3], appointments, 5)
    print_booking_result(fourth, message)
    print(
        "Current upcoming Pending/Accepted appointments:",
        patient.count_upcoming_appointments(appointments),
    )

    print("\nRequirement notes:")
    print("- R1-R4 are demonstrated by this command-line program.")
    print("- R5 (medical-data authorization), R6 (2-second display target), and")
    print("  R7 (mobile-screen usability) are design/documentation considerations;")
    print("  this command-line demo does not implement a medical-record UI or mobile UI.")


if __name__ == "__main__":
    run_demo()
