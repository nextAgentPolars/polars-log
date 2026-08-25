package main

import (
	"crypto/sha256"
	"encoding/hex"
)

// Receipt is the atomic claim: "at scan time, this source position contained
// this SQL, and here is the proof digest." Receipts are immutable — a changed
// world produces a new receipt, never an updated one.

type Receipt struct {
	ID           string `json:"id"`            // file:line:col:method
	File         string `json:"file"`
	Line         int    `json:"line"`
	Col          int    `json:"col"`
	Method       string `json:"method"`        // Exec / Query
	Op           string `json:"op"`            // DDL / INSERT / SELECT / UNKNOWN…
	SQL          string `json:"sql,omitempty"` // exact constant text, empty when UNKNOWN
	Complete     bool   `json:"complete"`
	Reason       string `json:"reason,omitempty"` // why UNKNOWN / why dead
	Dead         bool   `json:"dead,omitempty"`   // provably unreachable
	SourceSHA256 string `json:"source_sha256"`    // digest of the file at scan time
}

func (r Receipt) SHA() string {
	h := sha256.Sum256([]byte(r.ID + "|" + r.SQL + "|" + r.Op + "|" + r.SourceSHA256))
	return hex.EncodeToString(h[:])
}
