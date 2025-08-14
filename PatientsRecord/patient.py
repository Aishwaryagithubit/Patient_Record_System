from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt

# CONNECT TO MONGODB ATLAS
client = MongoClient("mongodb+srv://aishwaryasah25:CYySPKdYJBgmdoWQ@cluster0.sishdvs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["Medicaldb"]      # Database
patients = db["patients"]     # Collection


# FUNCTIONS

def add_patient():
    print("\n Add New Patient ")
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    gender = input("Enter gender (Male/Female/Other): ")
    contact = input("Enter contact number: ")
    address = input("Enter address: ")

    disease = input("Enter disease name: ")
    diagnosis_date = input("Enter diagnosis date (YYYY-MM-DD): ")
    treatment = input("Enter treatment: ")
    doctor = input("Enter doctor's name: ")

    patient = {
        "name": name,
        "age": age,
        "gender": gender,
        "contact": contact,
        "address": address,
        "medicalHistory": [
            {
                "disease": disease,
                "diagnosisDate": diagnosis_date,
                "treatment": treatment,
                "doctor": doctor
            }
        ],
        "createdAt": datetime.now()
    }

    patients.insert_one(patient)
    print("\nPatient record added successfully.\n")


def view_all_patients():
    print("\n All Patients Records \n")
    for patient in patients.find():
        print(f"Name: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}")
    print()



def search_by_disease():
    print("\n Search Patients by Disease ")
    disease = input("Enter disease name to search: ")
    print(f"\nPatients with {disease}:\n")
    for patient in patients.find({"medicalHistory.disease": disease}):
        print(f"Name: {patient['name']}, Contact: {patient['contact']}")
    print()


def update_treatment():
    print("\n  Update Treatment ")
    name = input("Enter patient name to update treatment: ")
    disease = input("Enter disease: ")
    new_treatment = input("Enter new treatment: ")

    result = patients.update_one(
        {"name": name, "medicalHistory.disease": disease},
        {"$set": {"medicalHistory.$.treatment": new_treatment}}
    )

    if result.modified_count > 0:
        print("\nTreatment updated successfully.\n")
    else:
        print("\nNo matching record found.\n")


def delete_patient():
    print("\n Delete Patient ")
    name = input("Enter patient name to delete: ")
    result = patients.delete_one({"name": name})

    if result.deleted_count > 0:
        print("\nPatient deleted successfully.\n")
    else:
        print("\nNo matching record found.\n")

def gender_bargraph():
    # Count genders
    male_count = patients.count_documents({"gender": "Male"})
    female_count = patients.count_documents({"gender": "Female"})
    other_count = patients.count_documents({"gender": "Other"})

    genders = ["Male", "Female", "Other"]
    counts = [male_count, female_count, other_count]

    # Plot bar graph
    plt.bar(genders, counts, color=['blue', 'pink', 'green'])
    plt.title("Patient Count by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Number of Patients")
    plt.show()

def age_distribution():
    # Fetch all patient ages
    ages = [patient['age'] for patient in patients.find()]

    if not ages:
        print("No patient records found.")
        return

    #(0-10, 11-20, 21-30, ...)
    bins = list(range(0, 101, 10))  
    # Plot histogram
    plt.hist(ages, bins=bins, edgecolor='black', color='skyblue')
    plt.title("Patient Age Distribution")
    plt.xlabel("Age Groups")
    plt.ylabel("Number of Patients")
    plt.xticks(bins)
    plt.show()


# MAIN MENU
while True:
    print("\n Welcome to Patient Record System ")
    print("1. Add New Patient")
    print("2. View All Patients")
    print("3. Search Patients by Disease")
    print("4. Update Treatment")
    print("5. Delete Patient")
    print("6. Gender Bar Graph")
    print("7. Age Distribution Histogram")
    print("8. Exit")

    choice = input("Enter choice (1-6): ")

    if choice == "1":
        add_patient()
    elif choice == "2":
        view_all_patients()
    elif choice == "3":
        search_by_disease()
    elif choice == "4":
        update_treatment()
    elif choice == "5":
        delete_patient()
    elif choice == "6":
        gender_bargraph()
    elif choice == "7":
        age_distribution()

    elif choice == "8":
        print("Exit")
        break
    else:
        print("Invalid choice!! Please try again.")




   
