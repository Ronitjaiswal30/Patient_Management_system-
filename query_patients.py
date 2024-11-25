import mysql.connector

   # Establish connection to the database
connection = mysql.connector.connect(
       host='localhost',         # e.g., 'localhost'
       user='root',     # your MySQL username
       password='Harsh2004',  # your MySQL password
       database='healthcare'   # your database name
   )

try:
       cursor = connection.cursor()

       # Define the patient_id you want to query
       pk_1 = 1  # Replace with the actual patient ID you want to look for

       # Execute the SQL query
       cursor.execute("SELECT patients.patient_id AS patients_id, "
                      "patients.user_id AS patients_user_id, "
                      "patients.date_of_birth AS patients_dob "
                      "FROM patients "
                      "WHERE patients.patient_id = %s", (pk_1,))

       # Fetch results
       results = cursor.fetchall()
       for row in results:
           print(row)

except mysql.connector.Error as err:
       print(f"Error: {err}")

finally:
       # Clean up
       cursor.close()
       connection.close()
   
