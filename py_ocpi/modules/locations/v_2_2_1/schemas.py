from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType
from py_ocpi.modules.locations.v_2_2_1.enums import (
    EnergySourceCategory,
    ParkingType,
    ParkingRestriction,
    Facility,
    Status,
    Capability,
    ConnectorFormat,
    ConnectorType,
    PowerType,
    ImageCategory,
    EnvironmentalImpactCategory,
)
from py_ocpi.core.data_types import (
    URL,
    CiString,
    DisplayText,
    Number,
    String,
    DateTime,
)


class PublishTokenType(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_publish_token_class
    """

    uid: Optional[CiString(max_length=36)]  # type: ignore
    type: Optional[TokenType]
    visual_number: Optional[String(max_length=64)]  # type: ignore
    issuer: Optional[String(max_length=64)]  # type: ignore
    group_id: Optional[CiString(max_length=36)]  # type: ignore


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1415-image-class
    """

    url: URL
    thumbnail: Optional[URL]
    category: ImageCategory
    type: CiString(max_length=4)  # type: ignore
    width: Optional[int]
    height: Optional[int]


class GeoLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_geolocation_class
    """

    latitude: String(max_length=10)  # type: ignore
    longitude: String(max_length=11)  # type: ignore


class AdditionalGeoLocation(GeoLocation):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_additionalgeolocation_class
    """

    name: Optional[DisplayText]


class Connector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#133-connector-object
    """

    id: CiString(max_length=36)  # type: ignore
    standard: ConnectorType
    format: ConnectorFormat
    power_type: PowerType
    max_voltage: int
    max_amperage: int
    max_electric_power: Optional[int]
    tariff_ids: List[CiString(max_length=36)] = []  # type: ignore
    terms_and_conditions: Optional[URL]
    last_updated: DateTime


class ConnectorPartialUpdate(BaseModel):
    id: Optional[CiString(max_length=36)]  # type: ignore
    standard: Optional[ConnectorType]
    format: Optional[ConnectorFormat]
    power_type: Optional[PowerType]
    max_voltage: Optional[int]
    max_amperage: Optional[int]
    max_electric_power: Optional[Optional[int]]
    tariff_ids: Optional[List[CiString(max_length=36)]]  # type: ignore
    terms_and_conditions: Optional[URL]
    last_updated: Optional[DateTime]


class StatusSchedule(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1423-statusschedule-class
    """

    period_begin: DateTime
    period_end: Optional[DateTime]
    status: Status


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_evse_object
    """

    uid: CiString(max_length=36)  # type: ignore
    evse_id: Optional[CiString(max_length=48)]  # type: ignore
    status: Status
    status_schedule: Optional[StatusSchedule]
    capabilities: List[Capability] = []
    connectors: List[Connector]
    floor_level: Optional[String(max_length=4)]  # type: ignore
    coordinates: Optional[GeoLocation]
    physical_reference: Optional[String(max_length=16)]  # type: ignore
    directions: List[DisplayText] = []
    parking_restrictions: List[ParkingRestriction] = []
    images: List[Image] = []
    last_updated: DateTime


class EVSEPartialUpdate(BaseModel):
    uid: Optional[CiString(max_length=36)]  # type: ignore
    evse_id: Optional[CiString(max_length=48)]  # type: ignore
    status: Optional[Status]
    status_schedule: Optional[StatusSchedule]
    capabilities: Optional[List[Capability]]
    connectors: Optional[List[Connector]]
    floor_level: Optional[String(max_length=4)]  # type: ignore
    coordinates: Optional[GeoLocation]
    physical_reference: Optional[String(max_length=16)]  # type: ignore
    directions: Optional[List[DisplayText]]
    parking_restrictions: Optional[List[ParkingRestriction]]
    images: Optional[List[Image]]
    last_updated: Optional[DateTime]


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_businessdetails_class
    """

    name: String(max_length=100)  # type: ignore
    website: Optional[URL]
    logo: Optional[Image]


class RegularHours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1421-regularhours-class
    """

    weekday: int
    period_begin: String(max_length=5)  # type: ignore
    period_end: String(max_length=5)  # type: ignore


class ExceptionalPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1411-exceptionalperiod-class
    """

    period_begin: DateTime
    period_end: DateTime


class Hours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_hours_class
    """

    twentyfourseven: bool
    regular_hours: List[RegularHours]
    exceptional_openings: List[ExceptionalPeriod] = []
    exceptional_closings: List[ExceptionalPeriod] = []


class EnergySource(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#147-energysource-class
    """

    source: EnergySourceCategory
    percentage: Number


class EnvironmentalImpact(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#149-environmentalimpact-class
    """

    category: EnvironmentalImpactCategory
    amount: Number


class EnergyMix(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_energymix_class
    """

    is_green_energy: bool
    energy_sources: List[EnergySource]
    environ_impact: Optional[EnvironmentalImpact]
    supplier_name: String(max_length=64)  # type: ignore
    energy_product_name: String(max_length=64)  # type: ignore


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#131-location-object
    """

    country_code: CiString(max_length=2)  # type: ignore
    party_id: CiString(max_length=3)  # type: ignore
    id: CiString(max_length=36)  # type: ignore
    publish: bool
    publish_allowed_to: List[PublishTokenType] = []
    name: Optional[String(max_length=255)]  # type: ignore
    address: String(max_length=45)  # type: ignore
    city: String(max_length=45)  # type: ignore
    postal_code: Optional[String(max_length=10)]  # type: ignore
    state: Optional[String(max_length=20)]  # type: ignore
    country: String(max_length=3)  # type: ignore
    coordinates: GeoLocation
    related_locations: List[AdditionalGeoLocation] = []
    parking_type: Optional[ParkingType]
    evses: List[EVSE] = []
    directions: List[DisplayText] = []
    operator: Optional[BusinessDetails]
    suboperator: Optional[BusinessDetails]
    owner: Optional[BusinessDetails]
    facilities: List[Facility] = []
    time_zone: String(max_length=255)  # type: ignore
    opening_times: Optional[Hours]
    charging_when_closed: Optional[bool]
    images: List[Image] = []
    energy_mix: Optional[EnergyMix]
    last_updated: DateTime


class LocationPartialUpdate(BaseModel):
    country_code: Optional[CiString(max_length=2)]  # type: ignore
    party_id: Optional[CiString(max_length=3)]  # type: ignore
    id: Optional[CiString(max_length=36)]  # type: ignore
    publish: Optional[bool]
    publish_allowed_to: Optional[List[PublishTokenType]]
    name: Optional[String(max_length=255)]  # type: ignore
    address: Optional[String(max_length=45)]  # type: ignore
    city: Optional[String(max_length=45)]  # type: ignore
    postal_code: Optional[String(max_length=10)]  # type: ignore
    state: Optional[String(max_length=20)]  # type: ignore
    country: Optional[String(max_length=3)]  # type: ignore
    coordinates: Optional[GeoLocation]
    related_locations: Optional[List[AdditionalGeoLocation]]
    parking_type: Optional[ParkingType]
    evses: Optional[List[EVSE]]
    directions: Optional[List[DisplayText]]
    operator: Optional[BusinessDetails]
    suboperator: Optional[BusinessDetails]
    owner: Optional[BusinessDetails]
    facilities: Optional[List[Facility]]
    time_zone: Optional[String(max_length=255)]  # type: ignore
    opening_times: Optional[Hours]
    charging_when_closed: Optional[bool]
    images: Optional[List[Image]]
    energy_mix: Optional[EnergyMix]
    last_updated: Optional[DateTime]
