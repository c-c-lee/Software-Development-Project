import sqlite3

db_path = "/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/instance/ArchGenome.db"
data_file = "/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/instance/admixture_data.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    with open(data_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line_number, line in enumerate(file, 1):
            try:
                id, population_code, superpopulation, ancestry1, ancestry2, ancestry3 = line.strip().split('|')
            except ValueError as e:
                print(f"Line {line_number} is malformed: {e}")
                continue

            query = '''INSERT OR IGNORE INTO admixture_k3 (id, population_code, superpopulation, Ancestry1, Ancestry2, Ancestry3)
                       VALUES (?, ?, ?, ?, ?, ?);'''
            data = (id, population_code, superpopulation, ancestry1, ancestry2, ancestry3)

            try:
                cursor.execute(query, data)
                print("Insertion successful.")
                print("Data to be inserted:", data)
            except sqlite3.IntegrityError as e:
                print(f"IntegrityError: {e}")
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")

    conn.commit()
    print("Data import completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()

