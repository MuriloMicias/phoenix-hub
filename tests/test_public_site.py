from pathlib import Path


def test_public_landing_page_exists() -> None:
    landing_page = Path(__file__).resolve().parents[1] / "docs" / "index.html"

    assert landing_page.exists()
    assert "Phoenix Hub" in landing_page.read_text(encoding="utf-8")
    assert "Public Release" in landing_page.read_text(encoding="utf-8")
