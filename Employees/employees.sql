CREATE TABLE IF NOT EXISTS Employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (name <> ''),
    department VARCHAR(100) NOT NULL,
    manager_id INTEGER REFERENCES Employees(employee_id) ON DELETE SET NULL CONSTRAINT check_not_self_manager CHECK (employee_id != manager_id)
);