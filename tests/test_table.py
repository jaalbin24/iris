"""Tests for iris.table module."""

import pytest

from iris import Semantic, Table


class TestTable:
    """Test Table class."""

    def test_table_creation(self):
        """Test creating a table with columns."""
        table = Table(["Name", "Status"])
        assert table._columns == ["Name", "Status"]
        assert table._rows == []

    def test_add_row(self):
        """Test adding rows to table."""
        table = Table(["Name", "Status"])
        table.add_row("backup-01", "OK")
        assert len(table._rows) == 1
        assert table._rows[0] == ["backup-01", "OK"]

    def test_add_row_wrong_count(self):
        """Test adding row with wrong number of values."""
        table = Table(["Name", "Status"])
        with pytest.raises(ValueError, match="Expected 2 values"):
            table.add_row("only-one")

    def test_render(self, capsys):
        """Test table rendering."""
        table = Table(["Name", "Status", "Size"])
        table.add_row("backup-01", "OK", "2.3 GB")
        table.add_row("backup-02", "OK", "1.8 GB")
        table.render()

        captured = capsys.readouterr()
        assert "Name" in captured.out
        assert "Status" in captured.out
        assert "Size" in captured.out
        assert "backup-01" in captured.out
        assert "backup-02" in captured.out
        assert "─" in captured.out

    def test_render_to_string(self):
        """Test rendering table to string."""
        table = Table(["Name", "Size"])
        table.add_row("test", "1 GB")
        result = table.render_to_string()

        assert "Name" in result
        assert "Size" in result
        assert "test" in result
        assert "1 GB" in result
        assert "─" in result

    def test_column_width_calculation(self):
        """Test that column widths adjust to content."""
        table = Table(["ID", "Description"])
        table.add_row("1", "Short")
        table.add_row("2", "A much longer description here")

        widths = table._calculate_widths()
        # "Description" header vs "A much longer description here"
        assert widths[1] == len("A much longer description here")

    def test_set_column_semantics_with_strings(self):
        """Test that string semantic names are coerced to Semantic enums."""
        table = Table(["Name", "Status"])
        table.set_column_semantics(1, {
            "valid": "SUCCESS",
            "expired": "warning",
            "revoked": "Error",
        })
        mapping = table._column_semantics[1]
        assert mapping["valid"] is Semantic.SUCCESS
        assert mapping["expired"] is Semantic.WARNING
        assert mapping["revoked"] is Semantic.ERROR

    def test_empty_table(self, capsys):
        """Test rendering empty table."""
        table = Table(["Col1", "Col2"])
        table.render()

        captured = capsys.readouterr()
        assert "Col1" in captured.out
        assert "Col2" in captured.out
