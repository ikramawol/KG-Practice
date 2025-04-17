from biocypher_metta.adapters import Adapter
import csv

class CCREAdapter(Adapter):
    # Example cCRE Data
    # #chromosome	start	end	accession_d	accession_e	ccre_type	nearest_gene	distance_bp
    # chr1	778570	778919	EH38D4327580	EH38E2776539	PLS,CTCF-bound	LINC01409	0
    # chr1	779026	779180	EH38D4327581	EH38E2776540	PLS,CTCF-bound	LINC01409	0
    # chr1	817080	817403	EH38D2115333	EH38E1310166	PLS	FAM87B	0
    # chr1	827417	827767	EH38D4327609	EH38E2776555	PLS,CTCF-bound	LINC00115	0
    # chr1	904578	904918	EH38D4327691	EH38E2776597	PLS,CTCF-bound	ENSG00000272438	0
    
    INDEX = {
        'chr': 0,
        'start': 1,
        'end': 2,
        'accession_d': 3,
        'accession_e': 4,
        'ccre_type': 5,
        'nearest_gene': 6,
        'distance': 7
    }
    
    def __init__(self, filepath, write_properties=True, add_provenance=False, delimiter='\t'):
        self.filepath = filepath
        self.delimiter = delimiter
        self.write_properties = write_properties
        self.add_provenance = add_provenance

        self.source = 'ENCODE'
        self.source_url = 'https://drive.google.com/uc?export=download&id=15V5yHLFX5d7Yu5rm1xiabhpV932mI3vg'
        self.label = 'regulatory_region'

        super().__init__(write_properties, add_provenance)

    def get_nodes(self):
        with open(self.filepath, 'r') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            next(reader)  # skip header
            for line in reader:
                chr = line[self.INDEX['chr']]
                start = int(line[self.INDEX['start']])
                end = int(line[self.INDEX['end']])
                region_id = f"{chr}:{start}-{end}"
                props = {}

                if self.write_properties:
                    props['accession_d'] = line[self.INDEX['accession_d']]
                    props['accession_e'] = line[self.INDEX['accession_e']]
                    props['ccre_type'] = line[self.INDEX['ccre_type']]
                    if self.add_provenance:
                        props['source'] = self.source
                        props['source_url'] = self.source_url

                yield region_id, self.label, props

    def get_edges(self):
        with open(self.filepath, 'r') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            next(reader)
            for line in reader:
                chr = line[self.INDEX['chr']]
                start = int(line[self.INDEX['start']])
                end = int(line[self.INDEX['end']])
                region_id = f"{chr}:{start}-{end}"
                gene_id = line[self.INDEX['nearest_gene']]
                props = {}

                if self.write_properties:
                    props['distance'] = int(line[self.INDEX['distance']])
                    if self.add_provenance:
                        props['source'] = self.source
                        props['source_url'] = self.source_url

                yield region_id, gene_id, 'nearest_gene', props
