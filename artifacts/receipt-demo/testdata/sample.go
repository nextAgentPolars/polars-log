package sample

import "database/sql"

// Sample file — three SQL shapes.

func Upsert(db *sql.DB, name string, legacy bool) error {
	// dynamic concatenation: precision refused
	db.Exec("INSERT INTO demo_users(name) VALUES('" + name + "')")

	// static and reachable
	db.Exec("CREATE TABLE IF NOT EXISTS demo_log(id INTEGER, actor TEXT)")

	// provably dead branch
	if false {
		db.Exec("DELETE FROM demo_log")
	}

	if legacy {
		return nil
	}
	return nil
}
