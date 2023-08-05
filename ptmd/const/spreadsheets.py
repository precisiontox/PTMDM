""" This module provide constants related to the generation and validation of spreadsheets.
"""
from collections import namedtuple

from .schema_loaders import INPUT_SCHEMA, EXPOSURE_SCHEMA, EXPOSURE_INFORMATION_SCHEMA
from .labels import (
    PTX_ID_LABEL, DOSE_LABEL, TIMEPOINT_LABEL,
    COMPOUND_NAME_LABEL, COMPOUND_HASH_LABEL,
    BATCH_LABEL
)


def extract_empty_columns() -> list[str]:
    """ Extracts the empty columns from the sample sheet.

    :return: The empty columns.
    """
    fields_map: dict = {}
    fields: list = []
    for field, schema in EXPOSURE_INFORMATION_SCHEMA['properties'].items():
        if schema['_role'] == "user":
            fields_map[schema['_order']] = field

    for i in range(1, len(fields_map) + 1):
        fields.append(fields_map[i])
    return fields


ReplicateBlankRange: namedtuple = namedtuple('ReplicateBlankRange', ['min', 'max'])

ALLOWED_PARTNERS: list[str] = INPUT_SCHEMA['properties']['partner']['enum']
ALLOWED_EXPOSURE_BATCH: str = INPUT_SCHEMA['properties'][BATCH_LABEL]['pattern']
EXPOSURE_BATCH_MAX_LENGTH: int = INPUT_SCHEMA['properties'][BATCH_LABEL]['maxLength']
REPLICATES_EXPOSURE_MIN: int = INPUT_SCHEMA['properties']['replicates4exposure']['minimum']
REPLICATES_CONTROL_MIN: int = INPUT_SCHEMA['properties']['replicates4control']['minimum']
ALLOWED_DOSE_VALUES: list[str] = EXPOSURE_SCHEMA['properties']['dose']['enum']
ALLOWED_VEHICLES: list[str] = INPUT_SCHEMA['properties']['vehicle']['enum']
TIMEPOINTS_MIN: int = INPUT_SCHEMA['properties']['timepoints']['items']['minimum']
REPLICATES_BLANK_RANGE: ReplicateBlankRange = ReplicateBlankRange(
    INPUT_SCHEMA['properties']['replicates_blank']['minimum'],
    INPUT_SCHEMA['properties']['replicates_blank']['maximum']
)

DOSE_MAPPING: dict = {
    0: "Z",
    '0': "Z",
    "BMD10": "L",
    "BMD25": "M",
    "10mg/L": "H",
}
TIME_POINT_MAPPING: dict = {
    "TP0": "S",
    "TP1": "A",
    "TP2": "B",
    "TP3": "C",
    "TP4": "D",
    "TP5": "E",
}

SAMPLE_SHEET_EMPTY_COLUMNS: list[str] = extract_empty_columns()


SAMPLE_SHEET_COLUMNS: list[str] = [
    PTX_ID_LABEL,
    COMPOUND_HASH_LABEL,
    *SAMPLE_SHEET_EMPTY_COLUMNS,
    "replicate",
    COMPOUND_NAME_LABEL,
    DOSE_LABEL,
    TIMEPOINT_LABEL,
    "timepoint_(hours)"
]
GENERAL_SHEET_COLUMNS: list[str] = [
    "partner_id",
    "biosystem_name",
    BATCH_LABEL,
    "control",
    "replicates",
    "blanks",
    "exposure_batch_startdate",
    "exposure_batch_enddate",
    "timepoints",
    "compound_vehicle",
]
EMPTY_FIELDS_VALUES: list[str] = [''] * len(SAMPLE_SHEET_EMPTY_COLUMNS)
