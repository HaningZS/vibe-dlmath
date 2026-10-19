#!/usr/bin/env python3
"""Audit proof-ledger consistency, not mathematical truth. Never execute evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
CLOSED = {"proved", "conditional"}
STATUSES = CLOSED | {"open", "refuted"}
KINDS = {"derivation", "source", "numerical", "symbolic", "formal"}
ARXIV_BASE = r"(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})"
ARXIV_ID = ARXIV_BASE + r"(?:v[1-9]\d*)?"
PIN = re.compile(r"(?:arxiv:" + ARXIV_BASE + r"v[1-9]\d*|sha256:[a-f0-9]{64}|commit:[a-f0-9]{40}|doi:10\.\d{4,9}/\S+)")


def reference_identity(reference):
    """Read identifiers already present in the record; never resolve URLs online."""
    if not isinstance(reference,str):
        return None
    value = reference.strip()
    if value.lower().startswith("arxiv:"):
        identifier = value[6:]
        return ("arxiv",identifier) if re.fullmatch(ARXIV_ID,identifier) else None
    if value.lower().startswith("doi:"):
        return ("doi",value[4:].casefold())
    parsed = urlparse(value)
    if parsed.scheme not in {"http","https"}:
        return None
    if parsed.hostname in {"arxiv.org","www.arxiv.org","export.arxiv.org"}:
        identifier = re.sub(r"^/(?:abs|pdf|html|src|e-print)/", "", unquote(parsed.path)).removesuffix(".pdf").rstrip("/")
        return ("arxiv",identifier) if re.fullmatch(ARXIV_ID,identifier) else None
    if parsed.hostname in {"doi.org","dx.doi.org"}:
        return ("doi",unquote(parsed.path).lstrip("/").casefold())
    return None


def audit(data, root=ROOT):
    root = Path(root).resolve()
    errors, notices = [], []
    claims, assumptions = {}, {}

    def issue(where, message):
        errors.append(f"{where}: {message}")

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def strings(value, where):
        if not isinstance(value, list) or not all(nonempty(x) for x in value):
            issue(where, "expected a list of nonempty strings")
            return []
        if len(set(value)) != len(value):
            issue(where, "duplicate entries")
        return value

    def artifact(value, where):
        if not isinstance(value, dict) or not nonempty(value.get("path")):
            issue(where, "artifact requires a relative path and sha256")
            return
        path = Path(value["path"])
        try:
            resolved = (root/path).resolve()
        except (OSError,ValueError,RuntimeError):
            issue(where, "artifact path cannot be resolved")
            return
        if path.is_absolute() or not resolved.is_relative_to(root):
            issue(where, "artifact escapes the declared root")
            return
        digest = value.get("sha256", "")
        if not isinstance(digest,str) or not re.fullmatch(r"[a-f0-9]{64}",digest):
            issue(where, "sha256 must be 64 lowercase hex characters")
            return
        try:
            with resolved.open("rb") as handle:
                actual = hashlib.file_digest(handle,"sha256").hexdigest()
            if actual != digest:
                issue(where, "artifact hash mismatch")
        except (OSError,ValueError,RuntimeError):
            issue(where, "artifact is missing or unreadable")

    if not isinstance(data,dict):
        return {"ledger_consistent":False,"mathematical_validity":"not_checked",
                "target_closed_under_given_assumptions":False,"errors":["ledger must be an object"]}
    if data.get("schema_version") != 1:
        issue("schema_version","expected 1")
    target = data.get("target",{})
    if not isinstance(target,dict):
        issue("target","expected an object")
        target = {}
    for field in ("requested_statement","formal_statement","quantifiers","output_rule","claim_id"):
        if not nonempty(target.get(field)):
            issue(f"target.{field}","must be stated explicitly")

    rows = data.get("assumptions",[])
    if not isinstance(rows,list):
        issue("assumptions","expected a list")
        rows = []
    for row in rows:
        if not isinstance(row,dict) or not nonempty(row.get("id")):
            issue("assumptions","each assumption requires an id")
            continue
        key = row["id"]
        if key in assumptions:
            issue(key,"duplicate assumption id")
        assumptions[key] = row
        if not nonempty(row.get("statement")) or not isinstance(row.get("origin"),str) or row["origin"] not in {"given","added"}:
            issue(key,"assumption needs a statement and origin given/added")
        if row.get("origin") == "added" and not nonempty(row.get("reason")):
            issue(key,"added assumption needs an explicit reason")

    rows = data.get("claims",[])
    if not isinstance(rows,list) or not rows:
        issue("claims","expected a nonempty list")
        rows = []
    for row in rows:
        if not isinstance(row,dict) or not nonempty(row.get("id")):
            issue("claims","each claim requires an id")
            continue
        key = row["id"]
        if key in claims or key in assumptions:
            issue(key,"duplicate or colliding id")
        claims[key] = row

    statuses = {key:row.get("status") if isinstance(row.get("status"),str) else None for key,row in claims.items()}
    for key,row in claims.items():
        status = statuses[key]
        if status not in STATUSES:
            issue(key,"unknown claim status")
        for field in ("statement","quantifiers","output_rule"):
            if not nonempty(row.get(field)):
                issue(f"{key}.{field}","must be stated explicitly")
        dependencies = strings(row.get("dependencies"),f"{key}.dependencies")
        used = strings(row.get("assumptions"),f"{key}.assumptions")
        gaps = strings(row.get("gaps"),f"{key}.gaps")
        for dependency in dependencies:
            if dependency not in claims:
                issue(key,f"unknown dependency {dependency}")
            elif status in CLOSED and statuses[dependency] not in CLOSED:
                issue(key,f"closed claim depends on unresolved/refuted {dependency}")
            elif status == "proved" and statuses[dependency] == "conditional":
                issue(key,f"proved claim silently inherits conditional dependency {dependency}")
        for assumption in used:
            if assumption not in assumptions:
                issue(key,f"unknown assumption {assumption}")
            elif status == "proved" and assumptions[assumption].get("origin") == "added":
                issue(key,f"added assumption {assumption} requires conditional status")
        if status in CLOSED and gaps:
            issue(key,"closed claim still has gaps")
        if status in CLOSED and not nonempty(row.get("argument")):
            issue(key,"closed claim needs an argument, not a status label alone")
        if status == "open" and not gaps:
            issue(key,"open claim must identify at least one concrete gap")
        if status == "refuted" and not nonempty(row.get("counterexample")):
            issue(key,"refuted claim needs a counterexample or contradiction")
        evidence = row.get("evidence",[])
        if not isinstance(evidence,list):
            issue(key,"evidence must be a list")
            evidence = []
        supportive = False
        for index,item in enumerate(evidence):
            where = f"{key}.evidence[{index}]"
            if not isinstance(item,dict) or not isinstance(item.get("kind"),str) or item["kind"] not in KINDS:
                issue(where,"unknown evidence kind")
                continue
            kind = item["kind"]
            if not nonempty(item.get("used_fact")):
                issue(where,"identify the exact fact being used")
            if "artifact" in item:
                artifact(item["artifact"],where)
            if kind == "source":
                for field in ("reference","version","locator","checked_scope"):
                    if status in CLOSED and not nonempty(item.get(field)):
                        issue(where,f"source-dependent closure needs {field}")
                if status in CLOSED and (item.get("checked") is not True or
                    not isinstance(item.get("version"),str) or not PIN.fullmatch(item["version"])):
                    issue(where,"external fact has not been checked against a fixed version")
                reference = reference_identity(item.get("reference"))
                pin = reference_identity(item.get("version"))
                if reference and pin and reference[0] == pin[0]:
                    if pin[0] == "arxiv":
                        ref_id, pin_id = reference[1], pin[1]
                        if re.sub(r"v\d+$","",ref_id) != re.sub(r"v\d+$","",pin_id):
                            issue(where,"source reference and version pin identify different papers")
                        elif re.search(r"v\d+$",ref_id) and ref_id != pin_id:
                            issue(where,"source reference and version pin identify different editions")
                    elif reference[1] != pin[1]:
                        issue(where,"source reference and DOI pin disagree")
                version = item.get("version")
                if isinstance(version,str) and version.startswith("sha256:"):
                    source_artifact = item.get("artifact")
                    if not isinstance(source_artifact,dict):
                        if status in CLOSED:
                            issue(where,"a checked sha256 pin requires its local artifact")
                    elif source_artifact.get("sha256") != version[7:]:
                        issue(where,"source sha256 pin and artifact digest disagree")
                supportive = supportive or item.get("checked") is True
            elif kind == "formal":
                for field in ("toolchain","command","declaration","formal_statement"):
                    if not nonempty(item.get(field)):
                        issue(where,f"record the actual {field}")
                if "artifact" not in item:
                    issue(where,"formal evidence needs the checked artifact")
                artifact(item.get("log"),where+".log")
                axioms = strings(item.get("axioms"),where+".axioms")
                if any(a.split(".")[-1] == "sorryAx" or a == item.get("declaration") for a in axioms):
                    issue(where,"placeholder or conclusion-as-axiom cannot close the claim")
                if status in CLOSED and (item.get("result") != "passed" or
                    item.get("statement_correspondence") != "checked" or item.get("axioms_reviewed") is not True):
                    issue(where,"formal closure needs a passed run, statement alignment and axiom review")
                supportive = supportive or item.get("result") == "passed"
                notices.append(f"{where}: recorded formal evidence; this audit did not run or authenticate the prover")
            elif kind == "derivation":
                supportive = True
            else:
                notices.append(f"{where}: {kind} evidence has the stated finite/algebraic scope")
        if status in CLOSED and not supportive:
            issue(key,"numerical/symbolic checks alone do not close a general mathematical claim; give a derivation or checked theorem")

    # Iterative topological sort also handles long chains without recursion limits.
    remaining, followers = {}, {key:[] for key in claims}
    for key,row in claims.items():
        raw = row.get("dependencies",[])
        deps = {d for d in raw if isinstance(d,str) and d in claims} if isinstance(raw,list) else set()
        remaining[key] = len(deps)
        for dep in deps:
            followers[dep].append(key)
    ready = [key for key,count in remaining.items() if count == 0]
    while ready:
        for child in followers[ready.pop()]:
            remaining[child] -= 1
            if remaining[child] == 0:
                ready.append(child)
    for key,count in remaining.items():
        if count:
            issue(key,"cyclic claim dependency or dependency on a cycle; a joint induction needs its own noncircular proof")
    target_id = target.get("claim_id")
    if not isinstance(target_id,str) or target_id not in claims:
        issue("target.claim_id","must identify an existing claim")
    chosen = claims.get(target_id,{}) if isinstance(target_id,str) else {}
    if chosen and chosen.get("statement") != target.get("formal_statement"):
        issue("target","formal statement must equal the selected claim statement")
    for field in ("quantifiers","output_rule"):
        if chosen and chosen.get(field) != target.get(field):
            issue(f"target.{field}","must equal the selected claim field; do not silently strengthen the conclusion")
    return {
        "ledger_consistent":not errors,
        "target_status":chosen.get("status","unknown"),
        "target_closed_under_given_assumptions":not errors and chosen.get("status") == "proved",
        "mathematical_validity":"not_checked",
        "scope":"Dependency, evidence-record and artifact-integrity checks only; no semantic theorem verification.",
        "open_claims":[key for key,row in claims.items() if row.get("status") == "open"],
        "conditional_claims":[key for key,row in claims.items() if row.get("status") == "conditional"],
        "refuted_claims":[key for key,row in claims.items() if row.get("status") == "refuted"],
        "errors":errors,"notices":notices,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger",type=Path)
    parser.add_argument("--root",type=Path,default=ROOT,help="Root for local evidence artifacts")
    parser.add_argument("--require-closed",action="store_true",help="Fail unless target is recorded as proved under given assumptions")
    args = parser.parse_args(argv)
    try:
        result = audit(json.loads(args.ledger.read_text(encoding="utf-8")),args.root)
    except (OSError,ValueError,TypeError) as exc:
        result = {"ledger_consistent":False,"mathematical_validity":"not_checked",
                  "target_closed_under_given_assumptions":False,"errors":[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if not result["ledger_consistent"] else (2 if args.require_closed and not result["target_closed_under_given_assumptions"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
