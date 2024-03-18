# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from fedora_messaging import message

TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "arch": {"type": "string"},
        "authenticated": {"type": "boolean"},
        "failed_tests": {"type": "string"},
        "fedora_version": {"type": ["string", "integer"]},
        "kernel_version": {"type": "string"},
        "release": {"type": "string"},
        "result": {"type": "string"},
        "testdate": {"type": "string"},
        "tester": {"type": "string"},
        "testset": {"type": "string"},
    },
    "required": ["kernel_version"],
}

RELEASE_SCHEMA = {
    "type": "object",
    "properties": {
        "support": {"type": "string"},
        "releasenum": {"type": ["string", "integer"]},
    },
    "required": ["support", "releasenum"],
}


class KerneltestMessage(message.Message):
    @property
    def app_name(self):
        """
        Return the name of the application that generated the message.

        Returns:
            the name of the application (kerneltest)
        """
        return "kerneltest"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/kerneltest.png"

    @property
    def agent_name(self):
        """Return the agent's username for this message.

        Returns:
            The agent's username
        """
        return self.body.get("agent")

    @property
    def usernames(self):
        """
        List of users affected by the action that generated this message.

        Returns:
            A list of affected usernames.
        """
        return []

    @property
    def groups(self):
        """
        List of groups affected by the action that generated this message.

        Returns:
            A list of affected groups.
        """
        return []

    @property
    def url(self):
        return None

    def __str__(self):
        """
        Return a human-readable representation of this message.

        This should provide a detailed representation of the message, much like the body
        of an email.

        Returns:
            A human readable representation of this message.
        """
        return self.summary


class UploadNewV1(KerneltestMessage):
    """The message sent when a user uploads a new kerneltest"""

    @property
    def summary(self):
        """
        Return a short, human-readable representation of this message.

        This should provide a short summary of the message, much like the subject line
        of an email.

        Returns:
            A summary for this message.
        """
        return (
            f"{self.agent_name} uploaded new kernel test results for "
            f"{self.body['test']['kernel_version']}"
        )

    topic = "kerneltest.upload.new"
    body_schema: typing.ClassVar = {
        "id": "http://fedoraproject.org/message-schema/noggin",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when a user uploads a new kernel test report",
        "type": "object",
        "required": ["agent", "test"],
        "properties": {
            "test": TEST_SCHEMA,
            "agent": {"type": "string"},
        },
    }


class ReleaseNewV1(KerneltestMessage):
    """The message sent when an admin creates a new release"""

    @property
    def summary(self):
        """
        Return a short, human-readable representation of this message.

        This should provide a short summary of the message, much like the subject line
        of an email.

        Returns:
            A summary for this message.
        """
        return (
            f"{self.agent_name} created a new release {self.body['release']['releasenum']}"
            f" with status {self.body['release']['support']}"
        )

    topic = "kerneltest.release.new"
    body_schema: typing.ClassVar = {
        "id": "http://fedoraproject.org/message-schema/noggin",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when an admin creates a new release",
        "type": "object",
        "required": ["agent", "release"],
        "properties": {
            "release": RELEASE_SCHEMA,
            "agent": {"type": "string"},
        },
    }


class ReleaseEditV1(KerneltestMessage):
    """The message sent when an admin creates a new release"""

    @property
    def summary(self):
        """
        Return a short, human-readable representation of this message.

        This should provide a short summary of the message, much like the subject line
        of an email.

        Returns:
            A summary for this message.
        """
        return (
            f"{self.agent_name} edited release {self.body['release']['releasenum']}"
            f" with status {self.body['release']['support']}"
        )

    topic = "kerneltest.release.edit"
    body_schema: typing.ClassVar = {
        "id": "http://fedoraproject.org/message-schema/noggin",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "The message sent when an admin edits a release",
        "type": "object",
        "required": ["agent", "release"],
        "properties": {
            "release": RELEASE_SCHEMA,
            "agent": {"type": "string"},
        },
    }
