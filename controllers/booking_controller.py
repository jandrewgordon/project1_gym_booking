from datetime import date
from models.upcoming_session import UpcomingSession
from flask import Flask, render_template, redirect, request, Blueprint
from models.booking import Booking
from models.member import Member
import repositories.member_repository as member_repository
import repositories.session_repository as session_repository
import repositories.booking_repository as booking_repository
import repositories.upcoming_sessions_repository as upcoming_session_repository

bookings_blueprint = Blueprint("bookings", __name__)

# INDEX
@bookings_blueprint.route("/bookings")
def bookings():
    bookings = booking_repository.select_all()
    upcoming_sessions = upcoming_session_repository.select_all()
    return render_template("bookings/index.html", all_bookings = bookings, all_upcoming_sessions = upcoming_sessions)

# NEW
@bookings_blueprint.route("/bookings/new", methods=['GET'])
def get_new_booking():
    members = member_repository.select_all()
    sessions = session_repository.select_all()
    return render_template("bookings/new.html", members=members, sessions=sessions)

# CREATE
@bookings_blueprint.route("/bookings", methods=['POST'])
def create_new_booking():

    # Creating booking
    member_id = request.form['member_id']
    session_id = request.form['session_id']
    booking_date = request.form['booking_date']
    member = member_repository.select(member_id)
    session = session_repository.select(session_id)
    capacity = session.capacity
    new_booking = Booking(member, session, booking_date, capacity)
    booking_repository.save(new_booking)

    # # Creating upcoming_session
    upcoming_session = UpcomingSession(session.name, booking_date, session.capacity, member)
    upcoming_session_repository.save(upcoming_session)

    return redirect("/bookings")

#EDIT
#UPDATE

@bookings_blueprint.route("/bookings/<id>")
def show_booking(id):
    booked_members = []
    selected_booking = booking_repository.select(id)
    bookings = booking_repository.select_all()
    members = member_repository.select_all()
    # for single_booking in bookings:
    #     if single_booking.session.id == selected_booking.session.id:
    #         booked_member_id = single_booking.member.id
    #         for member in members:
    #             if member.id == booked_member_id and selected_booking.session.capacity != 0:
    #                 booked_member = member
    #                 booked_members.append(booked_member)
    #                 booking_repository.update_capacity(selected_booking)                 
    
    return render_template("bookings/show.html", booking = selected_booking, booked_members = booked_members, all_members = members)

# DELETE
@bookings_blueprint.route("/bookings/<id>/delete", methods=["POST"])
def delete_booking(id):
    booking_repository.delete(id)
    return redirect("/bookings")






    
