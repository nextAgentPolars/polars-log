package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
)

// Ledger is an append-only hash chain. Each entry commits to the previous
// head, so any retroactive edit breaks every subsequent hash.

type Entry struct {
	Seq        int    `json:"seq"`
	ReceiptSHA string `json:"receipt_sha"`
	PrevHead   string `json:"prev_head"`
	Head       string `json:"head"`
}

type Ledger struct {
	Entries []Entry `json:"entries"`
}

func (l *Ledger) Append(receiptSHA string) Entry {
	prev := ""
	if len(l.Entries) > 0 {
		prev = l.Entries[len(l.Entries)-1].Head
	}
	h := sha256.Sum256([]byte(prev + "|" + receiptSHA))
	e := Entry{Seq: len(l.Entries) + 1, ReceiptSHA: receiptSHA, PrevHead: prev,
		Head: hex.EncodeToString(h[:])}
	l.Entries = append(l.Entries, e)
	return e
}

func LoadLedger(path string) (*Ledger, error) {
	l := &Ledger{}
	b, err := os.ReadFile(path)
	if err != nil {
		return l, nil // fresh ledger
	}
	err = json.Unmarshal(b, l)
	return l, err
}

func (l *Ledger) Save(path string) error {
	b, _ := json.MarshalIndent(l, "", "  ")
	return os.WriteFile(path, b, 0o644)
}
