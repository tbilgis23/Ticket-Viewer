'''
Author: Tugay Bilgis
Purpose: A simple CLI ticket viewer.
'''

import os
import requests as req
import json
from tabulate import tabulate
from pyfiglet import Figlet
from datetime import datetime


def menu():
    '''
    Displays the menu and returns the user's input.
    @return: the user's option
    '''
    print("\n\tSelect view options:")
    print("\t * Press 1 to view all tickets")
    print("\t * Press 2 to view an individual ticket")
    print("\t * Type 'quit' to exit")
    view = input("\n")
    return view


def get_json():
    '''
    Gets the JSON data from the API.
    @return: the JSON data or error if API call fails
    '''
    subdomain = os.environ.get('SUBDOMAIN')
    url = f"https://{subdomain}.zendesk.com/api/v2/tickets"
    user_email = os.environ.get("USER_EMAIL")
    password = os.environ.get('PASSWORD')
    
    if user_email is None or password is None:
        print("Please set your email and password as environment variables")
        return "error"
    
    response = req.get(url, auth=(user_email, password))
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("ERROR: Couldn't authenticate you. Please try again with the correct credentials\n")
        return "error"
    else:
        print("API call failed, please try again.")
        return "error"


def view_all():
    '''
    Prints out all of the tickets gotten from the API.
    @return: "menu" or "quit" to specify the next action
    '''
    data = get_json()
    if data == "error":
        return "menu"
    
    tickets = []
    for ticket in data["tickets"]:
        ticket_date = datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%S%z").strftime("%d %b %Y, %I:%M%p")  # convert the time to the desirable format 
        tickets.append([ticket["id"], ticket["subject"], ticket["submitter_id"], ticket_date])
    tickets = sorted(tickets, key=lambda x: x[3])  # sort the array by the date
    
    print()
    print(tabulate(tickets[:25], headers=['Ticket ID', 'Subject', 'Opened by', "Created at"], tablefmt='fancy_grid'))
    print(f"25 out of {len(tickets)} tickets are being displayed.")
    
    curr_table = 25
    while curr_table < len(tickets): 
        more = input("\nPress Enter to see more tickets or type 'menu' to go back to menu " \
                        + "or 'quit' to quit the program.\n")
        
        while more != 'menu' and more != '' and more != "quit":
            more = input("\nInvalid input, please press Enter to see more tickets." \
                + " or type 'menu' to go back to menu\n")
        
        if more == "":
            curr_arr = tickets[curr_table:curr_table+25]
            print(tabulate(curr_arr,
                headers=['Ticket ID', 'Subject', 'Opened by', "Created at"], tablefmt='fancy_grid'))
            print(f"{curr_table+len(curr_arr)} out of {len(tickets)} tickets are being displayed.")
            curr_table += 25
        
        if more == 'menu':
            return "menu"
        
        if more == 'quit':
            return "quit"
    return "menu"

def view_ticket():
    '''
    Prints out the ticket with the specified ID.
    @return: "menu" to print out the menu after returning
    '''
    data = get_json()
    if data == "error":
        return "menu"
    ticket_id = input("\nEnter the ticket ID you would like to view: \n")
    
    while ticket_id.isdigit() == False:
        ticket_id = input("\nInvalid input, please retry with a valid ticket ID: \n")
        return "menu"

    for ticket in data["tickets"]:
        if ticket["id"] == int(ticket_id):
            ticket_date = datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%S%z").strftime("%d %b %Y, %I:%M%p")
            print(f"\nOpened by {ticket['submitter_id']} at {ticket_date}\n")
            print(f"Subject: \n{ticket['subject']}\n")
            print(f"Description: \n{ticket['description'].strip()}")
            return "menu"
    print("\nTicket ID not found. Please try again.")
    return "menu"

def main():
    f = Figlet(font='slant')
    print(f.renderText("Welcome to the ticket viewer"))
    user_input = input("Type 'menu' to view options or 'quit' to exit\n")
    
    while user_input != "quit" and user_input != "menu":
        user_input = input("Invalid input. Type 'menu' to view options or 'quit' to exit\n")

    while user_input == 'menu':
        menu_input = menu()
        if menu_input == '1':
            user_input = view_all()
        elif menu_input == '2':
            user_input = view_ticket()
        elif menu_input == 'quit':
            user_input = 'quit'
    print("Closing the ticket viewer... See you again!")
    

if __name__ == "__main__":
    main()
