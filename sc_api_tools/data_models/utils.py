from datetime import datetime
from enum import Enum

import attr
from typing import Any, Union, Optional, TypeVar, Type, Callable, Dict, List

import cv2
import numpy as np

from sc_api_tools.data_models import TaskType
from sc_api_tools.data_models.enums import ShapeType, MediaType, AnnotationKind

EnumType = TypeVar("EnumType", bound=Enum)


def deidentify(instance: Any):
    """
    Sets all identifier fields of an instance of an attr.s decorated class within the
    SC REST DataModels to None

    :param instance: Object to deidentify
    """
    for field in attr.fields(type(instance)):
        if field.name in instance._identifier_fields:
            setattr(instance, field.name, None)


def str_to_enum_converter(
        enum: Type[EnumType]
) -> Callable[[Union[str, EnumType]], EnumType]:
    """
    Constructs a converter function to convert an input value into an instance of the
    Enum subclass passed in `enum`

    :param enum: type of the Enum to which the converter should convert
    :return: Converter function that takes an input value and attempts to convert it
        into an instance of `enum`
    """
    def _converter(input_value: Union[str, EnumType]) -> EnumType:
        """
        Converts an input value to an instance of an Enum

        :param input_value: Value to convert
        :return: Instance of the Enum
        """
        if isinstance(input_value, str):
            return enum(input_value)
        elif isinstance(input_value, enum):
            return input_value
        else:
            raise ValueError(
                f"Invalid argument! Cannot convert value {input_value} to Enum "
                f"{enum.__name__}"
            )
    return _converter


def str_to_task_type(task_type: Union[str, TaskType]) -> TaskType:
    """
    Converts an input string to a task type

    :param task_type:
    :return: TaskType instance corresponding to `task_type`
    """
    if isinstance(task_type, str):
        return TaskType(task_type)
    else:
        return task_type


def str_to_media_type(media_type: Union[str, MediaType]) -> MediaType:
    """
    Converts an input string to a media type

    :param media_type:
    :return: MediaType instance corresponding to `media_type`
    """
    if isinstance(media_type, str):
        return MediaType(media_type)
    else:
        return media_type


def str_to_shape_type(shape_type: Union[str, ShapeType]) -> ShapeType:
    """
    Converts an input string to a shape type

    :param shape_type:
    :return: ShapeType instance corresponding to `shape_type`
    """
    if isinstance(shape_type, str):
        return ShapeType(shape_type)
    else:
        return shape_type


def str_to_annotation_kind(annotation_kind: Union[str, AnnotationKind]) -> AnnotationKind:
    """
    Converts an input string to an annotation kind

    :param annotation_kind:
    :return: AnnotationKind instance corresponding to `annotation_kind`
    """
    if isinstance(annotation_kind, str):
        return AnnotationKind(annotation_kind)
    else:
        return annotation_kind


def str_to_datetime(datetime_str: Optional[Union[str, datetime]]) -> Optional[datetime]:
    """
    Converts a string to a datetime

    :param datetime_str:
    :return: datetime instance
    """
    if isinstance(datetime_str, str):
        return datetime.fromisoformat(datetime_str)
    elif isinstance(datetime_str, datetime):
        return datetime_str
    elif datetime_str is None:
        return None


def attr_value_serializer(instance, field, value):
    """
    Converts a value in an attr.s decorated class to string representation, used
    while converting the attrs object to a dictionary.

    Converts Enums and datetime objects to string representation

    :param instance:
    :param field:
    :param value:
    :return:
    """
    if isinstance(value, Enum):
        return str(value)
    elif isinstance(value, datetime):
        return datetime.isoformat(value)
    else:
        return value


def numpy_from_buffer(buffer: bytes) -> np.ndarray:
    """
    Converts a bytes string representing an image into a numpy array

    :param buffer: Bytes object to convert
    :return: Numpy.ndarray containing the numpy data from the image
    """
    numpy_array = np.frombuffer(buffer, dtype=np.uint8)
    return cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)


def round_dictionary(
        input_data: Union[Dict[str, Any], List[Any]], decimal_places: int = 3
) -> Union[Dict[str, Any], List[Any]]:
    """
    Converts all floats in a dictionary to string representation, rounded to
    `decimal_places`

    :param input_data: Input dictionary to convert and round
    :param decimal_places: Number of decimal places to round to. Defaults to 3
    :return: dictionary with all floats rounded
    """
    if isinstance(input_data, dict):
        for key, value in input_data.items():
            if isinstance(value, float):
                input_data[key] = f"{value:.{decimal_places}f}"
            elif isinstance(value, (dict, list)):
                input_data[key] = round_dictionary(value, decimal_places=decimal_places)
        return input_data
    elif isinstance(input_data, list):
        new_list = []
        for item in input_data:
            if isinstance(item, float):
                new_list.append(f"{item:.{decimal_places}f}")
            elif isinstance(item, (dict, list)):
                new_list.append(round_dictionary(item, decimal_places=decimal_places))
        return new_list
