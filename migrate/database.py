from database.connection import db

def migrate_database():
    create_students = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='students' AND xtype='U')
    BEGIN
        CREATE TABLE students (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1
        )
    END
    """

    create_teachers = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='teachers' AND xtype='U')
    BEGIN
        CREATE TABLE teachers (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            subject NVARCHAR(100) NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1
        )
    END
    """

    create_subjects = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='subjects' AND xtype='U')
    BEGIN
        CREATE TABLE subjects (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            credits INT NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1
        )
    END
    """

    create_notes = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='notes' AND xtype='U')
    BEGIN
        CREATE TABLE notes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            student_id INT NOT NULL FOREIGN KEY REFERENCES students(id),
            subject_id INT NOT NULL FOREIGN KEY REFERENCES subjects(id),
            grade INT NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1
        )
    END
    """

    for script in [create_students, create_teachers, create_subjects, create_notes]:
        db.execute_non_query(script)

    print("Migración completada ✅")

if __name__ == "__main__":
    migrate_database()
