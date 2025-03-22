from biocypher import BioCypher
import os
from adapters.adapter_1 import GenomicRegionAdapter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize BioCypher with configuration files
    bc = BioCypher(
        schema_config_path=os.path.join('config', 'schema_config.yaml'),
        biocypher_config_path=os.path.join('config', 'biocypher_config.yaml'),
    )

    # Initialize the adapter with the BED file path
    file_path = r"C:\Users\ikrua\Downloads\Telegram Desktop\cCRE-PLS-gene.bed"
    adapter = GenomicRegionAdapter(file_path)

    logger.info("Starting to process nodes...")
    bc.write_nodes(adapter.get_nodes())
    
    logger.info("Starting to process edges...")
    bc.write_edges(adapter.get_edges())

    bc.write_import_call()
    logger.info("Knowledge graph creation completed successfully!")
    
    # List created files
    print(f"\nFiles created in the '{output_dir}' directory:")
    for file in os.listdir(output_dir):
        print(f"- {file}")


if __name__ == "__main__":
    main()