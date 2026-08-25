// receipt-demo — a ~250-line pattern demonstration: receipt + AST anchor +
// digest chain + staleness flip. This is NOT the product; the product is a
// 230k-line governance platform. Run the mechanism yourself in 60 seconds.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"go/token"
	"os"
	"path/filepath"
)

func fileSHA(path string) (string, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return "", err
	}
	h := sha256.Sum256(b)
	return hex.EncodeToString(h[:]), nil
}

func scan(dir string, appendToLedger bool) ([]Receipt, *Ledger, error) {
	l, err := LoadLedger(filepath.Join(dir, "ledger.json"))
	if err != nil {
		return nil, nil, err
	}
	var all []Receipt
	err = filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() || filepath.Ext(path) != ".go" {
			return err
		}
		sha, err := fileSHA(path)
		if err != nil {
			return err
		}
		fset := token.NewFileSet()
		rs, err := detectFile(fset, path, sha)
		if err != nil {
			return err
		}
		all = append(all, rs...)
		return nil
	})
	if err != nil {
		return nil, nil, err
	}
	if appendToLedger {
		for i := range all {
			l.Append(all[i].SHA())
		}
	}
	return all, l, nil
}

func main() {
	if len(os.Args) < 3 {
		fmt.Fprintln(os.Stderr, "usage: receipt-demo scan|verify <dir>")
		os.Exit(2)
	}
	cmd, dir := os.Args[1], os.Args[2]
	receipts, ledger, err := scan(dir, cmd == "scan")
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
	switch cmd {
	case "scan":
		for _, r := range receipts {
			tag := ""
			if r.Dead {
				tag = "  [DEAD: " + r.Reason + "]"
			} else if r.Op == "UNKNOWN" {
				tag = "  [UNKNOWN: " + r.Reason + "]"
			}
			fmt.Printf("receipt %s  op=%-7s sql=%q%s\n", r.ID, r.Op, r.SQL, tag)
		}
		head := "genesis"
		if n := len(ledger.Entries); n > 0 {
			head = ledger.Entries[n-1].Head
		}
		fmt.Printf("\nledger: %d entries, head=%s...\n", len(ledger.Entries), head[:12])
		ledger.Save(filepath.Join(dir, "ledger.json"))
	case "verify":
		anchored := map[string]bool{}
		for _, e := range ledger.Entries {
			anchored[e.ReceiptSHA] = true
		}
		stale := 0
		for _, r := range receipts {
			if !anchored[r.SHA()] {
				stale++
				fmt.Printf("STALE  %s — current source digest %s... has no matching anchored claim\n",
					r.ID, r.SourceSHA256[:12])
			} else {
				fmt.Printf("VALID  %s\n", r.ID)
			}
		}
		if stale > 0 {
			fmt.Printf("\n%d claim(s) invalidated. The old world is gone; re-scan to re-anchor.\n", stale)
			os.Exit(1)
		}
		fmt.Println("\nall claims valid.")
	default:
		fmt.Fprintln(os.Stderr, "unknown command:", cmd)
		os.Exit(2)
	}
}
