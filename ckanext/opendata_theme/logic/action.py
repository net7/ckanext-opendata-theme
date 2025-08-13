import ckan.plugins.toolkit as tk
import ckanext.opendata_theme.logic.schema as schema


@tk.side_effect_free
def opendata_theme_get_sum(context, data_dict):
    tk.check_access(
        "opendata_theme_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.opendata_theme_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'opendata_theme_get_sum': opendata_theme_get_sum,
    }
