from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import psycopg2
from datetime import datetime

class CheckEnoughSpace(Action):
    def name(self) -> Text:
        return "action_check_enough_space"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[SlotSet]:
        try:
            remaining_places = 50
            slot_nb = tracker.get_slot("slot_nb")
            slot_date = datetime.strptime(tracker.get_slot("slot_date"), "%d/%m/%Y").strftime('%Y-%m-%d')
            
            print(slot_nb)
            print(slot_date)
            print("============")
            
            connection = psycopg2.connect(
                dbname="boh8g92em20wuq1uhc3z",
                user="uvrnmeghftjfmobhpj2k",
                password="YdbB0WZR7g5kIbI32J53fKJ7JwcBLF",
                host="boh8g92em20wuq1uhc3z-postgresql.services.clever-cloud.com",
                port="50013"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT SUM(nb_people) AS total_nb_people FROM booking.booking WHERE date = %s;", (slot_date,))
            total_nb_people = cursor.fetchone()[0]

            if total_nb_people is not None:
                remaining_places = remaining_places - total_nb_people
            if((remaining_places - int(slot_nb)) < 0):
                dispatcher.utter_message(f"Il y a seulement {remaining_places} disponibles, voulez vous saissir une nouvelle date ?")
                SlotSet("available", False)
                return [SlotSet("available", False)]
            
            dispatcher.utter_message(f"Il y assez de place disponibles, voulez vous confirmer ?")
            SlotSet("available", True)
            return [SlotSet("available", True)]
                
        except psycopg2.Error as e:
            dispatcher.utter_message("Error connecting to the database: {}".format(e))
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
        SlotSet("story_number", False)
        return [SlotSet("story_number", False)]

class CreateBooking(Action):
    def name(self) -> Text:
        return "action_create_booking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            slot_nb = tracker.get_slot("slot_nb")
            slot_date = datetime.strptime(tracker.get_slot("slot_date"), "%d/%m/%Y").strftime('%Y-%m-%d')
            slot_name = tracker.get_slot("slot_name")
            slot_n_phone = tracker.get_slot("slot_n_phone")
            
            connection = psycopg2.connect(
                dbname="boh8g92em20wuq1uhc3z",
                user="uvrnmeghftjfmobhpj2k",
                password="YdbB0WZR7g5kIbI32J53fKJ7JwcBLF",
                host="boh8g92em20wuq1uhc3z-postgresql.services.clever-cloud.com",
                port="50013"
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO booking.booking (c_name, nb_people, phone, date) VALUES (%s, %s, %s, %s) RETURNING ID;", (slot_name, slot_nb, slot_n_phone, slot_date))
            connection.commit()
            bookingId = cursor.fetchone()[0]
            
        except psycopg2.Error as e:
            dispatcher.utter_message("Error connecting to the database: {}".format(e))
            return []
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
                
        dispatcher.utter_message(f"Votre code de réservation est le suivant : {bookingId}")  
        dispatcher.utter_message(f"Voulez-vous ajouter un commentaire à la réservation ?")
        return []