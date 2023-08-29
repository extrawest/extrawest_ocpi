from abc import ABC, abstractmethod

from py_ocpi.modules.versions.enums import VersionNumber


class Adapter(ABC):
    @abstractmethod
    def location_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Location schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Location: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def session_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Session schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Session: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def charging_preference_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ChargingPreference schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            ChargingPreference: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def credentials_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Credential schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Credential: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def cdr_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CDR schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            CDR: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def tariff_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Tariff schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Tariff: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def command_response_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResponse schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            CommandResponse: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def command_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResult schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            CommandResult: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def token_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Token schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Token: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def authorization_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI AuthorizationInfo schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            AuthorizationInfo: The object data in proper OCPI schema
        """
        pass
