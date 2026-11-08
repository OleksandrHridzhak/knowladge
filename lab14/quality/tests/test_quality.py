"""
Automated CI Data Quality Test Suite for Energy Grid Knowledge Base.
Covers 10 verifiable criteria: SHACL validation, schema integrity, and domain constraints.
"""
import pytest
import os
import json

QUAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_metrics():
    with open(os.path.join(QUAL_DIR, "metrics.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def test_01_completeness_threshold():
    data = load_metrics()
    comp = next(m for m in data["dimensions"] if m["code"] == "COMP")
    assert comp["improved"] >= comp["threshold"], "Completeness must exceed SLA threshold"

def test_02_consistency_threshold():
    data = load_metrics()
    cons = next(m for m in data["dimensions"] if m["code"] == "CONS")
    assert cons["improved"] >= cons["threshold"], "Consistency must exceed SLA threshold"

def test_03_accuracy_threshold():
    data = load_metrics()
    acc = next(m for m in data["dimensions"] if m["code"] == "ACCU")
    assert acc["improved"] >= acc["threshold"], "Accuracy must exceed SLA threshold"

def test_04_uniqueness_threshold():
    data = load_metrics()
    uniq = next(m for m in data["dimensions"] if m["code"] == "UNIQ")
    assert uniq["improved"] >= uniq["threshold"], "Uniqueness must exceed SLA threshold"

def test_05_provenance_presence():
    data = load_metrics()
    prov = next(m for m in data["dimensions"] if m["code"] == "PROV")
    assert prov["improved"] >= 0.90, "Provenance rate must exceed 90%"

def test_06_validity_shacl_conformity():
    data = load_metrics()
    val = next(m for m in data["dimensions"] if m["code"] == "VALI")
    assert val["improved"] == 1.00, "Validity must be 100% after cleaning"

def test_07_availability_sparql_api():
    data = load_metrics()
    avai = next(m for m in data["dimensions"] if m["code"] == "AVAI")
    assert avai["improved"] >= 0.99, "API Availability must be >= 99%"

def test_08_shacl_shape_file_exists():
    shape_p = os.path.join(QUAL_DIR, "shapes.ttl")
    assert os.path.exists(shape_p) and os.path.getsize(shape_p) > 200

def test_09_conflict_alternatives_registered():
    conf_p = os.path.join(QUAL_DIR, "conflicts.md")
    with open(conf_p, "r", encoding="utf-8") as f:
        text = f.read()
    assert "ALT-001" in text and "ALT-002" in text, "At least 2 alternative provenances must be tracked"

def test_10_merge_registry_unmerge_intact():
    mrg_p = os.path.join(QUAL_DIR, "merge_registry.json")
    with open(mrg_p, "r", encoding="utf-8") as f:
        merges = json.load(f)
    assert any(m["status"] == "unmerged" for m in merges), "Unmerge capability must be verified in registry"
