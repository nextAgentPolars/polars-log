package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"strings"
)

// detect walks a Go file and emits receipts for database calls.
// Deliberately minimal: constant-arg Exec/Query calls get exact receipts,
// dynamic args get UNKNOWN (prefer unknown over false precision), and
// statements inside `if false { ... }` are marked provably dead.

type detNode struct {
	fset     *token.FileSet
	deadFrom map[token.Pos]bool // positions inside constant-false branches
}

func (d *detNode) isDead(pos token.Pos) bool { return d.deadFrom[pos] }

func markDead(n *detNode, ifstmt *ast.IfStmt) {
	if ident, ok := ifstmt.Cond.(*ast.Ident); ok && ident.Name == "false" {
		for pos := ifstmt.Body.Pos(); pos < ifstmt.Body.End(); pos++ {
			n.deadFrom[pos] = true
		}
	}
}

func detectFile(fset *token.FileSet, path string, srcSHA string) ([]Receipt, error) {
	f, err := parser.ParseFile(fset, path, nil, 0)
	if err != nil {
		return nil, err
	}
	n := &detNode{fset: fset, deadFrom: map[token.Pos]bool{}}
	ast.Inspect(f, func(node ast.Node) bool {
		if iff, ok := node.(*ast.IfStmt); ok {
			markDead(n, iff)
		}
		return true
	})
	var receipts []Receipt
	rel := path
	if i := strings.LastIndex(rel, "/"); i >= 0 {
		rel = rel[i+1:]
	}
	ast.Inspect(f, func(node ast.Node) bool {
		call, ok := node.(*ast.CallExpr)
		if !ok {
			return true
		}
		sel, ok := call.Fun.(*ast.SelectorExpr)
		if !ok || (sel.Sel.Name != "Exec" && sel.Sel.Name != "Query") {
			return true
		}
		method := sel.Sel.Name
		pos := fset.Position(call.Pos())
		r := Receipt{
			ID:           fmt.Sprintf("%s:%d:%d:%s", rel, pos.Line, pos.Column, method),
			File:         rel,
			Line:         pos.Line,
			Col:          pos.Column,
			Method:       method,
			SourceSHA256: srcSHA,
		}
		if n.isDead(call.Pos()) {
			r.Dead = true
			r.Reason = "provably unreachable: inside constant-false branch"
		}
		if len(call.Args) == 0 {
			r.Op, r.Reason = "UNKNOWN", "no arguments"
			return true
		}
		if lit, ok := call.Args[0].(*ast.BasicLit); ok && lit.Kind == token.STRING {
			sql := strings.Trim(lit.Value, "`\"")
			r.SQL = sql
			r.Complete = true
			switch {
			case strings.HasPrefix(sql, "CREATE"):
				r.Op = "DDL"
			case strings.HasPrefix(strings.ToUpper(sql), "INSERT"):
				r.Op = "INSERT"
			case strings.HasPrefix(strings.ToUpper(sql), "DELETE"):
				r.Op = "DELETE"
			case strings.HasPrefix(strings.ToUpper(sql), "UPDATE"):
				r.Op = "UPDATE"
			case strings.HasPrefix(strings.ToUpper(sql), "SELECT"):
				r.Op = "SELECT"
			default:
				r.Op = "UNKNOWN"
			}
		} else {
			r.Op = "UNKNOWN"
			r.Reason = "dynamic argument — precision refused, prefer unknown over guess"
		}
		receipts = append(receipts, r)
		return true
	})
	return receipts, nil
}
