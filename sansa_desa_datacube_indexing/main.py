import enum
import functools
import typing
import uuid
from pathlib import Path

import rasterio
import typer
from jinja2 import (
    Environment,
    FileSystemLoader,
)
from shapely import geometry


app = typer.Typer()
jinja_env = Environment(
    loader=FileSystemLoader(str(Path(__file__).resolve().parents[0] / "templates")),
    trim_blocks=True,
    keep_trailing_newline=True,
)


class DesaSpotArdFileType(enum.Enum):
    PSH = "PSH"
    CLS = "CLS"


@app.command()
def main(
        product: str,
        datasets_directory: Path,
        datasets_directory_spectral_classification: typing.Optional[Path] = None,
        dataset_pattern: typing.Optional[str] = None,
        output_path: typing.Optional[Path] = None,
        verbose: typing.Optional[bool] = False,
):
    echo = functools.partial(_maybe_echo, verbose)
    spectral_class_dir = (
            datasets_directory_spectral_classification or datasets_directory)
    # not using a context manager here because `output_path` is optional
    fh = None
    try:
        if output_path is not None:
            echo(f"Generating dataset document file at: {str(output_path)!r}...")
            fh = output_path.open("w", encoding="utf-8")
        for index, item in enumerate(datasets_directory.glob(dataset_pattern or "*")):
            if item.is_file() and DesaSpotArdFileType.PSH.value in item.stem:
                typer.secho(f"{index!r} - Processing dataset {item.name!r}...")
                cls_item = spectral_class_dir / item.name.replace(
                    DesaSpotArdFileType.PSH.value, DesaSpotArdFileType.CLS.value)
                if not cls_item.is_file():
                    echo(f"Could not find {cls_item.name!r}", fg=typer.colors.MAGENTA)
                rendered = process_spot_dataset(product, item, cls_item)
                echo(rendered, fg=typer.colors.BLUE)
                if fh is not None:
                    fh.write(rendered)
    finally:
        if fh is not None:
            fh.close()


@app.command()
def process_spot_dataset(
        product: str,
        psh_dataset: Path,
        cls_dataset: Path,
) -> str:
    template = jinja_env.get_template("dataset-document.yml")
    with rasterio.open(psh_dataset) as ds:
        ds_tags = ds.tags()
        band_names = {}
        for band_number in ds.indexes:
            band_tags = ds.tags(band_number)
            band_names[band_tags["WavelengthName"].lower()] = band_number
        geo_interface_mapping = geometry.mapping(
            geometry.Polygon(
                (
                    (ds.bounds.left, ds.bounds.top),
                    (ds.bounds.right, ds.bounds.top),
                    (ds.bounds.right, ds.bounds.bottom),
                    (ds.bounds.left, ds.bounds.bottom),
                    (ds.bounds.left, ds.bounds.top),
                )
            )
        )
        processing_datetime = psh_dataset.stem.split("_")[1]
        rendered = template.render(
            id_=uuid.uuid4(),
            label=psh_dataset.stem.replace(f"_{DesaSpotArdFileType.PSH.value}", ""),
            product=product,
            coord1_x=geo_interface_mapping["coordinates"][0][0][0],
            coord1_y=geo_interface_mapping["coordinates"][0][0][1],
            coord2_x=geo_interface_mapping["coordinates"][0][1][0],
            coord2_y=geo_interface_mapping["coordinates"][0][1][1],
            coord3_x=geo_interface_mapping["coordinates"][0][2][0],
            coord3_y=geo_interface_mapping["coordinates"][0][2][1],
            coord4_x=geo_interface_mapping["coordinates"][0][3][0],
            coord4_y=geo_interface_mapping["coordinates"][0][3][1],
            shape_x=ds.shape[0],
            shape_y=ds.shape[1],
            transform1=ds.transform[0],
            transform2=ds.transform[1],
            transform3=ds.transform[2],
            transform4=ds.transform[3],
            transform5=ds.transform[4],
            transform6=ds.transform[5],
            transform7=ds.transform[6],
            transform8=ds.transform[7],
            transform9=ds.transform[8],
            red_layer=band_names["red"],
            green_layer=band_names["green"],
            blue_layer=band_names["blue"],
            nir_layer=band_names["nir"],
            spclass_layer=1,
            psh_path=ds.name,
            cls_path=str(cls_dataset),
            platform=ds_tags["PlatformName"],
            datetime=ds_tags["Acquisition_DateTime"],
            processing_datetime=ds_tags.get("PRODUCTION_DATE", processing_datetime),
        )
        return rendered


def _maybe_echo(verbose: bool, msg: str, **kwargs):
    """Small utility function to control conditional printing to stdout

    This function exists because typer does not seem to provide a way to control
    verbosity of cli programs easily.

    """

    if verbose:
        typer.secho(msg, **kwargs)


if __name__ == "__main__":
    typer.run(main)
