import typing

SelBoxOptions = typing.TypedDict("SelBoxOptions", {
    "type": typing.Literal["SelectionBox"],
    "default": str,
    "selections": typing.List[str]
})

CheckBoxOptions = typing.TypedDict("CheckBoxOptions", {
    "type": typing.Literal["CheckBox"],
    "default": bool,
})

OptionConfigType = typing.Dict[str, typing.Union[SelBoxOptions, CheckBoxOptions]]

Vector2 = typing.Tuple[int, int]
RGBTuple = typing.Tuple[int, int, int]

JSONText = typing.TypedDict("JSONText", {
    "text": str,
    "translate": str,
    "color": str,
    "extra": typing.List[typing.Any]
})

ColorsType = typing.Dict[
    typing.Literal[
        "black",
        "dark_blue",
        "dark_green",
        "dark_aqua",
        "dark_red",
        "dark_purple",
        "gold",
        "gray",
        "dark_gray",
        "blue",
        "green",
        "aqua",
        "red",
        "light_purple",
        "yellow",
        "white"
    ],
    RGBTuple
]