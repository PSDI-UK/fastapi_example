import pytest
from src.utils.common_models import IdMixin, PyObjectId


def test_pyobjectid() -> None:
    # Check that PyObjectId.validate raises a ValueError
    with pytest.raises(ValueError, match="Invalid ObjectId"):
        PyObjectId.validate("invalid", None)


def test_id_mixin() -> None:
    # Test valid ObjectId passed into the _id field
    # It should be converted to a string and stored in the id field
    valid_id = PyObjectId()
    model = IdMixin(**{"_id": valid_id})
    assert model.id == str(valid_id)

    # Test valid ObjectId str passed into the id field
    valid_id = str(PyObjectId())
    model = IdMixin(**{"id": valid_id})
    assert model.id == valid_id

    # Test invalid ObjectId passed into the _id field
    with pytest.raises(ValueError):
        IdMixin(**{"_id": "invalid"})

    # Test valid ObjectId str pased into the id field
    with pytest.raises(ValueError):
        model = IdMixin(id="invalid")
