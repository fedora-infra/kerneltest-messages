# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from kerneltest_messages import UploadNewV1

from .utils import DUMMY_TEST


def test_minimal():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {
        "agent": "dummy-user",
        "test": DUMMY_TEST,
    }
    message = UploadNewV1(body=body)
    message.validate()
    assert message.url is None


def test_invalid_field_required():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {
        "agent": "dummy-user",
        "test": {"result": "asdfasdf"},
    }
    message = UploadNewV1(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_str():
    """Assert __str__ produces a human-readable message."""
    body = {
        "agent": "dummy-user",
        "test": DUMMY_TEST,
    }
    expected_str = (
        "dummy-user uploaded new kernel test results "
        "for 6.9.0-0.rc0.20240314git480e035fc4c7.5.fc41.aarch64"
    )
    message = UploadNewV1(body=body)
    message.validate()
    assert expected_str == str(message)


def test_summary():
    """Assert the summary is correct."""
    body = {
        "agent": "dummy-user",
        "test": DUMMY_TEST,
    }
    expected_summary = (
        "dummy-user uploaded new kernel test results "
        "for 6.9.0-0.rc0.20240314git480e035fc4c7.5.fc41.aarch64"
    )
    message = UploadNewV1(body=body)
    assert expected_summary == message.summary
