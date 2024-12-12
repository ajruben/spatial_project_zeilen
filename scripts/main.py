import os
import logging
from osgeo import ogr, gdal

class Logger:
    def __init__(self, log_dir="log"):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, "conversion.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger()

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

class ShapefileConverter:
    def __init__(self, logger):
        self.logger = logger

    def convert_shapefiles_to_geopackage(self, input_shapefiles, output_geopackage):
        try:
            if not input_shapefiles:
                raise ValueError("No input shapefiles provided.")

            for input_shapefile in input_shapefiles:
                if not os.path.exists(input_shapefile):
                    self.logger.error(f"Input shapefile not found: {input_shapefile}")
                    raise FileNotFoundError(f"Shapefile not found: {input_shapefile}")

                self.logger.info(f"Processing shapefile: {input_shapefile}")

                try:
                    srcDS = gdal.OpenEx(input_shapefile, allowed_drivers=['ESRI Shapefile'])
                    if srcDS is None:
                        raise RuntimeError(f"Failed to open shapefile: {input_shapefile}")

                    options = gdal.VectorTranslateOptions(
                        format='GPKG', accessMode='append', srcSRS='EPSG:28992', dstSRS='EPSG:28992',
                        addFields=True
                    )

                    gdal.VectorTranslate(srcDS=srcDS, destNameOrDestDS=output_geopackage, options=options)
                    self.logger.info(f"Successfully converted: {input_shapefile} to {output_geopackage}")

                    srcDS.Close()

                except Exception as e:
                    self.logger.error(f"Error processing shapefile {input_shapefile}: {e}")
                    raise

        except Exception as e:
            self.logger.error(f"Unexpected error during conversion: {e}")
            raise

        self.logger.info("All shapefiles processed.")
        return 'success'

if __name__ == "__main__":
    #file paths
    input_shapefiles = [
        r"..\data\vaarweg_markering_drijvend_detail\vaarweg_markering_drijvend_detailPoint.shp",
        r"..\data\vaarweg_markering_vast_detail\vaarweg_markering_vast_detailPoint.shp"
    ]
    output_geopackage = r"..\data\converted_data.gpkg"

    #init logger and converter
    logger = Logger()
    converter = ShapefileConverter(logger)

    #convert
    converter.convert_shapefiles_to_geopackage(input_shapefiles, output_geopackage)

