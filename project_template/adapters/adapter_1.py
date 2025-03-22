from enum import Enum, auto
from typing import Optional
from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


class GenomicRegionAdapterNodeType(Enum):
    """
    Define types of nodes the adapter can provide.
    """
    GENOMIC_REGION = auto()
    GENE = auto()


class GenomicRegionField(Enum):
    """
    Define possible fields for genomic regions.
    """
    ID = "id"
    CHROMOSOME = "chromosome"
    START = "start"
    END = "end"
    ACCESSION_E = "accession_e"
    CCRE_TYPE = "ccre_type"
    DISTANCE_BP = "distance_bp"


class GeneField(Enum):
    """
    Define possible fields for genes.
    """
    ID = "id"
    NAME = "name"


class GenomicRegionAdapterEdgeType(Enum):
    """
    Define types of edges the adapter can provide.
    """
    REGION_TO_GENE = "RegionToGene"


class RegionToGeneEdgeField(Enum):
    """
    Define possible fields for region-to-gene edges.
    """
    DISTANCE_BP = "distance_bp"


class GenomicRegionAdapter:
    """
    BioCypher adapter for genomic region data. Generates nodes and edges for creating a
    knowledge graph from BED file data.

    Args:
        file_path: Path to the BED file
        node_types: List of node types to include
        node_fields: List of node fields to include
        edge_types: List of edge types to include
        edge_fields: List of edge fields to include
    """

    def __init__(
        self,
        file_path: str,
        node_types: Optional[list] = None,
        node_fields: Optional[list] = None,
        edge_types: Optional[list] = None,
        edge_fields: Optional[list] = None,
    ):
        self.file_path = file_path
        self._set_types_and_fields(node_types, node_fields, edge_types, edge_fields)
        self.source = "ENCODE"
        self.version = "1.0"
        self.license = "MIT"

    def get_nodes(self):
        """
        Returns a generator of node tuples from the BED file data.
        """
        logger.info("Generating nodes from BED file.")

        with open(self.file_path, 'r') as file:
            for line in file:
                if line.startswith('#') or line.strip() == '':
                    continue
                
                fields = line.strip().split('\t')
                try:
                    chromosome = fields[0]
                    start = int(fields[1])
                    end = int(fields[2])
                    accession_d = fields[3]
                    accession_e = fields[4]
                    ccre_type = fields[5]
                    nearest_gene = fields[6]
                    distance_bp = int(fields[7])

                    if GenomicRegionAdapterNodeType.GENOMIC_REGION in self.node_types:
                        # Create GenomicRegion node tuple
                        yield (
                            accession_d,  # node_id
                            'GenomicRegion',  # node_type
                            {  # properties
                                'chromosome': chromosome,
                                'start': start,
                                'end': end,
                                'accession_e': accession_e,
                                'ccre_type': ccre_type,
                                'distance_bp': distance_bp,
                                'source': self.source,
                                'version': self.version,
                                'license': self.license,
                            }
                        )

                    if GenomicRegionAdapterNodeType.GENE in self.node_types:
                        # Create Gene node tuple
                        yield (
                            nearest_gene,  # node_id
                            'Gene',  # node_type
                            {  # properties
                                'name': nearest_gene,
                                'source': self.source,
                                'version': self.version,
                                'license': self.license,
                            }
                        )
                except Exception as e:
                    logger.warning(f"Error processing line: {e}")
                    continue

    def get_edges(self):
        """
        Returns a generator of edge tuples from the BED file data.
        """
        logger.info("Generating edges from BED file.")
        
        with open(self.file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                if line.startswith('#') or line.strip() == '':
                    continue
                
                try:
                    fields = line.strip().split('\t')
                    accession_d = fields[3]
                    nearest_gene = fields[6]
                    distance_bp = int(fields[7])

                    if GenomicRegionAdapterEdgeType.REGION_TO_GENE in self.edge_types:
                        # Create RegionToGene edge tuple
                        yield (
                            f"e{line_num}",  # edge_id
                            accession_d,  # source_id
                            nearest_gene,  # target_id
                            GenomicRegionAdapterEdgeType.REGION_TO_GENE.value,  # relationship_type
                            {  # properties
                                'distance_bp': distance_bp,
                                'source': self.source,
                                'version': self.version,
                                'license': self.license,
                            }
                        )
                except Exception as e:
                    logger.warning(f"Error processing line: {e}")
                    continue

    def _set_types_and_fields(self, node_types, node_fields, edge_types, edge_fields):
        """
        Set the types and fields for the adapter.
        """
        self.node_types = node_types or [type for type in GenomicRegionAdapterNodeType]
        self.node_fields = node_fields or [
            field for field in GenomicRegionField
        ] + [field for field in GeneField]
        self.edge_types = edge_types or [type for type in GenomicRegionAdapterEdgeType]
        self.edge_fields = edge_fields or [field for field in RegionToGeneEdgeField] 