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
            print("CheckEnoughSpace called")
            remaining_places = 50
            slot_nb = tracker.get_slot("slot_nb")
            slot_date = datetime.strptime(tracker.get_slot("slot_date"), "%d/%m/%Y").strftime('%Y-%m-%d')
            
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
            print("CreateBooking called")
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
        return []
    
class CheckCodeResa(Action):
    def name(self) -> Text:
        return "action_check_code_resa"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[SlotSet]:
        try:
            print("CheckCodeResa called")
            slot_code_resa = tracker.get_slot("slot_code_resa")
            slot_type = tracker.get_slot("infoResa")
            
            connection = psycopg2.connect(
                dbname="boh8g92em20wuq1uhc3z",
                user="uvrnmeghftjfmobhpj2k",
                password="YdbB0WZR7g5kIbI32J53fKJ7JwcBLF",
                host="boh8g92em20wuq1uhc3z-postgresql.services.clever-cloud.com",
                port="50013"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM booking.booking WHERE id = %s;", (slot_code_resa,))
            rows = cursor.fetchall()

            if rows is not None:
                for row in rows:
                    if(slot_type == True):
                        dispatcher.utter_message(f"Réservation trouvée !")
                        dispatcher.utter_message(f"Voici les informations de votre réservation :")
                        dispatcher.utter_message(f" - Nom de la réservation : {row[1]}")
                        dispatcher.utter_message(f" - Date de la réservation : {row[5]}")
                        dispatcher.utter_message(f" - Nombre de personne : {row[2]}")
                        dispatcher.utter_message(f" - Numéro de téléphone : {row[4]}")
                        dispatcher.utter_message(f" - Commentaire : {row[3]}")
                        dispatcher.utter_message(f"Voulez vous modifiez le commentaire ?")
                        SlotSet("bookingExist", True)
                        return [SlotSet("bookingExist", True)]
                    else:
                        dispatcher.utter_message(f"Réservation trouvée !")
                        dispatcher.utter_message(f"Voulez vous annulez la réservation ?")
                        SlotSet("bookingExist", True)
                        return [SlotSet("bookingExist", True)]
                dispatcher.utter_message(f"Réservation non trouvée...")
                dispatcher.utter_message(f"Veuillez resaisir votre code de réservation.")
                SlotSet("bookingExist", False)
                return [SlotSet("bookingExist", False)]
            
        except psycopg2.Error as e:
            dispatcher.utter_message("Error connecting to the database: {}".format(e))
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
                
class UpdateBookingComment(Action):
    def name(self) -> Text:
        return "action_update_booking_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print("UpdateBookingComment called")
            slot_code_resa = tracker.get_slot("slot_code_resa")
            slot_comment = tracker.get_slot("slot_comment")
            
            connection = psycopg2.connect(
                dbname="boh8g92em20wuq1uhc3z",
                user="uvrnmeghftjfmobhpj2k",
                password="YdbB0WZR7g5kIbI32J53fKJ7JwcBLF",
                host="boh8g92em20wuq1uhc3z-postgresql.services.clever-cloud.com",
                port="50013"
            )
            cursor = connection.cursor()
            cursor.execute("UPDATE booking.booking SET message=%s WHERE id=%s", (slot_comment, slot_code_resa))
            connection.commit()
            
        except psycopg2.Error as e:
            dispatcher.utter_message("Error connecting to the database: {}".format(e))
            return []
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
                
        dispatcher.utter_message(f"Enregistré !")
        return []
    
class SetSlotInfo(Action):
    def name(self) -> Text:
        return "action_set_slot_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[SlotSet]:
        print("SetSlotInfo called")
        
        SlotSet("infoResa", True)
        return [SlotSet("infoResa", True)]

class SetSlotCancel(Action):
    def name(self) -> Text:
        return "action_set_slot_cancel"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[SlotSet]:
        print("SetSlotCancel called")
        
        SlotSet("infoResa", False)
        return [SlotSet("infoResa", False)]
           
class DeleteBooking(Action):
    def name(self) -> Text:
        return "action_delete_booking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print("action_delete_booking called")
            slot_code_resa = tracker.get_slot("slot_code_resa")
            
            connection = psycopg2.connect(
                dbname="boh8g92em20wuq1uhc3z",
                user="uvrnmeghftjfmobhpj2k",
                password="YdbB0WZR7g5kIbI32J53fKJ7JwcBLF",
                host="boh8g92em20wuq1uhc3z-postgresql.services.clever-cloud.com",
                port="50013"
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM booking.booking WHERE id=%s", (slot_code_resa))
            connection.commit()
            
        except psycopg2.Error as e:
            dispatcher.utter_message("Error connecting to the database: {}".format(e))
            return []
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
                
        dispatcher.utter_message(f"Enregistré !")
        return []