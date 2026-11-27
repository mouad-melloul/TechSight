import pandas as pd
import pytest

REQUIRED_COLUMNS = {
    "Titre", "Entreprise", "Localisation",
    "Lien", "Compétences", "Date", "mapped_role",
}
VALID_ROLES = {
    "data engineer", "data analyst", "data scientist",
    "web developer", "software engineer",
}


@pytest.fixture(scope="module")
def df():
    return pd.read_csv("data/dataset_final.csv")


def test_not_empty(df):
    assert len(df) > 0


def test_required_columns(df):
    assert REQUIRED_COLUMNS.issubset(df.columns)


def test_no_duplicates(df):
    assert not df.duplicated(subset=["Titre", "Entreprise", "Localisation"]).any()


def test_roles_are_valid(df):
    assert set(df["mapped_role"].dropna()) <= VALID_ROLES


def test_dates_are_parseable(df):
    dates = pd.to_datetime(df["Date"], errors="coerce")
    assert dates.notna().mean() > 0.9