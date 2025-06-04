from typing import List, Optional

from pydantic import BaseModel
from py_ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod, CdrDimensionType

from py_ocpi.core.data_types import CiString, Number, Price, String, DateTime
from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType
from py_ocpi.modules.tariffs.v_2_2_1.schemas import Tariff
from py_ocpi.modules.locations.v_2_2_1.schemas import GeoLocation
from py_ocpi.modules.locations.v_2_2_1.enums import (
    ConnectorFormat,
    ConnectorType,
    PowerType,
)


class SignedValue(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#148-signedvalue-class
    """

    nature: CiString(32)  # type: ignore
    plain_data: String(512)  # type: ignore
    signed_data: String(5000)  # type: ignore


class SignedData(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#147-signeddata-class
    """

    encoding_method: CiString(36)  # type: ignore
    encoding_method_version: Optional[int]
    public_key: Optional[String(512)]  # type: ignore
    signed_values: List[SignedValue]
    url: Optional[String(512)]  # type: ignore


class CdrDimension(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#142-cdrdimension-class
    """

    type: CdrDimensionType
    volume: Number


class ChargingPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#146-chargingperiod-class
    """

    start_date_time: DateTime
    dimensions: List[CdrDimension]
    tariff_id: Optional[CiString(36)]  # type: ignore


class CdrToken(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#145-cdrtoken-class
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    uid: CiString(36)  # type: ignore
    type: TokenType
    contract_id: CiString(36)  # type: ignore


class CdrLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#144-cdrlocation-class
    """

    id: CiString(36)  # type: ignore
    name: Optional[String(255)]  # type: ignore
    address: String(45)  # type: ignore
    city: String(45)  # type: ignore
    postal_code: Optional[String(10)]  # type: ignore
    state: Optional[String(20)]  # type: ignore
    country: String(3)  # type: ignore
    coordinates: GeoLocation
    evse_id: CiString(48)  # type: ignore
    connector_id: CiString(36)  # type: ignore
    connector_standard: ConnectorType
    connector_format: ConnectorFormat
    connector_power_type: PowerType


class Cdr(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#131-cdr-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    id: CiString(39)  # type: ignore
    start_date_time: DateTime
    end_date_time: DateTime
    session_id: Optional[CiString(36)]  # type: ignore
    cdr_token: CdrToken
    auth_method: AuthMethod
    authorization_reference: Optional[CiString(36)]  # type: ignore
    cdr_location: CdrLocation
    meter_id: Optional[String(255)]  # type: ignore
    currency: String(3)  # type: ignore
    tariffs: List[Tariff] = []
    charging_periods: List[ChargingPeriod]
    signed_data: Optional[SignedData]
    total_cost: Price
    total_fixed_cost: Optional[Price]
    total_energy: Number
    total_energy_cost: Optional[Price]
    total_time: Number
    total_time_cost: Optional[Price]
    total_parking_time: Optional[Number]
    total_parking_cost: Optional[Price]
    total_reservation_cost: Optional[Price]
    remark: Optional[String(255)]  # type: ignore
    invoice_reference_id: Optional[CiString(36)]  # type: ignore
    credit: Optional[bool]
    credit_reference_id: Optional[CiString(39)]  # type: ignore
    home_charging_compensation: Optional[bool]
    last_updated: DateTime
