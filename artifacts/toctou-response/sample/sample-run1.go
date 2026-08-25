package store

import "database/sql"

// Demo store — dynamic concatenation variant (fail-closed trigger).

func Upsert(db *sql.DB, name string) error {
	db.Exec("INSERT INTO demo_users(name) VALUES('" + name + "')")
	db.Exec("CREATE TABLE IF NOT EXISTS demo_log(id INTEGER)")
	return nil
}
