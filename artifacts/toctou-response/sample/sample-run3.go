package store

import "database/sql"

// Demo store — two SQL shapes, one provably dead.

func Upsert(db *sql.DB, legacy bool) error {
	// static and reachable
	db.Exec("CREATE TABLE IF NOT EXISTS demo_log(id INTEGER, actor TEXT)")

	// provably dead branch: constant false
	if false {
		db.Exec("DELETE FROM demo_log")
	}

	if legacy {
		return nil
	}
	return nil
}
