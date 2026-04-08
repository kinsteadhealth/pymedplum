"""Tests for PatchOp and BundleInput Pydantic models."""

import pytest

from pymedplum.mcp.server import BundleInput, PatchOp


class TestPatchOp:
    def test_valid_replace(self):
        op = PatchOp(op="replace", path="/active", value=True)
        assert op.op == "replace"
        assert op.path == "/active"
        assert op.value is True

    def test_valid_remove_no_value(self):
        op = PatchOp(op="remove", path="/extension/0")
        assert op.value is None

    def test_invalid_op_rejected(self):
        with pytest.raises(Exception):
            PatchOp(op="invalid", path="/foo")

    def test_missing_path_rejected(self):
        with pytest.raises(Exception):
            PatchOp(op="add", value=1)

    def test_dump_excludes_unset(self):
        op = PatchOp(op="remove", path="/foo")
        dumped = op.model_dump(exclude_unset=True, by_alias=True)
        assert "value" not in dumped
        assert "from" not in dumped
        assert dumped == {"op": "remove", "path": "/foo"}

    def test_explicit_null_value_preserved(self):
        op = PatchOp(op="replace", path="/active", value=None)
        dumped = op.model_dump(exclude_unset=True, by_alias=True)
        assert "value" in dumped
        assert dumped["value"] is None

    def test_add_requires_value(self):
        with pytest.raises(Exception):
            PatchOp(op="add", path="/foo")

    def test_replace_requires_value(self):
        with pytest.raises(Exception):
            PatchOp(op="replace", path="/foo")

    def test_test_requires_value(self):
        with pytest.raises(Exception):
            PatchOp(op="test", path="/foo")

    def test_copy_requires_from(self):
        with pytest.raises(Exception):
            PatchOp(op="copy", path="/to")

    def test_move_requires_from(self):
        with pytest.raises(Exception):
            PatchOp(op="move", path="/to")

    def test_copy_with_from_serializes(self):
        op = PatchOp.model_validate({"op": "copy", "path": "/to", "from": "/src"})
        assert op.from_ == "/src"
        dumped = op.model_dump(exclude_unset=True, by_alias=True)
        assert dumped["from"] == "/src"
        assert "from_" not in dumped

    def test_move_with_from(self):
        op = PatchOp.model_validate({"op": "move", "path": "/to", "from": "/src"})
        dumped = op.model_dump(exclude_unset=True, by_alias=True)
        assert dumped == {"op": "move", "path": "/to", "from": "/src"}

    def test_remove_ignores_value(self):
        op = PatchOp(op="remove", path="/foo")
        dumped = op.model_dump(exclude_unset=True, by_alias=True)
        assert dumped == {"op": "remove", "path": "/foo"}


class TestBundleInput:
    def test_valid_batch(self):
        bundle = BundleInput(
            type="batch",
            entry=[{"request": {"method": "GET", "url": "Patient/123"}}],
        )
        assert bundle.type == "batch"
        assert bundle.resourceType == "Bundle"

    def test_valid_transaction(self):
        bundle = BundleInput(type="transaction", entry=[])
        assert bundle.type == "transaction"

    def test_invalid_type_rejected(self):
        with pytest.raises(Exception):
            BundleInput(type="invalid")

    def test_default_entry_empty(self):
        bundle = BundleInput(type="batch")
        assert bundle.entry == []

    def test_dump_uses_alias(self):
        bundle = BundleInput(type="batch")
        raw = bundle.model_dump(by_alias=True)
        assert raw["resourceType"] == "Bundle"
        assert raw["type"] == "batch"
