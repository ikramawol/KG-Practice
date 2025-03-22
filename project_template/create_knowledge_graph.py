from biocypher import BioCypher
import os
from adapters.adapter_1 import GenomicRegionAdapter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Create output directory
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
        # Write nodes to CSV
        bc.write_nodes(adapter.get_nodes())
        
        logger.info("Starting to process edges...")
        # Write edges to CSV
        bc.write_edges(adapter.get_edges())

        # Create the import call file
        bc.write_import_call()

        logger.info("Knowledge graph creation completed successfully!")
        
        # List created files
        print(f"\nFiles created in the '{output_dir}' directory:")
        for file in os.listdir(output_dir):
            print(f"- {file}")

    except Exception as e:
        logger.error(f"Error creating knowledge graph: {str(e)}")
        raise

if __name__ == "__main__":
    main()